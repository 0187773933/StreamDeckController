#!/bin/bash
APP_NAME="stream-deck-controller"
sudo docker rm $APP_NAME -f || echo "failed to remove existing $APP_NAME"
id=$(sudo docker run -dit --restart='always' \
--name $APP_NAME \
--privileged \
-v /dev/ttyACM0:/dev/ttyACM0 \
-p 17397:9377 \
$APP_NAME)
echo "ID = $id"
sudo docker logs -f "$id"

#--volume /mnt/blockstorage/PPTIG/IMAGES:/home/morphs/STORAGE/IMAGES \
#--volume /mnt/blockstorage/PPTIG/BLOBS:/home/morphs/STORAGE/BLOBS \
#--mount type=bind,source=/home/morphs/DOCKER_IMAGES/PowerPointInteractiveGamesGenerator/config.json,target=/home/config.json \
