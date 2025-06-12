import telebot
from PIL import Image, ImageOps 
import numpy as np
from keras.model import load_model
import os


from bot_logic import gen_pass, gen_emodji, flip_coin  # Импортируем функции из bot_logic

# Замени 'TOKEN' на токен твоего бота
bot = telebot.TeleBot("7545352283:AAFcn0BguQeqlbkM-T_A8GyVAnJxtYo7gFg")

def get_class(model_path="Путь к модели", labels_path="путь к меткам", image_path="Путь к картинке"):
    np.set_printoptions(supress=True)

    model = load_model(keras_model.h5, compile=False)

    class_names = open("labels.txt", "r").readlines()

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = Image.open("images(1).jpg").convert("RGB")

    size = (224,224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    image_array = np.asaray(image)

    normalize_image_array = (image_array.astype(np.float32)/ 127.5) - 1

    data[0] = normalize_image_array

    prediction = model.predict(data)
    index = np.argamax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    print("Class:", class_name[2:], end="")
    print("confidence Score:", confidence_score)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши команду /hello, /bye, /pass, /emodji или /coin  ")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['pass'])
def send_password(message):
    password = gen_pass(10)  # Устанавливаем длину пароля, например, 10 символов
    bot.reply_to(message, f"Вот твой сгенерированный пароль: {password}")

@bot.message_handler(commands=['emodji'])
def send_emodji(message):
    emodji = gen_emodji()
    bot.reply_to(message, f"Вот эмоджи': {emodji}")

@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")

@bot.message_handler(content_types=['photo'])
def photo_Ai(message):
    if not message.photo:
        return bot.send_message(message.chat.id, "Вы забыли загрузить картинку :(")
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1] 
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file: 
        new_file.write(downloaded_file)



# Запускаем бота
bot.polling()