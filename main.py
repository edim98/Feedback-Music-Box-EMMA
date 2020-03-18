import multiprocessing
#import heartrate
# import view

import os
import threading
import time
import cv2
from catalin.FaceNotDetectedError import FaceNotDetectedError
import catalin.azorel as azorel
import sys
import catalin.plotter as plotter
import catalin.GUI as GUI
import other_scripts.CLIparser as CLIparser

from pymongo import MongoClient
from app import progress_history, track_history, aggdata, descriptors
from audio import Tracklist, Playlist2
from model.fast_and_cam import facechop, classify

#  Detection/classifier parameters
SCALE_FACTOR = 1.2
MIN_NEIGHBORS = 4

DRAW = False  # Used to activate drawing the classifier boxes
WHICH_CLASSIFIER = [1, 1, 1, 0]  # Choose index 1 for simple frontal, 2 for improved frontal, 3 for profile, 4 4 smile
CLASSIFIER_PATHS = ['haarcascade_frontalface_default.xml', 'haarcascade_profileface.xml',
                    'lbpcascade_frontalface_improved.xml',
                    # This can be copied from https://raw.githubusercontent.com/opencv/opencv/master/data/lbpcascades/lbpcascade_frontalface_improved.xml
                    'haarcascade_smile.xml']

threshold = -10

def load_classifiers(which_classifiers):  # TODO: Decide whether or not remove this.
    result = []

    for index in which_classifiers:
        if index != 1:
            result.append(None)
        else:
            result.append(cv2.CascadeClassifier(cv2.data.haarcascades + CLASSIFIER_PATHS[index]))

    return result


def draw_face_boxes(frame):
    gray = cv2.cvtColor(frame, 0)
    classifiers = load_classifiers(WHICH_CLASSIFIER)

    faces = classifiers[0].detectMultiScale(gray, SCALE_FACTOR, MIN_NEIGHBORS) if classifiers[0] is not None else []
    faces_improved = classifiers[2].detectMultiScale(gray, SCALE_FACTOR, MIN_NEIGHBORS) if classifiers[2] is not None \
        else []
    profiles = classifiers[1].detectMultiScale(gray, SCALE_FACTOR, MIN_NEIGHBORS) if classifiers[1] is not None else []
    smiles = classifiers[3].detectMultiScale(gray, SCALE_FACTOR, MIN_NEIGHBORS) if classifiers[3] is not None else []

    for (x, y, w, h) in faces_improved:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (10, 250, 10), 1)
        cv2.putText(frame, "F2", (x - 10, y), 3, 1, (10, 250, 10))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 50, 0), 1)
        cv2.putText(frame, "F1", (x - 10, y), 3, 1, (200, 50, 0))

    for (x, y, w, h) in profiles:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 50, 200), 2)
        cv2.putText(frame, "Profile", (x - 10, y), 3, 1, (0, 50, 200))

    if smiles:
        cv2.putText(frame, "Smile detected", (20, 15), 3, 1, (80, 30, 200))


def get_frame(video_camera):
    if video_camera.isOpened():
        _, frame = video_camera.read()
    else:
        raise Exception("Camera is not opened")
    return frame


def display_frame(frame, title="Feedback Music Box"):
    cv2.imshow(title, frame)


def close_camera(video_camera):
    video_camera.release()
    cv2.destroyAllWindows()


def remove_frame(name="frame"):
    path_to_image = os.path.join(sys.path[0], "{}.png".format(name))
    try:
        if os.path.isfile(path_to_image):
            os.chmod(path_to_image, 0o777)
            os.unlink(path_to_image)
            os.remove(path_to_image)
        else:
            print("{}.png is apparently not a file".format(name))
    except FileNotFoundError:
        return
    except PermissionError:
        return  # Fuck Tkinter and the fact that it doesn't start a thread for its interface


def get_face_rectangles(azure_response):
    result = []
    for face in azure_response:
        result.append(face.face_rectangle)
    return result


def get_face_frames(frame, azure_response):
    result = []
    rectangles = get_face_rectangles(azure_response)
    for rectangle in rectangles:
        width = rectangle.width
        height = rectangle.height
        x_coord = rectangle.left
        y_coord = rectangle.top
        result.append(frame[y_coord: y_coord + height, x_coord: x_coord + width])
    return result


def get_forehead_frames(frame, azure_response):
    result = []
    f_x = 0.5
    f_y = 0.18
    f_w = 0.25
    f_h = 0.15
    rectangles = get_face_rectangles(azure_response)
    for rectangle in rectangles:
        w = rectangle.width
        h = rectangle.height
        x = rectangle.left
        y = rectangle.top
        forehead_x = int(x + w * f_x - (w * f_w / 2.0))
        forehead_y = int(y + h * f_y - (h * f_h / 2.0))
        forehead_w = int(w * f_w)
        forehead_h = int(h * f_h)
        result.append(frame[forehead_y: forehead_y + forehead_h,
                      forehead_x: forehead_x + forehead_w])
    return result


