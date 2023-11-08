#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import binascii
import requests
import math
import datetime
import logging
import logging.config
from logging.handlers import RotatingFileHandler
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.contrib import auth
from django.utils.translation import ugettext
from el_t01.settings import BASE_DIR
from el_t01_app.service.dft import get_site_lang, get_layout_scripts
from el_t01_app.service.dft import (get_dict_tickets_type,
                                   get_dict_tickets_type_random,
                                   get_dict_documentation_list,
                                   get_report_list,
                                   get_devices_list,
                                   get_external_company_list,
                                   get_site_skin,
                                   get_dict_payment_type,
                                   get_dict_cart_games,
                                   get_dict_game_status,
                                   get_dict_ticket_status,
                                   get_GlobalSettings_old,
                                   get_GlobalSettings,
                                   get_count_feed_new,
                                   get_count_payout_new,
                                   get_count_payadd_new,
                                   get_count_cashadd_new,
                                   get_dict_partner,
                                   get_dict_tasktype,
                                   get_dict_type_balanceoperation,
                                   get_dict_blacklist_type,
                                   get_dict_tickets_type_subs,
                                   get_list_lotto_types,
                                   get_dict_tickets_type_lotto
                                   # get_dict_notification_system,
                                   )
from el_t01_app.models import (List_jellyfish, DiscountHistory, DiscountSet)


