# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.
#Based on https://github.com/denverdino/face_recognition_pi

import face_recognition
import picamera
import numpy as np
import os

known_face_encodings = []
names = []

def load_face_encoding(name, file_name):
    image = face_recognition.load_image_file(file_name)
    face_encoding = face_recognition.face_encodings(image)
    if len(face_encoding) > 0:
        known_face_encodings.append(face_encoding[0])
        names.append(name)
        print("Image loaded: {}".format(name))

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Load a sample picture and learn how to recognize it.
print("Loading images from {}".format(os.path.dirname(os.path.abspath(__file__))+"/bilder/"))
load_face_encoding("Stefan", os.path.dirname(os.path.abspath(__file__))+"/../bilder/beffy.jpg")
load_face_encoding("Erik", os.path.dirname(os.path.abspath(__file__))+"/../bilder/erik.jpg")
load_face_encoding("Mika", os.path.dirname(os.path.abspath(__file__))+"/../bilder/mika.jpg")
load_face_encoding("Sonja", os.path.dirname(os.path.abspath(__file__))+"/../bilder/sonja.jpg")

# Initialize some variables
face_locations = []
face_encodings = []

while True:
    print("Taking picture.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    if len(face_encodings) > 0:
        
        # Loop over each face found in the frame to see if it's someone we know.
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.face_distance(known_face_encodings, face_encoding)
            name = "a stranger"
        
            min_distance = min(matches)
            if min_distance < 0.6:
                i = matches.argmin()
                name = names[i]
            
        
        print("I see {}!".format(name))