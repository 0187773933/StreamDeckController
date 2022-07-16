from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

# sudo apt-get install libusb-1.0-0-dev -y
# sudo apt-get install libusb-dev -y
# sudo apt install libhidapi-dev -y
stream_decks = DeviceManager().enumerate()
for index , stream_deck in enumerate( stream_decks ):
	stream_deck.open()
	deck_type = stream_deck.deck_type()
	serial_number = stream_deck.get_serial_number()
	print( deck_type , serial_number )
