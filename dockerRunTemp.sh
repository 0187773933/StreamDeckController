#!/bin/bash
APP_NAME="stream-deck-controller"
sudo docker rm $APP_NAME -f || echo "failed to remove existing $APP_NAME"
sudo docker run -it \
--name $APP_NAME \
--privileged \
-v /dev/ttyACM0:/dev/ttyACM0 \
-p 17397:9377 \
$APP_NAME

#--volume /mnt/blockstorage/PPTIG/IMAGES:/home/morphs/STORAGE/IMAGES \
#--volume /mnt/blockstorage/PPTIG/BLOBS:/home/morphs/STORAGE/BLOBS \
#--mount type=bind,source=/home/morphs/DOCKER_IMAGES/PowerPointInteractiveGamesGenerator/config.json,target=/home/config.json \