def get_main_args(request, section=""):
    args = {}
    me = auth.get_user(request)
    args['me'] = me
    args['lang'] = str(request.LANGUAGE_CODE)
    args['logged_in'] = me.is_authenticated
    args['site_lang'] = get_site_lang()
    args['main_currency'] = "ils"
    # Global Settings
    args.update(get_GlobalSettings())
    # Global Settings OLD
    args['globalset'] = get_GlobalSettings_old()
    try:
        args['GL_CabbNumberInPage'] = int(args['globalset'].get("CabbNumberInPage", 100))
    except:
        args['GL_CabbNumberInPage'] = 100

        # start dictionary formation
    #
    args['templ_call_centr_wa'] = f"{args['GL_MainSkin']}/common/section_call_centr_wa.html"
    #
    args['dict_birthday_year'] = []
    m_year_start = datetime.date.today().year - 18
    m_year_finish = datetime.date.today().year - 100
    for ItemYear in range(m_year_start, m_year_finish, -1 ):
        args['dict_birthday_year'].append(ItemYear)
    #
    args['count_feed_new'] = get_count_feed_new()
    args['count_payout_new'] = get_count_payout_new()
    args['count_payadd_new'] = get_count_payadd_new()
    args['count_cashadd_new'] = get_count_cashadd_new()
    #
    args['dict_tickets_type'] = get_dict_tickets_type()
    args['dict_tickets_type_lotto'] = get_dict_tickets_type_lotto()
    args['dict_tickets_type_subs'] = get_dict_tickets_type_subs()
    args['dict_tickets_type_random'] = get_dict_tickets_type_random()
    args['dict_payment_type'] = get_dict_payment_type()
    args['dict_documentation_list'] = get_dict_documentation_list()
    args['dict_game_status'] = get_dict_game_status()
    args['dict_partner'] = get_dict_partner()
    args['dict_tasktype'] = get_dict_tasktype()
    args['dict_type_balanceoperation'] = get_dict_type_balanceoperation()
    args['dict_blacklist_type'] = get_dict_blacklist_type()
    args['list_lotto_types'] = get_list_lotto_types()
    # args['dict_notification_system'] = get_dict_notification_system()
    ## stop dictionary formation
    # For lending
    args['index_section_slide'] = True
    args['index_section_services'] = True
    args['index_section_services_2'] = True
    args['index_section_video'] = True
    args['index_section_team'] = True
    args['index_section_pricing'] = True
    args['index_section_contact'] = True
    # Language Dropdown Menu
    args['section_language_dropdown'] = False
    args['section_language_dropdown'] = True
    args['lf_language'] = f"{args['GL_MainSkin']}/common/section_language_02.html"
    # print ("args = ", args)

    if args['logged_in']:
        args['discount_user'] = get_discount_user(args['me'])
        args['PAGE_TITLE'] = args.get('GL_PageCabinet_Title', "")

        args['dict_report_list'] = get_report_list()
        args['cart_games'] = get_dict_cart_games(args['me'])
        args['cart_games_num'] = args['cart_games'].count()

        args['l_head_list'] = []
        args['l_header_list'] = []
        args['l_footer_list'] = []
        args['l_script_list'] = []
        args['l_modal_list'] = []
        args['l_body_list'] = []

        # args['lf_index'] = f'cabinet/index.html'
        # args['lf_about'] = f'cabinet/about.html'
        # args['lf_contact'] = f'cabinet/contact.html'
        #
        args['l_layout_file'] = f"{args['GL_MainSkin']}/cabinet/layout.html"
        args['l_head_list'].append(f"{args['GL_MainSkin']}/cabinet/l_head_01.html")
        args['l_head_list'].append(f"{args['GL_MainSkin']}/cabinet/l_head_finish.html")
        args['l_header_list'].append(f"{args['GL_MainSkin']}/cabinet/l_header.html")
        args['l_footer_list'].append(f"{args['GL_MainSkin']}/cabinet/l_footer_01.html")
        args['l_script_list'].append(f"{args['GL_MainSkin']}/cabinet/l_script_01.html")
        # args['l_modal_list'].append(f"{args['GL_MainSkin']}/cabinet/l_modal_01.html")
        # args['l_modal_list'].append(f"{args['GL_MainSkin']}/cabinet/l_modal_02.html")
        args['l_modal_list'].append(f"{args['GL_MainSkin']}/cabinet/l_modal_03.html")

        args['l_layout_scripts_head_top'] = get_layout_scripts(file_loc='cab', script_loc='ht')
        args['l_layout_scripts_head_bottom'] = get_layout_scripts(file_loc='cab', script_loc='hb')
        args['l_layout_scripts_body_top'] = get_layout_scripts(file_loc='cab', script_loc='bt')
        args['l_layout_scripts_body_bottom'] = get_layout_scripts(file_loc='cab', script_loc='bb')
        args['l_layout_scripts_chat_bot'] = []

        if args.get('GL_Chat_Bot_App', False):
            args['l_layout_scripts_chat_bot'].append(f"chat_bot_app/l_script_chat_bot.html")

    else:
        args['PAGE_TITLE'] = args.get('GL_PageMain_Title', "")
        args['l_head_list'] = []
        args['l_header_list'] = []
        args['l_footer_list'] = []
        args['l_script_list'] = []
        args['l_modal_list'] = []
        args['l_index_list'] = []
        args['l_body_list'] = []
        args['lf_index'] = f"{args['GL_MainSkin']}/main/index.html"
        args['lf_about'] = f"{args['GL_MainSkin']}/main/about.html"
        args['lf_contact'] = f"{args['GL_MainSkin']}/main/contact.html"
        args['l_layout_file'] = f"{args['GL_MainSkin']}/main/layout.html"
        args['l_head_list'].append(f"{args['GL_MainSkin']}/main/l_head_01.html")
        args['l_head_list'].append(f"{args['GL_MainSkin']}/main/l_head_finish.html")
        args['l_header_list'].append(f"{args['GL_MainSkin']}/main/l_header.html")
        args['l_footer_list'].append(f"{args['GL_MainSkin']}/main/l_footer_01.html")
        args['l_script_list'].append(f"{args['GL_MainSkin']}/main/l_script_01.html")
        args['l_modal_list'].append(f"{args['GL_MainSkin']}/main/l_modal_01.html")
        args['l_modal_list'].append(f"{args['GL_MainSkin']}/main/l_modal_02.html")
        args['l_modal_list'].append(f"{args['GL_MainSkin']}/main/l_modal_03.html")
        # args['l_modal_list'].append(f"{args['GL_MainSkin']}/main/l_modal_04.html")
        args['l_modal_list'].append(f"{args['GL_MainSkin']}/main/l_modal_05.html")
        args['l_index_list'].append(f"{args['GL_MainSkin']}/main/index_01n.html")
        # args['l_index_list'].append(f"{args['GL_MainSkin']}/main/index_021n.html')
        args['l_index_list'].append(f"{args['GL_MainSkin']}/main/index_02n.html")
        args['l_index_list'].append(f"{args['GL_MainSkin']}/main/index_video.html")
        # args['l_index_list'].append(f"{args['GL_MainSkin']}/main/index_03.html')
        args['l_index_list'].append(f"{args['GL_MainSkin']}/main/index_04n.html")
        args['l_index_list'].append(f"{args['GL_MainSkin']}/main/index_05n.html")

        args['l_layout_scripts_head_top'] = get_layout_scripts(file_loc='main', script_loc='ht')
        args['l_layout_scripts_head_bottom'] = get_layout_scripts(file_loc='main', script_loc='hb')
        args['l_layout_scripts_body_top'] = get_layout_scripts(file_loc='main', script_loc='bt')
        args['l_layout_scripts_body_bottom'] = get_layout_scripts(file_loc='main', script_loc='bb')
    return args


def generate_hash(_len):
    return binascii.hexlify(os.urandom(_len)).decode('utf-8')


