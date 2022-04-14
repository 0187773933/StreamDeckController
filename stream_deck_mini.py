import sys
import os
import threading
import signal

from PIL import Image , ImageDraw , ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

DECK = False
def signal_handler( signal , frame ):
	global DECK
	print( "StreamDECK.py Closed , Signal = " + str( signal ) )
	DECK.reset()
	DECK.close()
	sys.exit( 0 )

signal.signal( signal.SIGABRT , signal_handler )
signal.signal( signal.SIGFPE , signal_handler )
signal.signal( signal.SIGILL , signal_handler )
signal.signal( signal.SIGSEGV , signal_handler )
signal.signal( signal.SIGTERM , signal_handler )
signal.signal( signal.SIGINT , signal_handler )

# https://python-elgato-streamDECK.readthedocs.io/en/stable/pages/backend_libusb_hidapi.html
# https://python-elgato-streamDECK.readthedocs.io/en/stable/examples/basic.html

# when state == False , then the button is released
# also need to build in cooloff / easing timers to prevent multiple clicks
def key_change_callback( deck , key , state ):

	print( f"Deck {deck.id()} : Key {key} = {state}" , flush=True )

	# # Update the key image based on the new key state.
	# update_key_image(DECK, key, state)

	# # Check if the key is changing to the pressed state.
	# if state:
	# 	key_style = get_key_style(DECK, key, state)

	# 	# When an exit button is pressed, close the application.
	# 	if key_style["name"] == "exit":
	# 		# Use a scoped-with on the DECK to ensure we're the only thread
	# 		# using it right now.
	# 		with DECK:
	# 			# Reset DECK, clearing all button images.
	# 			DECK.reset()

	# 			# Close DECK handle, terminating internal worker threads.
	# 			DECK.close()


def add_button_0():
	global DECK
	try:
		icon = Image.open( "./1f49a.png" )
		image = PILHelper.create_scaled_image( DECK , icon , margins=[ 0 , 0 , 20 , 0 ] )
		draw = ImageDraw.Draw( image )
		font = ImageFont.truetype( "./Roboto-Regular.ttf" , 14 )
		draw.text( ( ( image.width / 2 ) , ( image.height - 5 ) ) , text="Button 0" , font=font , anchor="ms" , fill="white" )
		rendered_image = PILHelper.to_native_format( DECK , image )
		with DECK:
			DECK.set_key_image( 0 , rendered_image )
		return True
	except Exception as e:
		print( e )
		return False

def add_button_1():
	global DECK
	try:
		icon = Image.open( "./1f49a.png" )
		image = PILHelper.create_scaled_image( DECK , icon , margins=[ 0 , 0 , 20 , 0 ] )
		draw = ImageDraw.Draw( image )
		font = ImageFont.truetype( "./Roboto-Regular.ttf" , 14 )
		draw.text( ( ( image.width / 2 ) , ( image.height - 5 ) ) , text="Button 1" , font=font , anchor="ms" , fill="white" )
		rendered_image = PILHelper.to_native_format( DECK , image )
		with DECK:
			DECK.set_key_image( 1 , rendered_image )
		return True
	except Exception as e:
		print( e )
		return False

def add_button_2():
	global DECK
	try:
		icon = Image.open( "./1f49a.png" )
		image = PILHelper.create_scaled_image( DECK , icon , margins=[ 0 , 0 , 20 , 0 ] )
		draw = ImageDraw.Draw( image )
		font = ImageFont.truetype( "./Roboto-Regular.ttf" , 14 )
		draw.text( ( ( image.width / 2 ) , ( image.height - 5 ) ) , text="Button 2" , font=font , anchor="ms" , fill="white" )
		rendered_image = PILHelper.to_native_format( DECK , image )
		with DECK:
			DECK.set_key_image( 2 , rendered_image )
		return True
	except Exception as e:
		print( e )
		return False

def add_button_3():
	global DECK
	try:
		icon = Image.open( "./1f49a.png" )
		image = PILHelper.create_scaled_image( DECK , icon , margins=[ 0 , 0 , 20 , 0 ] )
		draw = ImageDraw.Draw( image )
		font = ImageFont.truetype( "./Roboto-Regular.ttf" , 14 )
		draw.text( ( ( image.width / 2 ) , ( image.height - 5 ) ) , text="Button 3" , font=font , anchor="ms" , fill="white" )
		rendered_image = PILHelper.to_native_format( DECK , image )
		with DECK:
			DECK.set_key_image( 3 , rendered_image )
		return True
	except Exception as e:
		print( e )
		return False

def add_button_4():
	global DECK
	try:
		icon = Image.open( "./1f49a.png" )
		image = PILHelper.create_scaled_image( DECK , icon , margins=[ 0 , 0 , 20 , 0 ] )
		draw = ImageDraw.Draw( image )
		font = ImageFont.truetype( "./Roboto-Regular.ttf" , 14 )
		draw.text( ( ( image.width / 2 ) , ( image.height - 5 ) ) , text="Button 4" , font=font , anchor="ms" , fill="white" )
		rendered_image = PILHelper.to_native_format( DECK , image )
		with DECK:
			DECK.set_key_image( 4 , rendered_image )
		return True
	except Exception as e:
		print( e )
		return False

def add_button_5():
	global DECK
	try:
		icon = Image.open( "./1f49a.png" )
		image = PILHelper.create_scaled_image( DECK , icon , margins=[ 0 , 0 , 20 , 0 ] )
		draw = ImageDraw.Draw( image )
		font = ImageFont.truetype( "./Roboto-Regular.ttf" , 14 )
		draw.text( ( ( image.width / 2 ) , ( image.height - 5 ) ) , text="Button 5" , font=font , anchor="ms" , fill="white" )
		rendered_image = PILHelper.to_native_format( DECK , image )
		with DECK:
			DECK.set_key_image( 5 , rendered_image )
		return True
	except Exception as e:
		print( e )
		return False

def add_our_custom_images():
	try:
		button_0 = add_button_0()
		if button_0 == False:
			return False
		button_1 = add_button_1()
		if button_1 == False:
			return False
		button_2 = add_button_2( )
		if button_2 == False:
			return False
		button_3 = add_button_3()
		if button_3 == False:
			return False
		button_4 = add_button_4()
		if button_4 == False:
			return False
		button_5 = add_button_5()
		if button_5 == False:
			return False
		return True
	except Exception as e:
		print( e )
		return False

if __name__ == "__main__":
	streamDECKs = DeviceManager().enumerate()
	if len( streamDECKs ) < 1:
		print( "Couldn't Find any StreamDECKs attached !" )
		sys.exit( 1 )

	DECK = streamDECKs[ 0 ]
	DECK.open()
	DECK.reset()
	print( f"Opened {DECK.deck_type()} device ( serial number : {DECK.get_serial_number()} )" )

	DECK.set_brightness( 30 )

	# we are using the 'mini' so we have 6 keys
	# print( DECK.key_count() )
	# DECK.close()

	result = add_our_custom_images()
	if result == False:
		print( "Couldn't Add Custom Image Set for Some Reason" )
		sys.exit( 1 )

	DECK.set_key_callback( key_change_callback )
	for t in threading.enumerate():
		try:
			t.join()
		except RuntimeError:
			pass

	DECK.close()