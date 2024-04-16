import cv2
import easyocr
import numpy
import imutils


def get_car_numbers(file, extension):
    with open(f'file{extension}', 'wb') as f:
        f.write(file)
        img = cv2.imread(f'file{extension}')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # создаём фильтр для фото, чтобы уменьшить шум
    img_filter = cv2.bilateralFilter(gray, 11, 15, 15)
    # находим углы изображения
    edges = cv2.Canny(img_filter, 30, 200)
    # находим контуры изображения
    cont = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cont = imutils.grab_contours(cont)
    cont = sorted(cont, key=cv2.contourArea, reverse=True)
    position = None
    for el in cont:
        approx = cv2.approxPolyDP(el, 12, True)
        if len(approx) == 4:
            position = approx
            break

    mask = numpy.zeros(gray.shape, numpy.uint8)
    new_img = cv2.drawContours(mask, [position], 0, 255, -1)
    bitwise_img = cv2.bitwise_and(img, img, mask=mask)

    x, y = numpy.where(mask == 255)
    x1, y1 = numpy.min(x), numpy.min(y)
    x2, y2 = numpy.max(x), numpy.max(y)
    crop = gray[x1:x2, y1:y2]

    text = easyocr.Reader(['en'])
    text = text.readtext(crop)
    result = text[0][-2][:6]
    return result


def ai_dialog(sentence):
    pass

