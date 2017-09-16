"""
Video-based text stitcher & OCR.

Kenta Iwasaki & Vikram Sambamurthy
"""

import numpy as np

h_ratio = 0.8


def detect_edges(image, t1=50, t2=100):
    return cv2.Canny(image, t1, t2)


def crop_candidate_template(image):
    global h_ratio

    h, w = image.shape[:2]
    x1, y1, x2, y2 = int(float(w) * (1 - h_ratio)), 0, w, h
    return image[y1:y2, x1:x2]


def extend_image(image, top, bottom, left, right):
    h, w = image.shape[:2]
    result = np.zeros((h + top + bottom, w + left + right, 3), np.uint8)
    result[top:top + h, left:left + w] = image
    return result


def calculate_resulting_size(images, locations):
    global h_ratio

    max_margin_top = 0;
    max_margin_bottom = 0
    current_margin_top = 0
    current_margin_bottom = 0

    h_init, w_init = images[0].shape[:2]
    w_final = w_init

    for i in range(0, len(locations)):
        h, w = images[i].shape[:2]
        h2, w2 = images[i + 1].shape[:2]

        current_margin_top += locations[i][1]
        current_margin_bottom += (h2 - locations[i][1]) - h

        if current_margin_top > max_margin_top: max_margin_top = current_margin_top
        if current_margin_bottom > max_margin_bottom: max_margin_bottom = current_margin_bottom

        x_templ = int(float(w) * h_ratio)
        w_final += (w2 - x_templ - locations[i][0])

    h_final = h_init + max_margin_top + max_margin_bottom
    return max_margin_top, h_final, w_final


# Find feasible locations to template-match sequence candidates in a list. (1 -> 2, 2 -> 3)
def get_candidate_image_positions(images):
    image_locations = []
    for i in range(0, len(images) - 1):
        template = crop_candidate_template(images[i])
        template = detect_edges(template)

        candidate_height, candidate_width = template.shape[:2]

        margin_top = margin_bottom = candidate_height
        margin_left = margin_right = 0

        # Enlarge image by adding in margins.
        img = extend_image(images[i + 1], margin_top, margin_bottom, margin_left,
                           margin_right)

        # Detect the edges of the image.
        img = detect_edges(img)

        # Find a match to the template.
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF)
        _, _, _, best_candidate_position = cv2.minMaxLoc(res)

        # Subtract unnecessary margins.
        rectified_candidate_position = (
            best_candidate_position[0] - margin_left, best_candidate_position[1] - margin_top)
        image_locations.append(rectified_candidate_position)
    return image_locations


def stitch_images(imgs, templates_loc):
    y_offset, h_final, w_final = calculate_resulting_size(imgs, templates_loc)
    result = np.zeros((h_final, w_final, 3), np.uint8)

    h_init, w_init = imgs[0].shape[:2]
    result[y_offset:y_offset + h_init, 0:w_init] = imgs[0]
    origin = (y_offset, 0)

    for j in range(0, len(templates_loc)):
        h, w = imgs[j].shape[:2]
        ch, cw = imgs[j + 1].shape[:2]

        # Compute coordinates to stitch template into final image.
        y1 = origin[0] - templates_loc[j][1]
        y2 = origin[0] - templates_loc[j][1] + ch
        x_templ = int(float(w) * (1 - h_ratio))

        x1 = origin[1] + x_templ - templates_loc[j][0]
        x2 = origin[1] + x_templ - templates_loc[j][0] + cw

        result[y1:y2, x1:x2] = imgs[j + 1]  # Copy template into result.
        origin = (y1, x1)  # Shift new origin point for next candidate template image.

    return result


if __name__ == '__main__':
    import cv2

    # Read video frames.
    video = cv2.VideoCapture('video1.mp4')

    images = []

    while True:
        success, image = video.read()

        if success:
            images.append(image)
        else:
            break

    # Perform stitching.
    result = stitch_images(images, get_candidate_image_positions(images))

    grayscale = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, grayscale = cv2.threshold(grayscale, 127, 255, 0)
    _, contours, hierarchy = cv2.findContours(grayscale, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = cv2.minAreaRect(max(contours, key=cv2.contourArea))

    angle = largest_contour[2]
    height, width = grayscale.shape[:2]

    # Normalize rotation.
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    result = cv2.warpAffine(result, rotation_matrix, (width, height))

    copy = cv2.boxPoints((largest_contour[0], largest_contour[1], 0.0))
    region_vertices = np.int0(cv2.transform(np.array([copy]), rotation_matrix))[0]
    region_vertices[region_vertices < 0] = 0

    # Normalize translation.
    result = result[region_vertices[1][1]:region_vertices[0][1], region_vertices[1][0]:region_vertices[2][0]]

    cv2.imwrite("ocr.png", result)

    # Perform OCR.
    import base64
    import requests
    import config

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
    print(r.json()['responses'][0]['textAnnotations'][0]['description'])
