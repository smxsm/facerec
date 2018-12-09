#Dockerfile for face-recognition
#Based on https://github.com/denverdino/face_recognition_pi

FROM resin/raspberry-pi-python:3
COPY pip.conf /root/.pip/pip.conf
RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*
RUN python3 -m ensurepip --upgrade && pip3 install --upgrade picamera[array] dlib


RUN git clone --single-branch https://github.com/ageitgey/face_recognition.git
RUN cd /face_recognition && \
    pip3 install -r requirements.txt && \
    python3 setup.py install

# support for OpenCV added
RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    libtiff5-dev libjasper-dev libpng12-dev \
    libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev \
    libatlas-base-dev gfortran unzip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.4.zip
RUN wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.4.4.zip
RUN unzip opencv.zip
RUN unzip opencv_contrib.zip
RUN pip3 install numpy scipy
RUN mkdir -p /opencv-3.4.4/build
WORKDIR /opencv-3.4.4/build/
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib-3.4.4/modules \
    -D BUILD_EXAMPLES=ON ..
RUN make -j4
RUN make install
RUN ldconfig
RUN apt-get update
# copy .so for Python 3.6
RUN cp /opencv-3.4.4/build/lib/python3/cv2.cpython-36m-arm-linux-gnueabihf.so /usr/local/lib/python3.6/lib-dynload/cv2.so
RUN pip3 install imutils
# change work dir
WORKDIR /face_recognition/examples

CMD cd /face_recognition/examples && \
    python3 recognize_faces_in_pictures.py

