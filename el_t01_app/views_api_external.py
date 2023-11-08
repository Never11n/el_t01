# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import datetime
import logging
import logging.config

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from .service.dft import get_GlobalSettings
from .models import List_jellyfish, Ticket_history
from .views_cab import balance_recalculate


class JellyFishAccessPermission(permissions.BasePermission):
    message = 'JellyFish customers not allowed.'

    def has_permission(self, request, view):
        m_headers = request.headers
        m_token = m_headers.get("Token", "")
        m_external_company_list = List_jellyfish.objects.filter(api_token=m_token)
        if m_external_company_list.count() > 0:
            m_Devices_list = m_external_company_list[0]
            print("permission yes")
            return True
        else:
            print("permission no")
            return False


# @csrf_exempt
class jellyfish_rezult(APIView):
    permission_classes = [JellyFishAccessPermission]

    def post(self, request):
        m_dirlog_short = '../log/log_apiext'
        print("os.path.exists(m_dirlog_short) = ", os.path.exists(m_dirlog_short))
        if not os.path.exists(m_dirlog_short):
            os.makedirs(m_dirlog_short)
        m_log_file = os.path.join(m_dirlog_short, 'log_apiext.log')
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
        logging.info('***** jellyfish_rezult  new request ******')

        # 1 data from body
        m_exec = True
        m_error = []
        m_headers = request.headers
        m_token = m_headers.get("Token", "")
        logging.info(f'  m_token = {m_token}')

        try:
            m_body_unicode = request.body.decode('utf-8')
            m_body_data = json.loads(m_body_unicode)
            '''
            method: POST
            payload:
            {
              "Ticket_id": "string",
              "Ticket_nom": "string",
              "PhotoBefore": "string",
              "PhotoAfter": "string",
              "IsWin": true,
              "WinSum": 0,
              "IsCorect": true
            }
            '''
            logging.info(f'  m_body_data   = {m_body_data}')
            m_Ticket_id = m_body_data.get("Ticket_id", "")
            m_Ticket_nom = m_body_data.get("Ticket_nom", "")
            m_Ticket_nom_00 = m_body_data.get("Ticket_nom_00", "")
            m_PhotoBefore = m_body_data.get("PhotoBefore", "")
            m_PhotoAfter = m_body_data.get("PhotoAfter", "")
            m_PhotoBefore_00 = m_body_data.get("PhotoBefore_00", None)
            m_PhotoAfter_00 = m_body_data.get("PhotoAfter_00", None)
            m_answ_tabl = m_body_data.get("answ_tabl", None)

            m_IsWin = m_body_data.get("IsWin", False)
            m_IsWin_00 = m_body_data.get("IsWin_00", False)
            m_WinSum = m_body_data.get("WinSum", "")
            m_WinSum_00 = m_body_data.get("WinSum_00", "")
            m_IsCorect = m_body_data.get("IsCorect", "")
            m_Type = m_body_data.get("Type", "new")
            logging.info(f'  m_Ticket_id   = {m_Ticket_id}')
            logging.info(f'  Ticket_nom    = {m_Ticket_nom}')
            logging.info(f'  m_PhotoBefore_00 = {m_PhotoBefore_00}')
            logging.info(f'  m_PhotoAfter_00  = {m_PhotoAfter_00}')
            logging.info(f'  m_PhotoBefore = {m_PhotoBefore}')
            logging.info(f'  m_PhotoAfter  = {m_PhotoAfter}')
            logging.info(f'  m_IsWin       = {m_IsWin}')
            logging.info(f'  m_WinSum      = {m_WinSum}')
            logging.info(f'  m_IsCorect    = {m_IsCorect}')
            logging.info(f'  m_Type        = {m_Type}')
        except Exception as ex:
            m_body_data = {}
            m_error.append("data error")
            logging.info(f'  data error    = {ex}')

        # 2 по коду билета из ответа найти запись
        # записать информацию
        # поменять статус билета
        try:
            m_globalset = get_GlobalSettings()
            m_MaxWinSum = m_globalset.get("MaxWinSum", "1000000")
            try:
                m_MaxWinSum = int(m_MaxWinSum)
            except Exception as ex:
                m_MaxWinSum = 1000000

            try:
                m_WinSumInt = int(m_WinSum)
            except Exception as ex:
                m_WinSumInt = 0

            if m_WinSumInt >= m_MaxWinSum and m_Type != "edit":
                m_WinSum = "0"
            t_ticket_history = Ticket_history.objects.get(req_id=m_Ticket_id)
            if m_Type != "edit":
                t_ticket_history.answ_dt = datetime.datetime.now()
            # t_ticket_history.error_job = ""
            # m_IsCorect = m_body_data.get("IsCorect", "")
            # t_ticket_history.status = "33"
            m_WinSum_old = t_ticket_history.answ_win_sum
            m_bool__recalculate = False
            if m_WinSum_old != m_WinSum:
                m_bool__recalculate = True
            if m_PhotoBefore_00:
                t_ticket_history.img_03 = m_PhotoBefore_00
            if m_PhotoAfter_00:
                t_ticket_history.img_04 = m_PhotoAfter_00
            t_ticket_history.img_07 = m_PhotoBefore
            t_ticket_history.img_08 = m_PhotoAfter
            if m_answ_tabl:
                t_ticket_history.answ_tabl = m_answ_tabl
            t_ticket_history.answ_nom = m_Ticket_nom
            # t_ticket_history.answ_nom_00 = m_Ticket_nom_00
            t_ticket_history.answ_win = m_IsWin
            # t_ticket_history.answ_win_00 = m_IsWin_00
            t_ticket_history.answ_win_sum = m_WinSum
            # t_ticket_history.answ_win_sum_00 = m_WinSum_00
            # ToDo ('02', 'wait confirm'),

            if m_Ticket_nom == "0000-000000-000":
                t_ticket_history.status = "03"
                t_ticket_history.save()
            else:
                if t_ticket_history.status == "00":
                    m_Check_ticket_notwin_wait = m_globalset.get("GL_Check_ticket_notwin_wait", False)
                    m_Check_ticket_win_wait =  m_globalset.get("GL_Check_ticket_win_wait", False)
                    if (t_ticket_history.answ_win and m_Check_ticket_win_wait) or (not t_ticket_history.answ_win and m_Check_ticket_notwin_wait):
                        t_ticket_history.status = "02"
                    else:
                        t_ticket_history.status = "01"
                t_ticket_history.save()
                if t_ticket_history.games_id.ticket_list.get('gift', False):
                    sms_gift_set_ready(t_ticket_history)

            if m_bool__recalculate:
                balance_recalculate(t_ticket_history.games_id.user_id_id, t_ticket_history.id)

            logging.info(f'  ticket id     = {t_ticket_history.id}')
        except Exception as ex:
            m_body_data = {}
            m_error.append("data error")
            logging.info(f'  data error    = {ex}')

        # ToDo
        # проверить и поменять статус игры
        try:
            pass
        except Exception as ex:
            m_body_data = {}
            m_error.append("data error")
            logging.info(f'  data error    = {ex}')

        # ToDo
        # если выиграш - записываем операцию и меняем баланс
        # save balance operation
        # change balance user
        try:
            pass
        except Exception as ex:
            m_body_data = {}
            m_error.append("data error")
            logging.info(f'  data error    = {ex}')
        ###

        # ToDo
        if m_exec == True:
            m_return = {}
            m_return["success"] = True
        else:
            m_return = {}
            m_return["success"] = False
            m_return["error"] = m_error
            m_return["ticket_int"] = {}

        return Response(m_return)
