import telebot

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


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    DATA.append(message.text)
    sentence = message.text
    bot.reply_to(message, sentence)


bot.polling(none_stop=True)
print(DATA)