def get_forehead_frame(frame):
    result = []
    f_x = 0.5
    f_y = 0.18
    f_w = 0.25
    f_h = 0.15
    face_coordinates = get_face_coordinates(frame)
    for (x, y, h, w) in face_coordinates:
        forehead_x = int(x + w * f_x - (w * f_w / 2.0))
        forehead_y = int(y + h * f_y - (h * f_h / 2.0))
        forehead_w = int(w * f_w)
        forehead_h = int(h * f_h)
        result.append(frame[forehead_y: forehead_y + forehead_h,
                      forehead_x: forehead_x + forehead_w])
    return result


def get_forehead_coordinates(frame):
    result = []
    f_x = 0.5
    f_y = 0.18
    f_w = 0.25
    f_h = 0.15
    face_coordinates = get_face_coordinates(frame)
    for (x, y, h, w) in face_coordinates:
        forehead_x = int(x + w * f_x - (w * f_w / 2.0))
        forehead_y = int(y + h * f_y - (h * f_h / 2.0))
        forehead_w = int(w * f_w)
        forehead_h = int(h * f_h)
        result.append((forehead_x, forehead_y, forehead_h, forehead_w))
    return result


def get_face_coordinates(frame):
    result = []
    gray = cv2.cvtColor(frame, 0)
    faces = frontal_classifier.detectMultiScale(gray, SCALE_FACTOR, MIN_NEIGHBORS)
    if len(faces) >= 1:
        for (x, y, h, w) in faces:
            result.append((x, y, h, w))
    else:
        raise FaceNotDetectedError("Face was not detected by classifier. Please adjust your positioning")
    return result


def get_facial_emotion(frame):
    if DRAW:
        draw_face_boxes(frame)
    remove_frame()
    cv2.imwrite("frame.png", frame)
    try:
        detected_faces = azorel.get_faces()
        emotions = azorel.get_emotion(detected_faces)
    except FaceNotDetectedError:
        print("face.get_facial_emotion: Face was not detected by Azure. Please adjust your positioning.")
        emotions = {}

    return emotions

def initialize():

    client = MongoClient()
    db = client.test_database
    sessionID = 'test'

    track_history.create_track_log(db, sessionID)
    print('Created track history...')

    progress_history.create_progress_log(db, sessionID)
    print('Created progress history...')

    aggdata.create_agg_log(db, sessionID)
    print('Created aggregated data logs...')

    Playlist2.song_player(db, sessionID)

    return db, sessionID

def getEmotionList(emotions):
    emotionList = []
    for face_id in emotions:
        return emotions[face_id]

def main():

    azureFlag = CLIparser.parseFlags()

    db, sessionID = initialize()

    thread = threading.Thread(target=GUI.run)
    thread.setDaemon(True)
    vc = cv2.VideoCapture(0)
    # vc.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    thread.start()

    start_time = time.time()

    while True:

        frame = get_frame(vc)

        end_time = time.time()

        if end_time - start_time < 3.1:
            continue

        start_time = time.time()

        if not GUI.dead and not GUI.frozen:
            if azureFlag:
                emotions = get_facial_emotion(frame)
            else:
                face_isolated = facechop(frame)
                emotions = classify(None, face_isolated)
            if emotions:
                if Playlist2.is_playing():
                    current_song = Playlist2.get_current_song()
                    current_descriptors = Tracklist.get_song(db, sessionID, current_song)['descriptors']
                    emotion_list = getEmotionList(emotions)
                    descriptors.update_descriptors(emotion_list, current_descriptors)
                    progress_history.update_progress_log(db, sessionID, emotion_list)
                    current_song_score = descriptors.get_song_score(current_descriptors)
                    print('Current song score: %s' % current_song_score)
                    if current_song_score <= threshold:
                        Playlist2.skip_song()

                remove_frame("progress_plot")
                remove_frame("emotions_plot")
                # plotter.write_plot(emotions)
                GUI.refresh()
                print("ref")
                
            # print("New frame displayed in View")
            # for (x, y, h, w) in get_forehead_coordinates(frame):
            #     cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 50, 0), 1)
            #     break
            # HRV = heartrate.get_HRV(frame)
            # cv2.putText(frame, str(HRV), (20, 28), 3, 1, (0, 50, 200))

        # display_frame(frame)
        if GUI.dead:
            print("iese")
            break
            
        # print("nu iese")

    print("Closing camera")
    close_camera(vc)
    thread.join()
    


# frontal_classifier = load_classifiers([1, 0, 0, 0])[0]


if __name__ == "__main__": # TODO: Add CLI arguments (mainly for choosing between Azure and our model).
    main()
    # Face_process = multiprocessing.Process(target=main, name="EMMA")
    # Face_process.start()  # Also starts the GUI
    # #
    # Face_process.join()
    # print("Face Process just joined the main process")
    # print("EMMA will now be closed")
