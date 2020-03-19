import os
import threading
import time
import cv2
from catalin.FaceNotDetectedError import FaceNotDetectedError
import catalin.azorel as azorel
import sys
import catalin.plotter as plotter
import catalin.GUI as GUI

from pymongo import MongoClient
from app import progress_history, track_history, aggdata, descriptors
from audio import Tracklist, Playlist2

#  Detection/classifier parameters
SCALE_FACTOR = 1.2
MIN_NEIGHBORS = 4

WHICH_CLASSIFIER = [1, 1, 1, 0]  # Choose index 1 for simple frontal, 2 for improved frontal, 3 for profile, 4 4 smile
CLASSIFIER_PATHS = ['haarcascade_frontalface_default.xml', 'haarcascade_profileface.xml',
                    'lbpcascade_frontalface_improved.xml',
                    # This can be copied from https://raw.githubusercontent.com/opencv/opencv/master/data/lbpcascades/lbpcascade_frontalface_improved.xml
                    'haarcascade_smile.xml']
# frontal_classifier = load_classifiers([1, 0, 0, 0])[0]


THRESHOLD = -10


def load_classifiers(which_classifiers):
    """
    Initializes image classifiers and returns them. Allows you to choose which to initialize by using which_classifier.
    :param which_classifiers: List containing 1 or 0, depending on which classifier you want to load.
    Index 1 is for simple frontal, 2 is for improved frontal, 3 for profile classifier and 4 for smile classifier.
    Ex: [0, 0, 0, 0] would load no classifier.
    :return: A list containing the initialized classifiers.
    """
    result = []

    for index in which_classifiers:
        if index != 1:
            result.append(None)
        else:
            result.append(cv2.CascadeClassifier(cv2.data.haarcascades + CLASSIFIER_PATHS[index]))

    return result


def draw_face_boxes(frame):
    """
    Loads face detection classifiers from Open-CV, detects face and draws corresponding boxes for each classifier.
    This alters the original frames, so it should be used before performing emotion recognition, etc.
    :param frame: Frame from camera (from Open-CV)
    """
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
    """
    Checks if the camera is open and takes a frame if so.
    :param video_camera: A cv2.VideoCapture object representing the camera.
    :return: Last frame taken by the camera.
    """
    if video_camera.isOpened():
        _, frame = video_camera.read()
    else:
        raise Exception("Camera is not opened")
    return frame


def display_frame(frame, title="Feedback Music Box"):
    """
    Mainly used for testing Open-CV functionalities. Creates a window displaying an arbitrary frame.
    :param frame: Frame to be displayed in the window.
    :param title: The title of the window. Can be changed. Default set to "Feedback Music Box"
    """
    cv2.imshow(title, frame)


def close_camera(video_camera):
    """
    Releases the camera from use and kills any existing windows of Open-CV.
    :param video_camera: A cv2.VideoCapture object representing the camera.
    """
    video_camera.release()
    cv2.destroyAllWindows()


def remove_frame(name="frame"):
    """
    Attempts to remove a .png from the system with a given name.
    :param name: The name of the .png file. Default is set to "frame"
    """
    path_to_image = os.path.join(sys.path[0], "{}.png".format(name))
    try:
        if os.path.isfile(path_to_image):
            os.chmod(path_to_image, 0o777)
            os.unlink(path_to_image)
            os.remove(path_to_image)
        else:
            print("{}.png is apparently not a file".format(name))
    except FileNotFoundError:
        return  # We can just ignore this, won't make a difference in functionality. FIX: use images as bytes
        # instead of files.
    except PermissionError:  # FIX: use sudo when starting the script
        return


def get_face_rectangles(azure_response):
    """
    Returns the rectangles corresponding to the faces detected by Azure
    :param azure_response: Response from Azure Face request as dictionary.
    :return: The rectangles of any detected face with the format: (width, height, left, top)
    """
    result = []
    for face in azure_response:
        result.append(face.face_rectangle)
    return result


def get_face_frames(frame, azure_response):
    """
    Cuts and returns images of the faces detected by Azure. Uses get_face_rectangles for cutting parameters.
    :param frame: The frame that we want to cut from. Should be on par with azure_response.
    :param azure_response: Response from Azure Face request as dictionary.
    :return: A list containing frames of faces detected by Azure.
    """
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
    """
    Estimates, cuts and returns frames containing a portion of a forehead based on the Azure response.
    Uses get_face_rectangles for cutting parameters.
    :param frame: The frame that we want to cut from. Should be on par with azure_response.
    :param azure_response: Response from Azure Face request as dictionary.
    :return: A list containing frames of forehead portions of detected faces.
    """
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
    """
    Estimates, cuts and returns frames containing a portion of a forehead from detected faces by Open-CV.
    Uses get_face_coordinates for cutting parameters.
    :param frame: The frame that we want to cut from.
    :return: A list containing frames of forehead portions of detected faces.
    """
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
    """
    Estimates and returns the coordinates of foreheads for the faces detected in the frame by Open-CV.
    :param frame: Any frame taken from the camera.
    :return: A list containing rectangles for the foreheads of detected faces. Formatted as (left, top, height, width).
    """
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
    """
    Estimates and returns the coordinates of faces detected in the frame by Open-CV. Uses a simple frontal classifier
    for detecting faces (it is required to load it as a global variable).
    :param frame: Any frame taken from the camera.
    :return: A list containing rectangles of the faces detected. Formatted as (left, top, height, width).
    """
    global frontal_classifier

    result = []
    gray = cv2.cvtColor(frame, 0)
    faces = frontal_classifier.detectMultiScale(gray, SCALE_FACTOR, MIN_NEIGHBORS)
    if len(faces) >= 1:
        for (x, y, h, w) in faces:
            result.append((x, y, h, w))
    else:
        raise FaceNotDetectedError()
    return result


def get_facial_emotion(frame):
    """
    Attempts to get facial emotion dictionary from Azure Face and saves the corresponding frame as file.
    Attempts to remove any old version before saving the file to prevent any file system issues.
    :param frame: Any frame taken from the camera.
    :return: Emotions as a dictionary. Empty if no face was detected by Azure.
    """
    remove_frame()
    cv2.imwrite("frame.png", frame)  # Saves the file
    try:
        detected_faces = azorel.get_faces()
        emotions = azorel.get_emotion(detected_faces)
    except FaceNotDetectedError:
        print("get_facial_emotion: Face was not detected by Azure. Please adjust your positioning.")
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
            emotions = get_facial_emotion(frame)
            if emotions:
                if Playlist2.is_playing():
                    current_song = Playlist2.get_current_song()
                    current_descriptors = Tracklist.get_song(db, sessionID, current_song)['descriptors']
                    emotion_list = getEmotionList(emotions)
                    descriptors.update_descriptors(emotion_list, current_descriptors)
                    progress_history.update_progress_log(db, sessionID, emotion_list)
                    current_song_score = descriptors.get_song_score(current_descriptors)
                    print('Current song score: %s' % current_song_score)
                    if current_song_score <= THRESHOLD:
                        Playlist2.skip_song()

                remove_frame("progress_plot")
                remove_frame("emotions_plot")
                plotter.write_plot(emotions)
                GUI.refresh()
                # print("ref")

        if GUI.dead:
            print("GUI is closed, shutting down...")
            break

    print("[EMMA]: Closing the camera...")
    close_camera(vc)
    thread.join()


if __name__ == "__main__":  # TODO: Add CLI arguments (mainly for choosing between Azure and our model).
    main()
    print("[EMMA]: I will be closed now. See you soon!")
