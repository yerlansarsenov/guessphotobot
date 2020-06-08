import telebot
import time
import requests
import random
from flask import Flask, request

TOKEN = '1187434462:AAHS4tT9WDQlRfq3ps4lkrZV0hGdqGwDUwE'

URL = 'https://ruslan94.pythonanywhere.com/'

# app = Flask(__name__)

bot = telebot.TeleBot(TOKEN)
#
# bot.remove_webhook()
# bot.set_webhook(URL)

# @app.route('/', methods=['POST'])
# def webhook():
#     update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
#     bot.process_new_updates([update])
#     return 'ok', 200

def reqyan(url):
    # r = requests.request('GET', url='https://yandex.kz/images/search?source=collections&rpt=imageview&url='+url)
    r = requests.get(url='https://yandex.com/images/search?source=collections&rpt=imageview&url='+url)
    # print(r.json())
    print(r.text)
    return r

def getphotourl(file_id):
    r = requests.get(f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}')
    return r.json()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Отправь мне фото, а я угадаю что там изображено')
    bot.send_message(689642806, 'id: ' + str(message.chat.id) + ', username: ' + str(message.chat.username) + ' started bot')


@bot.message_handler(content_types=['photo'])
def sendedphoto(message):
    get = getphotourl(message.photo[0].file_id)
    file_path = get['result']['file_path']
    path = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
    print(path)
    reqjson = reqyan(path)
    text = reqjson.text
    print(text)
    span = '<span class="Button2-Text">'
    i = text.find(span)
    x = text[(i + len(span)):]
    j = x.find('<')
    answer = x[:j]
    # url = 'https://yandex.kz/images/search?source=collections&rpt=imageview&url=' + path
    # bot.send_message(message.chat.id, 'OK, got it, one second, please')
    guesstext = [
        'Я думаю, что это ',
        'Мне кажется, что это ',
        'Здесь я вижу '
    ]
    bot.send_message(689642806, 'photo req from username:' +  str(message.chat.username) + ', id:' + str(message.chat.id) + ' and answer is ' + answer)
    bot.send_photo(689642806, message.photo[0].file_id)
    bot.send_message(message.chat.id, guesstext[random.randint(0, 2)] + answer)
    if message.chat.id == 1124118858:
        bot.send_message(689642806, 'tot samyi: ' + str(1124118858) + '\n' + 'first_name: ' + str(message.chat.first_name) + '\ntext: ' + str(message.chat.text))
        bot.send_message(message.chat.id, 'Hey, friend!\nI think you have been interested in my bot, please tell me what can I improve in it\n thank you very much')

@bot.message_handler(content_types=['text', 'audio', 'video', 'sticker', 'document'])
def iftext(message):
    bot.send_message(message.chat.id, 'Просто отправь мне фото :)')
    try:
        bot.send_message(689642806,
                         'id: ' + str(message.chat.id) + ', username: ' + str(message.chat.username) + ' sended smthg: ' + message.text)
    except:
        bot.send_message(689642806, 'id: ' + str(message.chat.id) + ', username: ' + str(message.chat.username) + ' sended smthg')




############# polling
while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(10)
#
###############################