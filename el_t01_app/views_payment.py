# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import logging.config
import decimal
from datetime import datetime

from django.contrib import auth
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction as db_transaction
from django.contrib.auth.models import User

from .service.dft import (get_GlobalSettings)
from .service.service import get_main_args, send_sms_01
from .models import (Profile,
                     Game_history,
                     BalanceOperation,
                     Type_balanceoperation_status,
                     Type_blacklist,
                     Type_payment,
                     Blacklist,
                     IdConfirmation,
                     IdConfirmationStatus)
from .views_cab import start_game, make_pay_operation
from .bot_mess.message_send import message_send


def check_blacklist(m_tranzila_ccno):
    # проверяем карточку в списке запрещенных карточек - m_blacklist_checklist
    m_type = 'credit_card'
    m_type_id = Type_blacklist.objects.get(verbal=m_type).id
    m_check = not Blacklist.objects.filter(type_blacklist_id=m_type_id, enabled=True, text=m_tranzila_ccno).exists()
    if m_check:
        m_url_redirect = ''
    else:
        m_url_redirect = '/game-payment-fail/'
    return {"checking": m_check, "url_redirect": m_url_redirect}


def check_iddoc_confirmed(m_user_id, m_bal_oper):
    try:
        m_check = Profile.objects.get(user_id=m_user_id).i_confirmed
    except:
        m_check = False
    if m_check:
        m_url_redirect = ''
    else:
        if not IdConfirmation.objects.filter(user_id=m_user_id).exists():
            t_idconf = IdConfirmation()
            t_idconf.status_id = IdConfirmationStatus.objects.get(verbal='wait').id
            t_idconf.user_id = m_user_id
            t_idconf.dt_add = datetime.now()
            t_idconf.add_param["bal_oper"] = m_bal_oper
            t_idconf.save()
            try:
                bal_oper = BalanceOperation.objects.get(id=m_bal_oper)
                user_profile = bal_oper.user_id.profile
                game = bal_oper.games_id
                d_globalset = get_GlobalSettings()
                # data_for_bot_sms = {
                #     "company": d_globalset.get("GL_Name_Company", ""),
                #     "client_name": user_profile.name,
                #     "client_email": User.objects.get(id=m_user_id).email,
                #     "client_phone": user_profile.mobile,
                #     "client_id_doc": user_profile.i_doc,
                #     "id_conf_add": t_idconf.dt_add,
                #     "date_paid": bal_oper.confirm,
                #     "ticket_type": game.ticket_list["list_order"][0]["tic_caption"],
                #     "ticket_count": game.ticket_num,
                #     "messenger": "telegram",
                #     "message_type": "id_confirmation",
                #         }
                # message_send(data_for_bot_sms)

                m_receiver_phone_code = ""
                m_receiver_phone = user_profile.mobile
                m_sender_phone_from = d_globalset.get("GL_SMS_from", "")
                m_sms_text = d_globalset.get("GL_MES_u_idconfirm_01", "")
                if m_sms_text:
                    m_sms_send, m_sms_answ = send_sms_01(m_receiver_phone_code,
                                                         m_receiver_phone,
                                                         m_sender_phone_from,
                                                         m_sms_text,
                                                         d_globalset)
                    print ("m_sms_send, m_sms_answ = ", m_sms_send, m_sms_answ)
            except Exception:
                pass

        m_url_redirect = '/game-check-id/'
    return {"checking": m_check, "url_redirect": m_url_redirect}


# def check_username():
#     return {"checking": True, "url_redirect": ""}

def check_start_game(m_tranzila_ccno, m_user_id, m_bal_oper):
    m_return = {"checking": True}
    d_globalset = get_GlobalSettings()
    m_check_blacklist = d_globalset.get("GL_Payment_check_blacklist", False)
    m_check_id = d_globalset.get("GL_Payment_check_id", False)
    if m_check_blacklist:
        m_return = check_blacklist(m_tranzila_ccno)

    if m_return["checking"] and m_check_id:
        m_return = check_iddoc_confirmed(m_user_id, m_bal_oper)
    # if m_return["checking"]:
    #     m_return = check_username()

    return m_return


