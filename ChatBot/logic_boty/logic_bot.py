from telebot import TeleBot as tele
from telebot import types
import os
import json
import telebot


def send_teach(bot:tele,user_id,mess):
    
    bot.send_message(user_id,mess)



def choose_teach(bot:tele,file:json,message,file_wait):
    usr_data=load_user_data2(file)
    user_data=load_user_data2(file_wait)
    
    if usr_data !={}:
        for fio in usr_data.items():
            keyobar=types.InlineKeyboardMarkup()
            
            for usr in user_data['wait_message'].items():
                button=types.InlineKeyboardButton(f"send @{usr.get('username', 'Неизвестно') }",f"send_{usr}" )
                keyobar.add(button)
            bot.send_message(message,f"у преподавателя {fio} обнаружено неправильное заполнение темы")
        

def bot_handler_button(button_list:list):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    
    try:
        for button in button_list:
            butt=types.KeyboardButton(button)
            keyboard.add(butt)
    except:
        keyboard.add(types.KeyboardButton("не хуйня какая-то"))
    return keyboard
def bot_inline_handler_button(buttonInline_list:list,userID):
    
    if not buttonInline_list:  # Check if the list is empty
        keyboard_inline.add(types.InlineKeyboardButton("No buttons available"))
        return keyboard_inline

    keyboard_inline=types.InlineKeyboardMarkup(row_width=3)
    try:
        for button in buttonInline_list:
            butt = types.InlineKeyboardButton(text=button, callback_data=f"{button}_{userID}")
            keyboard_inline.add(butt)
    except:
        keyboard_inline.add(types.InlineKeyboardButton(text="не хуйня какая-то",callback_data=button[1]))
    return keyboard_inline

def load_user_data2(USER_DATA_FILE):
        USER_DATA_FILE 
        if os.path.exists(USER_DATA_FILE):
            if is_json_file_empty(USER_DATA_FILE):
                return None
            else:
                with open(USER_DATA_FILE, 'r') as file:
                    return json.load(file)
        return {}
def is_json_file_empty(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return content.strip() == ''
    
def info_user(message):
        return {'username': message.from_user.username,
                'first_name':message.from_user.first_name
                }
def del_file(file_path):
    
    os.remove(file_path)


def get_needly_info(file_path):
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return None
    try:
        with open(file_path, 'r') as file:
            token = file.read().strip()  # Убираем лишние пробелы и символы новой строки
        return token
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
def bot_Main_Menu(bot:tele,message):
    bot.send_message(message.chat.id, "Вы в главном меню",reply_markup=types.ReplyKeyboardRemove())
    
    pass
#def work_with_file_theme(bot:tele,message)

__all__ = ['choose_teach','load_user_data2','is_json_file_empty','bot_handler_button','bot_Main_Menu','del_file','bot_inline_handler_button','get_needly_info','info_user'] 