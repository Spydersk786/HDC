import cv2

def get_video_capture():
    cap = cv2.VideoCapture(0)  # Adjust index if needed
    return cap