def cab_game_payment(request, verbal=None):
    print("***** cab_game_payment *****")
    print("verbal = ", verbal)
    args = get_main_args(request, section="main")
    args['menu_item'] = 'nav-link_cabinet'
    if not args['logged_in']:
        return redirect('/')
    else:
        args['item_game_user'] = Game_history.objects.get(id=verbal)
        m_pay_type = args['item_game_user'].t_payment.verbal
        m_pay_sum = args['item_game_user'].ticket_sum

        print ("*******************  m_pay_sum ==", m_pay_sum)
        m_pay_sum_str = str(m_pay_sum).replace(",", ".")
        print("*******************  m_pay_sum_str ==", m_pay_sum_str)
        # m_pay_sum = decimal.Decimal(m_pay_sum_str)
        m_pay_sum = m_pay_sum_str
        print("*******************  m_pay_sum ==", m_pay_sum)

        args['l_header_list'] = []
        args['l_footer_list'] = []
        args['l_modal_list'] = []
        args['PAGE_TITLE'] = 'Tranzila'
        args['l_layout_file'] = f"{args['GL_MainSkin']}/payment/layout.html"
        print ("l_layout_file = ", args['l_layout_file'])

        args['l_body_list'].append(f"{args['GL_MainSkin']}/payment/frame_tranzila.html")
        args['main_tab'] = f"{args['GL_MainSkin']}/payment/main_tab.html"
        if args['item_game_user'].t_status.verbal != "add_to_cart":
            return redirect("/")
        else:
            print ("m_pay_type = ", m_pay_type)
            m_current_site_for_send = str(get_current_site(request))
            print("m_current_site_for_send = ", m_current_site_for_send)
            if m_pay_type == "balance":
                if args['me'].profile.balance >= args['item_game_user'].ticket_sum:
                    args['item_game_user'].t_status_id = args['dict_game_status']["wait_payment"]
                    args['item_game_user'].save()
                    m_pay_operation_id = make_pay_operation(l_user_id=args['me'].id,
                                                            l_sum=m_pay_sum,
                                                            l_game_id=args['item_game_user'].id,
                                                            l_status_verbal="04",
                                                            l_type_verbal="pay_from_balans")
                    # args['me'].profile.balance = args['me'].profile.balance - args['item_game_user'].ticket_sum
                    # args['me'].profile.save()
                    return start_game(request, l_game_id=args['item_game_user'].id)
                else:
                    return redirect("/")
            # elif m_pay_type == "credit_card_token":
            #     args['item_game_user'].t_status_id = args['dict_game_status']["wait_payment"]
            #     args['item_game_user'].save()
            #     m_pay_operation_id = make_pay_operation(l_user_id=args['me'].id,
            #                                             l_sum=m_pay_sum,
            #                                             l_game_id=args['item_game_user'].id,
            #                                             l_status_verbal="01",
            #                                             l_type_verbal="credit_card_token")
            #
            #
            elif m_pay_type == "bit":
                print ("BIT BIT BIT" )
                args['item_game_user'].t_status_id = args['dict_game_status']["wait_payment"]
                args['item_game_user'].save()
                m_pay_operation_id = make_pay_operation(l_user_id=args['me'].id,
                                                        l_sum=m_pay_sum,
                                                        l_game_id=args['item_game_user'].id,
                                                        l_status_verbal="01",
                                                        l_type_verbal="bit")
                args['m_order_id'] = m_pay_operation_id
                # prapere tranzila
                if args['lang'] == "ru" or args['lang'] == "ua":
                    args['m_lang'] = "ru"
                elif args['lang'] == "en":
                    args['m_lang'] = "us"
                else:
                    args['m_lang'] = "il"
                m_scheme = request.scheme
                m_domain_name = get_current_site(request).name

                args['m_url'] = args['globalset'].get("UrlTranzilaTerminalBit", "")
                args['get_param'] = f"?"
                args['get_param'] += f"lang={args['m_lang']}"
                args['get_param'] += f"&sum={m_pay_sum}"
                args['get_param'] += f"&currency=1"
                args['get_param'] += f"&&cc_pay=0"
                args['get_param'] += f"&hide_cc=1"
                args['get_param'] += f"&bit_pay=1"
                args['get_param'] += f"&email={args['me'].email}"
                args['get_param'] += f"&u71=1"
                args['get_param'] += f"&order_id={args['m_order_id']}"
                args['get_param'] += f"&DCdisable={args['m_order_id']}"
                args['get_param'] += f"&success_url_address={m_scheme}://{m_domain_name}/trz-done/{m_pay_operation_id}/"
                args['get_param'] += f"&fail_url_address={m_scheme}://{m_domain_name}/trz-fail/{m_pay_operation_id}/"
                args['get_param'] += f"&notify_url_address={m_scheme}://{m_domain_name}/trz-notify/{m_pay_operation_id}/"

            elif m_pay_type == "applepay":
                args['item_game_user'].t_status_id = args['dict_game_status']["wait_payment"]
                args['item_game_user'].save()
                m_pay_operation_id = make_pay_operation(l_user_id=args['me'].id,
                                                        l_sum=m_pay_sum,
                                                        l_game_id=args['item_game_user'].id,
                                                        l_status_verbal="01",
                                                        l_type_verbal="applepay")
                args['m_order_id'] = m_pay_operation_id
                m_scheme = request.scheme
                m_domain_name = get_current_site(request).name
                try:
                    # m_cc_type = "iframenew"  # direct iframenew
                    # m_cc_type = "direct"  # direct iframenew
                    m_cc_type = args.get('GL_Tranzila_AplePay_type', "iframenew")
                    print ("m_cc_type = ", m_cc_type)

                    if m_cc_type == "iframenew":
                        args['l_body_list'] = []
                        args['l_body_list'].append(f"{args['GL_MainSkin']}/payment/frame_tranzila_applepay.html")
                        args['l_script_list'] = []
                        args['l_script_list'].append(f"{args['GL_MainSkin']}/payment/l_script_01.html")
                        args['l_head_list'] = []
                        args['l_head_list'].append(f"{args['GL_MainSkin']}/payment/l_head_01.html")
                        #
                        if args['lang'] == "ru" or args['lang'] == "ua":
                            args['m_lang'] = "ru"
                        elif args['lang'] == "en":
                            args['m_lang'] = "us"
                        else:
                            args['m_lang'] = "il"
                        #
                        args['m_url'] = args.get("GL_UrlTranzilaTerminalAplePay", "")
                        #
                        args['m_pay_operation_id'] = m_pay_operation_id
                        args['m_sum'] = m_pay_sum
                        args['m_currency'] = 1
                        args['m_cred_type'] = 1
                        args['m_apple_pay'] = 1
                        args['m_hide_cc'] = 1
                        args['m_u71'] = 1
                        args['m_success_url_address'] = f"{m_scheme}://{m_domain_name}/trz-done/{m_pay_operation_id}/"
                        args['m_fail_url_address'] = f"{m_scheme}://{m_domain_name}/trz-fail/{m_pay_operation_id}/"
                        args['m_notify_url_address'] = f"{m_scheme}://{m_domain_name}/trz-notify/{m_pay_operation_id}/"
                        args['m_supplier'] = args.get("GL_TranzilaSupplier", "")
                        #
                        args['get_param'] = f"?"
                        args['get_param'] += f"lang={args['m_lang']}"
                        args['get_param'] += f"&sum={args['m_sum']}"
                        args['get_param'] += f"&currency={args['m_currency']}"
                        args['get_param'] += f"&cred_type={args['m_cred_type']}"
                        args['get_param'] += f"&apple_pay={args['m_apple_pay']}"
                        args['get_param'] += f"&hide_cc={args['m_hide_cc']}"
                        if args['m_supplier'] != "":
                            args['get_param'] += f"&supplier={args['m_supplier']}"
                        args['get_param'] += f"&email={args['me'].email}"
                        args['get_param'] += f"&u71={args['m_u71']}"
                        args['get_param'] += f"&order_id={args['m_order_id']}"
                        args['get_param'] += f"&DCdisable={args['m_order_id']}"
                        args['get_param'] += f"&success_url_address={m_scheme}://{m_domain_name}/trz-done/{m_pay_operation_id}/"
                        args['get_param'] += f"&fail_url_address={m_scheme}://{m_domain_name}/trz-fail/{m_pay_operation_id}/"
                        args['get_param'] += f"&notify_url_address={m_scheme}://{m_domain_name}/trz-notify/{m_pay_operation_id}/"
                        #
                        print ("************************")
                        print ("get_param = ", args['get_param'])
                        print ("************************")
                        #
                    else:
                        args['m_url'] = args.get("GL_UrlTranzilaTerminalAplePay", "")
                        args['m_sum'] = m_pay_sum
                        args['m_currency'] = 1
                        args['m_company'] = "WinWin"
                        if args['lang'] == "ru" or args['lang'] == "ua":
                            args['m_lang'] = "ru"
                        elif args['lang'] == "en":
                            args['m_lang'] = "us"
                        else:
                            args['m_lang'] = "il"
                        print("args['m_lang'] = ", args['m_lang'])

                        m_current_site_for_send = str(get_current_site(request))
                        print("m_current_site_for_send = ", m_current_site_for_send)
                        args['m_myid'] = f"{args['me'].profile.i_doc}"
                        args['m_email'] = f"{args['me'].email}"
                        args['m_success_url_address'] = f"{m_scheme}://{m_domain_name}/trz-done/{m_pay_operation_id}/"
                        args['m_fail_url_address'] = f"{m_scheme}://{m_domain_name}/trz-fail/{m_pay_operation_id}/"
                        return render(request, f"{args['GL_MainSkin']}/payment/direct_tranzila_post_aplepay.html", args)

                except Exception as ex:
                    print(f"ex = {ex}")

            elif m_pay_type == "credit_card_iframe_id":
                args['item_game_user'].t_status_id = args['dict_game_status']["wait_payment"]
                args['item_game_user'].save()
                m_pay_operation_id = make_pay_operation(l_user_id=args['me'].id,
                                                        l_sum=m_pay_sum,
                                                        l_game_id=args['item_game_user'].id,
                                                        l_status_verbal="01",
                                                        l_type_verbal="credit_card")
                # prapere tranzila
                m_scheme = request.scheme
                m_domain_name = get_current_site(request).name
                if True:
                    args['m_url'] = args.get("GL_UrlTranzilaTerminalCCIFrame", "")
                    # args['m_url'] = "https://direct.tranzila.com/shmulik3355ch/iframenew.php"
                    # args['get_param'] = f"?sum={m_pay_sum}&currency=1&cc_pay=0&hide_cc=1&bit_pay=1&order_id={pay_operation.id}"
                    args['get_param'] = f"?sum={m_pay_sum}&currency=1&cred_type=1&bit_pay=0&myid={args['me'].profile.i_doc}"
                    args['get_param'] += f"&success_url_address={m_scheme}://{m_domain_name}/trz-done/{m_pay_operation_id}/"
                    args['get_param'] += f"&fail_url_address={m_scheme}://{m_domain_name}/trz-fail/{m_pay_operation_id}/"

            elif m_pay_type == "credit_card":
                args['item_game_user'].t_status_id = args['dict_game_status']["wait_payment"]
                args['item_game_user'].save()
                m_pay_operation_id = make_pay_operation(l_user_id=args['me'].id,
                                                        l_sum=m_pay_sum,
                                                        l_game_id=args['item_game_user'].id,
                                                        l_status_verbal="01",
                                                        l_type_verbal="credit_card")
                m_scheme = request.scheme
                m_domain_name = get_current_site(request).name
                d_globalset = get_GlobalSettings()
                # m_cc_type = "direct" # direct iframenew galushka

                m_cc_type = d_globalset.get("GL_Tranzila_CreditCard_type", "")

                if m_cc_type == "galushka":
                    return redirect(f'/trz-done/{m_pay_operation_id}/')

                if m_cc_type == "direct":
                    if args['lang'] == "ru" or args['lang'] == "ua":
                        args['m_lang'] = "ru"
                    elif args['lang'] == "en":
                        args['m_lang'] = "us"
                    else:
                        args['m_lang'] = "il"
                    args['m_url'] = args.get("GL_UrlTranzilaTerminalDirect", "")
                    args['m_sum'] = m_pay_sum
                    args['m_currency'] = 1
                    args['m_company'] = args.get("GL_Name_Company", "")
                    args['m_order_id'] = m_pay_operation_id
                    args['m_myid'] = f"{args['me'].profile.i_doc}"
                    args['m_email'] = f"{args['me'].email}"
                    m_scheme = request.scheme
                    m_domain_name = get_current_site(request).name
                    args['m_success_url_address'] = f"{m_scheme}://{m_domain_name}/trz-done/{m_pay_operation_id}/"
                    args['m_fail_url_address'] = f"{m_scheme}://{m_domain_name}/trz-fail/{m_pay_operation_id}/"
                    args['m_notify_url_address'] = f"{m_scheme}://{m_domain_name}/trz-notify/{m_pay_operation_id}/"
                    # for check
                    # args['m_success_url_address'] = f"{m_scheme}://{m_domain_name}/222trz-done/{m_pay_operation_id}/"
                    # args['m_success_url_address'] = f"{m_scheme}://{m_domain_name}/trz-done/{m_pay_operation_id}/"
                    # args['m_fail_url_address'] = f"{m_scheme}://{m_domain_name}/trz-fail/{m_pay_operation_id}/"
                    # args['m_notify_url_address'] = f"{m_scheme}://{m_domain_name}/trz-done/{m_pay_operation_id}/"
                    # args['m_notify_url_address'] = "https://a.vucra.com/notify.php"
                    #
                    m_templ = f"{args['GL_MainSkin']}/payment/direct_tranzila_post.html"
                    return render(request, m_templ, args)
                if m_cc_type == "iframenew":
                    #
                    # https://secure5.tranzila.com/cgi-bin/tranzila71u.cgi
                    # ?supplier=shmulik3355tok
                    # &TranzilaPW=gjdukl78
                    # &TranzilaTK=x4f3b93b782fae52312
                    # &expdate=0927
                    # &myid=123456789
                    # &s=1&1=1=
                    ##
                    if False:
                        args['m_url'] = "https://direct.tranzila.com/shmulik3355/iframenew.php"
                        # args['m_url'] = "https://direct.tranzila.com/shmulik3355ch/iframenew.php"
                        # args['get_param'] = f"?sum={m_pay_sum}&currency=1&cc_pay=0&hide_cc=1&bit_pay=1&order_id={pay_operation.id}"
    #                    args['get_param'] = f"?sum={m_pay_sum}&currency=1&cc_pay=1&bit_pay=0&tranmode=VK"
    #                    args['get_param'] += f"&success_url_address={m_scheme}://{m_domain_name}/trz-done/{m_pay_operation_id}/"
    #                    args['get_param'] += f"&fail_url_address={m_scheme}://{m_domain_name}/trz-fail/{m_pay_operation_id}/"
                        args['get_param'] = f"?sum={m_pay_sum}&currency=1&cred_type=1&tranmode=AK"
                        args['get_param'] += f"&success_url_address={m_scheme}://{m_domain_name}/trz-done/{m_pay_operation_id}/"
                        args['get_param'] += f"&fail_url_address={m_scheme}://{m_domain_name}/trz-fail/{m_pay_operation_id}/"

                    ## https://direct.tranzila.com/shmulik3355/iframenew.php
                    # ?sum=5&currency=1&cred_type=1&lang=us&tranmode=AK
                    #POST =  <QueryDict: {'Response': ['000'], 'o_tranmode': ['AK'], 'expmonth': ['06'], 'myid': ['203459409'], 'currency': ['1'], 'expyear': ['26'], 'supplier': ['shmulik3355'], 'sum': ['1'], 'benid': ['0kpf14q2qkgrdv25bhg3not4h7'], 'o_cred_type': ['1'], 'lang': ['us'], 'ccard': [''], 'fail_url_address': ['http://45.80.70.249:50777/trz-fail/106/'], 'cred_type': ['1'], 'success_url_address': ['http://45.80.70.249:50777/trz-done/106/'], 'tranmode': ['AK'], 'ConfirmationCode': ['0826029'], 'cardtype': ['1'], 'cardissuer': ['1'], 'cardaquirer': ['6'], 'index': ['81586'], 'Tempref': ['82001025'], 'TranzilaTK': ['Jf799afe8cf96913633'], 'ccno': ['']}>
                    if True:
                        args['m_tranzila_pw'] = "gjdukl78"
                        args['m_supplier'] = "shmulik3355tok"

                        args['m_url'] = "https://secure5.tranzila.com/cgi-bin/tranzila71u.cgi"
                        # &sum=15¤cy=1&cred_type=1
                        # args['get_param'] = f"?sum={m_pay_sum}&currency=1&cc_pay=0&hide_cc=1&bit_pay=1&order_id={pay_operation.id}"
                        #                    args['get_param'] = f"?sum={m_pay_sum}&currency=1&cc_pay=1&bit_pay=0&tranmode=VK"
                        #                    args['get_param'] += f"&success_url_address={m_scheme}://{m_domain_name}/trz-done/{m_pay_operation_id}/"
                        #                    args['get_param'] += f"&fail_url_address={m_scheme}://{m_domain_name}/trz-fail/{m_pay_operation_id}/"
                        args['get_param'] = f"?supplier={args['m_supplier']}&TranzilaPW={args['m_tranzila_pw']}"
                        args['get_param'] += f"&TranzilaTK={args['me'].profile.tranzila_token}"
                        args['get_param'] += f"&sum={m_pay_sum}"
                        args['get_param'] += f"&success_url_address={m_scheme}://{m_domain_name}/trz-done/{m_pay_operation_id}/"
                        args['get_param'] += f"&fail_url_address={m_scheme}://{m_domain_name}/trz-fail/{m_pay_operation_id}/"

            elif m_pay_type == "pay_box":
                # args['item_game_user'].t_status_id = args['dict_game_status']["wait_payment"]
                # args['item_game_user'].save()
                # m_pay_operation_id = make_pay_operation(l_user_id=args['me'].id,
                #                                         l_sum=m_pay_sum,
                #                                         l_game_id=args['item_game_user'].id,
                #                                         l_status_verbal="01",
                #                                         l_type_verbal="credit_card")
                # # prapere tranzila
                # m_scheme = request.scheme
                # m_domain_name = get_current_site(request).name
                # if True:
                #     args['m_url'] = args.get("GL_UrlTranzilaTerminalCCIFrame", "")
                #     # args['m_url'] = "https://direct.tranzila.com/shmulik3355ch/iframenew.php"
                #     # args['get_param'] = f"?sum={m_pay_sum}&currency=1&cc_pay=0&hide_cc=1&bit_pay=1&order_id={pay_operation.id}"
                #     args['get_param'] = f"?sum={m_pay_sum}&currency=1&cred_type=1&bit_pay=0&myid={args['me'].profile.i_doc}"
                #     args['get_param'] += f"&success_url_address={m_scheme}://{m_domain_name}/trz-done/{m_pay_operation_id}/"
                #     args['get_param'] += f"&fail_url_address={m_scheme}://{m_domain_name}/trz-fail/{m_pay_operation_id}/"
                return redirect('https://payboxapp.page.link/jq9mzPGueaxxH7Rx9')

        return render(request, args['main_tab'], args)


