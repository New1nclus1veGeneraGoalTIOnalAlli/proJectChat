#!/bin/bash

VENV_DIR=".venv"

# Проверка, существует ли директория виртуального окружения
if [ ! -d "$VENV_DIR" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv $VENV_DIR
else
    echo "Виртуальное окружение уже существует."
fi

# Активация виртуального окружения
echo "Активация виртуального окружения..."
source $VENV_DIR/bin/activate

# Установка библиотек из requirements.txt

echo "Установка библиотек из requirements.txt..."
pip install pyTelegramBotAPI pandas


# Установка библиотек
#pip install pyTelegramBotAPI pandas

# Запрос токена у пользователя
read -p "Введите ваш токен: " TOKEN

read -p "Введите id пользователя : " ID_admin

# Создание поддиректории, если она не существует

mkdir ChatBot/logic_boty/datavasa


# Создание файлов JSON в поддиректории
echo \{\"$ID_admin\": \{\"role\": \"admin\"\}\} > ChatBot/logic_boty/datavasa/users.json
echo \{\"wait\":\{\},\"wait_message\":\{\}\} > ChatBot/logic_boty/datavasa/users_waiting.json

echo "Установка завершена!"
