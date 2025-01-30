
import telebot
import os
from logic_boty.logic_bot import *
from to_level.convert_file_6 import Theme_Load as theme
from to_level.convert_file_6 import loading_pair as pair
import json
#безыимянный пользователь
class baseUser:
    def __init__(self,bot:telebot.TeleBot):
        self.bot=bot
     
        self.wantAd=False

        #@b.message_handler(func=lambda message: message.text == "Задание 3")()
    def setCommm(self):
        comanda={
            "start": self.start_handler,  
            "help": self.help_handler,
          
            #"want_to_self":self.yourself
            
        }
        return comanda
    # def set_commands(self):
    #     commands = [
    #         #telebot.types.BotCommand("start", "Запуск бота"),
    #         telebot.types.BotCommand("help", "Помощь пользователю"),
    #         telebot.types.BotCommand("want_to_teacher", "Получать сообщения от учебки"),
    #         telebot.types.BotCommand("want_to_self", "получить самому информацию из эксель"),
            
    #     ]
    #     self.bot.set_my_commands(commands) 

   
    
    def handle_message(self,message):
        if self.wantAd:
            self.bot.send_message(message,"qwe")
            self.bot.send_message()   
        if message.text=="Выйти в главное меню":
                print("Вышел в главное меню\n")
                bot_Main_Menu(self.bot,message)
                return
    # def Rank_handler(self,message):
    #     self.bot.send_message(message.chat.id,f"твой ранг: {self.rank}")
    def start_handler(self,message):
         self.bot.send_message(message.chat.id,"приветики вы обычный пользователь")

    def help_handler(self, message):  
        mess = {
            "/want_to_teacher- для отправки запроса админу",
            
        }
        self.bot.send_message(message.chat.id,mess)
    

