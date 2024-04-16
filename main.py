import imutils
import numpy
import telebot
import os
import cv2
import easyocr
from matplotlib import pyplot as pl
from AI_scripts import get_car_numbers
from SpeechRecognizer import SpeechRecognizer

DATA = []

bot = telebot.TeleBot("7071139386:AAFsS-83DgpFqRevZ7UYk8N2htLPd-X0ok8")
recognizer = SpeechRecognizer()


@bot.message_handler(commands=["start"])
def start(message):
    DATA.append(message.text)
    mess = f"Здравствуйте, {message.from_user.first_name}!"
    bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types=['voice'])
def process_voice(message):
    voice_path = "sound.wav"
    text_path = "recognized_text.txt"

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(voice_path, "wb") as f:
        f.write(downloaded_file)
    temp_res, temp_res_text = recognizer.Recognize(voice_path, text_path)
    if temp_res == 1:
        bot.send_message(message.chat.id, f"Неизвестная ошибка: {temp_res_text}")
    else:
        with open(text_path, "r") as f:
            lines = f.readlines()
            bot.send_message(message.chat.id, lines)


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

    result = get_car_numbers(downloaded_file, file_extension)

    # pl.imshow(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    # pl.show()

    bot.send_message(message.chat.id, result)


bot.polling(none_stop=True)
print(DATA)
