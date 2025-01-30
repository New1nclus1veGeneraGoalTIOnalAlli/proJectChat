#файл для активации бота 
import os
from logic_boty.func_syns_bot import bot_convert_theme_3 as boty
from logic_boty.logic_bot import *
import telebot
import json
import os

TOKEN = get_needly_info('token.txt')
bot = boty(TOKEN)

   

    

# Запуск бота
if __name__ == "__main__":
    bot.bot.polling()


    