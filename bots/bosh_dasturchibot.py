import telebot
from telebot import types

import time
import random
import requests
import xml.etree.ElementTree as ET



def password_generator():
    chars = "abcdefghijklmnopqrstuvwxyz12345689807"
    return "".join(random.sample(chars, 8))


def kurs():
    url = "http://cbu.uz/uzc/arkhiv-kursov-valyut/xml/"
    root = ET.fromstring(requests.get(url).content)

    needed = {
        "USD", "AED", "AFN", "AMD", "ARS",
        "AUD", "AZN", "BDT", "BGN", "BDH",
        "BND", "BRL", "BYN", "JPY", "RUB", "ZAR"
    }

    text = ""

    for val in root.findall("CcyNtry"):
        ccy_el = val.find("Ccy")
        rate_el = val.find("Rate")

        if ccy_el is None or rate_el is None:
            continue

        ccy = ccy_el.text
        rate = rate_el.text

        date_el = val.find("Date")
        date = date_el.text if date_el is not None else None

        if ccy in needed and ccy != "ZAR":
            text += f"1 {ccy} - {rate} so'm\n"

        if ccy == "ZAR" and date:
            text += f"\nSo‘nggi yangilanish: {date}\n"

    return text

def change_fonts(text):
    # Ingliz alifbosi: 26 kichik + 26 katta = 52 ta belgi
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    fonts = {
        "bold": "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙",
        "decorative": "ᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭YᘔᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭Yᘔ",
        "double_struck": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ",
        "cursive": "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩",
        "monospace": "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉",
        "sans_italic": "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝🇮𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕",
        "gothic_bold": "𝖆𝖇𝖈𝖉𝖊f𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅",
        "bubbles": "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ",
        "squared": "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉",
        "small_caps": "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ",
        "black_bubbles": "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩",
        "upside_down": "ɐqɔpǝɟƃɥıɾʞןɯuodɹsʇunʌʍxʎzⱯᗺƆᗡƎℲפHIՐʞ˥WNOԀΌᴚS⊥∩ΛMX⅄Z",
        "flags": "🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿"
    }

    results = []

    for style, target_font in fonts.items():
        # Har bir shriftni tekshiramiz, uzunligi 52 bo'lishi shart
        if len(target_font) == 52:
            table = str.maketrans(normal, target_font)
            res = text.translate(table)
            
            if style == "upside_down":
                res = res[::-1]
            results.append(res)
        else:
            # Agar xato bo'lsa, konsolga chiqaradi (debug uchun)
            print(f"Xato: {style} uzunligi {len(target_font)} ta, 52 ta bo'lishi kerak.")

    # Sparkle alohida qo'shiladi
    sparkle_res = "".join([char + "҉" if char.isalpha() else char for char in text])
    results.append(sparkle_res)

    return results


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
    callback_button = types.InlineKeyboardMarkup()
    
    for i in range(0, len(btns), num):
        row = []
        for j in range(num):
            if i+1 < len(btns):
                row.append(types.InlineKeyboardButton(btns[i+1][0], url=btns[i+1][1]))
        callback_button.add(*row)
    return callback_button



token = ["7807701719:AAEEI6FMs6eFE6ffIEy1ri4KQ-HUehaKTbo", "5035661986:AAGHbdO-WNFHV9R1kf1LIJelYvPQ3OQGmy0"]
bosh_dasturchibot = telebot.TeleBot(token[1], threaded=False)

compane = ['BOSH DASTURCHI | BOT', '@bosh_dasturchibot']
state = {}

@bosh_dasturchibot.message_handler(commands=['start'])
def send_welcome(m):
    if m.chat.id not in state:
        state[m.chat.id] = {"step": "1"}

    state[m.chat.id]["step"] = "1"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🤖Bot xizmatlari")
    btn2 = types.KeyboardButton("📊Statistika")
    btn3 = types.KeyboardButton("🗄Kabinet")
    btn4 = types.KeyboardButton("❗️Bot haqida")

    markup.add(btn1)
    #markup.add(btn2)
    markup.add(btn4)

    bosh_dasturchibot.send_message(
        m.chat.id,
        f"Assalomu alaykum. <a href='tg://user?id={m.chat.id}'>{m.chat.first_name} {m.chat.last_name}</a>. {compane[0]} boti sizga yordam berishga tayyorman. Marhamat menyulardan foydalaning !",
        parse_mode="html",
        reply_markup=markup
    )

@bosh_dasturchibot.message_handler(commands=['help'])
def help(m):
    reply = ("Versiyasi: 1.2\nHolati: Aktiv\nDasturchi: <a href='tg:user?id=1190898538'>Xushnud Nishonov</a>")
    bosh_dasturchibot.reply_to(m, reply, parse_mode="html")