def payment_answer(request, verbal=None, m_tranzila_type=None):
    print("\n payment_answer =", verbal)
    m_dirlog_short = '../log/payment'
    if not os.path.exists(m_dirlog_short):
        os.makedirs(m_dirlog_short)
    m_log_file = os.path.join(m_dirlog_short, 'payment.log')

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
    logging.info(f'***** Payment Answer ******')
    logging.info(f'  m_tranzila_type = {m_tranzila_type}')
    logging.info(f'  verbal = {verbal}')
    logging.info(f'  POST   = {request.POST}')

    # <QueryDict: {
    # 'Response': ['000'],
    # 'expmonth': ['05'],
    # 'currency': ['1'],
    # 'expyear': ['25'],
    # 'supplier': ['shmulik3355ch'],
    # 'pdesc': [''],
    # 'company': ['WinWin'],
    # 'sum': ['5'],
    # 'o_cred_type': [''],
    # 'lang': ['il'],
    # 'ccard': [''],
    # 'fail_url_address': ['http://45.80.70.249:50777/trz-fail/13/'],
    # 'ccno': ['8398'],
    # 'success_url_address': ['http://45.80.70.249:50777/trz-done/13/'],
    # 'g-recaptcha-response': ['03AGdBq253rx-nf-vNbPKGjxyO3cgPyHbv_na0aidt_iRAxSq6GttMCLnVHTw0cPYq4AVLSuxp2Ky9XbUglTJFtXl0sIQDvSY0aMfcZrIjK6e_2lFFyfcPyvLP-LLhEtT2vU7hK9AGPRqIYMy_wzTRTf8J91iK7wYaE-lj9Pn_O5EIrbFpRIE41PUne6_31WoH2F7qZkfS3XoPi2FYAqR8z8Avx2Lpkbz_m40lhxYNPEqGX_BSZ_xCfuaSPs-Dl5PRHiCCC9ZbL0iXP80IVV8ci58DXkSFrxSW9Ub0F5nvFVEXP47eTcWww-Qvds_ipSmJRaVZzvGr_QGT5RP8emT5CxX-Oaany2FRQh4jcvpbUjZdDTWmzzj3PLYIqNsJ2RmKoxiPwWo8eq7tJwrXc5oe5TZn7DfAfeGszDNKgiBsOimyNItfxg2wPsAt_Owqvzo9dtVHbCSuMH4lTw9ICT8e6NCNT5ngjV8lxw'],
    # 'ConfirmationCode': ['0262563'],
    # 'cardtype': ['1'],
    # 'cardissuer': ['1'],
    # 'cardaquirer': ['6'],
    # 'index': ['80024'],
    # 'Tempref': ['42001009']}>
    '''
    AplePay
    <QueryDict: {
    'processor_response_code': ['000'], 
    'transaction_id': ['98134'], 
    'auth_number': ['0060101'], 
    'card_type': ['1'], 
    'card_type_name': ['Mastercard'], 
    'amount': ['12'], 
    'currency_code': ['ILS'], 
    'expiry_month': ['03'], 
    'expiry_year': ['25'], 
    'payment_plan': ['1'], 
    'token': ['q3caa012fcd20776696'], 
    'last_4': ['6696'], 
    'card_mask': ['533753******6696'], 
    'card_locality': ['domestic'], 
    'supplier': ['shmulik3355ch'], 
    'Response': ['000'], 
    'index': ['98134'], 
    'ccno': ['533753******6696'], 
    'ConfirmationCode': ['0060101'], 
    'sum': ['12'], 
    'currency': ['1'], 
    'mycvv': [''], 
    'success_url': ['https://winwin-hishgad.co.il/trz-done/30671/'], 
    'notify_url': ['https://winwin-hishgad.co.il/trz-notify/30671/']
    }>

    CreditCard
    <QueryDict: {
    'Response': ['004'], 
    'mycvv': ['0'], 
    'apple_pay': ['0'], 
    'expmonth': ['08'], 
    'myid': ['300988763'], 
    'currency': ['1'], 
    'email': ['simab6722@gmail.com'], 
    'CAVV': ['AAABAYEFd2kzlkFZgQV3ELxAz04'], 
    'expyear': ['26'], 
    'hide_bit': ['1'], 
    'supplier': ['shmulik3355ch'], 
    'pdesc': [''], 
    'company': ['WinWin'], 
    'sum': ['60'], 
    'o_cred_type': ['1'], 
    'track2': ['0'], 
    'lang': ['il'], 
    'order_id': ['30672'], 
    'hide_apple_pay': ['0'], 
    'fail_url_address': ['https://winwin-hishgad.co.il/trz-fail/30672/'], 
    'XID': ['ODkwMTcxYmZkNTE0NGU0Zjg2MmM'], 
    'ccno': ['0828'], 
    'cred_type': ['1'], 
    'success_url_address': ['https://winwin-hishgad.co.il/trz-done/30672/'], 
    'DclickTK': [''], 
    'ECI': ['05'], 
    'notify_url_address': ['https://winwin-hishgad.co.il/trz-notify/30672/'], 
    'ConfirmationCode': ['0000000'], 
    'index': ['98136'], 
    'Responsesource': ['2'], 
    'Responsecvv': ['3'], 
    'Responseid': ['3'], 
    'Tempref': ['83001079'], 
    'DBFIsForeign': ['0'], 
    'DBFcard': ['2'], 
    'cardtype': ['2'], 
    'DBFcardtype': ['6'], 
    'cardissuer': ['6'], 
    'DBFsolek': ['6'], 
    'cardaquirer': ['6'], 
    'tz_parent': ['shmulik3355ch'], 
    'TranzilaTK': ['be48394c7e631210828']
    }>
    '''
    d_globalset = get_GlobalSettings()
    if request.method == "POST" or d_globalset.get("GL_Tranzila_CreditCard_type", "") == "galushka":
        m_ver = 2

        if m_ver == 1:
            try:
                args = get_main_args(request, section="main")
                pay_operation = BalanceOperation.objects.get(id=verbal)
                if not args['logged_in']:
                    m_user_id = pay_operation.user_id_id
                    user = User.objects.get(id=m_user_id)
                    auth.login(request, user)
                    # args = get_main_args(request, section="main")
                pay_operation.pay_response = request.POST
                m_pay_operation_status_id = Type_balanceoperation_status.objects.get(verbal="04")
                if pay_operation.status_id != m_pay_operation_status_id:
                    pay_operation.status_id = m_pay_operation_status_id
                    pay_operation.save()
                    # ToDo на игре статус СТАРТ
                    # 	start
                    return start_game(request, l_game_id=pay_operation.games_id_id)
            except:
                pass

        if m_ver == 2:
            m_check_game = {}
            m_check_game["checking"] = False
            m_check_game["url_redirect"] = '/game-check-id/'

            m_history_txt = ""
            logging.info(f'  m_ver == 2')
            # готовим коды состояний wait succes block
            m_pay_operation_status_wait = Type_balanceoperation_status.objects.get(verbal="01").id
            m_pay_operation_status_succes = Type_balanceoperation_status.objects.get(verbal="04").id
            m_pay_operation_status_block = Type_balanceoperation_status.objects.get(verbal="02")
            # достаем параметры из ответа транзилы
            m_body_post = request.POST
            m_tranzila_ccno = m_body_post.get("last_4", "----")
            m_tranzila_token = m_body_post.get("TranzilaTK", "")
            m_tranzila_response = m_body_post.get("Response","---")
            m_tranzila_response_processor = m_body_post.get("processor_response_code","---")

            if m_tranzila_response == "000" or m_tranzila_response_processor == "000":
                m_tranzila_response = "000"

            m_history_txt += f"  tranzila Response  = {m_tranzila_response}\n"
            m_history_txt += f"  tranzila ccno      = {m_tranzila_ccno}\n"
            m_history_txt += f"  tranzila token     = {m_tranzila_token}\n"

            if d_globalset.get("GL_Tranzila_CreditCard_type", "") == "galushka":
                m_tranzila_response = "000"
                m_history_txt += f"  tranzila Response = galushka = {m_tranzila_response}\n"
            # ToDo if Response == '000'  or != '000'

            # ищем операцию id=verbal
            pay_operation_list = BalanceOperation.objects.filter(id=verbal)
            m_history_txt += f"  len(pay_operation_list) = {len(pay_operation_list)}\n"
            # если есть операция
            if len(pay_operation_list) == 1:
                m_user_id = pay_operation_list[0].user_id_id
                if m_tranzila_response == "000":
                    m_check_game = check_start_game(m_tranzila_ccno, m_user_id, verbal)
                    m_history_txt += f"  check_start_game = {m_check_game}\n"
                if m_tranzila_token != "":
                    user = User.objects.get(id=m_user_id)
                    user.profile.tranzila_token = m_tranzila_token
                    user.profile.save()

                # если код платежа не 000 - не успешно
                # если код платежа = 000 успешно
                # пробуем заблокировать запись id=verbal
                # если заблокировали -> проверяем статус если "01" = wait -> стартуем игру
                db_transaction.set_autocommit(False)
                for ItemOperation in range(10):
                    m_history_txt += f"  ItemOperation = {ItemOperation}\n"
                    pay_operation_list_block = BalanceOperation.objects.select_for_update(skip_locked=True).filter(id=verbal)
                    if len(pay_operation_list_block) == 0:
                        time.sleep(1)
                        m_history_txt += f"  wait block = {ItemOperation}\n"
                    else:
                        pay_operation_block = pay_operation_list_block[0]
                        m_history_txt += f"  pay_operation = {pay_operation_block}\n"
                        m_user_id = pay_operation_block.user_id_id
                        m_history_txt += f"  user_id = {m_user_id}\n"
                        m_add_history = f'{timezone.now()}, tranzila Response={m_tranzila_response}, tranzila_type={m_tranzila_type}'
                        pay_operation_block.pay_response = \
                            "" if pay_operation_block.pay_response is None else pay_operation_block.pay_response \
                            + f'{timezone.now()} tranzila_type={m_tranzila_type}\n{request.POST} \n'
                        # если статус операции - ожидание оплаты
                        if pay_operation_block.status_id == m_pay_operation_status_wait:
                            pay_operation_block.confirm = timezone.now()
                            if m_check_game["checking"] == True:
                                pay_operation_block.status_id = m_pay_operation_status_succes
                                pay_operation_block.description = \
                                    "" if pay_operation_block.description is None else pay_operation_block.description \
                                    + f'{m_add_history} - START GAME \n'
                            else:
                                pay_operation_block.status_id = m_pay_operation_status_block
                                pay_operation_block.description = \
                                    "" if pay_operation_block.description is None else pay_operation_block.description \
                                                                                       + f'{m_add_history} - CC in BLACKLIST \n'

                            '''
                            BalanceOperation
                            type_balanceoperation = models.ForeignKey(Type_balanceoperation, null=True, blank=True,
                            
                            t_payment = models.ForeignKey(Type_payment, null=True, blank=True, on_delete=models.CASCADE,
                            '''
                            m_baloperation_verbal = pay_operation_block.type_balanceoperation.verbal
                            m_baloperation_verbal_payment = pay_operation_block.type_balanceoperation.verbal_payment
                            m_payment_verbal = pay_operation_block.games_id.t_payment.verbal
                            m_history_txt += f"  m_baloperation_verbal         = {m_baloperation_verbal}\n"
                            m_history_txt += f"  m_baloperation_verbal_payment = {m_baloperation_verbal_payment}\n"
                            m_history_txt += f"  m_payment_verbal              = {m_payment_verbal}\n"

                            # if m_payment_verbal != m_baloperation_verbal_payment:
                            if True:
                                m_history_txt += f"  verbal != verbal \n"
                                try:
                                    m_history_txt += f"  verbal old = {pay_operation_block.games_id.t_payment_id}\n"
                                    m_baloperation_verbal_payment_id = Type_payment.objects.get(verbal=m_baloperation_verbal_payment).id
                                    pay_operation_block.games_id.t_payment_id = m_baloperation_verbal_payment_id
                                    m_history_txt += f"  verbal new = {m_baloperation_verbal_payment_id}\n"
                                except:
                                    m_history_txt += f"  not find new payment type\n"

                            pay_operation_block.games_id.history = m_history_txt
                            pay_operation_block.games_id.save()

                            pay_operation_block.save()
                            db_transaction.commit()
                            db_transaction.set_autocommit(True)

                            if m_check_game["checking"] != True:
                                # return redirect(f'{m_check_game["url_redirect"]}{pay_operation_block.games_id_id}/')
                                return redirect(f'{m_check_game["url_redirect"]}')
                            else:
                                logging.info(f'  {ItemOperation} ***** ===== start_game ===== *****')
                                logging.info(f'  {ItemOperation} ***** ===== stop work payment ===== *****')

                                args = get_main_args(request, section="main")
                                if not args['logged_in']:
                                    user = User.objects.get(id=m_user_id)
                                    auth.login(request, user)
                                if m_tranzila_response == '000':
                                    return start_game(request, l_game_id=pay_operation_block.games_id_id)
                        elif pay_operation_block.status_id == m_pay_operation_status_block:
                            return redirect('/game-check-id/')
                        else:
                            # time.sleep(5)
                            logging.info(f'  {ItemOperation} ***** ===== payment already received - go to play ===== *****')
                            logging.info(f'  redirect -> cab-game-play')
                            pay_operation_block.description = \
                                "" if pay_operation_block.description is None else pay_operation_block.description \
                                + f'{m_add_history} - SKIP \n'
                            pay_operation_block.save()
                            db_transaction.commit()
                            db_transaction.set_autocommit(True)
                            if m_check_game["checking"] != True:
                                # return redirect(f'{m_check_game["url_redirect"]}{pay_operation_block.games_id_id}/')
                                return redirect(f'{m_check_game["url_redirect"]}')
                            else:
                                return redirect(f"/cab-game-play/{pay_operation_block.games_id_id}/")
                args = get_main_args(request, section="main")
                if not args['logged_in']:
                    user = User.objects.get(id=m_user_id)
                    auth.login(request, user)
            else:
                # ищем операцию id=verbal - если не удалось просто на главную
                logging.info(f'  ***** ===== not fine id=verbal, or >1')
                return redirect('/')
    else:
        logging.info(f'  ***** ===== not post')
    return redirect('/')