def send_sms_01(loc_tel_code, loc_tel, loc_tel_from, loc_txt, loc_globalset):
    # print ("send_sms_01")
    payload = u''
    try:
        # print ("loc_tel_code = ", loc_tel_code)
        # print ("loc_tel      = ", loc_tel)
        # print ("loc_txt      = ", loc_txt)

       # m_cellphone = '972547117117'
        m_cellphone_from = loc_tel_from
        m_cellphone = loc_tel
        m_data_txt = 'TEST LINK TEST LINK TEST LINK '
        m_data_txt = loc_txt

        url = "https://globalsecureapi.soprano.co.il/"
        # payload = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n" \              "<sms>\r\n<account>\r\n<id>israelbl7</id>\r\n<password>israelbl777</password>\r\n</account>\r\n<attributes>\r\n<reference>972</reference>\r\n        <replyPath>543139995</replyPath>\r\n    </attributes>\r\n    <schedule>\r\n        <relative>0</relative>\r\n    </schedule>\r\n    <targets>\r\n        <cellphone reference=\"user_reference\">972547117117</cellphone>\r\n    </targets>\r\n    <data>Link</data>\r\n</sms>'
        payload = u'<?xml version="1.0" encoding="UTF-8"?>\r\n'
        payload += u' <sms>\r\n'
        payload += u' <account>\r\n'
        payload += u' <id>{}</id>\r\n'.format(loc_globalset.get("GL_SMS_tuser", "")) #israelbl7
        payload += u' <password>{}</password>\r\n'.format(loc_globalset.get("GL_SMS_tpass", "")) #israelbl777
        payload += u' </account>\r\n'
        payload += u' <attributes>\r\n <reference>972</reference>\r\n <replyPath>{}</replyPath>\r\n </attributes>\r\n'.format(m_cellphone_from)
        payload += u' <schedule>\r\n <relative>0</relative>\r\n </schedule>\r\n'
        payload += u' <targets>\r\n '
        payload += u'  <cellphone reference="user_reference">{}</cellphone>\r\n'.format(m_cellphone)
        payload += u' </targets>\r\n'
        payload += u' <data>{}</data>\r\n'.format(m_data_txt)
        payload += u'</sms>'
        # print (" payload = ", payload)
        # payload = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<sms>\r\n <account>\r\n <id>israelbl7</id>\r\n <password>israelbl777</password>\r\n </account>\r\n <attributes>\r\n <reference>972</reference>\r\n <replyPath>543139995</replyPath>\r\n </attributes>\r\n <schedule>\r\n <relative>0</relative>\r\n </schedule>\r\n <targets>\r\n <cellphone reference=\"user_reference\">972547117117</cellphone>\r\n </targets>\r\n <data>TEST LINK</data>\r\n</sms>"
        headers = {'Content-Type': 'application/xml'}
        # response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'), verify=False)
        response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'), verify=False, timeout=30 )

        m_response_text = response.text
        #m_response_text = "I confirm order 123654789."
    except Exception as ex:
        m_response_text = ex
    return (payload, m_response_text)


def paginate(_list, page, number_in_page):
    print ("page, number_in_page ", page, number_in_page)
    if page < 1:
        page = 1

    if len(_list) > (page * number_in_page):

        pass
    if len(_list) < ((page-1) * number_in_page):
        page = math.ceil(len(_list)/number_in_page)
    print("page = ", page, len(_list), number_in_page)

    if len(_list) > number_in_page:
        return (page, Paginator(_list, number_in_page).page(int(page)))
    else:
            try:
                return (page, Paginator(_list, len(_list)).page(int(page)))
            except Exception as ex:
                print("ex = ", ex)
                if len(_list) > 0:
                    return (page, Paginator(_list, len(_list)).page(1))
                else:
                    return (page, _list)

def check_template_exists(loc_name):
    m_glob = get_GlobalSettings()
    m_skin = m_glob.get('GL_MainSkin', "")
    path_short = os.path.join(BASE_DIR, "templates", "common", loc_name)
    path_long = os.path.join(BASE_DIR, "templates", m_skin, loc_name)

    if os.path.exists(path_long) and os.path.isfile(path_long):
        return_name = path_long
    else:
        return_name = path_short
    return return_name

