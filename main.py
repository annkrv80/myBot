import telebot
from telebot import types
import sqlite3
import random
import os


bot=telebot.TeleBot('5701526571:AAHj4t7GN4T6uTdjjKnp1LBvUYtgFaaygpg')
conn=sqlite3.connect('planner.db')
cursor=conn.cursor()

@bot.message_handler(commands=['start'])
def send_keyboard(message,text='Привет, чем я могу тебе помочь?'):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1=types.KeyboardButton('Добавить дело в список')
    itembtn2=types.KeyboardButton('Показать список дел')
    itembtn3=types.KeyboardButton('Удалить дело из списка')
    itembtn4=types.KeyboardButton('Удалить все дела из списка')
    itembtn5=types.KeyboardButton('Мотивация')
    itembtn6=types.KeyboardButton('Пока все!')
    keyboard.add(itembtn1,itembtn2)
    keyboard.add(itembtn3,itembtn4,itembtn5,itembtn6)

    msg = bot.send_message(message.from_user.id,
                    text=text,reply_markup=keyboard)
    bot.register_next_step_handler(msg,callback_worker)

def add_plan(msg):
    with sqlite3.connect('planner.db') as con:
        cursor = con.cursor()
        cursor.execute('INSERT INTO planner (user_id, plan) VALUES (?,?)',(msg.from_user.id,msg.text))
        con.commit()
    bot.send_message(msg.chat.id, 'Записал')
    send_keyboard(msg,'Чем еще могу помочь?')

def motiv(msg):
    photo=open('motivat/' + random.choice(os.listdir('motivat')), 'rb')
    bot.send_photo(msg.chat.id, photo)
    bot.send_message(msg.chat.id,'Твоя мотивация')
    send_keyboard(msg,'Я могу что-то еще для тебя сделать?')

def delete_one_plan(msg):
    markup=types.ReplyKeyboardMarkup(row_width=2)
    with sqlite3.connect('planner.db') as con:
        cursor=con.cursor()
        cursor.execute('SELECT plan FROM planner WHERE user_id=={}'.format(msg.from_user.id))
        tasks=cursor.fetchall()
        for value in tasks:
            markup.add(types.KeyboardButton(value[0]))
        msg = bot.send_message(msg.from_user.id, text = 'Выбери одно дело из списка', reply_markup=markup)
        bot.register_next_step_handler(msg,del_one_plan)

def del_one_plan(msg):
    with sqlite3.connect('planner.db') as con:
        cursor=con.cursor()
        cursor.execute('DELETE FROM planner WHERE user_id==? AND plan==?',(msg.from_user.id,msg.text))
        bot.send_message(msg.chat.id,'Минус одна задача')
        send_keyboard(msg,'Чем еще могу помочь?')

def delete_all_plan(msg):
    with sqlite3.connect('planner.db') as con:
        cursor=con.cursor()
        cursor.execute('DELETE FROM planner WHERE user_id=={}'.format(msg.from_user.id))
        con.commit()
        bot.send_message(msg.chat.id,'Удалены все дела. Хорошего отдыха!')
        send_keyboard(msg,'Чем еще могу помочь?')


def get_plans_string(tasks):
    tasks_str=[]
    for val in list(enumerate(tasks)):
        tasks_str.append(str(val[0]+1)+')'+val[1][0]+'\n')
    return ''.join(tasks_str)

def show_plans(msg):
    with sqlite3.connect('planner.db') as con:
        cursor = con.cursor()
        cursor.execute('SELECT plan FROM planner WHERE user_id=={}'.format(msg.from_user.id))
        tasks = get_plans_string(cursor.fetchall())
        bot.send_message(msg.chat.id,tasks)
        send_keyboard(msg, 'Чем еще могу помочь?')

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
    elif call.text=='Мотивация':
        motiv(call)
    elif call.text=='Пока все!':
        bot.send_message(call.chat.id,'Пока! Если захочешь продолжить нажми /start')


























bot.polling()