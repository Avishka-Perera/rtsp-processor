# start the rtsp server
nohup ./mediamtx > mediamtx.log &

# start the main script
nohup python src/main.py > main.log &
