from flask import Flask, request, render_template

from bots.bosh_dasturchibot import bosh_dasturchibot
import telebot
    
app = Flask(__name__)

@app.route('/')
def home():
    return "Botlarim uchun web sayt"

@app.route('/projects')
def projects():
    return "sahifalar"

@app.route('/projects/show')
def show():
    return render_template('./rotate/index.html')

@app.route('/bosh_dasturchibot', methods=['POST'])
def bosh_dasturchi():
    update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
    bosh_dasturchibot.process_new_updates([update])
    return 'ok', 200

if __name__ == "__main__":
    app.run(debug=True)