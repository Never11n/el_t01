# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import decimal
import os
import json
import base64
import datetime
import logging
import logging.config
import pytz
import requests
import pathlib2 as pathlib
from dateutil.relativedelta import *
from ipware import get_client_ip
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.utils.translation import gettext
from django.contrib.sites.shortcuts import get_current_site
from django.core.files import File

from el_t01.settings import MEDIA_ROOT, BASE_DIR
from .service.service import get_main_args
from .service.dft import get_GlobalSettings
from .models import (Profile, Ticket_history, Game_history, Ticket_type,
                     List_jellyfish, Payout, Payadd, Cashadd, Type_payment,
                     BalanceOperation, Type_balanceoperation, Type_balanceoperation_status,
                     BalRecalculate, GiftSmsToSend, IdConfirmation, Blogger,
                     Subscription, GameType
                     )
from .bot_mess.message_send import message_send


def make_pay_operation(l_user_id, l_sum, l_game_id, l_status_verbal, l_type_verbal,
                       l_description=None, l_create_user=None, l_subscription_id=None, l_lotto_subscription_id=None):

    m_type_balanceoperation_id = Type_balanceoperation.objects.get(verbal=l_type_verbal).id
    m_type_balanceoperation_status_id = Type_balanceoperation_status.objects.get(verbal=l_status_verbal).id

    pay_operation = BalanceOperation()
    pay_operation.user_id_id = l_user_id
    pay_operation.created = timezone.now()
    pay_operation.type_balanceoperation_id = m_type_balanceoperation_id
    pay_operation.games_id_id = l_game_id
    pay_operation.amount = l_sum
    pay_operation.status_id = m_type_balanceoperation_status_id
    pay_operation.description = l_description
    if l_create_user is None:
        pass
    else:
        pay_operation.t_create = True
        pay_operation.t_create_user_id = l_create_user
        pay_operation.t_create_dt = timezone.now()
    if l_subscription_id:
        pay_operation.subscription_id = l_subscription_id
    if l_lotto_subscription_id:
        pay_operation.lotto_subscription_id = l_lotto_subscription_id
    pay_operation.save()

    return pay_operation.id

def balance_recalculate(l_user_id, l_ticket_id, l_write_bool=True):
    print ("balance_recalculate")
    item_ticket = Ticket_history.objects.get(id=l_ticket_id)
    balance_recalculate_item(item_ticket.games_id.user_id_id, l_ticket_id, l_write_bool, False)

    if item_ticket.games_id.game_type.verbal ==  "game_gift" and item_ticket.games_id.user_recipient_id: # Gift
        balance_recalculate_item(item_ticket.games_id.user_recipient_id, l_ticket_id, l_write_bool, True)


def balance_recalculate_item(l_user_id, l_ticket_id, l_write_bool=True, l_recipient=False):
    print ("balance_recalculate_item")
    try:
        l_user_id = int(l_user_id)
    except:
        l_user_id = ""
    print ("l_user_id   = ", l_user_id, type(l_user_id))
    print ("l_ticket_id = ", l_ticket_id)
    m_user_profile = Profile.objects.get(user_id=l_user_id)
    m_job = ""
    m_text = ""
    # билеты от текущего и дальше
    # для пользователей - кто купил и для кого купил
    # отсортированные по айди (по созданию)
    _list_tickets = Ticket_history.objects.filter(
        Q(games_id__user_id__id=l_user_id) | Q(games_id__user_recipient_id=l_user_id)
    )
    _list_tickets = _list_tickets.filter(
        id__gte=l_ticket_id
    )
    t_ItemGame_ticket = _list_tickets.order_by("id")
    if t_ItemGame_ticket.count() == 0:
        print("NO TICKET")
        return

    #
    m_job_tmp = f"user            = {m_user_profile.name}"
    m_job += m_job_tmp + "\n"
    print (m_job_tmp)
    #
    m_job_tmp = f"user balance 00 = {m_user_profile.balance}"
    m_job += m_job_tmp + "\n"
    print (m_job_tmp)
    #
    m_balance_00 = t_ItemGame_ticket[0].balance_01
    m_balance_00_r = t_ItemGame_ticket[0].recipient_balance_01

    if l_recipient:
        # необходимо найти предыдущий билет получателя и взять последний баланс с этого билета
        _list_tickets_recipient = Ticket_history.objects.filter(
            Q(games_id__user_id__id=l_user_id) | Q(games_id__user_recipient_id=l_user_id)
        )
        _list_tickets_recipient = _list_tickets_recipient.filter(
            id__lt=l_ticket_id
        )
        _list_tickets_recipient = _list_tickets_recipient.order_by("-id")
        list_tickets_recipient = _list_tickets_recipient.count()
        if list_tickets_recipient > 0:
            list_tickets_recipient = _list_tickets_recipient.first()
            print("HAVE TICKET")
            # нужно проверить l_user_id для которого делаем он отправитель или получатель
            # l_user_id если отправитель - list_tickets_recipient.balance_02
            # l_user_id если получатель - list_tickets_recipient.recipient_balance_02
            if list_tickets_recipient.games_id.user_id_id == l_user_id:
                m_balance_00_r = list_tickets_recipient.balance_02
            if list_tickets_recipient.games_id.user_recipient_id == l_user_id:
                m_balance_00_r = list_tickets_recipient.recipient_balance_02
            print("m_balance_00_r = ", m_balance_00_r)
        else:
            print("NOT HAVE TICKET")

    m_job_tmp = f"start balance   = {m_balance_00}"
    m_job += m_job_tmp + "\n"
    print (m_job_tmp)
    #
    m_ItemGame_num = t_ItemGame_ticket.count()
    m_job_tmp = f"m_ItemGame_num = {m_ItemGame_num}"
    m_job += m_job_tmp + "\n"
    print (m_job_tmp)

    # полный список
    t_list_alloparation = []
    # операции баланса
    # найти первую операцию
    m_StartGameId = t_ItemGame_ticket[0].games_id_id
    m_job_tmp = f"m_StartGameId    = {m_StartGameId}"
    m_job += m_job_tmp + "\n"
    print (m_job_tmp)

    m_StartBalanceId = t_ItemGame_ticket[0].games_id.balance_games_id.all()[0].id
    m_job_tmp = f"m_StartBalanceId = {m_StartBalanceId}"
    m_job += m_job_tmp + "\n"
    print (m_job_tmp)

    t_balanceoperation = BalanceOperation.objects.filter(user_id_id=l_user_id,
                                                             id__gte=m_StartBalanceId,
                                                             status__verbal="04",
                                                             games_id__isnull=True,
                                                             ).order_by("id")
        #
    print("*** balance operation ***" )
    for ItemBalanceOparation in t_balanceoperation:
        m_job_tmp = f"Balance {ItemBalanceOparation.id} {ItemBalanceOparation.created} {ItemBalanceOparation.confirm} {ItemBalanceOparation.type_balanceoperation.verbal} {ItemBalanceOparation.amount} {ItemBalanceOparation.status}"
        m_job += m_job_tmp + "\n"
        print (m_job_tmp)
        ItemList = {}
        ItemList["type"] = "Bal_Op"
        ItemList["id"] = ItemBalanceOparation.id
        ItemList["dt"] = ItemBalanceOparation.created
        ItemList["val"] = ItemBalanceOparation
        t_list_alloparation.append(ItemList)
    #
    print("*** Tickets list ***")
    for ItemNum, ItemTicket in enumerate(t_ItemGame_ticket):
        ItemList = {}
        ItemList["type"] = "Ticket"
        ItemList["id"] = ItemTicket.id
        ItemList["dt"] = ItemTicket.req_dt
        ItemList["order"] = ItemNum
        ItemList["val"] = ItemTicket
        t_list_alloparation.append(ItemList)

    t_list_alloparation = sorted(t_list_alloparation, key=lambda d: (d['dt'], d['id']))
    m_job_tmp = f"*** ALL list ***   m_balance_00 = {m_balance_00}"
    m_job += m_job_tmp + "\n"
    print (m_job_tmp)

    for ItemOparationNum, ItemOparation in enumerate(t_list_alloparation):
        if ItemOparation['type'] == "Ticket":
            m_game_type = ItemOparation['val'].games_id.game_type.verbal

            l_item_ticket_change = False
            # определяем - донор или нет
            if ItemOparation['val'].games_id.user_id_id == l_user_id:
                m_user_donor = True
            else:
                m_user_donor = False
            # определяем - получатель или
            if ItemOparation['val'].games_id.user_recipient_id == l_user_id:
                m_user_recipient = True
            else:
                m_user_recipient = False

            # ToDo
            ## m_balance_00
            m_bal_01 = ItemOparation['val'].balance_01
            m_bal_01_r = ItemOparation['val'].recipient_balance_01
            if m_user_donor:
                m_bal_01 = m_balance_00
            if m_user_recipient:
                if ItemOparationNum == 0:
                    m_bal_01_r = m_balance_00_r
                else:
                    m_bal_01_r = m_balance_00

            m_sum_minus = 0
            m_sum_minus_r = 0
            m_sum_win = 0
            m_sum_win_r = 0

            if m_game_type in ["game", "game_lotto"]: # Regular game
                # если покупка с баланса то нужно вычесть стоимость билета
                if ItemOparation['val'].games_id.t_payment.verbal == "balance":
                    m_sum_minus = ItemOparation['val'].cost_2
                else:
                    m_sum_minus = 0
                # если клиент сыграл, билет в состоянии ФИНИШ
                if ItemOparation['val'].status == "33":
                    try:
                        # m_sum_win = int(ItemOparation['val'].answ_win_sum)
                        m_sum_win = decimal.Decimal(ItemOparation['val'].answ_win_sum)
                    except:
                        m_sum_win = 0

            elif m_game_type in ["game_gift", "game_lotto_gift"]: # Gift
                # если покупка с баланса то нужно вычесть стоимость билета только у донора
                # if m_user_donor:
                #     if ItemOparation['val'].games_id.t_payment.verbal == "balance":
                #         m_sum_minus = ItemOparation['val'].cost_2
                #     else:
                #         m_sum_minus = 0
                if ItemOparation['val'].games_id.t_payment.verbal == "balance":
                    m_sum_minus = ItemOparation['val'].cost_2
                    if m_user_donor and m_user_recipient:
                        m_sum_minus_r = m_sum_minus
                else:
                    m_sum_minus = 0
                if ItemOparation['val'].status == "33":
                    if m_user_donor and not m_user_recipient:
                        try:
                            m_sum_win_r = decimal.Decimal(ItemOparation['val'].answ_win_sum)
                        except:
                            m_sum_win_r = 0
                    if not m_user_donor and m_user_recipient:
                        try:
                            m_sum_win_r = decimal.Decimal(ItemOparation['val'].answ_win_sum)
                        except:
                            m_sum_win_r = 0
                    if m_user_donor and m_user_recipient:
                        try:
                            m_sum_win = decimal.Decimal(ItemOparation['val'].answ_win_sum)
                            m_sum_win_r = decimal.Decimal(ItemOparation['val'].answ_win_sum)
                        except:
                            m_sum_win = 0
                            m_sum_win_r = 0
            else:
                pass

            m_bal_02 = m_bal_01 - m_sum_minus + m_sum_win
            m_bal_02_r = m_bal_01_r - m_sum_minus_r + m_sum_win_r
            # рассчет m_balance_00
            if m_user_donor:
                m_balance_00 = m_bal_02
            if m_user_recipient:
                m_balance_00 = m_bal_02_r

            m_job_tmp = f"{ItemOparation['type']}" \
                        + "-" + f"{ItemOparation['val'].id}".ljust(7) \
                        + "-" + f"{ItemOparation['dt']}".ljust(32) \
                        + " =" + f"{ItemOparation['val'].games_id.t_payment.verbal}".ljust(11) \
                        + " =bal_1=" + f"{ItemOparation['val'].balance_01}".ljust(6) \
                        + " | " + f"{m_bal_01}".ljust(6) \
                        + " =cost=" + f"{ItemOparation['val'].cost_2}".ljust(4) \
                        + " =win=" + f"{ItemOparation['val'].answ_win_sum}".ljust(6) \
                        + " | " + f"{m_sum_win}".ljust(6) \
                        + " =bal_2=" + f"{ItemOparation['val'].balance_02}".ljust(6) \
                        + " | " + f"{m_bal_02}".ljust(6) \
                        + " =stat=" + f"{ItemOparation['val'].status}".ljust(2) \
                        + " =balance_00=" + f"{m_balance_00}".ljust(7)
            m_job += m_job_tmp + "\n"
            print (m_job_tmp)
            m_job_tmp = f"".ljust(47) \
                        + " =" + f"{ItemOparation['val'].games_id.t_payment.verbal}".ljust(11) \
                        + " =bal_1=" + f"{ItemOparation['val'].recipient_balance_01}".ljust(6) \
                        + " | " + f"{m_bal_01_r}".ljust(6) \
                        + " =cost=" + f"{str(ItemOparation['val'].cost_2)}".ljust(4) \
                        + " =win=" + f"{str(ItemOparation['val'].answ_win_sum)}".ljust(6) \
                        + " | " + f"{m_sum_win_r}".ljust(6) \
                        + " =bal_2=" + f"{ItemOparation['val'].recipient_balance_02}".ljust(6) \
                        + " | " + f"{m_bal_02_r}".ljust(6) \
                        + " =stat=" + f"{ItemOparation['val'].status}".ljust(2)
            m_job += m_job_tmp + "\n"
            print (m_job_tmp)

            if l_write_bool:
                if m_bal_01 != ItemOparation['val'].balance_01 \
                    or m_bal_02 != ItemOparation['val'].balance_02 \
                    or m_bal_01_r != ItemOparation['val'].recipient_balance_01 \
                    or m_bal_02_r != ItemOparation['val'].recipient_balance_02:

                    t_ItemGame_ticket[ItemOparation["order"]].balance_01 = m_bal_01
                    t_ItemGame_ticket[ItemOparation["order"]].balance_02 = m_bal_02
                    t_ItemGame_ticket[ItemOparation["order"]].recipient_balance_01 = m_bal_01_r
                    t_ItemGame_ticket[ItemOparation["order"]].recipient_balance_02 = m_bal_02_r
                    t_ItemGame_ticket[ItemOparation["order"]].save()
        else:
            if ItemOparation['val'].type_balanceoperation.for_balance == "minus":
                m_balance_00 = m_balance_00 - ItemOparation['val'].amount
            if ItemOparation['val'].type_balanceoperation.for_balance == "plus":
                m_balance_00 = m_balance_00 + ItemOparation['val'].amount
            m_job_tmp = f"{ItemOparation['type']} {ItemOparation['dt']} == {ItemOparation['val'].type_balanceoperation.verbal} {ItemOparation['val'].amount} == bal={m_balance_00} "
            m_job += m_job_tmp + "\n"
            print (m_job_tmp)

    if l_write_bool:
        m_user_profile.balance = m_balance_00
        m_user_profile.save()
    print ("m_user_profile.balance = ", m_user_profile.balance)

    m_BalRecalculate = BalRecalculate()
    m_BalRecalculate.user_id_id = l_user_id
    m_BalRecalculate.text = m_text
    m_BalRecalculate.job = m_job
    m_BalRecalculate.save()


