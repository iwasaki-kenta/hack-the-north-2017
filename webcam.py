import cv2

cam = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video = cv2.VideoWriter('test.avi', fourcc, 20.0, (640, 116))

recording = False

while True:
    success, image = cam.read()
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
        if key == 32: # Space
            recording = not recording
            print("NOW", recording)
            pass

    # Handle recording video.

    if recording:
        video.write(image)

cam.release()
video.release()
cv2.destroyAllWindows()
