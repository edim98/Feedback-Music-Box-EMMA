# import asyncio
#import io
#import glob #TODO: Change module name to something else...
import os
#import sys
#import time
#import uuid
#import requests
#from urllib.parse import urlparse
#from io import BytesIO
#from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient, models
from msrest.authentication import CognitiveServicesCredentials
#from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, \
    #OperationStatusType
from catalin.FaceNotDetectedError import FaceNotDetectedError

# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = "3108ba7dc2f84239b1b94961906167aa"

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "https://designprojectfacetest.cognitiveservices.azure.com"

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
emotion_attribute = models.FaceAttributeType.emotion


def request():
    return face_client.face.detect_with_stream(image=open("frame.png", 'rb'),
                                               return_face_attributes=[emotion_attribute],
                                               recognition_model='recognition_02')


def get_faces():
    detected_faces = request()

    if not detected_faces:
        raise FaceNotDetectedError()
    return detected_faces


def get_emotion(detected_faces):
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

        break  # IMPORTANT: We are only checking the first face that has been detected

    return result
