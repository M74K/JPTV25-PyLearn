import users
import asyncio
import sqlite3
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = ""

bot = Bot(token=TOKEN)
dp = Dispatcher()

MAX_LEVEL = 20


#Загрузка тестов из файла
#Testide laadimine failist
def load_tests():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "tests.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

tests = load_tests()


#Andmebaas
#База данных
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


#Создание клавиатуры для теста
#Testi klaviatuuri loomine
def create_test_keyboard(level):
    test = tests[str(level)]
    buttons = []
    
    for i, option in enumerate(test["options"]):
        button = InlineKeyboardButton(
            text=option,
            callback_data=f"answer_{level}_{i}"
        )
        buttons.append([button])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Команда /start которая отправляет в ответ приветственное сообщение
# Käsk /start saadab vastuseks tervitussõnumi.
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("🦛Tere, see on PyLearni bot.\n"
                         "See bot on loodud Pythoni õppimiseks.🐸")


# Команда /mina - показать статистику пользователя
# Käsk /mina - kuva kasutaja statistikat
@dp.message(Command("mina"))
async def mina_command(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Teadmata"
    level = get_user_level(user_id)
    
    stats = f"""👤 <b>Sinu statistika</b>

📛 Kasutajanimi: @{username}
🆔 Telegrammi ID: {user_id}
📊 Hetke tase: {level}/{MAX_LEVEL}"""
    
    await message.answer(stats, parse_mode="HTML")
    
    

# Команда /teema и ответ
# Käsk /teema ja vastus
@dp.message(Command("teema"))
async def topic_command(message: types.Message):

    # kasutajatunnuse hankimine
    # Получение user id
    user_id = message.from_user.id

    # Получение информации уровня user id  из базы данных
    # Kasutaja ID taseme teabe hankimine andmebaasist
    level = get_user_level(user_id)

    # Если пользователь прошел все темы получает поздравление
    # Kui kasutaja on kõik teemad läbinud, saab ta õnnitluse.
    if level > MAX_LEVEL:
        await message.answer(
            "Palju õnne! Sa oled läbinud kõik 20 teemat!"
        )
        return

    # Отправка текста пользователю
    # Tekstisõnumi saatmine kasutajale
    topic_text = get_topic(level)
    header = f"Tase {level}/{MAX_LEVEL}\n\n"
    await message.answer(header + topic_text)

    # Отправка теста с кнопками
    # Testi saatmine nupudega
    test = tests[str(level)]
    test_message = f"<b>Test</b>\n\n{test['question']}"
    keyboard = create_test_keyboard(level)
    
    await message.answer(test_message, reply_markup=keyboard, parse_mode="HTML")


# Обработка нажатия на кнопку теста
# Testi nupu kliki käsitlemine
@dp.callback_query()
async def answer_callback(query: types.CallbackQuery):
    data = query.data
    
    # Проверка если это ответ на тест
    # Kontrolli kas see on testi vastus
    if not data.startswith("answer_"):
        return
    
    # Извлечение уровня и выбранного ответа
    # Taseme ja valitud vastuse eraldamine
    parts = data.split("_")
    level = int(parts[1])
    selected_answer = int(parts[2])
    
    test = tests[str(level)]
    correct_answer = test["correct"]
    
    # Проверка правильности ответа
    # Vastuse õigsuse kontrollimine
    if selected_answer == correct_answer:

        user_id = query.from_user.id
        update_user_level(user_id, level + 1)
        
        await query.answer("✅ Õige vastus!", show_alert=True)
        await query.message.edit_text(
            f"<b>✅ Õige!</b>\n\nPalju õnne! Liigud järgmisele tasemele.",
            parse_mode="HTML"
        )
    else:
        # Неправильный ответ
        # Vale vastus
        correct_option = test["options"][correct_answer]
        
        await query.answer("❌ Vale vastus!", show_alert=True)
        await query.message.edit_text(
            f"<b>❌ Vale!</b>\n\n"
            f"Õige vastus oli: <b>{correct_option}</b>\n\n"
            f"Proovi uuesti käskga /teema",
            parse_mode="HTML"
        )
    

async def main():
    create_database()
    print("PyLearn bot on käivitatud!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