@csrf_exempt
def trz_done(request, verbal=None):
    return payment_answer(request, verbal=verbal, m_tranzila_type="done")


@csrf_exempt
def trz_notify(request, verbal=None):
    return payment_answer(request, verbal=verbal, m_tranzila_type="notify")


@csrf_exempt
def trz_fail(request, verbal=None):
    print ("trz_fail")
    #request.POST =  <QueryDict:
    # {'Response': ['447'],
    # 'expmonth': ['04'],
    # 'currency': ['1'],
    # 'expyear': ['24'],
    # 'supplier': ['shmulik3355ch'],
    # 'pdesc': [''],
    # 'company': ['WinWin'],
    # 'sum': ['23'],
    # 'o_cred_type': [''],
    # 'lang': ['il'],
    # 'ccard': [''],
    # 'fail_url_address': ['http://45.80.70.249:50777/trz-fail/42/'],
    # 'ccno': ['6465'],
    # 'success_url_address': ['http://45.80.70.249:50777/trz-done/42/'],
    # 'g-recaptcha-response': ['03AGdBq27KCpqIvlZjpmyYfKDUKmQ_6KKWi4NvFHPaZh6IlReIgmCz2TvBswE1amIkJr0e0rbyUzWBDeJZskejuAwQS6fqdAI2Eqvi3UK5J13jBPu8LK_XItRuZ66Lmn5U4btsdS_wnDuon1c9_4TT3dt-LrURuvrxBSsu5jX9uppp-zmb2s5UU2OeO2c00oE3hEPGMCROPQUZx0yf_wpve-rMXKjiTuZmb26z24jTekEb6Ecf7l_g3vLs4YAzjSUcjNw3YvcjqzQuCa5zRNRsd57mwRlPcpRutoDpEpxHlbGfCtC5HIqfqTQt7pYS4pqTAYxJvLPi8ww9RS2g9UCtnyvlROTM0AvJvbCYuxvcPakNaVgJhjbEJ1QlF4mv-TYxpHX92QozAxRi9Z8eqsO65w9BBVefdw4yvCtw7Y--JZxuOnOtstOlnqlZ6pcDURyjom-e5bdirDdH7SRDASGEfqLaanrGiNdJ_g'],
    # 'ConfirmationCode': ['0100000'],
    # 'cardtype': ['-'],
    # 'cardissuer': ['0'],
    # 'cardaquirer': ['1'],
    # 'index': ['80017'],
    # 'Tempref': ['00042001'],
    # 'maxpay': ['']}>
    if request.method == "POST":
        print ("POST = ", request.POST)
        try:
            args = get_main_args(request, section="main")
            pay_operation = BalanceOperation.objects.get(id=verbal)
            if not args['logged_in']:
                m_user_id = pay_operation.user_id_id
                user = User.objects.get(id=m_user_id)
                auth.login(request, user)
                # args = get_main_args(request, section="main")

            pay_operation.pay_response = request.POST
            m_pay_operation_status_id = Type_balanceoperation_status.objects.get(verbal="03")
            pay_operation.status_id = m_pay_operation_status_id
            pay_operation.save()
            return redirect(f'/game-payment-fail/{pay_operation.games_id_id}/')
        except:
            pass
    return redirect('/')


