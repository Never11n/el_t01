#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
from datetime import datetime
from . import bot_config_telegram as telegram_config
from ..models import BotMessageManagers


def message_ulist(type_message, messenger):
    ulist = []
    m_managers = BotMessageManagers.objects.filter(enabled=True, add_param__type_messages__contains=type_message)
    for manager in m_managers:
        if manager.add_param.get(messenger):
            ulist.append(manager.add_param[messenger])
    return ulist


def message_send(loc_data):
    bot = telebot.TeleBot(telegram_config.token)  # Бот lotto check id
    m_messenger = loc_data.get("messenger")
    m_mess_type = loc_data.get("message_type")
    print ("m_messenger = ", m_messenger )
    print ("m_mess_type = ", m_mess_type)
    if m_messenger and m_mess_type:
        m_text = ""
        m_photo = False
        if m_mess_type == "id_confirmation":
            # bot = telebot.TeleBot(telegram_config.vika_bot)
            m_company = loc_data.get("company", "")
            m_client_name = loc_data.get("client_name", "")
            m_client_email = loc_data.get("client_email", "")
            m_client_phone = loc_data.get("client_phone", "")
            m_client_id_doc = loc_data.get("client_id_doc", "")
            m_id_conf_add = loc_data.get("id_conf_add", "")
            m_date_paid = loc_data.get("date_paid", "")
            m_ticket_type = loc_data.get("ticket_type", "")
            m_ticket_count = loc_data.get("ticket_count", "")
            m_text = (f"New Confirmation <b><i>{m_company}</i></b>"
                      f"\n ID Confirmation add at: <b>{m_id_conf_add}</b>"
                      f"\n Client:"
                      f"\n     name: <b>{m_client_name}</b>"
                      f"\n     email: <b>{m_client_email}</b>"
                      f"\n     phone: <b>{m_client_phone}</b>"
                      f"\n     ID: <b>{m_client_id_doc}</b>")
                      # f"\n Game: <b>{m_ticket_type}</b>, Tikets-<b>{m_ticket_count}</b>"
                      # f"\n Paid at: <b>{m_date_paid}</b>")
        elif m_mess_type == 'disable_subscription_request':
            bot = telebot.TeleBot(telegram_config.udachi_manager_bot)
            m_company = loc_data.get("company", "")
            m_subs_info = loc_data.get("subs_info", "")
            m_client_name = loc_data.get("client_name", "")
            m_client_email = loc_data.get("client_email", "")
            m_client_phone = loc_data.get("client_phone", "")
            m_money_win = loc_data.get("money_win", "")
            m_money_spent_all_time = loc_data.get("money_spent_all_time", "")
            m_money_win_all_time = loc_data.get("money_win_all_time", "")
            m_text = (f"User want to stop subscription (<i>{m_company}</i>)"
                      f"\n Client:"
                      f"\n     name: <b>{m_client_name}</b>"
                      f"\n     email: <b>{m_client_email}</b>"
                      f"\n     phone: <b>{m_client_phone}</b>"
                      f"\n Enabled Subscription:"
                      f"{m_subs_info}"
                      f"\n Money win (enable subscriptions): <b>{m_money_win}</b>"
                      f"\n Money (all time): <b>{m_money_spent_all_time}</b>"
                      f"\n Win (all time): <b>{m_money_win_all_time}</b>")
        elif m_mess_type == 'subscriptions':
            bot = telebot.TeleBot(telegram_config.subs_bot_token)
            m_company = loc_data.get("company", "")
            m_subs_id = loc_data.get("sub_id", "")
            m_subs_dt_stop = loc_data.get("date_stop", "")
            m_client_name = loc_data.get("client_name", "")
            m_client_email = loc_data.get("client_email", "")
            m_client_phone = loc_data.get("client_phone", "")

            m_subs_dt_start = loc_data.get("date_start", "")
            m_ticket_type = loc_data.get("ticket_type", "")
            m_money_paid = loc_data.get("money_paid", "")
            m_sms_should_be = loc_data.get("sms_should_be", "")
            m_sms_for_today = loc_data.get("sms_for_today", "")
            m_games_should_be = loc_data.get("games_should_be", "")
            m_games_for_today = loc_data.get("games_for_today", "")
            m_tickets_should_be = loc_data.get("tickets_should_be", "")
            m_tickets_for_today = loc_data.get("tickets_for_today", "")
            m_sms_left = loc_data.get("sms_left", "")
            m_games_left = loc_data.get("games_left", "")
            m_tickets_left = loc_data.get("tickets_left", "")

            m_text = (f"Subscription ended soon (<i>{m_company}</i>)"
                      f"\n Sub. ID: <b>{m_subs_id} </b>"
                      f"\n Ended at: <b>{m_subs_dt_stop} </b>"
                      f"\n Client:"
                      f"\n     name: <b>{m_client_name}</b>"
                      f"\n     email: <b>{m_client_email}</b>"
                      f"\n     phone: <b>{m_client_phone}</b>"
                      f"\n Subscription:"
                      f"\n     period: <b>{m_subs_dt_start}-{m_subs_dt_stop}</b>"
                      f"\n     ticket type: <b>{m_ticket_type}</b>"
                      f"\n     paid: <b>{m_money_paid}</b>"
                      f"\n Report:"
                      f"\n     Games:"
                      f"\n         should be: <b>{m_games_should_be}</b>"
                      f"\n         for today: <b>{m_games_for_today}</b>"
                      f"\n         left: <b>{m_games_left}</b>"
                      f"\n     Tickets:"
                      f"\n          should be: <b>{m_tickets_should_be}</b>"
                      f"\n          for today: <b>{m_tickets_for_today}</b>"
                      f"\n          left: <b>{m_tickets_left}</b>"
                      f"\n     SMS:"
                      f"\n          should be: <b>{m_sms_should_be}</b>"
                      f"\n          for today: <b>{m_sms_for_today}</b>"
                      f"\n          left: <b>{m_sms_left}</b>"
                      )
        elif m_mess_type == 'subs_auto_pay':
            bot = telebot.TeleBot(telegram_config.udachi_manager_bot)
            m_company = loc_data.get("company", "")
            if loc_data.get("error", False):
                m_subs_id = loc_data.get("sub_id", "")
                m_client_name = loc_data.get("client_name", "")
                m_client_email = loc_data.get("client_email", "")
                m_client_phone = loc_data.get("client_phone", "")
                m_text = (f"Subscription auto pay error! (<i>{m_company}</i>)"
                          f"\n Sub. ID: <b>{m_subs_id} </b>"
                          f"\n Client:"
                          f"\n     name: <b>{m_client_name}</b>"
                          f"\n     email: <b>{m_client_email}</b>"
                          f"\n     phone: <b>{m_client_phone}</b>"
                          )
            else:
                m_task_start = loc_data.get('task_start', '')
                if isinstance(m_task_start, datetime):
                    m_task_start = datetime.strftime(m_task_start, "%Y-%m-%d %H:%M")
                m_payment_count = loc_data.get('payment_count', '')
                m_money_plan = loc_data.get('money_plan', '')
                m_fail_payments = loc_data.get('fail_payments', '')
                m_fail_money = loc_data.get('money_fail', '')
                m_task_end = loc_data.get('task_end', '')
                if isinstance(m_task_end, datetime):
                    m_task_end = datetime.strftime(m_task_end, "%Y-%m-%d %H:%M")
                m_text = (f"Subscription auto pay is done (<i>{m_company}</i>)"
                          f"\n { m_task_start } - { m_task_end }"
                          f"\n Total:"
                          f"\n     plan: {m_payment_count} subs."
                          f"\n     plan amount: {m_money_plan} ILS"
                          f"\n     fails: {m_fail_payments}"
                          f"\n     failed amount: {m_fail_money} ILS"
                          )
        elif m_mess_type == 'subs_user_pay':
            bot = telebot.TeleBot(telegram_config.udachi_manager_bot)
            m_company = loc_data.get("company", "")
            m_subs_id = loc_data.get("sub_id", "")
            m_client_name = loc_data.get("client_name", "")
            m_client_email = loc_data.get("client_email", "")
            m_client_phone = loc_data.get("client_phone", "")
            m_amount = loc_data.get("amount", "")
            m_error_message = loc_data.get("error_message")
            if m_error_message:
                m_text = (f"\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C"
                          f"\n{m_error_message} (<i>{m_company}</i>)")
            else:
                m_text = (f"User has successfully paid for the subscription (<i>{m_company}</i>)"
                          f"\nAmount: {m_amount} ILS")
            m_text += (f"\n Sub. ID: <b>{m_subs_id} </b>"
                       f"\n Client:"
                       f"\n     name: <b>{m_client_name}</b>"
                       f"\n     email: <b>{m_client_email}</b>"
                       f"\n     phone: <b>{m_client_phone}</b>")
        elif m_mess_type == 'suspicious_user':
            bot = telebot.TeleBot(telegram_config.udachi_manager_bot)
            m_company = loc_data.get("company", "")
            m_client_name = loc_data.get("games_id__user_id__profile__name", "")
            m_client_email = loc_data.get("games_id__user_id__email", "")
            m_client_phone = loc_data.get("games_id__user_id__profile__mobile", "")
            m_client_id_doc = loc_data.get("games_id__user_id__profile__i_doc", "")
            m_client_birthday = loc_data.get("games_id__user_id__profile__date_birthday", "")
            m_card_last_4 = loc_data.get("card_last_4_digits", "")
            m_tickets_count = loc_data.get("tickets_count", "")
            m_spent_sum = loc_data.get("money_sum", "")
            m_text = (f"Suspicious user (<i>{m_company}</i>)"
                      f"\n Client:"
                      f"\n     name: <b>{m_client_name}</b>"
                      f"\n     email: <b>{m_client_email}</b>"
                      f"\n     phone: <b>{m_client_phone}</b>"
                      f"\n     ID: <b>{m_client_id_doc}</b>"
                      f"\n     date of birth: <b>{m_client_birthday}</b>"
                      f"\n     card last 4 digits: <b>{m_card_last_4}</b>"
                      f"\n     today tickets: <b>{m_tickets_count}</b>"
                      f"\n     today spent: <b>{m_spent_sum} ILS</b>"
                      )
        elif m_mess_type == 'fail_set_whatsapp_instance':
            bot = telebot.TeleBot(telegram_config.udachi_manager_bot)
            m_company = loc_data.get("company", "")
            m_client_name = loc_data.get("games_id__user_id__profile__name", "")
            m_client_email = loc_data.get("games_id__user_id__email", "")
            m_client_phone = loc_data.get("games_id__user_id__profile__mobile", "")
            m_text = (f"\U0000203C"
                      f"An error occurred while assigning whatsapp instance  (<i>{m_company}</i>)"
                      f"\n Client:"
                      f"\n     name: <b>{m_client_name}</b>"
                      f"\n     email: <b>{m_client_email}</b>"
                      f"\n     phone: <b>{m_client_phone}</b>")
        elif m_mess_type == 'lottomatic_errors':
            bot = telebot.TeleBot(telegram_config.udachi_manager_bot)
            m_company = loc_data.get("company", "")
            m_text_error = loc_data.get("text_error", "")
            m_text = (f"\U0000203C"
                      f"An error occurred while receiveng data from Lottomatic  (<i>{m_company}</i>)"
                      f"\n {m_text_error}")
        elif m_mess_type == 'lotto_ticket':
            bot = telebot.TeleBot(telegram_config.udachi_manager_bot)
            # bot = telebot.TeleBot(telegram_config.vika_bot)
            m_company = loc_data.get("company", "")
            m_client_name = loc_data.get("client_name", "")
            m_client_email = loc_data.get("client_email", "")
            m_client_phone = loc_data.get("client_mobile", "")
            m_ticket_name = loc_data.get("ticket_name", "")
            m_ticket_id = loc_data.get("ticket_id")
            m_title = loc_data.get("title", "")
            m_additional_text = loc_data.get("add_text", "")
            m_error = loc_data.get("error", False)

            m_text = '' if not m_error else f"\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C"
            m_text += f"{m_title} (<i>{m_company}</i>)"
            m_text += (f"\n Client:"
                       f"\n     name: <b>{m_client_name}</b>"
                       f"\n     email: <b>{m_client_email}</b>"
                       f"\n     phone: <b>{m_client_phone}</b>"
                       f"\n Ticket: <b>{m_ticket_name}</b>")
            m_text += f"\n     ticket id:{m_ticket_id}" if m_ticket_id else ""
            m_text += m_additional_text
        elif m_mess_type == 'lotto_tg_report':
            bot = telebot.TeleBot(telegram_config.udachi_lotto_win_bot)
            m_company = loc_data.get("company", "")
            m_type_ticket_type = loc_data.get("type_ticket_type")
            m_tickets_count = loc_data.get("tickets_count")
            m_win_sum = loc_data.get("win_sum")
            m_date = loc_data.get("date")
            m_text = (f"Winning tickets {m_type_ticket_type} (<i>{m_company}</i>) {m_date}"
                      f"\n     number tickets: <b>{m_tickets_count}</b>"
                      f"\n     total money: <b>{m_win_sum}</b> ILS")
        elif m_mess_type == 'lotto_tg_report_photo':
            bot = telebot.TeleBot(telegram_config.udachi_lotto_win_bot)
            m_photo_path = loc_data.get("photo_path")
            m_error = loc_data.get('error', False)
            m_id = loc_data.get('ticket_id', '')
            if m_error:
                m_text = f"\U0000203C Ticket with id <i>{m_id}</i> have no photo"
            else:
                m_text = None
                m_photo = m_photo_path
        elif m_mess_type == 'lotto_subs_user_pay':
            bot = telebot.TeleBot(telegram_config.udachi_manager_bot)
            m_company = loc_data.get("company", "")
            m_subs_id = loc_data.get("sub_id", "")
            m_client_name = loc_data.get("client_name", "")
            m_client_email = loc_data.get("client_email", "")
            m_client_phone = loc_data.get("client_phone", "")
            m_amount = loc_data.get("amount", "")
            m_error_message = loc_data.get("error_message")
            m_sub_ticket_type = loc_data.get('sub_ticket_type', '')
            m_count_games = loc_data.get('count_games', '')
            m_infinity = loc_data.get('infinity', False)
            if m_infinity:
                m_count_games = 'Each next game'
            if m_error_message:
                m_text = (f"\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C"
                          f"\n{m_error_message} (<i>{m_company}</i>)")
            else:
                m_text = (f"User has successfully paid for the lotto subscription (<i>{m_company}</i>)"
                          f"\nAmount: {m_amount} ILS")
            m_text += (f"\n Lotto Sub:"
                       f"\n     id: <b>{m_subs_id}</b>"
                       f"\n     type: <b>{m_sub_ticket_type}</b>"
                       f"\n     games count: <b>{m_count_games}</b>"
                       f"\n Client:"
                       f"\n     name: <b>{m_client_name}</b>"
                       f"\n     email: <b>{m_client_email}</b>"
                       f"\n     phone: <b>{m_client_phone}</b>")
        elif m_mess_type == 'lotto_subscription_cron':
            bot = telebot.TeleBot(telegram_config.udachi_manager_bot)
            m_company = loc_data.get("company", "")
            m_message = loc_data.get("message")
            m_title = loc_data.get("title")
            m_error = loc_data.get("error", False)
            m_text = '' if not m_error else f"\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C\U0000203C"
            m_text += f"{m_title} (<i>{m_company}</i>)"
            m_text += f"\n {m_message}"
        m_list_address = message_ulist(m_mess_type, m_messenger)
        for Item_address in m_list_address:
            try:
                if not m_text and m_photo:
                    bot.send_photo(Item_address, photo=open(m_photo, 'rb'))
                else:
                    bot.send_message(Item_address, m_text, parse_mode='html')
            except Exception as ex:
                print ("ERROR USER = ", Item_address)
                print(f"ex = {ex}")

