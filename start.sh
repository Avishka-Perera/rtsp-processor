# start the rtsp server
nohup ./mediamtx > mediamtx.log &

# start the main script
nohup python main.py > main.log &
