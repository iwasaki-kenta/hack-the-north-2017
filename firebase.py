import pyrebase

import config

config = {
    "apiKey": config.google_key(),
    "authDomain": "test-764cc.firebaseapp.com",
    "databaseURL": "https://test-764cc.firebaseio.com",
    "storageBucket": "test-764cc.appspot.com",
    "serviceAccount": "firebase_key.json"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

image_key = db.generate_key()

user = auth.sign_in_with_email_and_password("dranithix@gmail.com", "hahaha")
storage.child("images/" + image_key + ".png").put("ocr.png")

image_url = storage.child("images/" + image_key + ".png").get_url(None)

data = {
    "user": user['idToken'],
    "note": "OCR Text Here",
    "image": image_url,
    "category": -1
}

db.child("notes").push(data)

