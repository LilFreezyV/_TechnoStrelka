import imutils
import numpy
import telebot
import os
import cv2
import easyocr
from matplotlib import pyplot as pl

DATA = []

bot = telebot.TeleBot("7071139386:AAFsS-83DgpFqRevZ7UYk8N2htLPd-X0ok8")


@bot.message_handler(commands=["start"])
def start(message):
    DATA.append(message.text)
    mess = f"Здравствуйте, {message.from_user.first_name}!"
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=["info"])
def start(message):
    DATA.append(message.text)
    mess = f"Этот чат-бот - дополненная версия знакомого всем нам чат-бота Олег из приложения Тинькофф. " \
           f"Он обучает подрастающее поколение финансовой грамотности, помогает определять новости на фейк" \
           f" и делает много чего еще!"
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=["credits"])
def start(message):
    mess = f'Команда жестких работяг: ...'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    DATA.append(message.text)
    sentence = message.text
    pass


@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_extension = os.path.splitext(message.document.file_name)[1]
    bot.send_message(message.chat.id, 'фото в обработке...')
    with open(f'file{file_extension}', 'wb') as f:
        f.write(downloaded_file)
        img = cv2.imread(f'file{file_extension}')
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


    #pl.imshow(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    #pl.show()

    bot.send_message(message.chat.id, result)


bot.polling(none_stop=True)
print(DATA)