def game_payment_fail(request, verbal=None):

    args = get_main_args(request, section="main")
    args['item_game_user'] = Game_history.objects.get(id=verbal)
    args['menu_item'] = ""
    args['l_body_list'].append(f"{args['GL_MainSkin']}/payment/payment_fail.html")
    args['main_tab'] = f"{args['GL_MainSkin']}/auth/auth.html"
    return render(request, args['main_tab'], args)


def game_payment_info(request):
    print("game_payment_info")
    args = get_main_args(request, section="main")
    answer = {"AnswerCod": "00",
              "AnswerText": gettext("error")}
    print("answer = ", answer)
    if not args['logged_in']:
        return JsonResponse(answer)
    if request.method == "POST":
        m_time_next = 5000
        try:
            print("request.POST = ", request.POST)
            m_pay_operation_id = request.POST.get('pay_operation_id', 0)
            pay_operation_list = BalanceOperation.objects.get(id=m_pay_operation_id)
            print("pay_operation_list = ", pay_operation_list)
            m_time_delta = (timezone.now() - pay_operation_list.created).seconds
            if m_time_delta > 300:
                m_time_next = 0
            else:
                m_time_next = 5000
            m_games_id = pay_operation_list.games_id_id
            m_pay_operation_status_succes = Type_balanceoperation_status.objects.get(verbal="04").id
            if pay_operation_list.status_id == m_pay_operation_status_succes:
                answer = {"AnswerCod": "01",
                          "GameId": m_games_id,
                          "m_time_delta": m_time_delta,
                          "NextTimeout": m_time_next,
                          }
            else:
                answer = {"AnswerCod": "00",
                          "NextTimeout": m_time_next,
                          }
        except:
            answer = {"AnswerCod": "00",
                      "NextTimeout": m_time_next,
                      }
    return JsonResponse(answer)
