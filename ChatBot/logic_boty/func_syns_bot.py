#тут указывается логика бота
import telebot

import sys
import os
from logic_boty.logic_bot import *
from logic_boty.users_bot import baseUser
from logic_boty.users_bot import admin_user
import json
# Добавляем родительский каталог в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Теперь относительный импорт будет работать
from to_level.convert_file_6 import Theme_Load as theme, loading_pair


class bot_convert_theme_3:
    def __init__(self, token):
        self.user_classes = {}
        self.bot = telebot.TeleBot(token)
        self.user_data = self.load_user_data()
        self.user_states=None
        self._keyDoc=False
        self._keyDoc2=False
        self.tolevel=loading_pair()
        # Регистрируем обработчик команды /start
        self.bot.message_handler(commands=["start"])(self.start_handler)
        self.bot.message_handler(commands=["check"])(self.check_users)
        self.bot.message_handler(commands=["want_to_teacher"])(self.sent_toAdmin)
        self.bot.message_handler(content_types=["document"])(self.send_document)
        self.bot.message_handler(commands=["sigma"])(self.buttons)
        self.bot.message_handler(commands=["help"])(self.help)

        self.bot.callback_query_handler(func=lambda call: True)(self.callback_query)

        self.bot.message_handler(func=lambda message: True)(self.message_handler)
    def help(self,message):
        user_id=message.from_user.id
        if self.user_data.get(str(user_id), {}).get('role') == 'admin': 
            ad=admin_user(self.bot,self.user_states,self._keyDoc)
            ad.help_handler(message)
        else:
            ba=baseUser(self.bot)
            ba.help_handler(message)

    def buttons(self,message):
        user_id=message.from_user.id

        if self.user_data.get(str(user_id), {}).get('role') == 'admin':  
            ad=admin_user(self.bot,self.user_states,self._keyDoc)
            ad.Buttnos_handler(message)

    def send_document(self,message):
        user_id=message.from_user.id
        if self.user_data.get(str(user_id), {}).get('role') == 'admin':  
            ad=admin_user(self.bot,self.user_states,self._keyDoc)
            ad.send_document(message,self.tolevel)
    def start_handler(self, message):
        user_id = message.from_user.id
        
        # Загружаем данные пользователя, если их нет
        if str(user_id) not in self.user_data:
            self._save_user_id(user_id)

        # Находим или создаем экземпляр пользователя
        self.find_user(user_id)

        # Отправляем приветственное сообщение
        self.user_classes[int(user_id)].start_handler(message)

    def find_user(self, user_id):
        if str(user_id) not in self.user_classes:
            role = self.user_data.get(str(user_id), {}).get('role', 'regular')  # По умолчанию 'regular'
            if role == 'admin':
                self.user_classes[user_id] = admin_user(self.bot)
            else:
                self.user_classes[user_id] = baseUser(self.bot)
            print(f"Пользователь {user_id} назначен в класс {role}")

    def load_user_data(self):
        USER_DATA_FILE = 'ChatBot/logic_boty/datavasa/users.json'
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r') as file:
                return json.load(file)
        return {}
    
    def load_user_data2(self):
        USER_DATA_FILE = 'ChatBot/logic_boty/datavasa/users_waiting.json'
        if os.path.exists(USER_DATA_FILE):
            if is_json_file_empty(USER_DATA_FILE):
                return None
            else:
                with open(USER_DATA_FILE, 'r') as file:
                    return json.load(file)
        return {}

    def save_user_data2(self, user_data):
        USER_DATA_FILE = 'ChatBot/logic_boty/datavasa/users_waiting.json'
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(user_data, file)

    def callback_query(self,call):
        if call.data.startswith('join_'):
            print("going")
            user=call.data.split('_')[1]
            user_data=self.load_user_data2()
            if user not in user_data['wait_message']:
                user_data['wait_message'][user]=user_data['wait'][user]
                del user_data['wait'][user]
                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=" удален!")

            self.save_user_data2(user_data)

        elif call.data.startswith('decline_'):
            user=call.data.split('_')[1]
            user_data=self.load_user_data2()
            del user_data['wait'][user]
            self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=" удален!")
            self.save_user_data2(user_data)

        if call.data.startswith('send_'):
            user=call.data.split('_')[1]
            user_data=self.load_user_data2()
            list=['where','NotWant']
            keybou=bot_inline_handler_button(list,user)
            self.bot.send_message(int(user),f"у вас обнаружено неправильное заполнение темы ")
        if call.data.endswith('_group'):
            print("работет пашет")
            group=call.data.split('_')[0]
            user=call.data.split('_')[1]
            if(isinstance(self.tolevel,loading_pair)):
                list3=self.tolevel.get_group(group)
                mess='\n'.join(list3)
                self.bot.send_message(user,mess)

    def save_user_data(self):
        USER_DATA_FILE = 'ChatBot/logic_boty/datavasa/users.json'
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(self.user_data, file)

    def _save_user_id(self, user_id):
        if str(user_id) not in self.user_data:
            file="admin_id.txt"

            if user_id == get_needly_info(file):  
                self.user_data[str(user_id)] = {'role': 'admin'}
            else:
                self.user_data[str(user_id)] = {'role': 'regular'}
            
            print(f"Пользователь {user_id} сохранен с ролью {self.user_data[str(user_id)]['role']}")
            self.save_user_data()


    # Обработчик команды для админа
    def check_users(self, message):
        user_id=message.from_user.id
        if self.user_data.get(str(user_id), {}).get('role') == 'admin':    
            user_data = self.load_user_data2()  # Вызываем метод для загрузки данных

            if user_data is None or 'wait' not in user_data or not user_data['wait']:
                self.bot.send_message(message.chat.id, "Никого нету")
                return
            lists=['join','decline']
            for user_id, user_info in user_data['wait'].items():
                username = user_info.get('username', 'Неизвестно') 
                 # Получаем имя пользователя, если оно есть
                keybor=bot_inline_handler_button(lists,user_id)
                self.bot.send_message(message.chat.id, f"WHO: @{username}, имя:{user_info.get('first_name', 'Неизвестно')}",reply_markup=keybor)
                

    #отработчик для пользователя
    def save_waiting(self, message):
        user_data = self.load_user_data2()   # Загружаем данные или создаем пустой словарь
        print("Загруженные данные пользователя:", user_data)  # Отладочное сообщение

        user_id = str(message.from_user.id)

        if user_id not in user_data['wait']:
            user_data['wait'][user_id] = info_user(message)  # Предполагается, что info_user возвращает информацию о пользователе
            print(f"Добавлен пользователь {user_id} в очередь.")  # Отладочное сообщение
            self.save_user_data2(user_data)
        else:
            self.bot.send_message(message.chat.id, "Дождитесь своей очереди")
            print(f"Пользователь {user_id} уже в очереди.")  # Отладочное сообщение
            
    def sent_toAdmin(self,message):
        print("set")
        if self.user_data.get(str(message.from_user.id), {}).get('role') == 'regular':   
            self.save_waiting(message)
            print("set2")
    def message_handler(self,message):

        user_id=message.from_user.id
        if self.user_data.get(str(user_id), {}).get('role') == 'admin': 
            if message.text=="Выйти в главное меню":
                print("Вышел в главное меню\n")
                bot_Main_Menu(self.bot,message)
                self._keyDoc=False
                self._keyDoc2=False
                return
            if self._keyDoc2:
                if self.user_states is None:
                    self.user_states={}

                if message.chat.id not in self.user_states:
                    self.user_states[message.chat.id] = None

                if self.user_states[message.chat.id] == 'waiting_for_students':
                    self.bot.send_message(message.chat.id, "Вы можете отправить только документ.")
                    return

            if self._keyDoc:

                if self.user_states is None:
                    self.user_states={}

                #При вводе "Отправить файл"
                if message.chat.id not in self.user_states:
                    self.user_states[message.chat.id] = None
                if self.user_states[message.chat.id] == 'waiting_for_document':
                    self.bot.send_message(message.chat.id, "Вы можете отправить только документ.")
                    return

                # Проверяем состояние пользователя
                
                
                if message.text and "Отправить файл" in message.text:
                    print("отправляет документ\n")
                    if self.user_states[message.chat.id] is None:
                        self.user_states[message.chat.id] = 'waiting_for_document'
                    self.bot.send_message(message.chat.id, "Теперь вы можете отправить документ.")
                    return
            else:
                # Обработка всех остальных сообщений

                if message.text=="Просмотр тем":
                    print("Задание 3\n")
                    self._keyDoc=True
                    list=["Отправить файл","Выйти в главное меню"]
                    keyboarb=bot_handler_button(list)

                    self.bot.send_message(message.chat.id, "Привет! Выберите кнопку:", reply_markup=keyboarb)
                    return
                if message.text=="данные по посещенным парам":
                    self._keyDoc2=True
                    self.bot.send_message(message.chat.id,"Отправьте файл где содержиться информация о проведенных парах" )
                    if self.user_states is None:
                        self.user_states={}
                    

                #При вводе "Отправить файл"
                    if message.chat.id not in self.user_states:
                        self.user_states[message.chat.id] = None
                        self.user_states[message.chat.id] = 'waiting_for_students'
                        self.bot.send_message(message.chat.id,"отправляйте документ")
                        return

                else:
                    print("что-то какая-то\n")
                    self.bot.reply_to(message,  message.text)
        else:
             ba=baseUser(self.bot)
             ba.handle_message(message)
        