def get_game_play_ticket_info(request, m_ticket_id=None):
    print ("get_game_play_ticket_info")

    args = get_main_args(request, section="main")
    t_ticket = Ticket_history.objects.get(id=m_ticket_id)
    m_box_html = ""
    m_template_name = f"{args['GL_MainSkin']}/cabinet/game_play_item_ticket/template_00.html"
    '''
    ('00', 'start'),
    ('01', 'ready'),
    ('30', 'error'),
    ('33', 'finish game'),
    '''
    m_canvas = "00"
    pic_canvas64 = ""
    args_templ = {}
    if t_ticket.status == "33":  # 'finish game'
        args_templ['pic_result'] = t_ticket.img_08
        m_template_name = f"{args['GL_MainSkin']}/cabinet/game_play_item_ticket/_ticket_finish.html"
        m_canvas = "00"
    elif t_ticket.status == "01":  # 'ready'
        # test
        # args["pic_result"] = "http://45.80.70.249:50777/media/ticket/tic/01/bursa-result.png"
        # args["pic_canvas"] = "http://45.80.70.249:50777/media/ticket/tic/01/bursa-scratch.png"
        #
        args_templ['pic_result'] = t_ticket.img_08
        m_tic_verbal = t_ticket.game_type.verbal
        # print("m_tic_verbal = ", m_tic_verbal)
        # args["pic_canvas"] = "http://45.80.70.249:50777/media/ticket/tic/01/bursa-scratch.png"
        # args["pic_canvas"] = f"http://45.80.70.249:50777/media/tic/{m_tic_verbal}/{m_tic_verbal}-scratch.png"
        # print("pic_canvas = ", args["pic_canvas"])

        # file = 'deer.jpg'
        # m_dir_short = os.path.join('media', 'ticket_in', str(m_Devices_item.id))
        # m_dir_full = os.path.join(BASE_DIR, m_dir_short)
        # file = f"http://45.80.70.249:50777/media/tic/{m_tic_verbal}/{m_tic_verbal}-scratch.png"

        # print("BASE_DIR = ", BASE_DIR)
        file = f"media/tic/{m_tic_verbal}/{m_tic_verbal}-scratch.png"
        # print("file 1 = ", file)
        file = os.path.join(BASE_DIR, file)
        # print("file 2 = ", file)
        image = open(file, 'rb')
        image_read = image.read()
        pic_canvas64 = base64.encodebytes(image_read).decode().strip()
        # print("pic_canvas64 = ", pic_canvas64)
        pic_canvas64 = f"data:image/png;base64,{pic_canvas64}"
        # print("pic_canvas64 = ", pic_canvas64)

        # pic_canvas64_str = str(pic_canvas64)
        # print ("pic_canvas64_str = ", pic_canvas64_str)

        # print("pic_canvas64 = ", type(pic_canvas64), len(pic_canvas64))

        # image = open('lol.jpeg', 'rb')  # open binary file in read mode
        #            image_read = image.read()
        #            image_64_encode = base64.encodebytes(image_read).decode().strip()
        #            print ("image_64_encode = ", image_64_encode)
        #
        # image_64_decode = base64.decodebytes(image_64_encode)
        # image_result = open('deer_decode.jpg', 'wb')  # create a writable image and write the decoding result
        # image_result.write(image_64_decode)
        args_templ['title_txt'] = gettext('Scratch the ticket by hand.')
        m_template_name = f"{args['GL_MainSkin']}/cabinet/game_play_item_ticket/_ticket_ready.html"
        m_canvas = "01"
    elif t_ticket.status == "00":  # 'start'
        m_time_wait = 50
        # Please wait up to 90 seconds to receive the ticket, the ticket is in preparation.
        args_templ['wait_title'] = gettext('Please wait up to 90 seconds to receive the ticket, the ticket is in preparation.')
        # args_templ['wait_title'] = gettext('It may take')
        # args_templ['wait_title'] += f" {m_time_wait} "
        # args_templ['wait_title'] += gettext('seconds to prepare your game')
        # gif
        args_templ['pic_tic_wait'] = f"{args['GL_MainSkin']}/main/images/loading/casino.gif"
        # m_template_name = 'cabinet/game_play_item_ticket/_ticket_wait_gif.html'
        # video
        # args_templ['wait_poster'] = "https://assets.codepen.io/32795/poster.png"
        # args_templ['wait_source'] = "http://media.w3.org/2010/05/sintel/trailer.mp4"
        args_templ['wait_poster'] = ""
        # args_templ['wait_source'] = "http://media.w3.org/2010/05/sintel/trailer.mp4"

        # поиск видио по типу билета
        # видио по типу билета
        m_wait_source = f"/media/prevideo/{args['GL_MainSkin']}/prevideo_{t_ticket.game_type.verbal}.mp4"
        m_source_for_check = MEDIA_ROOT + f"/prevideo/{args['GL_MainSkin']}/prevideo_{t_ticket.game_type.verbal}.mp4"
        if not (os.path.exists(m_source_for_check) and os.path.isfile(m_source_for_check)):
            m_wait_source = "/media/prevideo/prevideo_04.mp4"
        args_templ['wait_source'] = m_wait_source
        args_templ['wait_source_type'] = "video/mp4"
        args_templ['wait_ads_link'] = "https://japo.co.il/"
        m_template_name = f"{args['GL_MainSkin']}/cabinet/game_play_item_ticket/_ticket_wait_video.html"
        m_canvas = "00"
    else:
        m_template_name = f"{args['GL_MainSkin']}/cabinet/game_play_item_ticket/template_00.html"
        m_canvas = "00"

    m_template = get_template(m_template_name)
    m_box_html = m_template.render(args_templ)

    answer = {"AnswerCod": "01",
              "AnswerText": "ok",
              "s_canvas": m_canvas,
              "s_box_html": m_box_html,
              "pic_canvas64": pic_canvas64,
              "template_name": m_template_name,
              "args_templ": args_templ,
              "t_status": t_ticket.status
              }
    return (answer)

def create_game_play_list(l_game_id=None, l_mark=-1, l_lang="en"):
    t_game_tickets = Ticket_history.objects.filter(games_id_id=l_game_id).order_by("req_id")
    m_all_finish = True
    m_refresh = True
    m_ticket_dict = {}
    # id
    # n
    # mark
    # id
    # status 00 01 30 33
    # class
    # t_type_id
    # t_type_caption
    # t_number
    # t_win
    # t_win_sum
    # html

    m_ticket_list = []
    for ItemNum, ItemOrder in enumerate(t_game_tickets):
        # 1 вариант  ожидание Pending ('00', 'start'),
        # 2 вариант  готов к игре кнопка ПЛАЙ # ('01', 'ready'),
        # 3 вариант  уже сыграл кнопка СМОТРЕТЬ # ('33', 'finish game'),
        # 4 вариант    # ('30', 'error'),
        m_item = {}
        m_item["id"] = ItemOrder.id
        m_item["n"] = f"{ ItemNum + 1 } ({ItemOrder.req_id})"

        if l_mark == -1:
            if ItemNum == 0:
                m_item["mark"] = True
            else:
                m_item["mark"] = False
        else:
            if ItemOrder.id == l_mark:
                m_item["mark"] = True
            else:
                m_item["mark"] = False

        m_item["status"] = ItemOrder.status
        m_item["status_txt"] = ItemOrder.status
        m_item["t_type_id"] = ItemOrder.game_type.id
        m_templ_01 = gettext(ItemOrder.game_type.caption)
        m_item["t_type_caption"] = f"{ m_templ_01 }"
        m_item["t_number"] = ItemOrder.answ_nom
        m_item["t_win"] = ItemOrder.answ_win_sum
        m_item["t_win_sum"] = '***'

        m_item_class = f""
        m_item_html = f""
        m_item_status_txt = f""

        # if m_item["mark"]:
        if True:
            if l_lang == "he":
                m_item_html += f"<td class='ui-td'><i class='fa fa-arrow-alt-circle-left ui-mark'></i></td>"
            else:
                m_item_html += f"<td class='ui-td'><i class='fa fa-arrow-alt-circle-right ui-mark'></i></td>"
            # angle - left
            # arrow-alt-circle-left
        else:
            m_item_html += "<td class='ui-td'></td>"
        m_item_html += f"<td class='ui-td'>{ m_item['n'] }<br>{ m_item['t_type_caption'] }</td>"
        # m_item_html += f"<td class='ui-td'>{ m_item['t_type_caption'] }</td>"

        if ItemOrder.status == "00":  # ('00', 'start'),
            # m_item_html += f"<td class='ui-td'>{ '****-******-***' }</td>"
            # m_item_html += f"<td class='ui-td'>{gettext('Pending')}<img class='pending-dot' src='/static/main/002/images/loading/run_dot.gif' style='pointer-events: none;'></td>"
            m_templ_01 = gettext('In process')
            m_item_html += f"<td class='ui-td'>{m_templ_01}<img class='pending-dot' src='/static/main/002/images/loading/run_dot.gif' style='pointer-events: none;'></td>"
            # m_item_html += f"<td class='ui-td ui-tsum'>{ '***' }</td>"
            m_item_class += f"table-secondary"
            # m_item["status_txt"] =  f"{gettext('Pending')}<img class='pending-dot' src='/static/main/002/images/loading/run_dot.gif' style='pointer-events: none;'>" # 'start'
            m_templ_01 = gettext('In process')
            m_item["status_txt"] = f"{m_templ_01}<img class='pending-dot' src='/static/main/002/images/loading/run_dot.gif' style='pointer-events: none;'>" # 'start'
            m_item["t_number"] = '****-******-***'
            m_item["t_win_sum"] = '***'
        elif ItemOrder.status == "01":  # ('01', 'ready'),
            m_templ_01 = gettext('ready for play')
            m_item_html += f"<td class='ui-td'>{ ItemOrder.answ_nom }<br>{m_templ_01}</td>"
            # m_item_html += f"<td class='ui-td'>{gettext('ready for play')}</td>"
            # m_item_html += f"<td class='ui-td ui-tsum'>{ '***' }</td>"
            m_item_class += f"table-info"
            m_item["status_txt"] = 'ready for play'
            # m_item["t_number"] = '****-******-***'
            # m_item["t_win_sum"] = '***'
        elif ItemOrder.status == "30":  # ('30', 'error'),
            m_item_html += f"<td class='ui-td'>{ 'XXXX-XXXXXX-XXX' }</td>"
            m_templ_01 = gettext('error')
            m_item_html += f"<td class='ui-td'>{m_templ_01}</td>"
            # m_item_html += f"<td class='ui-td ui-tsum'>{ '***' }</td>"
            m_item_class += f"table-active"
            m_item["status_txt"] = 'error ticket'
            m_item["t_number"] = 'XXXX-XXXXXX-XXX'
            m_item["t_win_sum"] = '***'
        elif ItemOrder.status == "33":  # ('33', 'finish game'),
            if ItemOrder.answ_win:
                m_templ_01 = f"{gettext('Win sum')}<br>{ ItemOrder.answ_win_sum }"
                # m_item_html += f"<td class='ui-td ui-tsum'>{ ItemOrder.answ_win_sum }</td>"
                m_item["t_win_sum"] = f'{ ItemOrder.answ_win_sum }'
            else:
                m_templ_01 = gettext('Not Win')

            if ItemOrder.answ_nom is None:
                # m_templ_01 = gettext('finish game')
                m_item_html += f"<td class='ui-td'><br>{m_templ_01}</td>"
            else:
                # m_templ_01 = gettext('finish game')
                m_item_html += f"<td class='ui-td'>{ ItemOrder.answ_nom }<br>{m_templ_01}</td>"
            # m_item_html += f"<td class='ui-td'><button class='mybtn1 mybtn7'>{gettext('SHOW')}</button></td>"
            # m_item_html += f"<td class='ui-td'>{gettext('finish game')}<</td>"

            if ItemOrder.answ_win:
                # m_item_html += f"<td class='ui-td ui-tsum'>{ ItemOrder.answ_win_sum }</td>"
                m_item["t_win_sum"] = f'{ ItemOrder.answ_win_sum }'
            else:
                # m_item_html += f"<td class='ui-td'>0</td>"
                m_item["t_win_sum"] = f'{ 0 }'

            if ItemOrder.answ_win:
                m_item_class += f"table-success"
            else:
                m_item_class += f"table-light"
            m_item["status_txt"] = 'finish game'
            m_item["t_number"] = ItemOrder.answ_nom
        else:
            pass

        # if ItemOrder.status != "33" and ItemOrder.status != "01":
        if ItemOrder.status == "00":
            m_refresh = False
        if ItemOrder.status != "33":
            m_all_finish = False


        m_ticket_dict[f"k{ItemOrder.id}"] = {"status": ItemOrder.status}
        m_item["html"] = m_item_html
        m_item["class"] = f"{m_item_class} ui-btn_ticket_info js-btn_ticket_info"
        m_ticket_list.append(m_item)

    return (m_ticket_list, m_all_finish, m_ticket_dict, m_refresh)

