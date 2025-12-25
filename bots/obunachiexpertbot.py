import redis
import sqlite3
import telebot
import time

from telebot import types

token = "7891941044:AAELvUMD268kbhC0NCf2RCwJ-taRWxn3iuk"
obunachiexpertbot = telebot.TeleBot(token, threaded=False)
r = redis.Redis('localhost', port=6379, db=0, decode_responses=True)

connect = sqlite3.connect('bots/obunachiexpert-users.db')
cursor = connect.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user INTEGER UNIQUE,
                   balance INTEGER DEFAULT 0,
                   level TEXT DEFAULT 'user'
               )    
''')
connect.commit()

compane = "Obunachi Expert"

def find_users(column, value):
    query = f"SELECT * FROM users WHERE {column} = ?"
    cursor.execute(query, (value,))
    results = cursor.fetchall()
    lst = [description[0] for description in cursor.description]
    return [dict(zip(lst, row)) for row in results]

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user = ?", (user_id,))
    result = cursor.fetchone()
    lst = [description[0] for description in cursor.description]
    return dict(zip(lst, result)) if result else None

def insert(user, level="user"):
    cursor.execute("INSERT OR IGNORE INTO users (user, level) VALUES (?, ?)", (user, level))
    connect.commit()

def delete(user_id):
    cursor.execute("DELETE FROM users WHERE user = ?", (user_id,))
    connect.commit()
    return cursor.rowcount > 0
    
def get_balance(user):
    return get_user(user)['balance'] if get_user(user) else None



def set_admin(id):
    r.set("admin", id)
    insert(id, "admin")
    
if not r.get("admin"):
    db_admin = find_users("level", "admin")
    if db_admin:
        r.set("admin", db_admin[0]['user'])
    else:
        set_admin(1190898538)
        
admin = int(r.get("admin"))



def markup_button(btns, num, is_persistent=False, resize_keyboard=True, one_time_keyboard=False, input_field_placeholder=None, selective=False):
    markup = types.ReplyKeyboardMarkup(is_persistent=is_persistent,
                                      resize_keyboard=resize_keyboard,
                                      one_time_keyboard=one_time_keyboard,
                                      input_field_placeholder=input_field_placeholder,
                                      selective=selective)
    
    for i in range(0, len(btns), num):
        row = []
        for j in range(num):
            if i+j < len(btns):
                row.append(types.KeyboardButton(btns[i+j]))
        markup.add(*row)
    return markup


def inline_button(btns, num):
    keyboard = types.InlineKeyboardMarkup()

    for i in range(0, len(btns), num):
        row = []
        for j in range(num):
            if i + j < len(btns):
                params = {btns[i + j][2]: btns[i + j][1]}
                
                button = types.InlineKeyboardButton(text=btns[i + j][0], **params)
                row.append(button)
        
        keyboard.add(*row)
    return keyboard



@obunachiexpertbot.message_handler(commands=["start", "help"])
def welcome(m):
    r.setex(f"user:{m.chat.id}", 60, "1")
    reply = (f"Assalomu alaykum <a href='tg://user?id={m.from_user.id}'>{m.chat.first_name}</a>. Sizni <b>{compane}</b> botida ko‘rib turganimizdan xursandmiz!\n"
             f"Bu yerda siz o‘z sahifalaringizni yanada faol, mashhur va jozibador qilishingiz mumkin.\n"
             "Barcha xizmatlar menyuda mavjud.")
    btns = ["🚀 Xizmatni boshlash", "💳 Mening balansim", "📘 Foydalanish qo‘llanmasi", "📈 Rivojlanish statistikasi", "🤝 Yordam markazi"]
    if m.chat.id != admin:
        obunachiexpertbot.send_message(m.chat.id, reply, parse_mode='html', reply_markup=markup_button(btns, 2))
    else:
        btns.append("👨‍💻Admin panel")
        obunachiexpertbot.send_message(m.chat.id, reply, parse_mode='html', reply_markup=markup_button(btns, 2))
        

@obunachiexpertbot.message_handler()
def main(m):
    bot = obunachiexpertbot
    
    chat_id = m.chat.id
    text = m.text
    
    step = r.get(f"user:{chat_id}")
    
    if step == None:
        bot.reply_to(m, "sizga ajratrilgan sessiya tugadi. qaytadan boshlang!")
        time.sleep(1)
        r.setex(f"user:{m.chat.id}", 60, "1")
        reply = (f"Assalomu alaykum <a href='tg://user?id={m.from_user.id}'>{m.chat.first_name}</a>. Sizni <b>{compane}</b> botida ko‘rib turganimizdan xursandmiz!\n"
                f"Bu yerda siz o‘z sahifalaringizni yanada faol, mashhur va jozibador qilishingiz mumkin.\n"
                "Barcha xizmatlar menyuda mavjud.")
        btns = ["🚀 Xizmatni boshlash", "💳 Mening balansim", "📘 Foydalanish qo‘llanmasi", "📈 Rivojlanish statistikasi", "🤝 Yordam markazi"]
        if m.chat.id != admin:
            bot.send_message(m.chat.id, reply, parse_mode='html', reply_markup=markup_button(btns, 2))
        else:
            btns.append("👨‍💻Admin panel")
            bot.send_message(m.chat.id, reply, parse_mode='html', reply_markup=markup_button(btns, 2))
            
            
    
    if text == "🚀 Xizmatni boshlash":
        reply = "Kerakli bo'limni tanlang !"
        btns = [
            ("🔵 Telegram", "telegram", "callback_data"),
            ("🔴 YouTube", "youtube", "callback_data"),
            ("🟣 Instagram (Tez kunda)", "instagram", "callback_data"),
            ("⚫️ TikTok", "tiktok", "callback_data")
        ]
        bot.send_message(chat_id, reply, parse_mode='html', reply_markup=inline_button(btns, 2))
        
    if text == "💳 Mening balansim":
        reply = f"💳 Sizning balansingiz: {get_balance(chat_id)} so‘m"
        bot.reply_to(m, reply, reply_markup=inline_button([("➕ To‘ldirish", "pay", "callback_data")], 1))
    
    if text == "📘 Foydalanish qo‘llanmasi":
        reply = ("📘 Foydalanish qo‘llanmasi\n\n"
            ' 1️⃣ 🚀 "Xizmatni boshlash" tugmasini bosing.\n'
            " 2️⃣ Kerakli platformani tanlang (Telegram, YouTube, TikTok).\n" 
            " 3️⃣ Xizmat turini tanlang (obunachi, like, ko‘rish va boshqalar).\n"
            " 4️⃣ Buyurtma miqdorini kiriting.\n"
            " 5️⃣ 💳 Hisobingizni to‘ldiring va to‘lovni tasdiqlang.\n" 
            " 6️⃣ 📈 Rivojlanish statistikasi bo‘limidan buyurtma jarayonini kuzatishingiz mumkin.\n\n" 
            "⚠️ Eslatma:\n"
            " — Havolalarni to‘g‘ri kiriting.\n"
            "— Xizmat bajarilishi 1–24 soat davomida amalga oshiriladi.\n" 
            "— Muammo tug‘ilsa 🤝 Yordam markaziga murojaat qiling.")
        bot.send_message(chat_id, reply, parse_mode='html')
    
if __name__ == "__main__":
    obunachiexpertbot.polling()