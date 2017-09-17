import cv2

cam = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video = cv2.VideoWriter('test.avi', fourcc, 20.0, (640, 480))

recording = False

while True:
    success, image = cam.read()

    image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    image_channels = cv2.split(image)

    image_channels[0] = cv2.equalizeHist(image_channels[0])
    image = cv2.merge(image_channels)
    image = cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)

    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), 90, 1)
    image = cv2.warpAffine(image, rotation_matrix, (width, height))

    # image = cv2.fastNlMeansDenoisingColored(image)

    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayscale = cv2.GaussianBlur(grayscale, (5, 5), 0)

    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # grayscale = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    grayscale = cv2.Canny(grayscale, 100, 200)

    _, contours, hierarchy = cv2.findContours(grayscale, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

    cv2.imshow('Webcam', image)

    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break
    else:
        key = key & 0xFF
        print(key)
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