# в cabb_  такаяже функция запуска РЕСТАРТ БИЛЕТА jellyfish_game_restart
def jellyfish_game_start(request, l_game_id, l_tickets):
    m_dirlog_short = os.path.join(BASE_DIR, "..", "log/log_jellyfish_game_start")
    print("os.path.exists(m_dirlog_short) = ", os.path.exists(m_dirlog_short))
    if not os.path.exists(m_dirlog_short):
        os.makedirs(m_dirlog_short)
    m_log_file = os.path.join(m_dirlog_short, 'log_jellyfish_game_start.log')
    DictLOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s; %(levelname)s:%(name)s: %(message)s '
                          '(%(filename)s:%(lineno)d)',
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'rotate_file': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                #            'filename': 'rotated.log',
                'filename': m_log_file,
                'encoding': 'utf8',
                'maxBytes': 200000,
                'backupCount': 30,
            }
        }
        ,
        'loggers': {
            '': {
                'handlers': ['console', 'rotate_file'],
                # 'handlers': ['rotate_file'],
                # 'level': 'DEBUG',
                'level': 'INFO',
            },
        }
    }
    logging.config.dictConfig(DictLOGGING)
    logging.info('/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*')
    logging.info('***** jellyfish_game_start ******')
    print("jellyfish_game_start")
    try:
        # проверить доступна машина или нет
        t_jellyfish = List_jellyfish.objects.filter(enabled=True).order_by("order")
        print(f"t_jellyfish.count = {t_jellyfish.count()}")
        logging.info(f"t_jellyfish.count = {t_jellyfish.count()}")
        ##
        if request is None:
            m_GL_LIST = get_GlobalSettings()
            m_scheme = m_GL_LIST.get("GL_Subs_return_url_sh", "")
            m_domain_name = m_GL_LIST.get("GL_Subs_return_url_dom", "")
        else:
            m_current_site_for_send = str(get_current_site(request))
            print(f"m_current_site_for_send = {m_current_site_for_send}")
            logging.info(f"m_current_site_for_send = {m_current_site_for_send}")
            m_scheme = request.scheme
            m_domain_name = get_current_site(request).name
        l_return_url = f"{m_scheme}://{m_domain_name}/jellyfish_rezult"
        # l_return_url = f"http://return.com/jellyfish_rezult"
        ##
        if t_jellyfish.count() > 0:
            item_jellyfish = t_jellyfish[0]
            # id enabled verbal caption order ipadres api_token
            m_url_1 = item_jellyfish.ipadres
            m_url_2 = "" if m_url_1.strip()[-1] == "/" else "/"
            m_url_3 = "api/v07/external/new_game"
            url = f"{m_url_1}{m_url_2}{m_url_3}"
            m_payload = {
                "game_id": l_game_id,
                "tickets": l_tickets,
                "return_url": l_return_url
            }
            payload = json.dumps(m_payload)
            headers = {
                'Token': item_jellyfish.api_token,
                'Content-Type': 'application/json'
            }
            logging.info(f"game_id   = {l_game_id}")
            logging.info(f"l_tickets = {l_tickets}")
            logging.info(f"url       = {url}")
            logging.info(f"headers   = {headers}")
            logging.info(f"payload   = {payload}")
            print(f"url     = {url}")
            print(f"headers = {headers}")
            print(f"payload = {payload}")

            response = requests.request("POST", url, headers=headers, data=payload)
            # print("response.text =", response.text, response.status_code)
            logging.info(f"response.status_code = {response.status_code}")
            # logging.info(f"response.text        = {response.text}")

            # response.text = {"success":true,"approximate_waiting_time":"0:01:40","approximate_waiting_time_sec":100}

            if response.status_code == 200:
                try:
                    mj_response = json.loads(response.text)
                    if mj_response["success"] == True:
                        logging.info(f"check_jellyfish_game status start OK")
                        # self.ReturnBool = True
                        m_Text01 = gettext("We are preparing your game, the approximate waiting time is")
                        m_Text02 = mj_response.get("approximate_waiting_time_sec", "--")
                        m_Text03 = gettext("sec.")
                        m_ReturnText = f"{m_Text01} {m_Text02} {m_Text03}"
                        print ("m_ReturnText = ", m_ReturnText )
                        # self.ReturnText = f"{m_Text01} {m_Text02} {m_Text03}"
                    else:
                        logging.info(f"Error check_jellyfish_game status start NOT OK")
                        # self.ReturnBool = False
                        # self.ReturnText = gettext("Unable to start the game. Try later.")
                        # self.ReturnText = gettext("Unable to start the game. Try later.")
                        m_ReturnText = gettext("Unable to start the game. Try later.")
                        print ("m_ReturnText = ", m_ReturnText )

                except Exception as ex:
                    print(f"ex = {ex}")
                    # pass
                    logging.info(f"Error check_jellyfish_game status except")
                    logging.info(f"ex = {ex}")
                    # self.ReturnBool = False
                    # self.ReturnText = gettext("Unable to start the game. Try later.")
            else:
                # pass
                logging.info(f"Error check_jellyfish_game status {response.status_code}")
                # self.ReturnBool = False
                # self.ReturnText = gettext("Unable to start the game. Try later.")
        else:
            # pass
            logging.info("Error check_jellyfish_game not available")
            # self.ReturnBool = False
            # self.ReturnText = (gettext("The game is not available. Try later."))
        logging.info(f"check_jellyfish_game = ")
    except Exception as ex:
        # pass
        # self.t_Ticket_type = None
        logging.info(f"start_jelyfish Unable to start the game")
        logging.info(f"ex = {ex}")
        # self.ReturnBool = False
        # self.ReturnText = (gettext("start_jelyfish Unable to start the game. Try later."))
    logging.info(f"FINISH")

def start_game(request, l_game_id=None):
    m_history_txt = ""
    m_history_txt += f"= start_game = {l_game_id}\n"
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        print("redirect 1")
        return redirect('/')
    else:
        args['item_game_user'] = Game_history.objects.get(id=l_game_id)
        #
        #ToDo
        m_games_payment_verbal = args['item_game_user'].t_payment.verbal ## "balance"
        m_games_status_verbal = args['item_game_user'].t_status.verbal
        m_order_list = args['item_game_user'].ticket_list["list_order"]
        m_history_txt += f" payment    = {m_games_payment_verbal}\n"
        m_history_txt += f" status     = {m_games_status_verbal}\n"
        m_history_txt += f" order list = {len(m_order_list)}\n"
        m_history_txt += f" order list = {m_order_list}\n"

        if args['item_game_user'].user_id_id != args['me'].id:
            m_history_txt += f" game not owner \n"
            args['item_game_user'].history = m_history_txt
            args['item_game_user'].save()
            return redirect('/')

        if m_games_status_verbal == "wait_payment":
            m_balance_00 = args['me'].profile.balance
            args['all_quantity'] = 0
            args['all_sum'] = 0
            for ItemOrder in m_order_list:
                m_itemGame_type = ItemOrder["tic_type"]
                m_history_txt += f" m_itemGame_type = {m_itemGame_type}\n"
                t_ItemTicket_type = Ticket_type.objects.get(id=m_itemGame_type)
                m_ItemGame_num_01 = int(ItemOrder["tic_num"])
                m_history_txt += f" m_ItemGame_num_01 = {m_ItemGame_num_01}\n"
                t_ItemGame_ticket = Ticket_history.objects.filter(games_id__id=args['item_game_user'].id,
                                                                  game_type__id=m_itemGame_type)
                m_ItemGame_num_02 = t_ItemGame_ticket.count()
                m_history_txt += f" m_ItemGame_num_02 = {m_ItemGame_num_02}\n"
                # создаем количество билетов в Ticket_history
                if m_ItemGame_num_02 < m_ItemGame_num_01:
                    for ItemTicketAdd in range(m_ItemGame_num_01 - m_ItemGame_num_02):
                        m_history_txt += f" ItemTicketAdd = {ItemTicketAdd}\n"
                        t_ItemGame_ticket_new = Ticket_history()
                        t_ItemGame_ticket_new.games_id_id = args['item_game_user'].id
                        t_ItemGame_ticket_new.game_type_id = m_itemGame_type
                        t_ItemGame_ticket_new.save()
                        m_req_id = str(t_ItemGame_ticket_new.id)
                        for item_check in range(20):
                            if not Ticket_history.objects.filter(req_id=m_req_id).exists():
                                break
                            m_req_id += ".1"

                        t_ItemGame_ticket_new.req_id = m_req_id
                        t_ItemGame_ticket_new.req_dt = datetime.datetime.now()
                        t_ItemGame_ticket_new.save()
                        m_history_txt += f" t_ItemGame_ticket_new.id = {t_ItemGame_ticket_new.id}\n"
                #
                t_ItemGame_ticket = Ticket_history.objects.filter(games_id__id=args['item_game_user'].id,
                                                                  game_type__id=m_itemGame_type).order_by("id")
                #
                m_discount = args['item_game_user'].ticket_list.get("discount", 0)
                for ItemTicket in t_ItemGame_ticket:
                    ItemTicket.balance_01 = m_balance_00
                    if ItemTicket.games_id.game_type.verbal == "game_lotto":
                        ItemTicket.cost_1 = ItemTicket.games_id.ticket_list.get('cost_1', 0)
                        ItemTicket.cost_02 = ItemTicket.games_id.ticket_sum
                        ItemTicket.cost_discount = m_discount
                        ItemTicket.cost_2 = ItemTicket.games_id.ticket_sum - m_discount
                    else:
                        ItemTicket.cost_1 = ItemTicket.game_type.cost_1
                        ItemTicket.cost_02 = ItemTicket.game_type.cost_2
                        ItemTicket.cost_discount = m_discount
                        ItemTicket.cost_2 = ItemTicket.game_type.cost_2 - m_discount

                    if ItemTicket.games_id.t_payment.verbal == "balance":
                        m_sum_minus = ItemTicket.cost_2
                    else:
                        m_sum_minus = 0

                    m_balance_00 = m_balance_00 - m_sum_minus
                    ItemTicket.balance_02 = m_balance_00
                    ItemTicket.save()
                #
                m_history_txt += f" new balance = {m_balance_00}\n"
                args['me'].profile.balance = m_balance_00
                args['me'].profile.save()
                #
                m_history_txt += f" count tickets = {t_ItemGame_ticket.count()}\n"
                if args['item_game_user'].game_type.verbal in ["game", "game_gift"]:
                    # создаем список билетов для МЕДУЗЫ
                    item_tickets_list = []
                    for ItemTicket in t_ItemGame_ticket:
                        m_list_add = {"ticket_id": ItemTicket.req_id}
                        item_tickets_list.append(m_list_add)

                    m_history_txt += f" tickets list for jelyfish = {item_tickets_list}\n"
                    m_history_txt += f" ***jellyfish_game_start***\n"
                    ## проверить на лотто
                    jellyfish_game_start(request, l_game_id=t_ItemTicket_type.verbal_jellyfish, l_tickets=item_tickets_list)

            args['item_game_user'].t_status_id = args['dict_game_status']["start"]
            args['item_game_user'].history = m_history_txt
            args['item_game_user'].save()

            if args['item_game_user'].ticket_list.get('gift', False):
                # если подарок выводим сообщение и вызываем создание смс
                make_gift_sms(args['item_game_user'])
                return redirect('/gift-ok/')
            elif args['item_game_user'].game_type.verbal == "game_lotto":
                try:
                    user_profile = args['item_game_user'].user_id.profile
                    d_globalset = get_GlobalSettings()
                    data_for_bot_sms = {
                        "company": d_globalset.get("GL_Name_Company", ""),
                        "client_name": user_profile.name,
                        "client_email": args['item_game_user'].user_id.email,
                        "client_phone": user_profile.mobile,
                        "ticket_name": args['item_game_user'].ticket_list["list_order"][0]["tic_caption"],
                        "messenger": "telegram",
                        "message_type": "lotto_ticket",
                        "title": "New lotto ticket has been purchased ",
                        "add_text": f"\n     sum: <b>{args['item_game_user'].ticket_sum}</b>ILS"
                    }
                    message_send(data_for_bot_sms)
                except Exception:
                    pass
                return cab_game_lotto_start(request, verbal=args['item_game_user'].id)
            else:
                # если для себя - играть
                return redirect(f"/cab-game-play/{args['item_game_user'].id}/")
        else:
            return redirect(f"/cab-game-play/{args['item_game_user'].id}/")


