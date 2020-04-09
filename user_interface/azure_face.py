from azure.cognitiveservices.vision.face import FaceClient, models
from msrest.authentication import CognitiveServicesCredentials

from user_interface.FaceNotDetectedError import FaceNotDetectedError

import configparser

config = configparser.ConfigParser()
config.read('settings.cfg')

# This key will serve all examples in this document.
# KEY = "3108ba7dc2f84239b1b94961906167aa"
KEY = config['AZURE']['AZURE_KEY']

# This endpoint will be used in all examples in this quickstart.
# ENDPOINT = "https://designprojectfacetest.cognitiveservices.azure.com"
ENDPOINT = config['AZURE']['AZURE_ENDPOINT']

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
emotion_attribute = models.FaceAttributeType.emotion


def request():
    """
    Asks the Azure Face API to detect faces from a file. It more specifically asks for the emotion_attribute. It also
    asks Azure to use 'recognition_02' model which is a little bit more accurate than 'recognition_01' (default).
    :return: A dictionary containing the detected faces and their associated attributes.
    """
    return face_client.face.detect_with_stream(image=open("frame.png", 'rb'),
                                               return_face_attributes=[emotion_attribute],
                                               recognition_model='recognition_02')


def get_faces():
    """
    Attempts to get a response from Azure given the current frame in the file system.
    :return: A dictionary containing the detected faces and their associated attributes.
    :raise: FaceNotDetectedError to alert EMMA that Azure did not detect any face.
    """
    detected_faces = request()

    if not detected_faces:
        raise FaceNotDetectedError()
    return detected_faces


def get_emotion(detected_faces):
    """
    Looks into the response of Azure and compiles an easy-to-read dictionary of emotion values for
    the first detected face.
    :param detected_faces: A dictionary containing the detected faces and their associated attributes.
    :return: A dictionary containing the emotion values of the first detected face.
    """
    result = {}
    for face in detected_faces:
        emotions = face.face_attributes.emotion
        result[face.face_id] = {'anger': emotions.anger,
                                'contempt': emotions.contempt,
                                'disgust': emotions.disgust,
                                'fear': emotions.fear,
                                'happiness': emotions.happiness,
                                'neutral': emotions.neutral,
                                'sadness': emotions.sadness,
                                'surprise': emotions.surprise}

        break  # !! IMPORTANT !!: We are only checking the first face that has been detected.

    return result
