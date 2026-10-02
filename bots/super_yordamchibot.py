import telebot

from groq import Groq

import json
import os
from datetime import datetime

# Fayl nomi
LOG_FILE = "chat_history.json"

def save_to_json(user_id, user_name, question, answer):
    # Yangi ma'lumot strukturasi
    data_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "user_name": user_name,
        "question": question,
        "answer": answer
    }

    # Fayl mavjudligini tekshirish va o'qish
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Yangi ma'lumotni qo'shish
    data.append(data_entry)

    # Faylga qayta yozish
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

token = "7807701719:AAEEI6FMs6eFE6ffIEy1ri4KQ-HUehaKTbo"
groq_key = "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"
models = [
    "llama-3.3-70b-versatile",   # Eng aqlli va yangi (Llama 3.3)
    "llama-3.1-70b-versatile",   # Barqaror va kuchli mantiq
    "llama-3.1-8b-instant",      # Juda tez va limitlari yuqori
    "mixtral-8x7b-32768",        # Ko'p tillarda yaxshi ishlaydi
    "llama3-70b-8192",           # Eski lekin ishonchli 70B versiya
    "llama3-8b-8192",            # Eski lekin juda tez 8B versiya
    "qwen-2.5-32b",              # Jadvalingizdagi Qwen (matematika va kodda kuchli)
    "gemma2-9b-it"               # Google'ning ochiq modeli (o'zbekchada yomon emas)
]

stt_models = [
    "whisper-large-v3",        # Eng aniq va ko'p tillarni (shu jumladan o'zbekchani) tushunadigan model
    "whisper-large-v3-turbo",  # Whisper-ning tezlashtirilgan versiyasi (sifat deyarli bir xil, lekin tezroq)
    # "distil-whisper-large-v3-en" # Faqat ingliz tili uchun o'ta tezkor model
]

tts_models = [
    "canopylabs/orpheus-v1-english", # Sifatli inglizcha ovoz
    "playai-tts",                    # Umumiy TTS modeli
    "playai-tts-arabic"              # Arab tili uchun ixtisoslashgan ovoz
]

groq_api = Groq(api_key=groq_key)

model_counter = 0

def get_next_model():
    global model_counter
    current_model = models[model_counter]
    
    # Navbatni bittaga oshirish (agar ro'yxat tugasa, 0 ga qaytadi)
    model_counter = (model_counter + 1) % len(models)
    return current_model

def groq_chat(text, model=get_next_model(), role="user"):
    chat_completion = groq_api.chat.completions.create(
        messages=[
            {
                "role": "system", 
                "content": "Siz foydali yordamchisiz. FAQAT <b>, <i>, <pre><code> formatlarini ishlating. Boshqa teglarni ishlatmang."
            },
            {
                "role":role,
                "content":text
            }
        ],
        model=model
    )
    return chat_completion.choices[0].message.content




super_yordamchibot = telebot.TeleBot(token=token, threaded=False)


# 1. Admin ID sini o'zgaruvchiga saqlang (o'zingizning Telegram ID ingizni yozing)
ADMIN_ID = 1190898538  # Bu yerga o'z ID ingizni kiriting

@super_yordamchibot.message_handler(commands=['json'])
def send_json_logs(message):
    bot = super_yordamchibot
    user_id = message.from_user.id
    
    # Faqat admin ekanligini tekshirish
    if user_id == ADMIN_ID:
        if os.path.exists("chat_history.json"):
            try:
                # Faylni yuborish
                with open("chat_history.json", "rb") as file:
                    bot.send_document(
                        message.chat.id, 
                        file, 
                        caption="📊 Barcha savol-javoblar tarixi (JSON formatda)"
                    )
            except Exception as e:
                bot.reply_to(message, f"❌ Faylni yuborishda xatolik: {str(e)}")
        else:
            bot.reply_to(message, "📁 Hozircha chat tarixi fayli mavjud emas.")
    
    
    

@super_yordamchibot.message_handler(commands=['start'])
def welcome(m):
    super_yordamchibot.reply_to(m, "Assalomu alaykum! 👋\nSavolingizni yozing.")
    
@super_yordamchibot.message_handler()
def answer(m):
    bot = super_yordamchibot
    text = m.text
    user_id = m.from_user.id
    user_name = m.from_user.first_name
    
    # AI dan javob olish
    ai_response = groq_chat(text)
    
    # Telegramga yuborish
    bot.reply_to(m, ai_response, parse_mode="HTML")
    
    # JSON ga saqlash
    save_to_json(user_id, user_name, text, ai_response)

    
    
    
if __name__ == "__main__":
    super_yordamchibot.polling()
