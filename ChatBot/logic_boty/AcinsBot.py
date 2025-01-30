from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
import sys
import os
from logic_bot import *
# Добавляем родительский каталог в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Теперь относительный импорт будет работать
from to_level.convert_file_6 import Theme_Load as theme

class bot_Asins_convert_theme:
        def __init__(self, token):
            self.bot = Bot(token)
            self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        
        # Register handlers
            self.dp.register_message_handler(self.start_handler, commands=['start'])
            self.dp.register_message_handler(self.help_handler, commands=['help'])
            self.dp.register_message_handler(self.buttons_handler, commands=['sigma'])
            self.dp.register_message_handler(self.send_document, content_types=['document'])
            self.dp.register_message_handler(self.handle_message)

        async def start_handler(self, message: types.Message):
            await message.answer("Привет, друг.")
            await message.answer(f"{message.from_user.id}")

        async def help_handler(self, message: types.Message):
            await message.answer("Вот список команд: /start, /help")

        async def buttons_handler(self, message: types.Message):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Задание 1")
            button2 = types.KeyboardButton("Задание 2")
            button3 = types.KeyboardButton("Задание 3")
            keyboard.add(button1, button2, button3)
            await message.answer("Привет! Выберите кнопку:", reply_markup=keyboard)

        async def send_document(self, message: types.Message):
            if message.document:
                file_info = await self.bot.get_file(message.document.file_id)
                downloaded_file = await self.bot.download_file(file_info.file_path)

                file_path = 'received_file' + os.path.splitext(file_info.file_path)[1]
                with open(file_path, 'wb') as new_file:
                    new_file.write(downloaded_file.getvalue())

                file_extension = os.path.splitext(file_path)[1]
                per_ext = ['.xlsx', '.xls', '.xlsm']

                if file_extension in per_ext:
                    theme_loader = theme(file_path)  # Assuming theme is defined elsewhere
                    await self.make_keyboard_for_lists_exs(message, theme_loader.get_list())

                    fio_list = theme_loader.get_FIO()
                    if fio_list:
                        await self.send_file(fio_list, message, theme_loader)
                    else:
                        await self.bot.send_message(message.chat.id, "Не удалось получить данные.")
                else:
                    await self.bot.send_message(message.chat.id, "Неподдерживаемый формат файла. Пожалуйста, загрузите файл с одним из следующих расширений: " + ", ".join(per_ext))
            else:
                await self.bot.send_message(message.chat.id, "Не удалось получить документ. Пожалуйста, отправьте файл.")

        async def send_file(self, fio_list, message, theme_loader):
            with open(fio_list, "rb") as file:
                await self.bot.send_document(message.chat.id, file)

            os.remove(fio_list)

        async def handle_message(self, message: types.Message):
            if message.text == "Задание 3":
                await self.bot_handler_button3(message)  # Assuming this function is defined elsewhere
            else:
                await message.reply("Вы написали: " + message.text)

        

        def run(self):
            executor.start_polling(self.dp, skip_updates=True)