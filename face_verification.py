import glob

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


class FaceVerification:
    KEY = 'b9728001037d4e409030bd1ed1cc687f'
    ENDPOINT = 'https://designprojectfacetest.cognitiveservices.azure.com/'
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

    def __init__(self, target_person_name):
        print("Initializing the FaceVerification module")
        self.set_target_person(target_person_name)
        

    def set_target_person(self, target_person_name):
        self.set_target_person_name(target_person_name)
        self.set_target_face_id()

    def set_target_person_name(self, person_name):
        if (len(person_name) == 0):
            raise ValueError("Cannot supply person name of length 0 to the FaceVerification module")
        else:
            self.person_name = person_name
    
    def set_target_face_id(self):
        img_fns = self.get_images_of_target_person()
        self.target_face_id = self.get_face_ids(img_fns)[0] # only taking a single face as the target for now
        print("set target face id to", self.target_face_id)

    def get_images_of_target_person(self):
        path = "user_verification/" + self.person_name
        img_filenames = glob.glob(path + "//*.jpg")
        if len(img_filenames) == 0:
            raise Exception("You must first supply some example pictures of the patient in this session")
        else:
            return img_filenames

    def get_face_ids(self, img_fns):
        face_ids = []
        for img_fn in img_fns:
            detected_faces = self.face_client.face.detect_with_stream(image=open(img_fn, 'rb'),
                                               return_face_id = True,
                                               recognition_model='recognition_02')
            if len(detected_faces) != 1:
                print(img_fn, " is rejected, because the number of detected face is not 1")
                continue
            else:
                face_ids.append(detected_faces[0].face_id)
            
        return face_ids


    def find_verified_face(self, detected_faces):
        for face in detected_faces:
            current_face_id = face.face_id
            target_face_id = self.target_face_id
            verify_result = self.face_client.face.verify_face_to_face(current_face_id, target_face_id)

            if verify_result.is_identical:
                print("same person, super lit")
                return face, verify_result.confidence
            else:
                print("different person, skipping")
                continue
        # get id list of supplied faces
        # get an id to compare to
        # find the face with the highest confidence of being the same
        # return that face

        return None, -1



# =========================
fv = FaceVerification("me")

comp_photos = glob.glob("comp/what.jpg")
for photo_fn in comp_photos:
    print("ayo : ", photo_fn)
    some_faces = fv.face_client.face.detect_with_stream(image=open(photo_fn, 'rb'),
                                               return_face_id = True,
                                               recognition_model='recognition_02')
    print(some_faces)
    face, confidence = fv.find_verified_face(some_faces)
    print(face, confidence)
    print(face.face_rectangle)
    # break