def cabinet(request, cab_type=None):
    print ("==cabinet==")
    print ("cab_type ", cab_type)
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        print ("args['lang'] = ", args['lang'])
        args['cabinet_form'] = True
        if cab_type == "cab_history":
            args['cabinet_form'] = True
            args['page_caption'] = gettext('History Game')
            game_history_list = Ticket_history.objects.filter(
                Q(games_id__user_id__id=args['me'].id) | Q(games_id__user_recipient__id=args['me'].id)
            ).filter(game_type__t_type__verbal='old').order_by("-req_dt", "-id")
            args['game_history_list'] = game_history_list

            args['menu_item'] = 'nav-link_history'
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_history.html")
        elif cab_type == "cab_contact":
            args['cabinet_form'] = True
            args['page_caption'] = gettext('Pay operation')
            args['menu_item'] = 'nav-link_contact'
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_contact.html")
        elif cab_type == "cab_profile":
            args['cabinet_form'] = True
            args['page_caption'] = gettext('Pay operation')
            args['menu_item'] = 'nav-link_profile'
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_profile.html")
        elif cab_type == "cab_pasw":
            args['cabinet_form'] = True
            args['page_caption'] = gettext('Change pasword')
            args['menu_item'] = 'nav-link_profile'
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_pasw.html")
        elif cab_type == "cab_payadd":
            args['cabinet_form'] = True
            args['page_caption'] = gettext('Bank Transfer')
            args['menu_item'] = 'nav-link_payadd'
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_payadd.html")
        elif cab_type == "cab_payout":
            args['cabinet_form'] = True
            args['page_caption'] = gettext('Order PayOut')
            args['menu_item'] = 'nav-link_payout'
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_payout.html")
            # Редактирование конкретной записи
            m_pId = request.GET.get('pId', "")
            if m_pId != '':
                if Payout.objects.filter(id=m_pId).exists():
                    payout_edit = Payout.objects.get(id=m_pId)
                    args['payout_edit'] = payout_edit
                    args['payout_form'] = True
            # Кнопка new
            m_pNew = request.GET.get('pNew', "")
            # Неподтвержденные пэйауты
            new_payouts_list = Payout.objects.filter(user_id=args['me'], status='00')
            if m_pNew == '' and m_pId == '' and new_payouts_list.count() > 0:
                args['new_payouts'] = new_payouts_list
                args['payout_form'] = False
            else:
                args['payout_form'] = True
        elif cab_type == "cab_cashadd":
            args['cabinet_form'] = True
            args['page_caption'] = gettext('Cash Add')
            args['menu_item'] = 'nav-link_cashadd'
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_cashadd.html")
        elif cab_type == "cab_balance":
            args['cabinet_form'] = True
            args['page_caption'] = f"{gettext('Balance')} ({args['me'].profile.balance})"
            t_balanceOperation = BalanceOperation.objects.filter(user_id_id=args['me'].id).order_by("-created")
            args['balanceOperation'] = t_balanceOperation
            args['menu_item'] = 'nav-link_profile'
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_balance.html")
        elif cab_type == "cab_cabinet_gift":
            args['cabinet_form'] = False
            args['page_caption'] = gettext('Cabinet')
            # return redirect('/hishgadonline')
            # args['l_layout_file'] = f"{args['GL_MainSkin']}/cabinet/layout_cab.html"
            args['box_message_title'] = gettext("Guiding video")
            args['box_message_subtitle'] = ""
            args['box_message_text'] = ""
            args['video_source'] = f"/media/prevideo/{args['GL_Movie_list']}"
            args['video_source_type'] = "video/mp4"
            args['menu_item'] = 'nav-link_cabinet_gift'
            args['tickets_gift'] = True
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_game_list.html")
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_video.html")
            if len(args['dict_partner']) > 0:
                args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_partner.html")
        elif cab_type == 'cab_subs_history':
            args['cabinet_form'] = True
            args['page_caption'] = gettext('Subscriptions History')
            subs_list = Subscription.objects.filter(user_id=args['me'].id, paid_amount__gt=0
                                                    ).order_by('-dt_start')
            # subs_list = []
            args['subs_history_list'] = subs_list
            args['menu_item'] = 'nav-link_subs_history'
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_subs_history.html")
        elif cab_type == 'cab_referrals':
            if not args['me'].profile.settings.get('i_am_blogger'):
                return redirect('/')
            else:
                m_daterange_joined = request.GET.get('daterange', '')
                m_ref_hash = args['me'].profile.settings.get('i_am_blogger')
                blogger = Blogger.objects.get(ref_hash=m_ref_hash).id
                now_date = datetime.datetime.now().date()
                referrals = Profile.objects.filter(settings__ref_blogger_id=blogger, date_joined__date=now_date).order_by('-date_joined')
                if m_daterange_joined != '':
                    args['date_range'] = m_daterange_joined
                    m_daterange_joined_list = m_daterange_joined.split("-")
                    try:
                        m_date_start = datetime.datetime.strptime(m_daterange_joined_list[0].strip(), "%d.%m.%Y")
                        m_date_finish = datetime.datetime.strptime(m_daterange_joined_list[1].strip(), "%d.%m.%Y")
                        referrals = Profile.objects.filter(settings__ref_blogger_id=blogger,
                                                           date_joined__range=[m_date_start, m_date_finish]).order_by('-date_joined')
                    except Exception:
                        referrals = referrals
                args['cabinet_form'] = True
                args['page_caption'] = gettext('My referrals')
                args['l_script_list'].append(f"{args['GL_MainSkin']}/cabinet/l_script_02.html")
                args['l_head_list'].append(f"{args['GL_MainSkin']}/cabinet/l_head_02.html")
                args['referrals_list'] = referrals
                args['menu_item'] = 'nav-link_referrals'
                args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_blogger_referrals.html")
        #
        elif cab_type == 'cab_block':
            args['cabinet_form'] = True
            args['page_caption'] = gettext('Delete account')
            args['menu_item'] = 'nav-link_cab_block'
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_block.html")
            args['m_fullname'] = args['me'].profile.name
            args['m_email'] = args['me'].email

        else: # cab_type == "cab_cabinet":
            args['cabinet_form'] = False
            args['page_caption'] = gettext('Cabinet')
            # return redirect('/hishgadonline')
            # args['l_layout_file'] = f"{args['GL_MainSkin']}/cabinet/layout_cab.html"
            args['box_message_title'] = gettext("Guiding video")
            args['box_message_subtitle'] = ""
            args['box_message_text'] = ""
            args['video_source'] = f"/media/prevideo/{args['GL_Movie_list']}"
            args['video_source_type'] = "video/mp4"
            args['menu_item'] = 'nav-link_cabinet'

            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_notif_list.html")
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_game_list.html")
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_video.html")
            if len(args['dict_partner']) > 0:
                args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_partner.html")

        args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
        return render(request, args['main_tab'], args)


