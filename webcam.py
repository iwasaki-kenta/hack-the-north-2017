import base64
import re

import cv2
import requests

import config
from stitcher import stitch_images, get_candidate_image_positions, firebase_upload

from sklearn.externals import joblib
import indicoio

classifier = joblib.load('classifier.pkl')
indicoio.config.api_key = config.indico_key()



def finish_recording(images):
    result = stitch_images(images, get_candidate_image_positions(images))
    cv2.imwrite("ocr.png", result)

    # Perform OCR.

    with open("ocr.png", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
        payload = {
            "requests": [
                {
                    "image": {
                        "content": encoded_image
                    },
                    "features": [
                        {
                            "type": "TEXT_DETECTION"
                        }
                    ]
                }
            ]
        }

    r = requests.post('https://vision.googleapis.com/v1/images:annotate?key=' + config.google_key(), json=payload)
    text = r.json()['responses'][0]['textAnnotations'][0]['description']

    print("OCR Result:", text)

    sentence = re.sub('[^0-9a-zA-Z]+', ' ', text).strip()
    features = indicoio.text_features(sentence)

    category = classifier.predict([features])[0]

    firebase_upload(config.google_key(), text, category)


if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    recording = False
    count = 0
    images = []

    while True:
        success, image = cam.read()

        if success:
            height, width = image.shape[:2]

            rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), 90, 1)
            image = cv2.warpAffine(image, rotation_matrix, (width, height))

            image = image[int(height / 2) - 58: int(height / 2) + 58, :]

            cv2.imshow('Webcam', image)

            key = cv2.waitKey(1)
            if key == 27:  # ESC
                break
            else:
                key = key & 0xFF
                if key == 32:  # Space
                    recording = not recording
                    if recording:
                        images = []
                    else:
                        finish_recording(images)
                    print("NOW", recording)
                    pass

            # Handle recording video.

            if recording:
                images.append(image)

    cam.release()
    cv2.destroyAllWindows()