@bosh_dasturchibot.message_handler()
def texts(m):
    bot = bosh_dasturchibot

    text = m.text
    message_id = m.message_id
    chat_id = m.chat.id

    if chat_id not in state:
        state[chat_id] = {"step": "1"}

    back = types.KeyboardButton("🔙ortga")
    start = types.KeyboardButton("🔝Bosh sahifa")

    # Bwebhook = types.KeyboardButton("🕸webhook qilish")
    # Bmath = types.KeyboardButton("🔢Misol yechish")


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    callback_button = types.InlineKeyboardMarkup()

    back_menu = [back, start]

    step = state[chat_id]["step"]

    #main menu
    if text == "🔝Bosh sahifa":
        state[chat_id]["step"] = "1"

        btn1 = types.KeyboardButton("🤖Bot xizmatlari")
        btn2 = types.KeyboardButton("📊Statistika")
        btn3 = types.KeyboardButton("🗄Kabinet")
        btn4 = types.KeyboardButton("❗️Bot haqida")

        markup.add(btn1)
        # markup.add(btn2)
        markup.add(btn4)

        bot.send_message(
            m.chat.id,
            f"Assalomu alaykum. <a href='tg://user?id={chat_id}'>{m.chat.first_name} {m.chat.last_name}</a>. {compane[0]} boti sizga yordam berishga tayyorman. Marhamat menyulardan foydalaning !",
            parse_mode="html",
            reply_markup=markup
        )


    #services
    if text == "🤖Bot xizmatlari" and step == "1" or text == "🔙ortga" and (
        step == "2.1" or step == "2.2" or step == "2.3" or step == "2.4" or step == "2.5" or
        step == "2.6" or step == "2.7"
        ):
        state[chat_id]["step"] = "2"
        
        services_name = [
            "📝 Telegram tillari",
            "🎇Telegram fon",
            "🔐Random Parol",
            "💱Valyuta kursi",
            "🧩Matiqli savollar🧩",
            "♻Yangilash",
            "✔️Nick yasash✔️",
            "🤖BOT YASASH XIZMATI🤖"
        ]

        bot.send_message(
            chat_id, "Xizmatlar bo'limiga xush kelibsiz !",
            reply_markup=markup_button(services_name, 2).add(start)
        )


    #Telegram languages
    if text == "📝 Telegram tillari":
        reply = "💫 <i>Telegramingiz tilini osongina o'zgartirish uchun quyidagi tillardan birini tanlang </i>👇"

        btns = [
            ("🇺🇿 Крил тили", "tg://setlanguage?lang=uzbekcyr"),
            ("🇺🇿O'zbek tili", "tg://setlanguage?lang=uz-beta"),
            ("🇷🇺Руский язик", "tg://setlanguage?lang=ru"),
            ("🇵🇷English Languge", "tg://setlanguage?lang=en"),
            ("💠 Arab tili", "tg://setlanguage?lang=ar-beta"),
            ("💠 Koreys tili", "tg://setlanguage?lang=ko"),
            ("💠 Turk tili", "tg://setlanguage?lang=tk-beta"),
            ("💠 Ispan tili", "tg://setlanguage?lang=ues"),
            ("💠 Belarussiya tili", "tg://setlanguage?lang=be-beta"),
            ("💠 Azerbayjan tili", "tg://setlanguage?lang=az-beta"),
            ("👨‍💻Adminstrator", "t.me/xushnud_nishonov")
        ]

        bot.reply_to(
            m, reply, parse_mode="html",
            reply_markup=inline_button(btns, 2)
        )

    # Telegram backgrounds
    if text == "🎇Telegram fon":
        reply = "<b>🌐Telegram fonlar uzingizga yoqqanini tanlang.</b>"
        
        btns = [
            ("🌅Telegram 1fon", "https://t.me/bg/sp-xMi7A-VEBAAAABRn6rGsUKFs"),
            ("🌅Telegram 2fon", "https://t.me/bg/CiwwsoTP-VEBAAAAmDYEizr71BQ"),
            ("🌅Telegram 3fon", "https://t.me/bg/MzLRSHubAVIBAAAAqKgYQTObnhw"),
            ("🌅Telegram 4fon", "https://t.me/bg/Br6nNA9WAVIBAAAAe6AHvL7eOMM"),
            ("🌅Telegram 5fon", "https://t.me/bg/MiE64ER4AFIBAAAAHQZRZyDCfu0"),
            ("🌅Telegram 6fon", "https://t.me/bg/CiwwsoTP-VEBAAAAmDYEizr71BQ"),
            ("🌅Telegram 7fon", "https://t.me/bg/7wznfgBk-VEBAAAAncxYg0vokZY"),
            ("🌅Telegram 8fon", "https://t.me/bg/EhCMFgys-FEBAAAA04qJyrs1G6M"),
            ("🌅Telegram 9fon", "https://t.me/bg/7wznfgBk-VEBAAAAncxYg0vokZY"),
            ("🌅Telegram 10fon", "https://t.me/bg/7wznfgBk-VEBAAAAncxYg0vokZY"),
            ("🌅Telegram 11fon", "https://t.me/bg/FJIYygt_iVIBAAAA8tzV8Ju0QvM"),
            ("🌅Telegram 12fon", "https://t.me/bg/Qe9IiLLfiVIBAAAAn_BDUKSYaCs"),
            ("👨‍💻Adminstrator", "t.me/xushnud_nishonov")
        ]

        bot.reply_to(
            m, reply, parse_mode="html",
            reply_markup=inline_button(btns, 2)
        )
        
        
    
    #Random password
    if text == "🔐Random Parol":
        reply = f"● Ishonchli parol: <code>{password_generator()}</code>\n😎 By: ** {compane[1]} **"
        bot.reply_to(m, reply, parse_mode="html")
        
        
    
    #Exchange rate
    if text == "💱Valyuta kursi":
        reply = f"{kurs()}"
        bot.send_message(chat_id, reply, parse_mode="html")
        
        
    
    #Mantiqli savollar
    if text == "🧩Matiqli savollar🧩":
        state[chat_id]["step"] = "2.5"
        
        reply = "Tanlang!"
        
        btns = []
        for i in range(1, 205):
            if i == 1:
                btns.append("🔙ortga")
                btns.append("🔝Bosh sahifa")
            btns.append(f"{i}-savol")
            
        bot.send_message(chat_id, reply, parse_mode="html", reply_markup=markup_button(btns, 3).add(*back_menu))
        
        
        
    #♻Yangilash
    if text == "♻Yangilash":
        reply = []
        for i in range(11):
            reply.append(f"<b>{"●"*i}{"○"* (10-i)}{i*10}%</b>")
        reply.append(f"● Botimiz yangilandi ✔\n● Qayta /start ni bosing!\n😎 By: {compane[0]}")
        
        send_msg = bot.send_message(chat_id, reply[0], parse_mode="html")
        msg_id = send_msg.message_id
        
        for i in range(1, len(reply)):
            bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=reply[i], parse_mode="html")
            time.sleep(1)
            
            
            
    #✔️Nick yasash✔️
    if text == "✔️Nick yasash✔️":
        state[chat_id]["step"] = "2.7"
        
        reply = "Bu bo'limda 13 xil nick yasay olasiz.\nkerakli so'zni yozing !"
        bot.send_message(chat_id, reply, reply_markup=markup.add(*back_menu))
    
    if step == "2.7" and text != back_menu[0] and text != back_menu[1]:
        lst = change_fonts(text)
        for i in lst:
            bot.send_message(chat_id, i)
        
        
        
    #create bots services
    if text == "🤖BOT YASASH XIZMATI🤖":
        reply = (
            "<b>ASSALOMU ALAYKUM BOTIMIZ AZOSI ✌️😎</b>\n"
            "BOTIMIZDAN KO‘P FOYDALANGAN BO‘LSANGIZ XURSANDMAN 👍🤓\n"
            "XUDDI SHUNDAY BOTINGIZ BO‘LISHINI XOXLARDINGIZ TO‘G‘RIMI..? 🤔\n\n"
            "BIZ SIZGA BUNDAY BOT EMAS ☝️😁\n"
            "LEKIN SHU VAZIFANI BAJARADIGAN BOTLAR 🤟😝\n"
            "YASAB BERAMIZ\n\n"
            "<b>XIZMAT KO‘RSATISH PULLI!</b> 😜\n\n"
            "⭐ TO‘LOVLAR FAQAT ⭐\n\n"
            "💳 CLICK\n"
            "💳 PAYME\n"
            "💵 PAYNET\n\n"
            "ORQALI AMALGA OSHIRILADI ☝️😀\n\n"
            "🤖 BOTLAR MENYUSI\n\n"
            "1) GURUH NAZORATCHI BOT 👮\n"
            "2) MAJBUR BOT 🤓\n"
            "3) REFERAL BOT 🤑\n"
            "4) OB-HAVO BOT 🌤\n"
            "5) MULTIPHOTO BOT 👻\n"
            "6) LIKE SHARE BOT ♻️\n"
            "7) MP3 BOT 🎵\n"
            "8) USA NOMER BOT 🇺🇸\n"
            "9) MEMBERSGRAM BOT 👥\n"
            "10) TAKSI BOT 🚖\n"
            "11) ZAKASNOY BOT ☺️\n\n"
            "LICHKAM 👇😎\n"
            "@xushnud_nishonov"
        )

        bot.reply_to(m, reply, parse_mode="HTML")

            
    
    
    #bot about
    if text == "❗️Bot haqida":
        reply = ("Versiyasi: 1.2\nHolati: Aktiv\nDasturchi: <a href='tg:user?id=1190898538'>Xushnud Nishonov</a>")
        bot.reply_to(m, reply, parse_mode="html")

if __name__ == "__main__":
    bosh_dasturchibot.polling()