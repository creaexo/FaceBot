import time

import requests
import telebot
from telebot import types



bot = telebot.TeleBot('6362163618:AAE7qhovHRXqaDiMAqYbHeEBqpkb14LbJKE')
# Обновить маркап
def markup1():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn = types.KeyboardButton('Получить изображение')
    btn2 = types.KeyboardButton('Получить 9 изображений')
    btn3 = types.KeyboardButton('Своё количество')
    markup.add(btn,btn2,btn3)
    return markup

def markup2():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn = types.KeyboardButton('Назад')
    btn2 = types.KeyboardButton('30')
    btn3 = types.KeyboardButton('60')
    btn4 = types.KeyboardButton('90')
    markup.add(btn,btn2,btn3,btn4)
    return markup

# Приветственное сообщение
@bot.message_handler(commands=['start'])
def start(message):
    send_mess = "Привет! Нажми на кнопку и получи сгенерированное лицо"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup1())
# Распознование текстовых команд
@bot.message_handler(content_types=['text'])
def get_face(message):
    command = message.id
    try:
        bot.delete_message(message.chat.id, message.id-1)
    except Exception as E:
        print(str(E)+" - "+str(message.id-1))
    get_message_bot = message.text.strip().lower()
    done = False
    if get_message_bot == 'получить изображение':
        done = False
        p = requests.get("https://thispersondoesnotexist.com/")
        out = open("images/img.jpg", "wb")
        out.write(p.content)
        out.close()
        img = open("images/img.jpg", "rb")
        bot.send_photo(message.chat.id, img)
        try:
            bot.delete_message(message.chat.id, message.id)
        except:
            pass
        done = True
        # bot.send_message(message.chat.id, parse_mode='html', reply_markup=markup)
    elif get_message_bot == 'получить 9 изображений':
        done = False
        images = []
        progress = bot.send_message(message.chat.id, f"Генерация 0/9. Не отправляйне мне сообщения, пока она не закончится, а то произойдёт ошибка.", parse_mode='html')
        for i in range(1,10):
            p = requests.get("https://thispersondoesnotexist.com/")
            out = open(f"images/img{i}.jpg", "wb")
            out.write(p.content)
            out.close()
            images.append(telebot.types.InputMediaPhoto(open(f'images/img{i}.jpg', 'rb')))
            bot.edit_message_text(chat_id=message.chat.id, message_id=progress.message_id, text=f"Генерация {i}/9. Не отправляйне мне сообщения, пока она не закончится, а то произойдёт ошибка.")
        try:
            bot.delete_message(message.chat.id, progress.message_id)
        except:
            pass
        try:
            bot.delete_message(message.chat.id, command)
        except:
            pass
        bot.send_media_group(message.chat.id, images)
        done = True
    elif get_message_bot == 'своё количество':
        done = False
        msg = bot.send_message(message.chat.id, 'Напишите, сколько лиц сгенерировать. Максимум 100', parse_mode='html',
                               reply_markup=markup2())
        @bot.message_handler(content_types=['text'])
        def get_q_faces(message):
            if message.text == 'Назад':
                try:
                    bot.delete_message(message.chat.id, message.id)
                except:
                    pass
                try:
                    bot.delete_message(message.chat.id, msg.message_id)
                except:
                    pass
                bot.send_message(message.chat.id, f"Вы вернулись на главную страницу", parse_mode='html',
                                 reply_markup=markup1())
                return False
            q = 0
            try:
                q = int(message.text)
            except:
                pass
            if q>0 and q<=100:
                images = []
                progress = bot.send_message(message.chat.id, f"Генерация 0/{q}. Не отправляйне мне сообщения, пока она не закончится, а то произойдёт ошибка.", parse_mode='html')
                for i in range(1, q+1):
                    p = requests.get("https://thispersondoesnotexist.com/")
                    out = open(f"images/img{i}.jpg", "wb")
                    out.write(p.content)
                    out.close()
                    images.append(telebot.types.InputMediaPhoto(open(f'images/img{i}.jpg', 'rb')))
                    bot.edit_message_text(chat_id=message.chat.id, message_id=progress.message_id,
                                          text=f"Генерация {i}/{q}. Не отправляйне мне сообщения, пока она не закончится, а то произойдёт ошибка.")
                    if (i % 9 == 0 and i != 0) or i == q:
                        try:
                            bot.delete_message(message.chat.id, progress.message_id)
                        except:
                            pass
                        bot.send_media_group(message.chat.id, images)
                        progress = bot.send_message(message.chat.id, f"Генерация {i}/{q}. Не отправляйне мне сообщения, пока она не закончится, а то произойдёт ошибка.", parse_mode='html')
                        images = []
                try:
                    bot.delete_message(message.chat.id, progress.message_id)
                except:
                    pass
                bot.send_message(message.chat.id, "Готово! Выберите следующую команду", parse_mode='html',
                                 reply_markup=markup1())
            else:
                bot.register_next_step_handler(bot.send_message(message.chat.id, f"Введите число <b>от 0 до 100</b>",
                                                                parse_mode='html', reply_markup=markup2()), get_q_faces)

        # get_q_faces()
        bot.register_next_step_handler(msg, get_q_faces)
    else:
        bot.send_message(message.chat.id, f"главную страницу", parse_mode='html',
                         reply_markup=markup1())
    if done:
        print("готова - " + str(message.id - 1))
        bot.send_message(message.chat.id, "Готово! Выберите следующую команду", parse_mode='html', reply_markup=markup1())
        # bot.send_message(message.chat.id, "Готово", parse_mode='html', reply_markup=markup1())
bot.polling(none_stop=True)