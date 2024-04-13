#! /bin/bash

# create environment
conda env create -f environment.yaml
conda activate rs

# install mediamtx
wget https://github.com/bluenviron/mediamtx/releases/download/v1.6.0/mediamtx_v1.6.0_linux_amd64.tar.gz
tar -xzvf mediamtx_v1.6.0_linux_amd64.tar.gz
rm mediamtx_v1.6.0_linux_amd64.tar.gz

# install opencv from source
sudo apt-get install libgstreamer1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-rtsp gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio libavcodec-dev libavformat-dev libavutil-dev libswscale-dev
sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-tools pkg-config libgtk-3-dev libva-dev
wget https://github.com/opencv/opencv/archive/refs/tags/4.9.0.zip
unzip unzip 4.9.0.zip
cd opencv-4.9.0/
mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local INSTALL_PYTHON_EXAMPLES=ON -D INSTALL_C_EXAMPLES=OFF -D OPENCV_ENABLE_NONFREE=ON -D PYTHON_EXECUTABLE=$(which python) -D BUILD_opencv_python2=OFF -D CMAKE_INSTALL_PREFIX=$(python -c "import sys; print(sys.prefix)") -D PYTHON3_EXECUTABLE=$(which python) -D PYTHON3_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") -D PYTHON3_PACKAGES_PATH=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") -D WITH_GSTREAMER=ON -D BUILD_EXAMPLES=ON ..
make -j$(nproc)
make install
sudo ldconfig
cd ../..
rm 4.9.0.zip
rm -r opencv-4.9.0