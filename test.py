import sys
import os
import threading
import stackprinter
import time
import signal
from box import Box
import requests
from datetime import datetime

from PIL import Image , ImageDraw , ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

# https://python-elgato-streamDECK.readthedocs.io/en/stable/pages/backend_libusb_hidapi.html
# https://python-elgato-streamDECK.readthedocs.io/en/stable/examples/basic.html
class StreamDeckMini:
	def __init__( self , config={} ):
		self.config = Box( config )
		self.DECK = False
		self.buttons = {}
		self.total_added_buttons = 0
		signal.signal( signal.SIGABRT , self.signal_handler )
		signal.signal( signal.SIGFPE , self.signal_handler )
		signal.signal( signal.SIGILL , self.signal_handler )
		signal.signal( signal.SIGSEGV , self.signal_handler )
		signal.signal( signal.SIGTERM , self.signal_handler )
		signal.signal( signal.SIGINT , self.signal_handler )
		self.find_devices()
		print( self.config )
		if "serial_number" not in self.config:
			return None
		if self.config.serial_number not in self.devices:
			print( f"Couldn't Find Device Attached with Serial Number : {self.config.serial_number}" )
			return None
		self.DECK = self.devices[ self.config.serial_number ].deck
		if "brightness" in self.config:
			self.DECK.set_brightness( self.config.brightness )
		self.global_last_pressed = datetime.now()
		self.DECK.set_key_callback( self.key_change_callback )

	def signal_handler( self , signal , frame ):
		print( "StreamDECK.py Closed , Signal = " + str( signal ) )
		self.DECK.reset()
		self.DECK.close()
		sys.exit( 0 )

	def find_devices( self ):
		self.devices = {}
		try:
			stream_decks = DeviceManager().enumerate()
			if len( stream_decks ) < 1:
				print( "Couldn't Find any StreamDECKs attached !" )
				return False
			for index , stream_deck in enumerate( stream_decks ):
				try:
					stream_deck.open()
					# stream_deck.reset()
					deck_type = stream_deck.deck_type()
					serial_number = stream_deck.get_serial_number()
					print( f"Opened {deck_type} device ( serial number : {serial_number} )" )
					if serial_number not in self.devices:
						self.devices[ serial_number ] = Box({
							"type": deck_type ,
							"deck": stream_deck
						})
				except Exception as e:
					print( e )
		except Exception as e2:
			print( e2 )

	def connect( self ):
		self.DECK = self.devices[ self.config.serial_number ].deck
		self.DECK.open()
		self.DECK.reset()

	def get_ms_duration( self , start_time , end_time ):
		dt = ( end_time - start_time )
		duration_milliseconds = ( ( dt.days * 24 * 60 * 60 + dt.seconds ) * 1000 + dt.microseconds / 1000.0 )
		return duration_milliseconds

	# when state == False , then the button is released
	# also need to build in cooloff / easing timers to prevent multiple clicks
	def press_button( self , button_index ):
		try:
			now = datetime.now()
			if "global_cooldown_milliseconds" in self.config:
				global_duration_milliseconds = self.get_ms_duration( self.global_last_pressed , now )
				self.global_last_pressed = now
				if global_duration_milliseconds < self.config.global_cooldown_milliseconds:
					remaining_global_milliseconds = ( self.config.global_cooldown_milliseconds - global_duration_milliseconds )
					print( f"\nDeck { self.DECK.id() } : Button [ { button_index + 1 } ] === Trigger On : [ { self.buttons[ button_index ].trigger_on } ] === Still inside Global Cooldown Window , [ {remaining_global_milliseconds} ] milliseconds remaining" , flush=True )
					return False
			duration_milliseconds = self.get_ms_duration( self.buttons[ button_index ].last_pressed , now )
			self.buttons[ button_index ].last_pressed = now
			if "cooldown_milliseconds" in self.buttons[ button_index ]:
				if duration_milliseconds < self.buttons[ button_index ].cooldown_milliseconds:
					remaining_milliseconds = ( self.buttons[ button_index ].cooldown_milliseconds - duration_milliseconds )
					print( f"\nDeck { self.DECK.id() } : Button [ { button_index + 1 } ] === Trigger On : [ { self.buttons[ button_index ].trigger_on } ] === Still inside Cooldown Window , [ {remaining_milliseconds} ] milliseconds remaining" , flush=True )
					return False

			print( f"\nDeck { self.DECK.id() } : Button [ { button_index + 1 } ] === Trigger On : [ { self.buttons[ button_index ].trigger_on } ] === {self.buttons[ button_index ].end_point_url}" , flush=True )
			response = requests.get( self.buttons[ button_index ].end_point_url )
			response.raise_for_status()
			print( response.status_code )
			# print( response.text )
			print( response.json() )
		except Exception as e:
			print( e )

	def key_change_callback( self , key_object , button_index , pressed ):
		if pressed == True:
			if self.buttons[ button_index ].trigger_on == "press":
				self.press_button( button_index )
		else:
			if self.buttons[ button_index ].trigger_on == "release":
				self.press_button( button_index )

	def add_button( self , options ):
		try:
			options = Box( options )
			if "index" not in options:
				options.index = self.total_added_buttons
			if "image_path" not in options:
				return False
			if "font_path" not in options:
				return False
			if "margins" not in options:
				options.margins = [ 0 , 0 , 20 , 0 ]
			if "font_size" not in options:
				options.font_size = 14
			if "text" not in options:
				options.text = f"Button {options.index}"
			if "fill" not in options:
				options.fill = "white"
			options.last_pressed = datetime.now()
			self.buttons[ options.index ] = options
			icon = Image.open( options.image_path )
			if len( options.text ) > 0:
				options.margins = [ 0 , 0 , 20 , 0 ]
				image = PILHelper.create_scaled_image( self.DECK , icon , margins=options.margins )
				draw = ImageDraw.Draw( image )
				font = ImageFont.truetype( options.font_path , options.font_size )
				draw.text( ( ( image.width / 2 ) , ( image.height - 5 ) ) , text=options.text , font=font , anchor="ms" , fill=options.fill )
			else:
				options.margins = [ 0 , 0 , 0 , 0 ]
				image = PILHelper.create_scaled_image( self.DECK , icon , margins=options.margins )
				draw = ImageDraw.Draw( image )
			rendered_image = PILHelper.to_native_format( self.DECK , image )
			with self.DECK:
				self.DECK.set_key_image( options.index , rendered_image )
			self.total_added_buttons += 1
			return True
		except Exception as e:
			print( e )
			return False

	def start( self ):
		# https://python-elgato-streamdeck.readthedocs.io/en/stable/modules/transports.html#StreamDeck.Transport.Transport.Transport.Device.connected
		#could change everything here to
		while self.DECK.connected() == True:
			print( "device is still connected , sleeping for 30 seconds on the main thread" )
			time.sleep( 30 )
		print( "device disconnected , attempting to reconnect" )
		self.DECK.reset()
		self.DECK.close()
		self.connect()
		self.start()

		# for t in threading.enumerate():
		# 	try:
		# 		t.join()
		# 	except RuntimeError:
		# 		pass

