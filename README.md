# Face recognition for Docker on Raspberry

Docker Image for [face_recognition](https://github.com/ageitgey/face_recognition) on Raspberry Pi
Based on https://github.com/denverdino/face_recognition_pi

This fork adds support for OpenCV and displays a video on the host during face recognition (see "scripts/video.py").
Be aware that building OpenCV may take approx. another 2 hours on a Raspberry 3, in addition to the 3 to 5 hours for building the base image.
This fork also fixes an error when no face is recognized in any of the images ("list index out of range", see https://github.com/jamct/facerec/issues/4) and it mounts the complete "script" dir into the docker container instead of a single script.

### *License*
This software is released under the Apache 2.0 license.

## Getting started

Build container: 

```bash
docker build -t facerec:latest .
```

Run container:

```bash
docker run -it --device /dev/vchiq -v $PWD/scripts:/face_recognition/examples/scripts -v $PWD/bilder:/face_recognition/examples/bilder facerec bash
```

In the container, change to "/face_recogition/example/scripts" and call:

```bash
python beispiel.py
```

To run a container with OpenCV support utilizing the x-server of the host, use this command:

```bash
docker run -e DISPLAY=$DISPLAY -it --device /dev/vchiq -v /tmp/.X11-unix:/tmp/.X11-unix -v $PWD/scripts:/face_recognition/examples/scripts -v $PWD/bilder:/face_recognition/examples/bilder --privileged facerec bash
```

It exposes the host X11 display to the container (which doesn't have a "GUI") and the docker container renders the video on the raspberry desktop.

You may have to allow access for the container before starting it - the easiest, although insecure way is to disable display-auth completely with

```bash
xhost +
```

on the host (Raspberry).

You can now try to run

```bash
python video.py
```

in the container.