def jellyfish_change_data(l_ticket_id, l_ticket_nom, l_ticket_win ):
    m_dirlog_short = os.path.join(BASE_DIR, "..", "log/log_jellyfish_change_data")

    print("os.path.exists(m_dirlog_short) = ", os.path.exists(m_dirlog_short))
    if not os.path.exists(m_dirlog_short):
        os.makedirs(m_dirlog_short)
    m_log_file = os.path.join(m_dirlog_short, 'log_jellyfish_change_data.log')
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
    logging.info('***** jellyfish_change_data ******')
    try:
        t_jellyfish = List_jellyfish.objects.filter(enabled=True).order_by("order")
        ##
        if t_jellyfish.count() > 0:
            item_jellyfish = t_jellyfish[0]
            m_url_1 = item_jellyfish.ipadres
            m_url_2 = "" if m_url_1.strip()[-1] == "/" else "/"
            m_url_3 = "api/v07/external/change_data"
            url = f"{m_url_1}{m_url_2}{m_url_3}"

            # m_url_3 = "http://45.80.70.249:50711/api/v07/external/change_data"
            # url = f"{m_url_3}"

            m_payload = {
                "ticket_id": f"'{l_ticket_id}'",
                "ticket_nom": l_ticket_nom,
                "ticket_win": l_ticket_win,
            }
            payload = json.dumps(m_payload)
            headers = {
                'Token': item_jellyfish.api_token,
                'Content-Type': 'application/json'
            }

            logging.info(f"url       = {url}")
            logging.info(f"headers   = {headers}")
            logging.info(f"payload   = {payload}")

            response = requests.request("POST", url, headers=headers, data=payload)
            logging.info(f"response.status_code = {response.status_code}")

            if response.status_code == 200:
                logging.info(f"jellyfish_change_data status {response.status_code}")
            else:
                logging.info(f"Error jellyfish_change_data status {response.status_code}")
        else:
            logging.info("Error change_data not available")
    except Exception as ex:
        logging.info(f"jellyfish_change_data Unable to change_data")
        logging.info(f"ex = {ex}")
    logging.info(f"FINISH")

def get_discount_user(l_user_id):
    try:
        m_date_check = datetime.datetime.now()
        t_discount_history = DiscountHistory.objects.filter(user=l_user_id,
                                                            start_date__lte=m_date_check,
                                                            stop_date__gte=m_date_check,
                                                            discount__enabled=True
                                                            ).order_by("-id")
        # print ("disc = ", t_discount_history.count() )
        if t_discount_history.count() > 0:
            discount_user = {"discount": True,
                             "discount_id": t_discount_history[0].id,
                             "discount_caption": t_discount_history[0].discount.caption,
                             "discount_caption_user": t_discount_history[0].discount.caption_user,
                             "discount_product_list": {},
                             }
            t_discount_set = DiscountSet.objects.filter(disc_id=t_discount_history[0].discount_id).order_by("ticket_type")
            for ItemDiscSet in t_discount_set:
                discount_user["discount_product_list"][ItemDiscSet.ticket_type_id] = ItemDiscSet.discount_amount
        else:
            discount_user = {"discount": False}
    except:
        discount_user = {"discount": False}
    return discount_user


def setup_logger(name_dir, name_file, name_logger, level=logging.INFO, maxBytes=200000, backupCount=30):
    """To setup as many loggers as you want"""

    m_dirlog_short = os.path.join(BASE_DIR, "..", "log", name_dir)
    if not os.path.exists(m_dirlog_short):
        os.makedirs(m_dirlog_short)
    log_file = os.path.join(m_dirlog_short, f'{name_file}.log')

    # DictLOGGING = {
    #     'version': 1,
    #     'disable_existing_loggers': False,
    #     'formatters': {
    #         'standard': {
    #             'format': '%(asctime)s; %(levelname)s:%(name)s: %(message)s '
    #                       '(%(filename)s:%(lineno)d)',
    #         }
    #     },
    #     'handlers': {
    #         'console': {
    #             'level': 'DEBUG',
    #             'formatter': 'standard',
    #             'class': 'logging.StreamHandler',
    #         },
    #         'rotate_file': {
    #             'level': 'DEBUG',
    #             'formatter': 'standard',
    #             'class': 'logging.handlers.RotatingFileHandler',
    #             #            'filename': 'rotated.log',
    #             'filename': 'm_log_file',
    #             'encoding': 'utf8',
    #             'maxBytes': 200000,
    #             'backupCount': 30,
    #         }
    #     }
    #     ,
    #     'loggers': {
    #         '': {
    #             'handlers': ['console', 'rotate_file'],
    #             # 'handlers': ['rotate_file'],
    #             # 'level': 'DEBUG',
    #             'level': 'INFO',
    #         },
    #     }
    # }
    # logging.config.dictConfig(DictLOGGING)
    # log_mess_sms = logging.getLogger('mess_sms')
    # log_mess_sms = logging.getLogger('mess_sms')

    formatter = logging.Formatter('%(asctime)s; %(levelname)s:%(name)s: %(message)s (%(filename)s:%(lineno)d)')
    handler = RotatingFileHandler(log_file,
                                  maxBytes=maxBytes,
                                  backupCount=backupCount,
                                  encoding='utf8')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name_logger)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