def _run():
	# connected = False
	# while connected == False:
	# 	try:
	# 		x = StreamDeckMini({
	# 			 "serial_number": "BL12K1B42830" ,
	# 			"brightness": 30 ,
	# 			"global_cooldown_milliseconds": 1000
	# 		})
	# 		connected = True
	# 	except Exception as e:
	# 		print( "no devices , sleeping for 30 seconds" )
	# 		time.sleep( 30 )

	x = StreamDeckMini({
		#"serial_number": "BL12K1B42830" ,
		"serial_number": "AL02K2C02319" ,
		"brightness": 30 ,
		"global_cooldown_milliseconds": 1000
	})

	# endpoint_hostname = "https://buttons.olahmb.com"
	endpoint_hostname = "http://localhost:9371"
	endpoint_token = "x=q27f2854ae49b194c34ced0fa0787d4047885e2bca4350f895279fbab38b"
	x.add_button({
		"index": 0 ,
		"image_path": "./icons/spotify.png" ,
		"font_path": "./Roboto-Regular.ttf" ,
		"font_size": 14 ,
		"text": "" ,
		"fill": "white" ,
		"cooldown_milliseconds": 1000 ,
		"trigger_on": "press" , # or release
		"end_point_url": f"{endpoint_hostname}/streamdeck/1?{endpoint_token}"
	})
	x.add_button({
		"index": 1 ,
		"image_path": "./icons/twitch.png" ,
		"font_path": "./Roboto-Regular.ttf" ,
		"font_size": 14 ,
		"text": "" ,
		"fill": "white" ,
		"cooldown_milliseconds": 1000 ,
		"trigger_on": "press" , # or release
		"end_point_url": f"{endpoint_hostname}/streamdeck/2?{endpoint_token}"
	})
	x.add_button({
		"index": 2 ,
		"image_path": "./icons/youtube.png" ,
		"font_path": "./Roboto-Regular.ttf" ,
		"font_size": 14 ,
		"text": "" ,
		"fill": "white" ,
		"cooldown_milliseconds": 1000 ,
		"trigger_on": "press" , # or release
		"end_point_url": f"{endpoint_hostname}/streamdeck/3?{endpoint_token}"
	})
	x.add_button({
		"index": 3 ,
		"image_path": "./icons/disney.png" ,
		"font_path": "./Roboto-Regular.ttf" ,
		"font_size": 14 ,
		"text": "" ,
		"fill": "white" ,
		"cooldown_milliseconds": 1000 ,
		"trigger_on": "press" , # or release
		"end_point_url": f"{endpoint_hostname}/streamdeck/4?{endpoint_token}"
	})
	x.add_button({
		"index": 4 ,
		"image_path": "./1f49a.png" ,
		"font_path": "./Roboto-Regular.ttf" ,
		"font_size": 14 ,
		"text": "5" ,
		"fill": "white" ,
		"cooldown_milliseconds": 1000 ,
		"trigger_on": "press" , # or release
		"end_point_url": f"{endpoint_hostname}/streamdeck/5?{endpoint_token}"
	})
	x.add_button({
		"index": 5 ,
		"image_path": "./1f49a.png" ,
		"font_path": "./Roboto-Regular.ttf" ,
		"font_size": 14 ,
		"text": "6" ,
		"fill": "white" ,
		"cooldown_milliseconds": 1000 ,
		"trigger_on": "press" , # or release
		"end_point_url": f"{endpoint_hostname}/streamdeck/6?{endpoint_token}"
	})
	x.start()


if __name__ == "__main__":
	while True:
		try:
			_run()
		except Exception as e:
			# print( stackprinter.format() )
			print( "failed to connect , trying again in 30 seconds" )
			time.sleep( 30 )

