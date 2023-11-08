import telebot
from datetime import datetime

from .models import MessageManager, MessengerType, Messenger


def get_managers_list(type_message, messenger):
    """ Return a list of managers' specified messenger IDs if they
        should receive notifications of the specified type
    """
    managers_ids_list = []
    managers = MessageManager.objects.filter(enabled=True, add_param__type_messages__contains=type_message)
    for manager in managers:
        if manager.add_param.get(messenger):
            managers_ids_list.append(manager.add_param[messenger])
    return managers_ids_list


def send_message(data):
    """ Send message to the specified bot """
    messenger = data.get('messenger')
    message_type = data.get('message_type')
    if not messenger or not message_type or not MessengerType.objects.filter(verbal=messenger).exists() or \
            Messenger.objects.filter(messenger_type__verbal=messenger, verbal=message_type).exists():
        return
    managers_ids_list = get_managers_list(message_type, messenger)
    text_to_send = get_text_to_send(message_type, data)
    if message_type == 'telegram':
        token = Messenger.objects.get(messenger_type__verbal=message_type, verbal=message_type).settings.get('token')
        bot = telebot.TeleBot(token, parse_mode='html')
        for manager in managers_ids_list:
            try:
                bot.send_message(manager, text_to_send)
            except Exception:
                continue


def get_text_to_send(message_type, data):
    """Returns a html-message depending on the message type"""
    text = ''
    company = data.get('company', '')
    if message_type == 'id_confirmation':
        client_name = data.get('client_name', '')
        client_email = data.get('client_email', '')
        client_phone = data.get('client_phone', '')
        client_id_doc = data.get('client_id_doc', '')
        id_conf_add = data.get('id_conf_add', '')
        date_paid = data.get('date_paid', '')
        ticket_type = data.get('ticket_type', '')
        ticket_count = data.get('ticket_count', '')
        text = (f'New Confirmation <b><i>{company}</i></b>'
                f'\n ID Confirmation add at: <b>{id_conf_add}</b>'
                f'\n Client:'
                f'\n     name: <b>{client_name}</b>'
                f'\n     email: <b>{client_email}</b>'
                f'\n     phone: <b>{client_phone}</b>'
                f'\n     ID: <b>{client_id_doc}</b>'
                f'\n Game: <b>{ticket_type}</b>, Tickets-<b>{ticket_count}</b>'
                f'\n Paid at: <b>{date_paid}</b>')
    elif message_type == 'subs_auto_pay':
        if data.get('error', False):
            subs_id = data.get("sub_id", "")
            client_name = data.get("client_name", "")
            client_email = data.get("client_email", "")
            client_phone = data.get("client_phone", "")
            text = (f"Subscription auto pay error! (<i>{company}</i>)"
                    f"\n Sub. ID: <b>{subs_id} </b>"
                    f"\n Client:"
                    f"\n     name: <b>{client_name}</b>"
                    f"\n     email: <b>{client_email}</b>"
                    f"\n     phone: <b>{client_phone}</b>"
                    )
        else:
            task_start = data.get('task_start', '')
            if isinstance(task_start, datetime):
                m_task_start = datetime.strftime(task_start, "%Y-%m-%d %H:%M")
            payment_count = data.get('payment_count', '')
            money_plan = data.get('money_plan', '')
            fail_payments = data.get('fail_payments', '')
            fail_money = data.get('fail_money', '')
            task_end = data.get('task_end', '')
            if isinstance(task_end, datetime):
                m_task_end = datetime.strftime(task_end, "%Y-%m-%d %H:%M")
            text = (f"Subscription auto pay is done (<i>{company}</i>)"
                    f"\n {task_start} - {task_end}"
                    f"\n Total:"
                    f"\n     plan: {payment_count} subs."
                    f"\n     plan amount: {money_plan} ILS"
                    f"\n     fails: {fail_payments}"
                    f"\n     failed amount: {fail_money} ILS"
                    )
    elif message_type == 'suspicious_user':
        client_name = data.get('games_id__user_id__profile__name', '')
        client_email = data.get('games_id__user_id__email', '')
        client_phone = data.get('games_id__user_id__profile__mobile', '')
        client_id_doc = data.get('games_id__user_id__profile__i_doc', '')
        client_birthday = data.get('games_id__user_id__profile__date_birthday', '')
        card_last_4 = data.get('card_last_4_digits', '')
        tickets_count = data.get('tickets_count', '')
        spent_sum = data.get('money_sum', '')
        text = (f'Suspicious user (<i>{company}</i>)'
                f'\n Client:'
                f'\n     name: <b>{client_name}</b>'
                f'\n     email: <b>{client_email}</b>'
                f'\n     phone: <b>{client_phone}</b>'
                f'\n     ID: <b>{client_id_doc}</b>'
                f'\n     date of birth: <b>{client_birthday}</b>'
                f'\n     card last 4 digits: <b>{card_last_4}</b>'
                f'\n     today tickets: <b>{tickets_count}</b>'
                f'\n     today spent: <b>{spent_sum} ILS</b>'
                )
    elif message_type == 'subscriptions':                       #TODO Переименовать
        subs_id = data.get('sub_id', '')
        subs_dt_stop = data.get('date_stop', '')
        client_name = data.get('client_name', '')
        client_email = data.get('client_email', '')
        client_phone = data.get('client_phone', '')
        subs_dt_start = data.get('date_start', '')
        ticket_type = data.get('ticket_type', '')
        money_paid = data.get('money_paid', '')
        sms_should_be = data.get('sms_should_be', '')
        sms_for_today = data.get('sms_for_today', '')
        games_should_be = data.get('games_should_be', '')
        games_for_today = data.get('games_for_today', '')
        tickets_should_be = data.get('tickets_should_be', '')
        tickets_for_today = data.get('tickets_for_today', '')
        sms_left = data.get('sms_left', '')
        games_left = data.get('games_left', '')
        tickets_left = data.get('tickets_left', '')
        text = (f'Subscription ended soon (<i>{company}</i>)'
                f'\n Sub. ID: <b>{subs_id} </b>'
                f'\n Ended at: <b>{subs_dt_stop} </b>'
                f'\n Client:'
                f'\n     name: <b>{client_name}</b>'
                f'\n     email: <b>{client_email}</b>'
                f'\n     phone: <b>{client_phone}</b>'
                f'\n Subscription:'
                f'\n     period: <b>{subs_dt_start}-{subs_dt_stop}</b>'
                f'\n     ticket type: <b>{ticket_type}</b>'
                f'\n     paid: <b>{money_paid}</b>'
                f'\n Report:'
                f'\n     Games:'
                f'\n         should be: <b>{games_should_be}</b>'
                f'\n         for today: <b>{games_for_today}</b>'
                f'\n         left: <b>{games_left}</b>'
                f'\n     Tickets:'
                f'\n          should be: <b>{tickets_should_be}</b>'
                f'\n          for today: <b>{tickets_for_today}</b>'
                f'\n          left: <b>{tickets_left}</b>'
                f'\n     SMS:'
                f'\n          should be: <b>{sms_should_be}</b>'
                f'\n          for today: <b>{sms_for_today}</b>'
                f'\n          left: <b>{sms_left}</b>'
                )
    return text
