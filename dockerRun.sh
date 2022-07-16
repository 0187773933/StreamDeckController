#!/bin/bash
APP_NAME="stream-deck-controller"
sudo docker rm $APP_NAME -f || echo "failed to remove existing $APP_NAME"
id=$(sudo docker run -dit --restart='always' \
--name $APP_NAME \
--privileged \
-v /dev:/dev \
$APP_NAME)
echo "ID = $id"
sudo docker logs -f "$id"

## Find StreamDeck
# https://weinimo.github.io/how-to-write-udev-rules-for-usb-devices.html
# udevadm monitor
# or
# lsusb
# or
# dmesg -w
# ls -lah /dev/input/by-id
# file /dev/input/event0
	# event0: character special (13/64)
# udevadm info -a -p $(udevadm info -q path -n /dev/bus/usb/001/006)
# udevinfo info -a -p $(udevinfo info -q path -n /dev/bus/usb/001/006)
# sudo nano /etc/udev/rules.d/10-local.rules
# echo 'SUBSYSTEMS=="usb", ATTRS{product}=="Stream Deck Mini", GROUP="sudo"' | sudo tee -a /etc/udev/rules.d/10-local.rules
# sudo udevadm test /devices/platform/soc/3f980000.usb/usb1/1-1/1-1.3
# unplug and replug usb device


#-p 17397:9377 \

#-v /dev/ttyACM0:/dev/ttyACM0 \
#-v /dev/bus/usb:/dev/bus/usb \
#--device=/dev/ttyUSB0 \

#--volume /mnt/blockstorage/PPTIG/IMAGES:/home/morphs/STORAGE/IMAGES \
#--volume /mnt/blockstorage/PPTIG/BLOBS:/home/morphs/STORAGE/BLOBS \
#--mount type=bind,source=/home/morphs/DOCKER_IMAGES/PowerPointInteractiveGamesGenerator/config.json,target=/home/config.json \
