import firebase_admin
from firebase_admin import storage, firestore
from dataType import QuestionData
import os
import sys

# from google.cloud import storage

class Firebase():
    def __init__(self):
        super().__init__()


        cred = firebase_admin.credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred,{
        'storageBucket': 'gov-exams-cf534.appspot.com'
        })
        self.db = firestore.client()
        self.bucket = storage.bucket()


    def uploadImage(self,file_name):
        blob = self.bucket.blob(file_name)
        blob.upload_from_filename(file_name)
        blob.make_public()
        
        return blob.public_url
    
    def send2firebase(self, col_name, doc_name, data_arr):
        print(col_name)
        print(doc_name)
        ref = self.db.collection(col_name).document(doc_name).collection("questions")
        for data in data_arr:
            
            doc_ref = ref.document(data.number)
            doc_ref.set({"question":data.question,"image":data.q_image_url,"options":data.options,"optionImage":data.opt_image_url,"answer":data.answer,"descriptipn":data.description })
        self.delete_files_in_folder()
        python = sys.executable
        os.execl(python, python, *sys.argv)


    def get_exam_types(self):
        doc_snapshot = self.db.collection("exam-types").document("types").get()
        if doc_snapshot.exists:
            doc_data = doc_snapshot.to_dict()
            print(doc_data)
            return doc_data


    def delete_files_in_folder(self):
        folder_path = "temp/"
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"{file_path} dosyası silindi.")