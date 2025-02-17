from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_sub = InlineKeyboardMarkup()
btn_sub = InlineKeyboardButton('Subscribe', callback_data='subscribe')
kb_sub.add(btn_sub)

kb_pay = InlineKeyboardMarkup()
btn_pay = InlineKeyboardButton(text='Pay 100 XTR', pay=True)
kb_pay.add(btn_pay)