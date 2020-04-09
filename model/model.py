# from fastai.vision import *


import threading
import configparser
from time import sleep, time

import cv2
import requests

config = configparser.ConfigParser()
config.read('settings.cfg')
ENDPOINT = config['RENDER']['RENDER_ENDPOINT']

# Angry, happy, neutral, sad

def get_face_expanded(x, y, width, height, img):
    frame_height = len(img)
    padding_top = int((height/0.7 - height)/2)
    
    top = max(0, y - padding_top)
    bot = min(frame_height, (y + height + padding_top))
    
    
    frame_width = len(img[0])
    padding_sides = int((width/0.7 - width)/2)

    left = max(0, x - padding_sides)
    right = min(frame_width, x+width + padding_sides)

    return img[top:bot, left:right]

def show_distance_indicator(x, y, width, height, img):
    needed_size = 224 * 0.7 # 224 is what the model is trained on, but face only fills 70%
    if (int(width) < needed_size or int(height) < needed_size):
        color = (0, 0, 230)
        text = "You're too far away"
        # print('ur too far u pumpkin')
    else:
        color = (0, 200, 0)
        text = "Good distance"

    cv2.putText(img,
        text,
        (x, y + height + 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2)
    cv2.rectangle(img, (x,y), (x+width,y+height), color)

def facechop(img):  
    facedata = "./model/haarcascade_frontalface_default.xml"
    # facedata = 'haarcascade_frontalface_default.xml'
    cascade = cv2.CascadeClassifier(facedata)

    minisize = (img.shape[1],img.shape[0])
    miniframe = cv2.resize(img, minisize)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for f in faces:
        x, y, w, h = [ v for v in f ]

        sub_face = get_face_expanded(x, y, w, h, img)
        # show_distance_indicator(x, y, w, h, img)

        # cv2.imshow("Capturing", img)
        cv2.imwrite('frame.png', img)
        
        return sub_face

def parseResults(emotionJson):
    res = {}
    emotionDict = emotionJson['emotions']
    for emotion in emotionDict:
        res[emotion] = float(emotionDict[emotion].split('(')[1].split(')')[0])

    res['contempt'] = 0
    res['disgust'] = 0
    res['fear'] = 0
    res['surprise'] = 0

    return res

def classify(learn, face_isolated):
    if face_isolated is None:
        print("no face found")
        return

    # seemed to be needed when converting to fastai image, don't think i need it for sending to Render
    # face_isolated = cv2.cvtColor(face_isolated, cv2.COLOR_BGR2RGB)

    face_224 = cv2.resize(face_isolated, (224, 224))
    # cv2.imwrite('face.jpg', face_224)
    # cv2.imwrite('frame.png', face_224)

    byte_image = get_image_bytes(face_224)
    emotionJson = send_to_server(byte_image)

    return parseResults(emotionJson)
    


def get_image_bytes(img):
    is_success, im_buf_arr = cv2.imencode(".jpg", img)
    return im_buf_arr.tobytes()

def send_to_server(byte_image):
    send_time = time()

    files = {'file': ('img.jpg', byte_image, 'image/jpeg', {'Expires': '0'})}
    response = requests.post(ENDPOINT, files=files)
    jsonboi = response.json()

    receival_time = time()
    # print('\n', jsonboi, '\n send_time:', send_time, '\n receival time:', receival_time)
    print('Time taken for our own model: %f' % (receival_time - send_time))
    return jsonboi


if __name__ == "__main__":
    # learn = initialize_fastai_model()
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)
    sleep(2)
    i = 0
    while True:
        
        try:
            i += 1
            check, frame = webcam.read()
            key = cv2.waitKey(1)
            if key == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break

            face_isolated = facechop(frame)

            if i % 30 == 0:        
                t = threading.Thread(target=classify, args=(None, face_isolated))
                t.start()
            
        
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break