#пользователь админ
class admin_user:
    def __init__(self,bot:telebot.TeleBot,user_states,keyDoc):
        self.bot=bot
        self.user_states=user_states
        self._keyDoc=keyDoc
        self._pair=None
        
        # Регистрируем команды
     
        #@b.message_handler(func=lambda message: message.text == "Задание 3")()
        
        
        #self.bot.message_handler(func=self.custom_message_handler)(self.message_handler)
    def setCommm(self):
        comanda={
            #"start": self.start_handler,  
            "help": self.help_handler,
            "sigma": self.Buttnos_handler,
            "check": self.check_users
        }
        return comanda
    # def set_commands(self):
    #     commands = [
    #         #telebot.types.BotCommand("start", "Запуск бота"),
    #         telebot.types.BotCommand("help", "Помощь пользователю"),
    #         telebot.types.BotCommand("sigma", "Помощь пользователю"),
    #         telebot.types.BotCommand("check", "посмотреть кто хочет присоединиться"),
            
    #     ]
    #     self.bot.set_my_commands(commands)

    def start_handler(self, message):  
         bot_Main_Menu(self.bot,message)
        
        
         self.bot.send_message(message.chat.id,
                              
                                "Привет, друг. Привет,друг")  
         self.bot.send_message(message.chat.id, f"{message.from_user.id }" )  

    def help_handler(self, message):  
        mess= {
            "Этот бот сделан для того чтобы администратору и учителям стало удобней работать с эксель файлами\n",
            "\n",
            "\n/sigma- для работы с документами\n"
            "\"получить данные по проведенным парам\" это у нас выводиться кто отсидет всего пар в определенной группе\n",
            "\"Просмотр тем\" здесь мы смотрим кто неправильно заполнил тему\n",
            "/check - для просмотра кто хочет присоединиться из учителей",

            
        }
        self.bot.send_message(message.chat.id, 
                              (mess))    
    
    def Buttnos_handler(self, message):  
        list=["данные по посещенным парам", "Просмотр тем","Выйти в главное меню"]
       
       
        keyboard=bot_handler_button(list)
        self.bot.send_message(message.chat.id, "Привет! Выберите кнопку:", reply_markup=keyboard)
   
    def send_document(self,message,tolevel:pair):
    
    # b.send_message(message.chat.id, f"отправьте файл:")
        # if message.document:
    
        
        user_id = message.chat.id

        # Проверяем состояние пользователя
        if self.user_states is not None:
            
               
                # Обработка документа
                if message.document:
                    # Получаем файл
                    file_info = self.bot.get_file(message.document.file_id)
                    downloaded_file = self.bot.download_file(file_info.file_path)  # Загружаем файл

                    # Сохраняем файл на диск
                    file_path = 'received_file' + os.path.splitext(file_info.file_path)[1]  # Сохраняем с оригинальным расширением
                    with open(file_path, 'wb') as new_file:
                        new_file.write(downloaded_file)

                    # Проверяем расширение файла
                    file_extension = os.path.splitext(file_path)[1]
                    per_ext = ['.xlsx', '.xls', '.xlsm']
                    
                    if file_extension in per_ext:
                        if user_id in self.user_states and self.user_states[user_id] == 'waiting_for_document':
                            
                            ttoLevel=theme()
                            ttoLevel.set_file(file_path)
                            try:
                                fio_list = ttoLevel.get_FIO()
                                if fio_list:
                                    Keybo=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

                                    
                                    button2=telebot.types.KeyboardButton("Выйти в главное меню")

                                    Keybo.add(button2)
                                    
                                    USSE = 'ChatBot/logic_boty/datavasa/users_waiting.json'
                                    usr_data = load_user_data2(fio_list)
                                    user_data = load_user_data2(USSE)

                                    if usr_data:
                                        for fio_key, fio_value in usr_data.items():  # Распаковываем кортеж
                                            keyobar = telebot.types.InlineKeyboardMarkup()
                                            for usr in user_data['wait_message'].items():
                                                # Предполагаем, что usr - это кортеж (ключ, значение)
                                                username = usr[1].get('username', 'Неизвестно')  # Получаем username из значения
                                                button = telebot.types.InlineKeyboardButton(f"send {usr[1].get('first_name', 'Неизвестно')}", callback_data=f"send_{usr[0]}")  # usr[0] - это ключ
                                                keyobar.add(button)
                                            self.bot.send_message(message.chat.id, f"У преподавателя {fio_key} обнаружено неправильное заполнение темы",reply_markup=keyobar)

                                # Удаляем файл после отправки
                                    #os.remove(fio_list)
                                
                                    self.user_states.pop(user_id)    
                                else:
                                    self.bot.send_message(message.chat.id, "Н удалось получить данные.")
                            except Exception as r:
                                self.bot.send_message(message.chat.id, f"Не удалось получить данные. {r} ")
                            
                        elif user_id in self.user_states and self.user_states[user_id] == 'waiting_for_students':
                            try:
                                tolevel.set_file(file_path)
                                
                                keybo=bot_inline_handler_button(tolevel.get_Button_group(),f"{user_id}_group")
                                self.bot.send_message(message.chat.id, "вот выбирайте группы",reply_markup=keybo)
                                self.user_states.pop(user_id)   
                            except:
                                self.bot.send_message(message.chat.id, "Не удалось получить данные.")
                        
                        os.remove(file_path)
                    else:
                        self.bot.send_message(message.chat.id, "Неподдерживаемый формат файла. Пожалуйста, загрузите файл с одним из следующих расширений: " + ", ".join(per_ext))
                else:
                    self.bot.send_message(message.chat.id, "Не удалось получить документ. Пожалуйста, отправьте файл.")
            
                
                
           
                #print(self.user_states[user_id])
        else:
            self.bot.send_message(user_id, "нельзя")
   
    
    
    def handle_message(self, message):
        if message.text=="Выйти в главное меню":
                print("Вышел в главное меню\n")
                bot_Main_Menu(self.bot,message)
                self._keyDoc=False
                return
        
        if self._keyDoc:

            if self.user_states is None:
                self.user_states={}

            #При вводе "Отправить файл"
            if message.chat.id not in self.user_states:
                self.user_states[message.chat.id] = None

            # Проверяем состояние пользователя
            if self.user_states[message.chat.id] == 'waiting_for_document':
                self.bot.send_message(message.chat.id, "Вы можете отправить только документ.")
                return
            
            if message.text and "Отправить файл" in message.text:
                print("отправляет документ\n")
                if self.user_states[message.chat.id] is None:
                    self.user_states[message.chat.id] = 'waiting_for_document'
                self.bot.send_message(message.chat.id, "Теперь вы можете отправить документ.")
                return
        else:
            # Обработка всех остальных сообщений
            if message.text=="Задание 3":
                print("Задание 3\n")
                self._keyDoc=True
                list=["Отправить файл","Выйти в главное меню"]
                keyboarb=bot_handler_button(list)

                self.bot.send_message(message.chat.id, "Привет! Выберите кнопку:", reply_markup=keyboarb)
                return

            else:
                print("что-то какая-то\n")
                self.bot.reply_to(message,  message.text)

#пользователь учитель