def cab_payout_save(request):
    print ("= cab_payout_save =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.POST:
            print ("POST = ", request.POST)
            try:
                m_user_id = args['me'].id
                m_created = datetime.datetime.now()
                m_status = "00"
                m_acc_name = request.POST.get('f_acc_name', "")
                m_name_bank = request.POST.get('f_name_bank', "")
                m_branch = request.POST.get('f_branch', "")
                m_acc_num = request.POST.get('f_acc_num', "")
                m_amount = request.POST.get('f_amount', 0)
                m_id = request.POST.get('f_id')
                try:
                    # m_amount = int(m_amount)
                    m_amount = decimal.Decimal(m_amount)
                except Exception as ex:
                    m_amount = 0
                if m_id:
                    t_Payout = Payout.objects.get(id=m_id)
                else:
                    t_Payout = Payout()
                    m_pay_operation_id = make_pay_operation(l_user_id=m_user_id,
                                                            l_sum=m_amount,
                                                            l_game_id=None,
                                                            l_status_verbal="04",
                                                            l_type_verbal="payout")
                    if args['me'].profile.balance >= m_amount:
                        args['me'].profile.balance = args['me'].profile.balance - m_amount
                        args['me'].profile.save()
                        d_globalset = get_GlobalSettings()
                        percent = d_globalset.get('GL_Payout_percent_minus')
                        try:
                            percent = decimal.Decimal(percent)
                        except Exception:
                            percent = decimal.Decimal('3.9')
                        # amount_minus_percent = (m_amount / 100) * (100 - percent)
                        amount_minus_percent = m_amount - percent
                        amount_minus_percent = decimal.Decimal(amount_minus_percent).quantize(decimal.Decimal('.01'),
                                                                                              rounding=decimal.ROUND_HALF_UP)
                        t_Payout.user_id_id = m_user_id
                        t_Payout.created = m_created
                        t_Payout.status = m_status
                        t_Payout.bal_oper_id = m_pay_operation_id
                        t_Payout.amount = m_amount
                        t_Payout.percent = percent
                        t_Payout.amount_minus_percent = amount_minus_percent
                    else:
                        return redirect('/payout-err-sum')
                t_Payout.acc_name = m_acc_name
                t_Payout.name_bank = m_name_bank
                t_Payout.branch = m_branch
                t_Payout.acc_num = m_acc_num
                t_Payout.save()
                return redirect('/payout-ok')

            except Exception as ex:
                return redirect('/payout-err')
        else:
            return redirect('/')


def cab_payout_delete(request):
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.POST:
            print("POST = ", request.POST)
            try:
                m_id = request.POST.get('f_id')
                t_payout = Payout.objects.get(id=m_id)
                t_payout.status = '02'  # Reject status
                t_payout.save()
                t_balop = t_payout.bal_oper
                t_type_balanceoperation_status = Type_balanceoperation_status.objects.get(verbal="03")  # Reject status
                t_balop.status = t_type_balanceoperation_status
                t_balop.save()
                #  Return money on balance
                m_pay_operation_id = make_pay_operation(l_user_id=args['me'].id,
                                                        l_sum=t_payout.amount,
                                                        l_game_id=None,
                                                        l_status_verbal="04",
                                                        l_type_verbal="add_money")
                args['me'].profile.balance = args['me'].profile.balance + t_payout.amount
                args['me'].profile.save()
                answer = {"AnswerCod": "01",
                          "AnswerText": ""}
            except Exception as ex:
                answer = {"AnswerCod": "00",
                          "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cab_payout_ok(request, verbal=None):
    print ("= cab_payout_ok =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        # ToDo check ADMIN
        if True:
            pass
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                print ("POST = ", request.POST)
                try:
                    m_user_id = args['me'].id
                    m_pay_out_id = request.POST.get('f_pay_out_id', "")
                    t_payout = Payout.objects.get(id=m_pay_out_id)
                    t_payout.status = "01"
                    t_payout.t_check = True
                    t_payout.t_check_user_id = m_user_id
                    t_payout.t_check_dt = timezone.now()
                    t_payout.save()

                    m_type_balanceoperation_status_id = Type_balanceoperation_status.objects.get(verbal="04").id
                    pay_operation = BalanceOperation.objects.get(id=t_payout.bal_oper_id)
                    pay_operation.status_id = m_type_balanceoperation_status_id
                    pay_operation.save()
                    answer = {"AnswerCod": "00"}
                except:
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cab_payout_block(request, verbal=None):
    print ("= cab_payout_block =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        # ToDo check ADMIN
        if True:
            pass
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            # if request.POST:
            #     print ("POST = ", request.POST)
            #     try:
            #         m_user_id = args['me'].id
            #         m_pay_out_id = request.POST.get('f_pay_out_id', "")
            #         t_payout = Payout.objects.get(id=m_pay_out_id)
            #         t_payout.status = "01"
            #         t_payout.t_check = True
            #         t_payout.t_check_user_id = m_user_id
            #         t_payout.t_check_dt = timezone.now()
            #         t_payout.save()
            #
            #         m_type_balanceoperation_status_id = Type_balanceoperation_status.objects.get(verbal="04").id
            #         pay_operation = BalanceOperation.objects.get(id=t_payout.bal_oper_id)
            #         pay_operation.status_id = m_type_balanceoperation_status_id
            #         pay_operation.save()
            #         answer = {"AnswerCod": "00"}
            #     except:
            #         answer = {"AnswerCod": "00",
            #                   "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cab_payadd_save(request):
    print ("= cab_payadd_save =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.POST:
            print ("POST          = ", request.POST)
            print ("request.FILES = ", request.FILES)
            try:
                m_user_id = args['me'].id
                m_created = datetime.datetime.now()
                m_status = "00"

                m_amount = request.POST.get('f_add_amount', 0)
                try:
                    m_amount = decimal.Decimal(m_amount)
                except Exception as ex:
                    m_amount = 0
                m_upload_doc = ""
                if "f_add_file" in request.FILES:
                    #
                    m_time_now = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
                    file_to_upload = request.FILES["f_add_file"]
                    m_file_save_name = os.path.splitext(file_to_upload.name)[0]
                    m_file_save_name = f"{m_time_now}_{m_file_save_name}"
                    m_file_save_ext = os.path.splitext(file_to_upload.name)[1]
                    user_dir_short = os.path.join("media", "users", str(m_user_id), "doc_add")
                    user_file_short = os.path.join(user_dir_short, m_file_save_name + m_file_save_ext)
                    user_dir = os.path.join(BASE_DIR, user_dir_short)
                    user_file = os.path.join(BASE_DIR, user_file_short)
                    print("user_dir_short  = ", user_dir_short)
                    print("user_file_short = ", user_file_short)
                    print("user_dir        = ", user_dir)
                    print("user_file       = ", user_file)

                    pathlib.Path(user_dir).mkdir(parents=True, exist_ok=True)
                    # for filename in os.listdir(user_dir):
                    #         filepath = os.path.join(user_dir, filename)
                    #         if os.path.isfile(filepath):
                    #             if os.path.splitext(filepath)[0] == m_file_save_name:
                    #                 os.remove(filepath)
                    f = File(file_to_upload)
                    with open(user_file, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                    m_upload_doc = user_file_short

                    # if args['me'].profile.balance >= m_amount:
                    #     args['me'].profile.balance = args['me'].profile.balance - m_amount
                    #     args['me'].profile.save()

                    m_pay_operation_id = make_pay_operation(l_user_id=m_user_id,
                                                            l_sum=m_amount,
                                                            l_game_id=None,
                                                            l_status_verbal="01",
                                                            l_type_verbal="add_money")

                    t_Payadd = Payadd()
                    t_Payadd.user_id_id = m_user_id
                    t_Payadd.created = m_created
                    t_Payadd.status = m_status
                    t_Payadd.bal_oper_id = m_pay_operation_id
                    t_Payadd.amount = m_amount
                    t_Payadd.upload_doc = m_upload_doc
                    t_Payadd.save()
                    return redirect('/payadd-ok')

            except Exception as ex:
                return redirect('/payadd-err')
        else:
            return redirect('/')


def cab_payadd_ok(request, verbal=None):
    print ("= cab_payout_ok =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        # ToDo check ADMIN
        if True:
            pass
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                print ("POST = ", request.POST)
                try:
                    m_user_id = args['me'].id
                    m_pay_out_id = request.POST.get('f_pay_out_id', "")
                    t_payout = Payout.objects.get(id=m_pay_out_id)
                    t_payout.status = "01"
                    t_payout.t_check = True
                    t_payout.t_check_user_id = m_user_id
                    t_payout.t_check_dt = timezone.now()
                    t_payout.save()

                    m_type_balanceoperation_status_id = Type_balanceoperation_status.objects.get(verbal="04").id
                    pay_operation = BalanceOperation.objects.get(id=t_payout.bal_oper_id)
                    pay_operation.status_id = m_type_balanceoperation_status_id
                    pay_operation.save()
                    answer = {"AnswerCod": "00"}
                except:
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)
#

def cab_game_addnew(request, verbal=None, addparam=None):
    print ("= cab_game_addnew =")
    print ("verbal   = ", verbal)
    print ("addparam = ", addparam)
    args = get_main_args(request, section="main")
    args['menu_item'] = 'nav-link_cabinet'
    args['addparam'] = addparam

    if addparam == "gift":
        args['tickets_gift'] = True
        args['menu_item'] = 'nav-link_cabinet_gift'
    if not args['logged_in']:
        return redirect('/')
    else:
        try:
            args['item_ticket_type'] = Ticket_type.objects.get(verbal=verbal)
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_game_item.html")
            args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
            # ip_request
            m_in_ip, m_in_is_routable = get_client_ip(request)
            # logging.info(f'  ip, is_routable = {m_in_ip}, {m_in_is_routable}')
            if m_in_ip is None:
                pass
                # logging.info('  NONE')
                # Unable to get the client's IP address
            else:
                # We got the client's IP address
                if m_in_is_routable:
                    pass
                    # logging.info("  The client's IP address is publicly routable on the Internet")
                else:
                    pass
                    # logging.info("  The client's IP address is private")
            #
            item_game_user = Game_history()
            if addparam == "gift":
                item_game_user.game_type = GameType.objects.get(verbal='game_gift')
            else:
                item_game_user.game_type = GameType.objects.get(verbal='game')
            item_game_user.user_id_id = args['me'].id
            item_game_user.dt_add = timezone.now()
            item_game_user.user_ip = f'{m_in_ip} {m_in_is_routable}'
            mj_tickets_list = {}
            mj_tickets_list["list_order"] = []
            mj_tickets_list_item = {}
            mj_tickets_list_item["date"] = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
            mj_tickets_list_item["tic_type"] = args['item_ticket_type'].id
            mj_tickets_list_item["tic_caption"] = args['item_ticket_type'].caption
            mj_tickets_list_item["tic_num"] = "1"
            mj_tickets_list_item["ip"] = f'{m_in_ip} {m_in_is_routable}'
            mj_tickets_list["list_order"].append(mj_tickets_list_item)
            item_game_user.ticket_list = mj_tickets_list
            try:
                if args['discount_user'].get("discount") == True:
                    item_game_user.t_discount_id = args['discount_user']["discount_id"]
            except:
                item_game_user.t_discount_id = None
            item_game_user.save()
            return redirect(f'/cab-game-item/{item_game_user.id}/{addparam}')
        except:
            return redirect('/')


def cab_game_item(request, verbal=None, addparam=None): # verbal= id game
    print ("= cab_game_item =")
    print ("verbal = ", verbal)
    print ("addparam = ", addparam)
    args = get_main_args(request, section="main")
    args['menu_item'] = 'nav-link_cabinet'
    args['page_caption'] = gettext('Add Ticket')
    if addparam == "gift":
        args['tickets_gift'] = True
        args['addparam'] = addparam
        args['menu_item'] = 'nav-link_cabinet_gift'
        args['page_caption'] = gettext('Add the lottery ticket as a gift')
    print("args['lang'] = ", args['lang'])
    if not args['logged_in']:
        return redirect('/')
    else:
        try:
            args['cabinet_form'] = True
            args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
            m_idconf = False
            if IdConfirmation.objects.filter(user_id=args['me'].id).exists():
                args['idconf'] = IdConfirmation.objects.filter(user_id=args['me'].id)[0]
                if args['idconf'].status.verbal != "ok":
                    m_idconf = True

            if m_idconf:
                args['page_caption'] = gettext('Check ID')
                args['menu_item'] = 'nav-link_payout'
                if args['idconf'].photo_id == "" or args['idconf'].photo_face == "" :
                    args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_check_id.html")
                else:
                    args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_check_id_info.html")
            else:
                args['item_game_user'] = Game_history.objects.get(id=verbal)
                m_item_game_ticket = args['item_game_user'].ticket_list["list_order"][0]["tic_type"]
                args['item_ticket_type'] = Ticket_type.objects.get(id=m_item_game_ticket)
                if args['discount_user'].get("discount") == True:
                    args['item_game_user'].t_discount_id = args['discount_user']["discount_id"]
                    args['discount_user_num'] = args['discount_user']["discount_product_list"].get(args['item_ticket_type'].id, 0)
                    print ('discount_user_num = ', args['discount_user_num'])
                    # m_discount_user_num = args['discount_user']["discount_product_list"].get(args['item_ticket_type'].id, None)
                    # if m_discount_user_num is None:
                    #     args['discount_user_num'] = 0
                    # else:
                    #     args['discount_user_num'] = m_discount_user_num["discount_num"]
                else:
                    args['item_game_user'].t_discount_id = None
                args['item_game_user'].save()
                args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_game_item.html")

            return render(request, args['main_tab'], args)
        except:
            return redirect('/')


def cab_game_order(request, verbal=None):
    print("= cab_game_order =")
    print("verbal = ", verbal)
    args = get_main_args(request, section="main")
    args['menu_item'] = 'nav-link_cabinet'
    print("args['lang'] = ", args['lang'])
    if not args['logged_in']:
        return redirect('/')
    else:
        try:
            ##
            # 1 проверить код игры
            # 2 составить список вариантов оплаты
            # 3 составить список - ордер-заказ
            #
            # 1
            m_game_id = verbal
            try:
                m_game_id = int(m_game_id)
                print("m_game_id = ", m_game_id)
            except:
                return redirect('/')
            # 2
            m_payment_type_count = args['dict_payment_type'].count()
            if m_payment_type_count == 1:
                args['m_payment_column_css'] = 12
                m_payment_column_count = 1
            elif m_payment_type_count == 2:
                args['m_payment_column_css'] = 6
                m_payment_column_count = 2
            elif m_payment_type_count == 3:
                args['m_payment_column_css'] = 4
                m_payment_column_count = 3
            elif m_payment_type_count == 4:
                args['m_payment_column_css'] = 3
                m_payment_column_count = 4
            elif m_payment_type_count == 5:
                args['m_payment_column_css'] = 4
                m_payment_column_count = 3
            elif m_payment_type_count == 6:
                args['m_payment_column_css'] = 4
                m_payment_column_count = 3
            else:
                args['m_payment_column_css'] = 3
                m_payment_column_count = 4

            args['PaymentList'] = []
            m_ItemPaymentList = []
            for ItemCounter, ItemPaymentList in enumerate(args['dict_payment_type']):
                if (ItemCounter) % m_payment_column_count == 0 and ItemCounter != 0:
                    args['PaymentList'].append(m_ItemPaymentList)
                    m_ItemPaymentList = []
                m_ItemPaymentList.append(ItemPaymentList)

            if len(m_ItemPaymentList) > 0:
                args['PaymentList'].append(m_ItemPaymentList)

            print("PaymentList = ", args['PaymentList'])
            args['Payment_column_count'] = m_payment_column_count
            # 3
            args['game_order_list'] = []
            args['item_game_user'] = Game_history.objects.get(id=m_game_id)

            if args['discount_user'].get("discount") == True:
                args['item_game_user'].t_discount_id = args['discount_user']["discount_id"]
                args['discount_user_num'] = args['discount_user']["discount_product_list"].get(
                    args['item_ticket_type'].id, 0)

                # m_discount_user_num = args['discount_user']["discount_product_list"].get(args['item_ticket_type'].id, None)
                # if m_discount_user_num is None:
                #     args['discount_user_num'] = 0
                # else:
                #     args['discount_user_num'] = m_discount_user_num["discount_num"]
            else:
                args['item_game_user'].t_discount_id = None
                args['discount_user_num'] = 0
            args['item_game_user'].save()

            print('discount_user_num = ', args['discount_user_num'])

            m_order_list = args['item_game_user'].ticket_list["list_order"]
            args['all_quantity'] = 0
            args['all_sum'] = 0
            for ItemOrder in m_order_list:
                m_itemGame_type = ItemOrder["tic_type"]
                t_itemGameType = Ticket_type.objects.get(id=m_itemGame_type)

                m_ItemGame = {}
                m_ItemGame["n"] = 11
                m_ItemGame["type"] = t_itemGameType
                m_ItemGame["name"] = t_itemGameType.caption
                m_ItemGame["pic"] = 11
                m_ItemGame["num"] = ItemOrder["tic_num"]
                m_ItemGame["cost_1"] = t_itemGameType.cost_1
                m_ItemGame["cost_2"] = t_itemGameType.cost_2
                m_ItemGame["currency"] = t_itemGameType.type_currency.code
                args['game_order_list'].append(m_ItemGame)
                try:
                    m_quantity = int(ItemOrder["tic_num"])
                except:
                    m_quantity = 0
                args['all_quantity'] += m_quantity
                try:
                    m_sum = m_quantity * (t_itemGameType.cost_2 - args['discount_user_num'])
                except:
                    m_sum = 0
                m_ItemGame["sum_i"] = m_sum
                m_ItemGame["sum_t"] = m_sum
                args['all_sum'] += m_sum
            #
            m_balance_last = args['me'].profile.balance
            m_balance_last = '{0:,}'.format(m_balance_last)
            args['balance_last'] = f"{m_balance_last} {gettext(args['main_currency'])}"
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_game_pay.html")
            args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
            #
            return render(request, args['main_tab'], args)
        except:
            return redirect('/')


def cab_game_buy(request):
    print("= cab_game_buy =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        try:
            if request.method == "POST":
                # 1 проверить код игры
                # 3 составить список - ордер-заказ
                #
                # 1
                print("request.POST = ", request.POST)
                m_game_id = request.POST.get('game_order', 0)
                m_ticket_id = request.POST.get('ticket_order', 0)
                m_quantity_ticket = request.POST.get('quantity_ticket', 0)
                m_addparam = request.POST.get('addparam', "")
                args['addparam'] = m_addparam

                try:
                    m_ticket_id = int(m_ticket_id)
                except:
                    return redirect('/')
                try:
                    m_game_id = int(m_game_id)
                except:
                    return redirect('/')
                # 3
                args['game_order_list'] = []
                args['item_game_user'] = Game_history.objects.get(id=m_game_id)
                m_order_list = args['item_game_user'].ticket_list["list_order"]
                print("m_order_list = ", m_order_list)
                m_all_quantity = 0
                m_all_sum = 0

                for ItemOrder in m_order_list:
                    print("ItemOrder = ", ItemOrder)
                    m_itemGame_type = ItemOrder["tic_type"]
                    t_itemGameType = Ticket_type.objects.get(id=m_itemGame_type)
                    if ItemOrder["tic_type"] == m_ticket_id:
                        print(" i find")
                        ItemOrder["tic_num"] = m_quantity_ticket
                    try:
                        m_quantity = int(ItemOrder["tic_num"])
                    except:
                        m_quantity = 0
                    try:
                        m_sum = m_quantity * t_itemGameType.cost_2
                    except:
                        m_sum = 0
                    print ("m_quantity = ", m_quantity)
                    print ("m_sum      = ", m_sum)
                    m_all_quantity += m_quantity
                    m_all_sum += m_sum

                args['item_game_user'].ticket_list["list_order"] = m_order_list
                args['item_game_user'].ticket_num = m_all_quantity
                args['item_game_user'].ticket_sum = m_all_sum
                if m_addparam == "gift":
                    m_gift = True
                else:
                    m_gift = False
                args['item_game_user'].ticket_list["addparam"] = m_addparam
                args['item_game_user'].ticket_list["gift"] = m_gift
                args['item_game_user'].save()
                #
                GL_hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                            '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
                            '22', '23']
                GL_minutes = ['00', '15', '30', '45']
                GL_tel_prefix = '+972'
                GL_operators = ['50', '52', '53', '54', '58']
                if args['item_game_user'].ticket_list["gift"]:
                    args['m_range_hours'] = GL_hours
                    args['m_range_minut'] = GL_minutes
                    args['m_tel_prefix'] = GL_tel_prefix
                    args['m_operators'] = GL_operators
                    args['l_head_list'].insert(len(args['l_head_list'])-1, f"{args['GL_MainSkin']}/cabinet/l_head_02.html")
                    args['l_script_list'].append(f"{args['GL_MainSkin']}/cabinet/l_script_02.html")

                    args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_gift.html")
                    args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
                    return render(request, args['main_tab'], args)
                else:
                    return redirect(f"/cab-game-pay/{args['item_game_user'].id}/")
            else:
                return redirect('/')
        except Exception as ex:
            print ("ex = ", ex)
            return redirect('/')


def cab_game_gift_info(request, verbal=None):
    print("= cab_game_gift_info =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        try:
            if request.method == "POST":
                print("request.POST = ", request.POST)
                m_game_id = request.POST.get('f_game_id', 0)
                m_name = request.POST.get('f_name', 0)
                m_text = request.POST.get('f_text', 0)
                m_date = request.POST.get('f_date_start', 0)
                m_hour = request.POST.get('f_t_hours', 0)
                m_minute = request.POST.get('f_t_minut', 0)
                m_t_prefix = request.POST.get('f_t_prefix', '')
                m_t_operator = request.POST.get('f_t_operator', '')
                m_phone = request.POST.get('f_phone', '')
                m_is_adult_confirm = request.POST.get('is_adult_confirm')
                m_gift_info = {}
                m_gift_info["name"] = m_name
                m_gift_info["phone"] = m_t_prefix + m_t_operator + m_phone
                m_gift_info["text"] = m_text
                m_gift_info["date"] = m_date
                m_gift_info["hour"] = m_hour
                m_gift_info["minute"] = m_minute
                m_gift_info["is_adult_confirm"] = m_is_adult_confirm
                try:
                    m_game_id = int(m_game_id)
                except:
                    return redirect('/')
                args['item_game_user'] = Game_history.objects.get(id=m_game_id)
                args['item_game_user'].ticket_list["gift_info"] = m_gift_info
                args['item_game_user'].save()
                # TODO not empty
                #
                # if args['item_game_user'].ticket_list["gift"]:
                #     args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_gift.html")
                #     args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
                #     return render(request, args['main_tab'], args)
                # else:
                #     return redirect(f"/cab-game-pay/{args['item_game_user'].id}/")
                return redirect(f"/cab-game-pay/{args['item_game_user'].id}/")
            else:
                return redirect('/')
        except Exception as ex:
            print ("ex = ", ex)
            return redirect('/')

#####

def cab_game_pay(request, verbal=None):
    print("= cab_game_pay =")
    args = get_main_args(request, section="main")
    args['menu_item'] = 'nav-link_cabinet'
    if not args['logged_in']:
        return redirect('/')
    else:
        try:
            # 1 проверить код игры
            # 2 составить список вариантов оплаты
            # 3 составить список - ордер-заказ
            #
            # 1
            m_game_id = verbal
            try:
                m_game_id = int(m_game_id)
            except:
                return redirect('/')
            # 2
            m_payment_type_count = args['dict_payment_type'].count()
            if m_payment_type_count == 1:
                args['m_payment_column_css'] = 12
                m_payment_column_count = 1
            elif m_payment_type_count == 2:
                args['m_payment_column_css'] = 6
                m_payment_column_count = 2
            elif m_payment_type_count == 3:
                args['m_payment_column_css'] = 4
                m_payment_column_count = 3
            elif m_payment_type_count == 4:
                args['m_payment_column_css'] = 3
                m_payment_column_count = 4
            elif m_payment_type_count == 5:
                args['m_payment_column_css'] = 4
                m_payment_column_count = 3
            elif m_payment_type_count == 6:
                args['m_payment_column_css'] = 4
                m_payment_column_count = 3
            else:
                args['m_payment_column_css'] = 3
                m_payment_column_count = 4
            args['PaymentList'] = []
            m_ItemPaymentList = []
            for ItemCounter, ItemPaymentList in enumerate(args['dict_payment_type']):
                if (ItemCounter) % m_payment_column_count == 0 and ItemCounter != 0:
                    args['PaymentList'].append(m_ItemPaymentList)
                    m_ItemPaymentList = []
                m_ItemPaymentList.append(ItemPaymentList)
            if len(m_ItemPaymentList) > 0:
                args['PaymentList'].append(m_ItemPaymentList)
            args['Payment_column_count'] = m_payment_column_count
            # 3
            args['game_order_list'] = []
            args['item_game_user'] = Game_history.objects.get(id=m_game_id)

            if args['discount_user'].get("discount") == True:
                args['item_game_user'].t_discount_id = args['discount_user']["discount_id"]
                # args['discount_user_num'] = args['discount_user']["discount_product_list"].get(
                #     args['item_ticket_type'].id, 0)

                # m_discount_user_num = args['discount_user']["discount_product_list"].get(args['item_ticket_type'].id, None)
                # if m_discount_user_num is None:
                #     args['discount_user_num'] = 0
                # else:
                #     args['discount_user_num'] = m_discount_user_num["discount_num"]
            else:
                args['item_game_user'].t_discount_id = None
                args['discount_user_num'] = 0
            args['item_game_user'].save()

            if args['item_game_user'].ticket_list.get("gift", False):
                args['menu_item'] = 'nav-link_cabinet_gift'

            m_order_list = args['item_game_user'].ticket_list["list_order"]
            for ItemOrder in m_order_list:
                print ("ItemOrder = ", ItemOrder)
                m_itemGame_type = ItemOrder["tic_type"]
                t_itemGameType = Ticket_type.objects.get(id=m_itemGame_type)
                m_ItemGame = {}
                # m_ItemGame["n"] = 11
                m_ItemGame["type"] = t_itemGameType
                m_ItemGame["name"] = t_itemGameType.caption
                m_ItemGame["pic"] = 11
                m_ItemGame["num"] = ItemOrder["tic_num"]
                m_ItemGame["cost_1"] = t_itemGameType.cost_1
                m_ItemGame["cost_2"] = t_itemGameType.cost_2
                m_ItemGame["currency"] = t_itemGameType.type_currency.code
                m_ItemGame["max_win"] = t_itemGameType.max_win
                args['game_order_list'].append(m_ItemGame)
                if args['discount_user'].get("discount") == True:
                    args['discount_user_num'] = args['discount_user']["discount_product_list"].get(t_itemGameType.id, 0)
                else:
                    args['discount_user_num'] = 0

                try:
                    m_quantity = int(ItemOrder["tic_num"])
                except:
                    m_quantity = 0
                try:
                    args['discount_user_sum'] = m_quantity * args['discount_user_num']
                    args['all_quantity'] = args['item_game_user'].ticket_num
                    m_sum = m_quantity * t_itemGameType.cost_2
                    m_sum_d = m_quantity * (t_itemGameType.cost_2 - args['discount_user_num'])
                except:
                    m_sum = 0
                    m_sum_d = 0

                m_ItemGame["sum_i"] = m_sum
                m_ItemGame["sum_t"] = '{0:,}'.format(m_sum)

            args['item_game_user'].ticket_sum = m_sum_d
            args['item_game_user'].save()

            args['all_quantity'] = args['item_game_user'].ticket_num
            # args['all_sum'] = args['item_game_user'].ticket_sum
            args['all_sum'] = '{0:,}'.format(args['item_game_user'].ticket_sum)
            args['item_game_user'].ticket_list["list_order"] = m_order_list
            args['item_game_user'].save()
            m_balance_last = args['me'].profile.balance
            m_balance_last = '{0:,}'.format(m_balance_last)
            args['balance_last'] = f"{m_balance_last} {gettext(args['main_currency'])}"

            if args['item_game_user'].ticket_list.get("lotto_ticket_info", False):
                args['game_group_type'] = "game_group_lotto"
            else:
                args['game_group_type'] = "game_group_scratch"

            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_game_pay.html")
            args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
            print ("cab_game_pay")
            #
            return render(request, args['main_tab'], args)
        except Exception as ex:
            print ("ex = ", ex)
            return redirect('/')


def cab_game_paybtn(request, verbal=None):
    print("cab_game_paybtn")
    args = get_main_args(request, section="main")
    args['menu_item'] = 'nav-link_cabinet'
    print("args['lang'] = ", args['lang'])
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.method == "POST":
            m_CheckStartGame_Bool = True
            m_CheckStartGame_day = args.get("GL_CheckStartGame_day", 0)
            m_CheckStartGame_maxamount = args.get("GL_CheckStartGame_maxamount", 0)
            m_UserSettings = args['me'].profile.settings

            print("check limit")
            if m_UserSettings.get("limit") is not None:
                m_max_sum_d = m_UserSettings["limit"].get("max_sum_d", "0")
                m_max_sum_w = m_UserSettings["limit"].get("max_sum_w", "0")
                m_max_sum_m = m_UserSettings["limit"].get("max_sum_m", "0")
                print("m_max_sum_d = ", m_max_sum_d)
                print("m_max_sum_w = ", m_max_sum_w)
                print("m_max_sum_m = ", m_max_sum_m)

                m_date_game_start_d = datetime.datetime.now() + relativedelta(hour=0, minute=0, second=0,
                                                                               microsecond=0)
                m_date_game_start_w = datetime.datetime.now() + relativedelta(weekday=SU(-1), hour=0, minute=0, second=0,
                                                                               microsecond=0)
                m_date_game_start_m = datetime.datetime.now() + relativedelta(day=1, hour=0, minute=0, second=0,
                                                                               microsecond=0)
                m_date_game_finish = datetime.datetime.now() + relativedelta(days=+1, hour=0, minute=0, second=0,
                                                                               microsecond=0)

                utc = pytz.UTC
                m_date_game_start_d = utc.localize(m_date_game_start_d)
                m_date_game_start_w = utc.localize(m_date_game_start_w)
                m_date_game_start_m = utc.localize(m_date_game_start_m)
                m_date_game_finish = utc.localize(m_date_game_finish)

                print("m_date_game_start_d = ", m_date_game_start_d )
                print("m_date_game_start_w = ", m_date_game_start_w )
                print("m_date_game_start_m = ", m_date_game_start_m )
                print("m_date_game_finish  = ", m_date_game_finish  )
                # day
                try:
                    m_max_sum_d_int = int(m_max_sum_d)
                    if m_max_sum_d_int > 0:
                        m_date_game_start = m_date_game_start_d
                        game_history_list = Game_history.objects.filter(user_id_id=args['me'].id,
                                                                        dt_start__range=[m_date_game_start,
                                                                                         m_date_game_finish]) \
                            .filter(Q(t_status__verbal='start') | Q(t_status__verbal='finish')) \
                            .exclude(t_payment__verbal="balance")
                        m_amount_check = 0
                        print("ItemGame.count = ", len(game_history_list))
                        for ItemGame in game_history_list:
                            m_amount_check += ItemGame.ticket_sum
                        print("day amount = ", m_amount_check )
                        if m_amount_check >= m_max_sum_d_int:
                            m_CheckStartGame_Bool = False
                            args['me'].profile.max_ticket_m += 1
                            answer = {"AnswerCod": "00",
                                      "AnswerText": gettext(
                                          "You have exceeded the allowed day payment limit. Contact the Site Administrator.")}
                            ## עברת את הסכום המקסימלי ליום זה
                except:
                    m_max_sum_d_int = 0

                if m_CheckStartGame_Bool:
                    # week
                    try:
                        m_max_sum_w_int = int(m_max_sum_w)
                        if m_max_sum_w_int > 0:
                            m_date_game_start = m_date_game_start_w
                            game_history_list = Game_history.objects.filter(user_id_id=args['me'].id,
                                                                            dt_start__range=[m_date_game_start,
                                                                                             m_date_game_finish]) \
                                .filter(Q(t_status__verbal='start') | Q(t_status__verbal='finish')) \
                                .exclude(t_payment__verbal="balance")
                            m_amount_check = 0
                            print("ItemGame.count = ", len(game_history_list))
                            for ItemGame in game_history_list:
                                m_amount_check += ItemGame.ticket_sum
                            print("week amount = ", m_amount_check)
                            if m_amount_check >= m_max_sum_w_int:
                                m_CheckStartGame_Bool = False
                                args['me'].profile.max_ticket_m += 1
                                answer = {"AnswerCod": "00",
                                          "AnswerText": gettext(
                                              "You have exceeded the allowed week payment limit. Contact the Site Administrator.")}
                                ## עברת את הסכום המקסימלי לשבוע זה

                    except:
                        m_max_sum_w_int = 0

                if m_CheckStartGame_Bool:
                    # month
                    try:
                        m_max_sum_m_int = int(m_max_sum_m)
                        if m_max_sum_m_int > 0:
                            m_date_game_start = m_date_game_start_m
                            game_history_list = Game_history.objects.filter(user_id_id=args['me'].id,
                                                                            dt_start__range=[m_date_game_start,
                                                                                             m_date_game_finish]) \
                                .filter(Q(t_status__verbal='start') | Q(t_status__verbal='finish')) \
                                .exclude(t_payment__verbal="balance")
                            m_amount_check = 0
                            print("ItemGame.count = ", len(game_history_list))
                            for ItemGame in game_history_list:
                                m_amount_check += ItemGame.ticket_sum
                            print("month amount = ", m_amount_check)
                            if m_amount_check >= m_max_sum_m_int:
                                m_CheckStartGame_Bool = False
                                args['me'].profile.max_ticket_m += 1
                                answer = {"AnswerCod": "00",
                                          "AnswerText": gettext(
                                              "You have exceeded the allowed month payment limit. Contact the Site Administrator.")}
                                ## עברת את הסכום המקסימלי לחודש זה

                    except:
                        m_max_sum_m_int = 0

            if args['me'].profile.max_sum_m >= 0:
                if m_CheckStartGame_maxamount > 0:
                    m_date_join = args['me'].profile.date_joined + relativedelta(hour=0, minute=0, second=0,
                                                                                 microsecond=0)
                    m_date_check = datetime.datetime.now() + relativedelta(days=-m_CheckStartGame_day, hour=0, minute=0,
                                                                           second=0, microsecond=0)
                    utc = pytz.UTC
                    m_date_check = utc.localize(m_date_check)
                    m_date_game_start = args['me'].profile.date_joined
                    m_date_game_finish = datetime.datetime.now()
                    # m_date_game_finish = utc.localize(m_date_game_finish)

                    print("m_date_join        = ", m_date_join)
                    print("m_date_check       = ", m_date_check)

                    print("m_date_game_start  = ", m_date_game_start)
                    print("m_date_game_finish = ", m_date_game_finish)

                    if m_date_join >= m_date_check:
                        print("LESS")
                        print("m_CheckStartGame_Bool = False")
                        # check   m_CheckStartGame_maxamount

                        game_history_list = Game_history.objects.filter(user_id_id=args['me'].id,
                             dt_start__range=[m_date_game_start, m_date_game_finish]) \
                            .filter(Q(t_status__verbal='start') | Q(t_status__verbal='finish')) \
                            .exclude(t_payment__verbal="balance")

                        print("game_history_list.count  = ", game_history_list.count())
                        m_amount_check = 0
                        for ItemGame in game_history_list:
                            print("ItemGame = ", ItemGame.id, ItemGame.ticket_sum, ItemGame.dt_start)
                            m_amount_check += ItemGame.ticket_sum

                        print("m_amount_check = ", m_amount_check)
                        if m_amount_check >= m_CheckStartGame_maxamount:
                            m_CheckStartGame_Bool = False
                            args['me'].profile.max_ticket_m += 1
                            answer = {"AnswerCod": "00",
                                      "AnswerText": gettext("You have exceeded the allowed payment limit. Contact the Site Administrator.")}
                    else:
                        print("MORE")
                        print("m_CheckStartGame_Bool = True")

            if m_CheckStartGame_Bool:
                answer = {"AnswerCod": "00",
                          "AnswerText": gettext("The game is not available. Try later.")}
                m_pay_ticket_type = request.POST.get('pay_ticket_type', "")
                m_pay_ticket_col = request.POST.get('pay_ticket_col', "")
                m_pay_method = request.POST.get('pay_method', "")
                m_pay_game_id = request.POST.get('pay_game_id', "")
                m_pay_ads = request.POST.get('pay_ads', "0")
                if m_pay_ads == "1":
                    args['me'].profile.reklama = True
                    args['me'].profile.save()
                try:
                    t_type_payment = Type_payment.objects.get(verbal=m_pay_method)
                except:
                    return redirect('/')

                if t_type_payment.popup :
                    answer = {}
                    answer["AnswerCod"] = "01"
                    answer["AnswerText"] = ""
                    answer["AnswerHref"] = f"{t_type_payment.link_redirect}"
                else:
                    from el_t01_app.service.def_start_game import StartGame
                    args['me']
                    print ("********************")
                    print ("m_pay_ticket_type = ", m_pay_ticket_type)
                    print ("m_pay_ticket_col  = ", m_pay_ticket_col)
                    print ("m_pay_method      = ", m_pay_method)
                    print ("m_pay_game_id     = ", m_pay_game_id)

                    ItemGame = StartGame(args['me'], m_pay_ticket_type, m_pay_ticket_col, m_pay_method, m_pay_game_id, args['discount_user'])
                    print ("10")
                    answer = ItemGame.run_job()

            print("answer = ", answer)
            return JsonResponse(answer)
        else:
            return redirect('/')


def cab_game_play(request, verbal=None):
    print("cab_game_play")
    print("verbal = ", verbal)
    args = get_main_args(request, section="main")
    args['menu_item'] = 'nav-link_cabinet'
    print("cab_game_play user = ", args['me'].id)
    try:
        args['item_game_user'] = Game_history.objects.get(id=verbal)
        b_gift = args['item_game_user'].ticket_list.get('gift', False)
    except:
        b_gift = False
        # return redirect('/')
    print("cab_game_play user = ", args['me'].id, args['item_game_user'].user_id_id, args['logged_in'], b_gift)
    if not args['logged_in'] and not b_gift:
        return redirect('/')
    else:
        if args['item_game_user'].user_id_id != args['me'].id and not b_gift:
            return redirect('/')
        if b_gift:
            args['gift'] = True

        try:
            args['sms_gift'] = GiftSmsToSend.objects.get(t_game=verbal)
        except:
            args['sms_gift'] = {}

        (args['game_play_list'], args['game_all_finish'], args['game_play_dict'], args["game_refresh"]) = \
            create_game_play_list(
                l_game_id=args['item_game_user'].id,
                l_mark=-1,
                l_lang=args['lang']
                )

        args['all_quantity'] = args['item_game_user'].ticket_num
        args['all_sum'] = args['item_game_user'].ticket_sum

        args['ticket_id_00'] = args['game_play_list'][0]['id']
        args['ticket_status_00'] = args['game_play_list'][0]['status']
        args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_game_play.html")

        if b_gift and not args['GL_GIFT_SYSTEM_need_registration']:
            args['l_body_list_add'] = f"{args['GL_MainSkin']}/cabinet/cab_game_play_gift_01.html"
        else:
            args['l_body_list_add'] = f"{args['GL_MainSkin']}/cabinet/cab_game_play_general.html"

        args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
        return render(request, args['main_tab'], args)


def cab_game_play_info(request):
    print("cab_game_play_info")
    args = get_main_args(request, section="main")
    answer = {"AnswerCod": "00",
              "AnswerText": gettext("error")}
    print("answer = ", answer)

    if request.method == "POST":
        try:
            print("request.POST = ", request.POST)
            m_game_id = request.POST.get('game_id', 0)
            print("m_game_id = ", m_game_id)
            t_game_user = Game_history.objects.get(id=m_game_id)

            b_gift = t_game_user.ticket_list.get('gift', False)
            if not args['logged_in'] and not b_gift:
                return JsonResponse(answer)

            if t_game_user.user_id_id != args['me'].id and not b_gift:
                return JsonResponse(answer)

            (m_ticket_info, m_game_all_finish, m_ticket_dict, m_game_refresh) = \
                create_game_play_list(
                    l_game_id=t_game_user.id,
                    l_mark=-1,
                    l_lang=args['lang']
                )
            print(" m_ticket_info, m_game_all_finish = ", m_ticket_info, m_game_all_finish)
            # args["pic_result"] = "http://45.80.70.249:50777/media/ticket/tic/01/bursa-result.png"
            # args["pic_canvas"] = "http://45.80.70.249:50777/media/ticket/tic/01/bursa-scratch.png"
            m_total_win = 0
            print('START WIN SUM', m_total_win)
            t_game_tickets = Ticket_history.objects.filter(games_id_id=m_game_id).values_list('answ_win_sum')
            for ticket_win_sum in t_game_tickets:
                print('In for statement', m_total_win)
                if str(ticket_win_sum[0]).isdigit():
                    m_total_win += int(ticket_win_sum[0])
                else:
                    m_total_win += 0
            answer = {"AnswerCod": "01",
                      "TicketInfo": m_ticket_info,
                      "GameFinish": m_game_all_finish,
                      "TicketDict": m_ticket_dict,
                      "NextTimeout": 0 if m_game_refresh else 2000,
                      "WinSum": m_total_win,
                      }
        except:
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("error")}
    return JsonResponse(answer)


def cab_game_play_ticket_info(request):
    print("cab_game_play_ticket_info")
    args = get_main_args(request, section="main")
    answer = {"AnswerCod": "00",
              "AnswerText": gettext("An error occured, please try again later."),
              "s_canvas": "00",
              "s_box_html": "",
              }
    if request.method == "POST":
        try:
            print("request.POST = ", request.POST)
            m_tickets_id = request.POST.get('ticket_id', 0)
            print ("m_tickets_id = ", m_tickets_id)
            b_gift = Ticket_history.objects.get(id=m_tickets_id).games_id.ticket_list.get('gift', False)
            if not args['logged_in'] and not b_gift:
                return JsonResponse(answer)
            answer = get_game_play_ticket_info(request, m_tickets_id)
            # print ("answer = ", answer)
        except Exception as ex:
            print ("ex = ", ex)
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("An error occured, please try again later."),
                      "s_canvas": "00",
                      "s_box_html": "",
                      }
    return JsonResponse(answer)


def cab_game_play_ticket_send_status(request):
    print("cab_game_play_ticket_send_status")
    args = get_main_args(request, section="main")
    answer = {"AnswerCod": "00",
              "AnswerText": gettext("An error occured, please try again later."),
              }
    print("answer = ", answer)
    if request.method == "POST":
        try:
            print("request.POST = ", request.POST)
            m_ticket_id = request.POST.get('ticket_id', 0)
            print ("m_ticket_id = ", m_ticket_id)
            t_ticket = Ticket_history.objects.get(id=m_ticket_id)


            b_gift = t_ticket.games_id.ticket_list.get('gift', False)
            if not args['logged_in'] and not b_gift:
                return JsonResponse(answer)

            if t_ticket.games_id.user_id_id != args['me'].id and not b_gift:
                return JsonResponse(answer)

            m_game_id = t_ticket.games_id_id
            t_ticket.status = "33"
            t_ticket.save()
            print ("b_gift = ", b_gift)
            print ("args['GL_GIFT_SYSTEM_need_registration'] = ", args['GL_GIFT_SYSTEM_need_registration'])

            balance_recalculate(t_ticket.games_id.user_id_id, t_ticket.id)

            # if not b_gift:
            #     balance_recalculate(t_ticket.games_id.user_id_id, t_ticket.id)
            # if b_gift and args['GL_GIFT_SYSTEM_need_registration'] == True:
            #     balance_recalculate(t_ticket.games_id.user_recipient_id, t_ticket.id)
            #
            t_ticket_all = Ticket_history.objects.filter(games_id_id=m_game_id)
            m_all_finish = True
            for ItemTicket in t_ticket_all:
                if ItemTicket.status != "33":
                    m_all_finish = False

            answer = {"AnswerCod": "01",
                      "AnswerText": "",
                      "game_finish": m_all_finish
                      }
            # print ("answer = ", answer)
        except Exception as ex:
            print ("ex = ", ex)
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("An error occured, please try again later."),
                      }
    return JsonResponse(answer)




def cab_game_ticket_del(request, game_id=None, ticket_id=None):
    # cab-game-ticket-del/<int:game_id>/<int:ticket_id>/
    print ("cab_game_ticket_del")
    print ("game_id   = ", game_id)
    print ("ticket_id = ", ticket_id)
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')

    t_game_user = Game_history.objects.get(id=game_id)
    if t_game_user.user_id_id != args['me'].id:
        print("redirect 2")
        return redirect('/')

    m_order_list = t_game_user.ticket_list["list_order"]
    print("m_order_list = ", m_order_list )
    print("m_order_list = ", len(m_order_list) )
    if len(m_order_list):
        t_game_user.t_status_id = args['dict_game_status']["delete"]
        t_game_user.dt_stop = timezone.now()
        t_game_user.save()
        return redirect("/cabinet/")


    #ToDo проверить пользователя
    #ToDo проверить статус игры
    return redirect(f"/cab-game-item/{game_id}/")


    # return redirect("cab_game_order(request, verbal=None)")

def cab_cartpage(request):
    print ("==cartpage==")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        print ("args['lang'] = ", args['lang'])

        game_history_list = Ticket_history.objects.filter(games_id__user_id__id=args['me'].id).order_by("-req_dt")
        args['game_history_list'] = game_history_list

        # args['menu_item'] = 'nav-link_history'
        args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_cartpage.html")
        args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
        return render(request, args['main_tab'], args)


def cab_profile_save(request):
    print ("= cab_profile_save =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.POST:
            print ("POST = ", request.POST)
            try:
                m_user_id = args['me'].id
                m_created = datetime.datetime.now()

                m_name = request.POST.get('f_u_name', "")
                m_phone = request.POST.get('f_u_phone', "")
                m_u_id = request.POST.get('f_u_id', "")

                if m_name == "":
                    pass
                else:
                    args['me'].profile.name = m_name
                if m_phone == "":
                    pass
                else:
                    args['me'].profile.mobile = m_phone
                if m_u_id == "":
                    pass
                else:
                    if len(m_u_id) ==9:
                        args['me'].profile.i_doc = m_u_id
                    else:
                        pass
                args['me'].profile.save()
                return redirect('/profile-ok')
            except Exception as ex:
                return redirect('/profile-err')
        else:
            return redirect('/')

def cab_pasw_save(request):
    print ("= cab_pasw_save =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.POST:
            print ("POST = ", request.POST)
            try:
                m_passw = request.POST.get('f_u_password1', "")
                if m_passw != "":
                    if len(m_passw) >= 6:
                        args['me'].set_password(m_passw)
                        args['me'].save()
                else:
                    pass
                args['me'].profile.save()
                return redirect('/cabpass-ok')
            except Exception as ex:
                return redirect('/cabpass-err')
        else:
            return redirect('/')


def cab_cashadd_save(request):
    print ("= cab_cashadd_save =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.POST:
            print ("POST = ", request.POST)
            try:
                m_user_id = args['me'].id
                m_created = datetime.datetime.now()
                m_status = "00"
                m_cashadd_city = request.POST.get('f_cashadd_city', "")
                m_cashadd_street = request.POST.get('f_cashadd_street', "")
                m_cashadd_building = request.POST.get('f_cashadd_building', "")
                m_cashadd_amount = request.POST.get('f_cashadd_amount', 0)
                try:
                    m_amount = int(m_cashadd_amount)
                except Exception as ex:
                    m_amount = 0

                if args['GL_CashAdd_min'] <= m_amount <= args['GL_CashAdd_max']:
                    m_pay_operation_id = make_pay_operation(l_user_id=m_user_id,
                                                            l_sum=m_amount,
                                                            l_game_id=None,
                                                            l_status_verbal="01",
                                                            l_type_verbal="cashadd")
                    t_Cashadd = Cashadd()
                    t_Cashadd.user_id_id = m_user_id
                    t_Cashadd.created = m_created
                    t_Cashadd.status = m_status
                    t_Cashadd.bal_oper_id = m_pay_operation_id
                    t_Cashadd.city = m_cashadd_city
                    t_Cashadd.street = m_cashadd_street
                    t_Cashadd.building = m_cashadd_building
                    t_Cashadd.amount = m_cashadd_amount
                    t_Cashadd.save()
                    return redirect('/cashadd-ok')
                else:
                    return redirect('/cashadd-err-sum')

            except Exception as ex:
                return redirect('/cashadd-err')
        else:
            return redirect('/')


def cab_cashadd_ok(request, verbal=None):
    print ("= cab_cashadd_ok =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        # ToDo check ADMIN
        if True:
            pass
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                print ("POST = ", request.POST)
                try:
                    m_user_id = args['me'].id
                    m_pay_out_id = request.POST.get('f_pay_out_id', "")
                    t_payout = Payout.objects.get(id=m_pay_out_id)
                    t_payout.status = "01"
                    t_payout.t_check = True
                    t_payout.t_check_user_id = m_user_id
                    t_payout.t_check_dt = timezone.now()
                    t_payout.save()

                    m_type_balanceoperation_status_id = Type_balanceoperation_status.objects.get(verbal="04").id
                    pay_operation = BalanceOperation.objects.get(id=t_payout.bal_oper_id)
                    pay_operation.status_id = m_type_balanceoperation_status_id
                    pay_operation.save()
                    answer = {"AnswerCod": "00"}
                except:
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cab_payout_block(request, verbal=None):
    print ("= cab_payout_block =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        # ToDo check ADMIN
        if True:
            pass
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            # if request.POST:
            #     print ("POST = ", request.POST)
            #     try:
            #         m_user_id = args['me'].id
            #         m_pay_out_id = request.POST.get('f_pay_out_id', "")
            #         t_payout = Payout.objects.get(id=m_pay_out_id)
            #         t_payout.status = "01"
            #         t_payout.t_check = True
            #         t_payout.t_check_user_id = m_user_id
            #         t_payout.t_check_dt = timezone.now()
            #         t_payout.save()
            #
            #         m_type_balanceoperation_status_id = Type_balanceoperation_status.objects.get(verbal="04").id
            #         pay_operation = BalanceOperation.objects.get(id=t_payout.bal_oper_id)
            #         pay_operation.status_id = m_type_balanceoperation_status_id
            #         pay_operation.save()
            #         answer = {"AnswerCod": "00"}
            #     except:
            #         answer = {"AnswerCod": "00",
            #                   "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)

###################
@csrf_exempt
def cab_game_play_ticket_send_status_test(request):
    print("cab_game_play_ticket_send_status_test")
    args = get_main_args(request, section="main")
    answer = {"AnswerCod": "00",
              "AnswerText": gettext("An error occured, please try again later."),
              }
    print("answer = ", answer)
    if request.method == "POST":
        try:
            print("request.POST = ", request.POST)
            m_ticket_id = request.POST.get('ticket_id', 0)
            print ("m_ticket_id = ", m_ticket_id)
            t_ticket = Ticket_history.objects.get(id=m_ticket_id)
            m_game_id = t_ticket.games_id_id
            t_ticket.status = "33"
            t_ticket.save()
            #
            balance_recalculate(t_ticket.games_id.user_id_id, t_ticket.id)
            #
            t_ticket_all = Ticket_history.objects.filter(games_id_id=m_game_id)
            m_all_finish = True
            for ItemTicket in t_ticket_all:
                if ItemTicket.status != "33":
                    m_all_finish = False

            answer = {"AnswerCod": "01",
                      "AnswerText": "",
                      "game_finish": m_all_finish,
                      }
            print ("answer = ", answer)
        except Exception as ex:
            print ("ex = ", ex)
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("An error occured, please try again later."),
                      }
    return JsonResponse(answer)
