# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import json
import importlib
# from multiprocessing import Process
import time
from django.http import JsonResponse
from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
# from django.db import connection
# from oauthlib.oauth2.rfc6749.tokens import random_token_generator
# from django.db import transaction as db_transaction
# from django.template.loader import get_template
# from django.core.files import File
# import pathlib2 as pathlib
# from django.utils import timezone

# from el_t01.settings import MEDIA_ROOT, BASE_DIR

# from el_t01_app.service.service import get_main_args
# from el_t01_app.models import Profile, Devices_list, Ticket_type, Device_history
from el_t01_app.models import List_external_company

# import requests
# from el_t01.env import TOKEN_DEVICE, TOKEN_SERVER, URL_PHOTO, URL_RESULT, URL_FREE

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

class CustomerAccessPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'
    def has_permission(self, request, view):
        print ("has_permission --")
        m_headers = request.headers
        m_token = m_headers.get("Token", "")
        print ("m_token = ", m_token)
        t_token_list = List_external_company.objects.filter(api_token=m_token, enabled=True)
        if t_token_list.count() > 0:
            t_token_item = t_token_list[0]
            return True
        else:
            return False

class Report_data_get(APIView):
    permission_classes = [CustomerAccessPermission]

    def post(self, request, format='jpg'):
        # report_data
        # verbal  номер отчета
        # daterange_1  # 05/02/2021 12:00 AM - 05/22/2021 11:00 PM
        # daterange_2  # 05/02/2021 12:00 AM - 05/22/2021 11:00 PM
        # find_type_game_list

        m_headers = request.headers
        m_token = m_headers.get("Token", "")
        print ("m_token          = ", m_token )
        print ("m_headers        = ", m_headers )

        try:
            m_data = request.data
            print (f"m_data        = {m_data}")
            m_daterange_1 = m_data.get("daterange_1", "")
            m_daterange_2 = m_data.get("daterange_2", "")
            m_verbal = m_data.get("verbal", "") # code report
            m_lang = m_data.get("lang", "") # code lang
            m_date = m_data.get("date", "")
            m_args = {}
            m_args["daterange_1"] = m_daterange_1
            m_args["daterange_2"] = m_daterange_2
            m_args["verbal"] = m_verbal
            m_args["lang"] = m_lang
            m_args["date"] = m_date

            #
            # logging.info(f'  m_daterange_1 = {m_daterange_1}')
            # logging.info(f'  m_daterange_2 = {m_daterange_2}')
            # logging.info(f'  m_verbal      = {m_verbal}')
            print(f'  m_daterange_1 = {m_daterange_1}')
            print(f'  m_daterange_2 = {m_daterange_2}')
            print(f'  m_verbal      = {m_verbal}')
            ReportDef_name = f"el_t01_app.service.report.report_data"
            ReportDef_module = importlib.import_module(ReportDef_name)
            ReportDef_module = importlib.reload(ReportDef_module)
            d_report_data = getattr(ReportDef_module, 'report_data')
            return_list, return_args = d_report_data(request, m_verbal, add_api=m_args )
            m_return = {"status": "ok", "return_list": return_list, "return_args": return_args}
        except Exception as ex:
            print(f'  data error    = {ex}')
            m_return = {"status": "error", "return_list": [], "return_args": []}

        return Response(m_return)

'''
    print("jellyfish_game_start")
    try:
        # проверить доступна машина или нет
        t_jellyfish = List_jellyfish.objects.filter(enabled=True).order_by("order")
        print(f"t_jellyfish.count = {t_jellyfish.count()}")
        logging.info(f"t_jellyfish.count = {t_jellyfish.count()}")
        ##
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
            print("response.text =", response.text, response.status_code)
            logging.info(f"response.status_code = {response.status_code}")
            logging.info(f"response.text        = {response.text}")

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

'''