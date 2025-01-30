@echo off

set VENV_DIR=".venv"

REM Проверка, существует ли директория виртуального окружения
if not exist %VENV_DIR% (
    echo Создание виртуального окружения...
    python -m venv %VENV_DIR%
) else (
    echo Виртуальное окружение уже существует.
)

REM Активация виртуального окружения
echo Активация виртуального окружения...
call %VENV_DIR%\Scripts\activate.bat

REM Установка библиотек из requirements.txt
echo Установка библиотек из requirements.txt...
pip install pyTelegramBotAPI pandas

REM Запрос токена у пользователя

set /p TOKEN="Введите ваш токен: "
echo TOKEN > token.txt
set /p ID_admin="Введите id пользователя: "

REM Создание поддиректории, если она не существует
if not exist ChatBot\logic_boty\datavasa (
    mkdir ChatBot\logic_boty\datavasa
)

REM Создание файлов JSON в поддиректории
echo {"%ID_admin%": {"role": "admin"}} > ChatBot\logic_boty\datavasa\users.json
echo {"wait":{}, "wait_message":{}} > ChatBot\logic_boty\datavasa\users_waiting.json

echo Установка завершена!
