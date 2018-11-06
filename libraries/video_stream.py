import cv2
import face_recognition
from base64 import b64encode

video_capture = cv2.VideoCapture(0)

def get_frame():
    # Grab a single frame of video
    ret, frame = video_capture.read()
    # RGBFrame = frame[: , : , ::-1]
    # face_location = face_recognition.face_locations(RGBFrame)
    # for (top,right,bottom,left) in face_location:
    #     frame = frame[top:bottom, left:right]
    #     # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    code = cv2.imencode(".jpg",frame)[1].tostring()
    return b64encode(code)
        

def close_stream():
    video_capture.release()