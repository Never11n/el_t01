# -*- coding: utf-8 -*-
import bot_config_telegram as bot_config
import telebot

bot = telebot.TeleBot(bot_config.token)

@bot.message_handler(commands=["start"])
def send_start(message):
    print ( "message.text=", message.text )
    m_adress = message.chat.id
    print ("m_adress = ", m_adress)
    m_text = 'Вы зарегистрированы на сайте для получения сообщений'

    bot.send_message(m_adress, m_text, parse_mode='html')

@bot.message_handler(func=lambda message: True, content_types=["text"])
def start_message(message):
    print ("message.chat.id = ", message.chat.id )
    print ("message.text    = ", message.text )

    m_message = message.text.strip()
    m_adress = message.chat.id
    if len(m_message) == 8:
        m_text = 'Поздравляем! Вы успешно прошли настойку мессенджера!'
        bot.send_message(m_adress, m_text, parse_mode='html')
    else:
        m_text = 'Мессенджер Telegram используется только для информирования пользователей сайта'
        bot.send_message(m_adress, m_text, parse_mode='html')

if __name__ == "__main__":
    bot.polling(none_stop=True)