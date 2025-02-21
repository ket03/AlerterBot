import threading
import time

from telebot import TeleBot
from os import getenv
from dotenv import load_dotenv

from telebot.types import LabeledPrice
from Keyboard import kb_sub, kb_pay

load_dotenv()
bot = TeleBot(getenv('TOKEN'))
users = set()
current_count_gift = len(bot.get_available_gifts().gifts)


def check_subscribe(user_id):
    f = open('id.txt', 'r')
    all_id = f.read()
    f.close()
    if all_id.find(user_id) != -1:
        return True
    return False


def write_id_to_file(user_id):
    f = open('id.txt', 'r')
    all_id = f.read()
    f.close()
    if all_id.find(user_id) == -1:
        with open('id.txt', 'a') as f:
        f.write(user_id + '\n')


def get_all_id_from_file():
    with open('id.txt', 'r') as f:
        for line in f:
            users.add(line.strip())


def alert():
    get_all_id_from_file()
    for i in range(3):
        for user in users:
            try:
                bot.send_message(chat_id=user, text='New gifts incoming!!!')
                time.sleep(0.1)
            except:
                continue
        time.sleep(1)


def counter_gifts():
    global current_count_gift
    counter = len(bot.get_available_gifts().gifts)
    while counter == current_count_gift:
        try:
            counter = len(bot.get_available_gifts().gifts)
        except:
            continue
        finally:
            time.sleep(10)
    if counter > current_count_gift:
        alert()
    current_count_gift = counter
    counter_gifts()


@bot.callback_query_handler(func=lambda call: call.data == 'subscribe')
def handle_subscribe(call):
    prices = [LabeledPrice(label='XTR', amount=100)]
    if call.data == 'subscribe':
        bot.send_invoice(call.message.chat.id,
                         title='Subscribe to Alerter',
                         description='🔔 After subscribe, bot will alert you when gift incoming 🎁 ✨',
                         invoice_payload='sub_purchase_payload',
                         provider_token='',
                         currency='XTR',
                         prices=prices,
                         reply_markup=kb_pay)
    bot.answer_callback_query(call.id)


@bot.pre_checkout_query_handler(func=lambda query: True)
def handle_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    bot.send_message(message.chat.id,'✨ You have successfully paid for your subscription! 🌟\n'
                                'Thank you for your support! 🎉 Now you will receive all gift alerts! 🎁')
    write_id_to_file(str(message.chat.id))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if check_subscribe(str(message.chat.id)):
        bot.send_message(message.chat.id, 'You have already purchased a subscription')
    else:
        bot.send_message(message.chat.id,'👋 Hello, I am BotAlerter! 🤖\n'
                                          '🔧 Working with official API telegram 📱\n'
                                        '🎯 My mission is alert you when new gift will coming 🎁\n'
                                        '!!! After subscribe you can check your status, just send /start again !!!',
                         reply_markup=kb_sub)


def main():
    counter_gifts_thread = threading.Thread(target=counter_gifts)
    counter_gifts_thread.daemon = True
    counter_gifts_thread.start()

    bot.infinity_polling()


if __name__ == '__main__':
    main()
