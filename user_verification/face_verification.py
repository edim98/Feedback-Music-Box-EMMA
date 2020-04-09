import glob
import os
import configparser

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


class FaceVerification:

    config = configparser.ConfigParser()
    config.read('settings.cfg')

    KEY = config['FACE_IDENTIFICATION']['FACE_IDENTIFICATION_KEY']
    ENDPOINT = config['FACE_IDENTIFICATION']['FACE_IDENTIFICATION_ENDPOINT']
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    isSetUp = False

    def __init__(self, target_person_name, testFlag):
        if len(target_person_name) == 0:
            raise ValueError("Cannot supply person name of length 0 to the FaceVerification module")

        self.person_name = target_person_name
        self.target_face_id = self.get_target_face_id()
        self.testFlag = testFlag
        # print("Initialized the FaceVerification module with name", self.person_name,
        #       ", and face_id:", self.target_face_id)

    def set_target_face_id(self, face_id):
        self.target_face_id = face_id

    def get_target_face_id(self):
        img_fns = self.__get_images_of_target_person()
        if img_fns:
            return self.__get_face_ids(img_fns)[0]  # only taking a single face as the target for now
        return None

    def __get_images_of_target_person(self):
        # path = self.person_name
        path = os.path.relpath('user_verification/' + self.person_name)
        img_files = glob.glob(path + "/*.png")
        if len(img_files) == 0:
            # raise Exception("You must first supply some example pictures of the patient in this session")
            if self.testFlag:
                print('No images of target person were found...')
            self.isSetUp = False
            return None
        else:
            return img_files

    def __get_face_ids(self, img_fns):
        face_ids = []
        for img_fn in img_fns:
            detected_faces = self.face_client.face.detect_with_stream(image=open(img_fn, 'rb'),
                                                                      return_face_id=True,
                                                                      recognition_model='recognition_02')
            if len(detected_faces) != 1:
                # print(img_fn, " is rejected, because the number of detected face is not 1")
                continue
            else:
                face_ids.append(detected_faces[0].face_id)

        return face_ids

    def find_verified_face(self, detected_faces):
        """
        Attempts to find and return a face that would belong to the person specified upon initialization of the module.
        If not found, returns None.
        :param detected_faces: a face bunch from azure, where we don't know who they belong to
        :return: A tuple of a face that belongs to the target person, and the confidence. (None, -1) if no face matches.
        """
        for face in detected_faces:
            current_face_id = face.face_id
            target_face_id = self.target_face_id
            # print('cur face: ', current_face_id)
            # print('target face: ', target_face_id)
            verify_result = self.face_client.face.verify_face_to_face(current_face_id, target_face_id)

            if verify_result.is_identical:
                if self.testFlag:
                    print("Found the person we're looking for")
                return face, verify_result.confidence
            else:
                if self.testFlag:
                    print("Found a different person, skipping")
                continue

        return None, -1

    def getStatus(self):
        return self.isSetUp

    def setStatus(self, status):
        self.isSetUp = status


if __name__ == "__main__":
    fv = FaceVerification("mantas")

    comp_photos = glob.glob("comp/what.jpg")
    for photo_fn in comp_photos:
        some_faces = fv.face_client.face.detect_with_stream(image=open(photo_fn, 'rb'),
                                                            return_face_id=True,
                                                            recognition_model='recognition_02')
        face, confidence = fv.find_verified_face(some_faces)
        print(face, confidence)
        print(face.face_rectangle)
