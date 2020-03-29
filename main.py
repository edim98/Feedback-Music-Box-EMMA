import threading
import time
import cv2

from face_verification import FaceVerification
from user_interface.FaceNotDetectedError import FaceNotDetectedError
import user_interface.azure_face as azure
from user_interface.face_utils import get_frame, remove_frame, close_camera
import user_interface.plotter as plotter
import user_interface.GUI as GUI
import other_scripts.CLIparser as CLIparser

from pymongo import MongoClient
from app import progress_history, track_history, aggdata, descriptors
from audio import Tracklist, Playlist
from model.fast_and_cam import facechop, classify

THRESHOLD = -10


def get_facial_emotion(frame, face_verification = None):
    """
    Attempts to get facial emotion dictionary from Azure Face and saves the corresponding frame as file.
    Attempts to remove any old version before saving the file to prevent any file system issues.
    :param frame: Any frame taken from the camera.
    :return: Emotions as a dictionary. Empty if no face was detected by Azure.
    """
    remove_frame()
    cv2.imwrite("frame.png", frame)  # Saves the file
    try:
        detected_faces = azure.get_faces()
        if face_verification is not None:
            verified_face, confidence = face_verification.find_verified_face(detected_faces)
            emotions = azure.get_emotion([verified_face])
        else:
            emotions = azure.get_emotion(detected_faces)
    except FaceNotDetectedError:
        print("get_facial_emotion: Face was not detected by Azure. Please adjust your positioning.")
        emotions = {}

    return emotions


def initialize():
    """
    Initialize the MongoDB client and create all collections.
    :return: Nothing.
    """

    client = MongoClient()
    db = client.test_database
    sessionID = 'test'

    track_history.create_track_log(db, sessionID)
    print('Created track history...')

    progress_history.create_progress_log(db, sessionID)
    print('Created progress history...')

    aggdata.create_agg_log(db, sessionID)
    print('Created aggregated data logs...')

    #TODO: raise IndexError('Cannot choose from an empty sequence') from None
    Playlist.song_player(db, sessionID)

    return db, sessionID


def getEmotionList(emotions):
    """
    Get the emotion list from an Azure response.
    :return: A list of user emotions from an Azure response.
    """

    emotionList = []
    for face_id in emotions:
        return emotions[face_id]


def main():
    """
    Main method.
    """

    # Choose running model.
    azureFlag = CLIparser.parseFlags()

    db, sessionID = initialize()

    fv = FaceVerification("mantas")

    # Start the camera and the GUI.
    thread = threading.Thread(target=GUI.run)
    thread.setDaemon(True)
    vc = cv2.VideoCapture(0)
    # vc.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    thread.start()

    start_time = time.time()

    while True:

        frame = get_frame(vc)

        # Query the Model once every 3 seconds.
        end_time = time.time()

        if end_time - start_time < 3.1:
            continue

        start_time = time.time()

        if not GUI.dead and not GUI.frozen:
            if azureFlag:
                # Query Azure.
                emotions = get_facial_emotion(frame, fv)
            else:
                # Query our model.
                face_isolated = facechop(frame)
                emotions = classify(None, face_isolated)
            if emotions:
                if Playlist.is_playing():
                    # Update global descriptors based on song descriptors and user emotions.
                    current_song = Playlist.get_current_song()
                    current_descriptors = Tracklist.get_song(db, sessionID, current_song)['descriptors']
                    emotion_list = getEmotionList(emotions)
                    descriptors.update_descriptors(emotion_list, current_descriptors)
                    progress_history.update_progress_log(db, sessionID, emotion_list)
                    current_song_score = descriptors.get_song_score(current_descriptors)
                    print('Current song score: %s' % current_song_score)

                    # Change song if song score is low.
                    if current_song_score <= THRESHOLD:
                        Playlist.skip_song()

                remove_frame("progress_plot")
                remove_frame("emotions_plot")
                plotter.write_plot(emotions)
                GUI.refresh()

        if GUI.dead:
            print("GUI is closed, shutting down...")
            break

    print("[EMMA]: Closing the camera...")
    close_camera(vc)
    thread.join()


if __name__ == "__main__":  # TODO: Add CLI arguments (mainly for choosing between Azure and our model).
    main()
    print("[EMMA]: I will be closed now. See you soon!")
