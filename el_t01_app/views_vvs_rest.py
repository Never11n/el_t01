# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import json
import importlib
from multiprocessing import Process
import time
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from oauthlib.oauth2.rfc6749.tokens import random_token_generator
from django.db import transaction as db_transaction
from django.template.loader import get_template
from django.core.files import File
import pathlib2 as pathlib
from django.utils import timezone

from el_t01.settings import MEDIA_ROOT, BASE_DIR

from el_t01_app.service.service import get_main_args
from el_t01_app.models import Profile, Devices_list, Ticket_type, Device_history

import requests
from el_t01.env import TOKEN_DEVICE, TOKEN_SERVER, URL_PHOTO, URL_RESULT, URL_FREE

# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

class CustomerAccessPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        print ("has_permission --")
        # body_unicode = request.body.decode('utf-8')
        # try:
        #     body = json.loads(body_unicode)
        # except:
        #     body = {}
        m_headers = request.headers
        m_token = m_headers.get("Token", "")
        print ("m_token = ", m_token)
        m_Devices_list = Devices_list.objects.filter(api_token=m_token)
        if m_Devices_list.count() > 0:
            m_Devices_list = m_Devices_list[0]
            return True
        else:
            return False

class FileUploadView_Vvs(APIView):
    print ("FileUploadView_Vvs")
    permission_classes = [CustomerAccessPermission]
    # parser_classes = (FileUploadView_Vvs, )

    def post(self, request, format='jpg'):
        m_return = {"status": "error"}
        m_headers = request.headers
        m_token = m_headers.get("Token", "")
        m_jellyfish_type = m_headers.get("JellyfishType", "")
        m_ticket_type = m_headers.get("TicketType", "")
        m_ticketid = m_headers.get("TicketId", "")

        print ("m_token          = ", m_token )
        print ("m_jellyfish_type = ", m_jellyfish_type )
        print ("m_ticket_type    = ", m_ticket_type )
        print ("m_ticketid       = ", m_ticketid )

        # если новая система - ищем запись
        # если старвя система - создаем запись

        # найти запись в истории
        try:
            t_ticket_history = Device_history.objects.get(id=m_ticketid)
        except:
            pass

        m_Devices_list = Devices_list.objects.filter(api_token=m_token)
        print ("m_Devices_list.count() = ", m_Devices_list.count() )
        # ToDo
        if m_Devices_list.count() > 0:
            m_Devices_item = m_Devices_list[0]
        else:
            m_Devices_item = None

        if m_Devices_item is not None:
            if request.FILES:
                print ("FILES YES")
                if 'image' in request.FILES:
                    file_to_upload = request.FILES['image']
                    m_time_now = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
                    m_dir_short = os.path.join('media', 'ticket_in', str(m_Devices_item.id))
                    m_file_name = "in_{}_{}_{}.png".format(m_ticketid, m_ticket_type, m_time_now )
                    m_file_short = os.path.join(m_dir_short, m_file_name)
                    m_dir_full = os.path.join(BASE_DIR, m_dir_short)
                    m_file_full = os.path.join(m_dir_full, m_file_name)
                    print ("m_file_full = ", m_file_full)
                    file_in = File(file_to_upload)
                    with open(m_file_full, 'wb+') as file_out:
                        for chunk in file_in.chunks():
                            file_out.write(chunk)

                    m_return = {"status": "ok"}

                    if t_ticket_history.game_type.verbal == "01":
                        from el_t01_app.service.v003.def_ticket_01 import TicketJob
                    elif t_ticket_history.game_type.verbal == "02":
                        from el_t01_app.service.v003.def_ticket_02 import TicketJob
                    elif t_ticket_history.game_type.verbal == "03":
                        from el_t01_app.service.v003.def_ticket_03 import TicketJob
                    elif t_ticket_history.game_type.verbal == "04":
                        from el_t01_app.service.v003.def_ticket_04 import TicketJob
                    elif t_ticket_history.game_type.verbal == "05":
                        from el_t01_app.service.v003.def_ticket_05 import TicketJob

                    if m_ticket_type == "01":
                        t_ticket_history.img_01 = m_file_short
                        t_ticket_history.step_ticket = m_ticket_type
                        t_ticket_history.save()
                        ItemJob = TicketJob(item_ticket_job=t_ticket_history)
                        m_return = ItemJob.run_job_01()

                    if m_ticket_type == "02":
                        t_ticket_history.img_02 = m_file_short
                        t_ticket_history.step_ticket = m_ticket_type
                        t_ticket_history.save()
                        ItemJob = TicketJob(item_ticket_job=t_ticket_history)
                        m_return = ItemJob.run_job_02()

            else:
                print ("FILES NO")

        return Response(m_return)


class Tickets_Get_Vvs(APIView):
    print ("Tickets_Get_Vvs")
    permission_classes = [CustomerAccessPermission]
    # parser_classes = (FileUploadView_Vvs, )

    def post(self, request, format='jpg'):
        m_return = {"status": "error"}
        m_headers = request.headers
        m_token = m_headers.get("Token", "")
        m_jellyfish_type = m_headers.get("JellyfishType", "")
        m_ticket_type = m_headers.get("TicketType", "")
        m_ticketid = m_headers.get("TicketId", "")

        try:
            m_Devices_item = Devices_list.objects.get(api_token=m_token)
        except:
            return Response([])

            ## api_token

        print ("m_token          = ", m_token )
        print ("m_jellyfish_type = ", m_jellyfish_type )
        print ("m_ticket_type    = ", m_ticket_type )
        print ("m_ticketid       = ", m_ticketid, type(m_ticketid) )

        body_unicode = request.body.decode('utf-8')
        print ("body_unicode     = ", body_unicode )
        body_data = json.loads(body_unicode)
        print ("body_data        = ", body_data )
        m_tickets_in = body_data.get('JobTickets',[])
        print ("m_tickets_in     = ", m_tickets_in )

        m_device_ticket_list = []
        for item_ticket in m_tickets_in:
            t_history = Device_history()
            t_history.req_id = item_ticket
            t_history.req_dt = timezone.now()
            t_history.step_job = ""
            t_history.type_ticket = m_Devices_item.t_type.verbal
            t_history.status = "00"
            t_history.type_jellyfish = "02"
            t_history.t_dev_id = m_Devices_item.id
            t_history.save()
            m_device_ticket_list.append(t_history.id)

        t_history.send_free = True
        t_history.save()

        m_return = {"status": "ok", "ticket_list": m_device_ticket_list}
        return Response(m_return)
