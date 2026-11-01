from flask import Flask, request
from telebot import types

from bots.bosh_dasturchibot import bosh_dasturchibot
from bots.super_yordamchibot import super_yordamchibot
    
app = Flask(__name__)

@app.route('/')
def home():
    return "Botlarim uchun web sayt"

@app.route('/api')
def api():
    pass

@app.route('/bosh_dasturchibot', methods=['POST'])
def bosh_dasturchi():
    update = types.Update.de_json(request.get_data().decode('utf-8'))
    bosh_dasturchibot.process_new_updates([update])
    return 'ok', 200

@app.route('/super_yordamchibot', methods=['POST'])
def super_yordamchi():
    update = types.Update.de_json(request.get_data().decode('utf-8'))
    super_yordamchibot.process_new_updates([update])
    return 'ok', 200

if __name__ == "__main__":
    app.run(debug=True)