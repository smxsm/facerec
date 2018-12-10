import face_recognition
import cv2
import os
import time
import imutils
from imutils.video import VideoStream
from imutils.video import FPS

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

known_face_encodings = []
known_face_names = []

def load_face_encoding(name, file_name):
    image = face_recognition.load_image_file(file_name)
    face_encoding = face_recognition.face_encodings(image)
    if len(face_encoding) > 0:
        known_face_encodings.append(face_encoding[0])
        known_face_names.append(name)
        print("Image loaded: {}".format(name))
    else:
        print("Unable load image: {}".format(name))        

# Get a reference to webcam #0 (the default one)
#video_capture = cv2.VideoCapture(0)
#video_capture = VideoStream(src=0).start()
# use Raspbi cam
video_capture = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

print("Loading images from {}".format(os.path.dirname(os.path.abspath(__file__))+"/bilder/"))
load_face_encoding("Stefan", os.path.dirname(os.path.abspath(__file__))+"/../bilder/beffy.jpg")
load_face_encoding("Erik", os.path.dirname(os.path.abspath(__file__))+"/../bilder/erik.jpg")
load_face_encoding("Mika", os.path.dirname(os.path.abspath(__file__))+"/../bilder/mika.jpg")
load_face_encoding("Sonja", os.path.dirname(os.path.abspath(__file__))+"/../bilder/sonja.jpg")

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    #small_frame = imutils.resize(frame, width=500)
    (h, w) = frame.shape[:2]
    smallW = int(round(w*0.25))
    #print("Breite {}!".format(smallW))
    small_frame = frame #imutils.resize(frame, smallW)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            # default tolerance is 0.6, the lesser the stricter
            tolerance = 0.5
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)
            print("Hello, {}".format(name))

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        #top *= 4
        #right *= 4
        #bottom *= 4
        #left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()