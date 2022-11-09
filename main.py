import telebot
from telebot import types
import sqlite3

bot=telebot.TeleBot('5701526571:AAHj4t7GN4T6uTdjjKnp1LBvUYtgFaaygpg')
conn=sqlite3.connect('planner.db')
cursor=conn.cursor()

try:
    query = "CREATE TABLE \"planner\" (\"ID\" INTEGER UNIQUE,\"user_id\" INTEGER,\"plan\" TEXT, PRIMARY KEY (\"ID\"))
    cursor.execute(query)
except:
    pass

@bot.message_handler(commands=['start'])
def send_keyboard(message,text='Привет, чем я могу тебе помочь?'):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1=types.KeyboardButton('Добавить дело в список')
    itembtn2=types.KeyboardButton('Показать список дел')
    itembtn3=types.KeyboardButton('Удалить дело из списка')
    itembtn4=types.KeyboardButton('Удалить все дела из списка')
    itembtn5=types.KeyboardButton('Другое')
    itembtn6=types.KeyboardButton('Пока все!')
    keyboard.add(itembtn1,itembtn2)
    keyboard.add(itembtn3,itembtn4,itembtn5,itembtn6)

    msg = bot.send_message(message.from_user.id,
                    text=text,reply_markup=keyboard)
    bot.register_next_step_handler(msg,callback_worker)



def callback_worker(call):
    if call.text=='Добавить дело в список':
        msg=bot.send_message(call.chat.id, 'Давайте добавим дело!Напишите его в чат')
        bot.register_next_step_handler(msg,add_plan)
    elif call.text=='Показать список дел':
        try:
            show_plans(call)
        except:
            bot.send_message(call.chat.id,'Здесь пусто. Можно отдыхать!')
            send_keyboard(call,'Чем еще могу помочь?')
    elif call.text=='Удалить дело из списка':
        try:
            delete_one_plan(call)
        except:
            bot.send_message(call.chat.id,'Здесь пусто. Можно отыхать!')
            send_keyboard(call,'Чем еще могу помочь?')
    elif call.text=='Удалить все дела из списка':
        try:
            delete_all_plan(call)
        except:
            bot.send_message(call.chat.id,'Здесь пусто. Иди отдыхай!')
            send_keyboard(call,'Чем еще могу помочь?')
    elif call.text=='Другое':
        bot.send_message(call.chat.id,'Я больше пока ничего не умею!')
        send_keyboard(call,'Чем-то еще могу помочь?')
    elif call.text=='Пока все!':
        bot.send_message(call.chat.id,'Пока! Если захочешь продолжить нажми /start')



bot.polling(none_stop=True)