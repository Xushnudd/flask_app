import telebot

from groq import Groq

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

@super_yordamchibot.message_handler(commands=['start'])
def welcome(m):
    super_yordamchibot.reply_to(m, "Assalomu alaykum! 👋\nSavolingizni yozing.")
    
@super_yordamchibot.message_handler()
def answer(m):
    bot = super_yordamchibot
    text = m.text
    
    bot.reply_to(m, groq_chat(text), parse_mode="HTML")
    
    
    
    
if __name__ == "__main__":
    super_yordamchibot.polling()