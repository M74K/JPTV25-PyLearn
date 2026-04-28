#импортирование нужных библиотек и настройка бота
#vajalike teekide importimine ja roboti seadistamine
import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "Bot_token_from_botfather"

bot = Bot(token=TOKEN)
dp = Dispatcher()

MAX_LEVEL = 20


#andmebaas
def create_database():
    #подключение  к базе данных
    #andmebaasiga ühenduse loomine
    connection = sqlite3.connect("pylearn.db")
    cursor = connection.cursor()
 

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            level INTEGER DEFAULT 1
        )
    """)
    #сохранение изменений в базу данных
    #andmebaasi muudatuste salvestamine
    connection.commit()
    connection.close()


#работа с уровнями пользователей
#kasutajatasemetega töötamine
def get_user_level(user_id):
    connection = sqlite3.connect("pylearn.db")
    cursor = connection.cursor()
    cursor.execute("SELECT level FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    #добавление пользователя в базу данных если его нет
    #kasutaja lisamine andmebaasi, kui seda pole olemas
    if result is None:
        cursor.execute("INSERT INTO users (user_id, level) VALUES (?, 1)", (user_id,))
        connection.commit()
        connection.close()
        return 1

    #если пользователь есть в базе то ничего не делать
    #kui kasutaja on andmebaasis olemas, siis ära tee midagi.
    connection.close()
    return result[0]

#повышение уровня пользователя 
#kasutaja taseme tõus
def update_user_level(user_id, new_level):
    connection = sqlite3.connect("pylearn.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET level = ? WHERE user_id = ?", (new_level, user_id))
    connection.commit()
    connection.close()


#Чтение файлов с сообщениями бота
#Boti sõnumifailide lugemine
def get_topic(level):
    if level == 1:
        file = open("topics/1.txt", "r", encoding="utf-8")
    elif level == 2:
        file = open("topics/2.txt", "r", encoding="utf-8")
    elif level == 3:
        file = open("topics/3.txt", "r", encoding="utf-8")
    elif level == 4:
        file = open("topics/4.txt", "r", encoding="utf-8")
    elif level == 5:
        file = open("topics/5.txt", "r", encoding="utf-8")
    elif level == 6:
        file = open("topics/6.txt", "r", encoding="utf-8")
    elif level == 7:
        file = open("topics/7.txt", "r", encoding="utf-8")
    elif level == 8:
        file = open("topics/8.txt", "r", encoding="utf-8")
    elif level == 9:
        file = open("topics/9.txt", "r", encoding="utf-8")
    elif level == 10:
        file = open("topics/10.txt", "r", encoding="utf-8")
    elif level == 11:
        file = open("topics/11.txt", "r", encoding="utf-8")
    elif level == 12:
        file = open("topics/12.txt", "r", encoding="utf-8")
    elif level == 13:
        file = open("topics/13.txt", "r", encoding="utf-8")
    elif level == 14:
        file = open("topics/14.txt", "r", encoding="utf-8")
    elif level == 15:
        file = open("topics/15.txt", "r", encoding="utf-8")
    elif level == 16:
        file = open("topics/16.txt", "r", encoding="utf-8")
    elif level == 17:
        file = open("topics/17.txt", "r", encoding="utf-8")
    elif level == 18:
        file = open("topics/18.txt", "r", encoding="utf-8")
    elif level == 19:
        file = open("topics/19.txt", "r", encoding="utf-8")
    elif level == 20:
        file = open("topics/20.txt", "r", encoding="utf-8")
    else:
        return "Teema ei leitud!"

    #faili teksti lugemine ja faili sulgemine
    #чтение текста в файле и закрытие файла
    text = file.read()
    file.close()
    return text
