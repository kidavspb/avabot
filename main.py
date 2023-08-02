import telebot
from PIL import Image
import time
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s - %(levelname)s: %(lineno)d - %(message)s",
    handlers=[
        logging.FileHandler("Ava.log"),
        logging.StreamHandler()
    ],
    datefmt='%d/%b %H:%M:%S',
)

TOKEN = "token_here"
bot = telebot.TeleBot(TOKEN)

while True:
    try:
        @bot.message_handler(commands=['start'])
        def welcome_message(message):
            logging.info(f"Start message from user @{message.from_user.username}")
            bot.send_message(message.chat.id, "Здравствуйте! Пожалуйста, пришлите ваш квадратный аватар")


        @bot.message_handler(content_types=['photo'])
        def get_image(message):
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)
            with open("avatar.png", 'wb') as new_file:
                new_file.write(downloaded_file)
            logging.info(f"Get image from user @{message.from_user.username}")

            foreground = Image.open('template.png')

            background = Image.open("avatar.png")
            background = background.resize(foreground.size, Image.LANCZOS)

            background = background.convert("RGBA")
            foreground = foreground.convert("RGBA")

            background.paste(foreground, (0, 0), foreground)
            background.save("result.png", "PNG")
            logging.info(f"Result saved")

            background.close()
            foreground.close()

            with open("result.png", 'rb') as result:
                bot.send_photo(message.chat.id, result)
                logging.info(f"Sent avatar to user @{message.from_user.username}")

        logging.info("Bot running...")
        bot.polling(none_stop=True)

    except Exception as e:
        logging.error(e)
        bot.stop_polling()

        time.sleep(15)

        logging.info("Running again!")
