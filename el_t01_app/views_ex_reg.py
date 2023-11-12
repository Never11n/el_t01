# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import binascii
import os
import json
from datetime import datetime
import random

from dateutil.relativedelta import relativedelta
import logging
import logging.config

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from el_t01_app.models import (Profile, List_external_company, APIExtPage, APIExtHash, IdConfirmation,
                               Ticket_history, Blogger, Game_history)
from el_t01_app.service.dft import get_GlobalSettings
from el_t01_app.service.report.report_data import report_data
from el_t01_app.service.service import get_main_args, check_template_exists
import re


def test_print(request):
    print('Hello World!')


def valid_input(val):
    if len(val) >= 20:
        return False
    return True


def valid_email_length(email):
    return len(email) <= 100


def valid_values_registration(val_dict):
    m_reg_name = val_dict['m_reg_name']
    m_reg_id = val_dict['m_reg_id']
    m_reg_phone = val_dict['m_reg_phone']
    regex_name = r'^[a-zA-Z\s-]+$'
    regex_phone = r'^[0-9]+$'
    regex_id = r'^[a-zA-Z0-9/-]+$'
    message = ''

    if not re.match(regex_name, m_reg_name):
        message = 'Please enter correct name'
        return False, message
    if not re.match(regex_phone, m_reg_phone):
        message = 'Please enter correct phone'
        return False, message
    if not re.match(regex_id, m_reg_id):
        message = 'Please enter correct id'
        return False, message

    if not valid_input(m_reg_id):
        print("False")
        message = 'Please enter correct id'
        return False, message
    if not valid_input(m_reg_phone):
        print("False")
        message = 'Please enter correct phone'
        return False, message
    if not valid_input(m_reg_phone):
        print("False")
        message = 'Please enter correct phone'
        return False, message
    return True, message


def is_legal_age(date_of_birth):
    current_date = datetime.now()
    birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
    age = current_date.year - birth_date.year - (
            (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
    print(age)
    message = ''

    if birth_date.year < 1920:
        message = 'Please enter correct date of birth'
        return False, message

    if age < 18:
        message = 'Your age is lower than 18 y.o'
        return False, message
    return True, message


class ExtApi_AccessPermission(permissions.BasePermission):
    message = 'ExtApi_Registration customers not allowed.'

    def has_permission(self, request, view):
        # m_headers = request.headers
        # m_token = m_headers.get("Token", "")
        # m_external_company_list = List_external_company.objects.filter(api_token=m_token, verbal="ext_reg")
        # if m_external_company_list.count() > 0:
        #   m_Devices_list = m_external_company_list[0]
        print("permission yes")
        return True
    # else:
    #   print("permission no")
    #  return False


# @csrf_exempt
class ext_shop(APIView):
    print('Test')
    permission_classes = [ExtApi_AccessPermission]

    def post(self, request):
        m_return = {}
        m_dirlog_short = '../log/log_apiext'
        print("os.path.exists(m_dirlog_short) = ", os.path.exists(m_dirlog_short))
        if not os.path.exists(m_dirlog_short):
            os.makedirs(m_dirlog_short)
        m_log_file = os.path.join(m_dirlog_short, 'log_apiext_reg.log')
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
        logging.info('***** ExtApi_Registration new request ******')
        # проверить данные входные
        # проверить есть ли такой
        # проверить каждый параметр
        #
        # 1 data from body
        join_errors = []
        m_headers = request.headers
        m_token = m_headers.get("Token", "")
        t_profile = None
        logging.info(f'  m_token = {m_token}')
        try:
            print('data')
            m_data = request.data
            print(m_data)
            logging.info(f'  m_data   = {m_data}')
            # m_reg_param = json.loads(m_data.get("reg_param", ""))
            # m_reg_param = json.loads(m_data)
            print('data1')
            '''
            m_reg_param =  {
            "reg_name": "qwerty", 
            "reg_shopcode": "123456", 
            "reg_phone": "1234567891", 
            }            
            '''

            m_reg_name = m_data.get("f_name", "")
            print(m_reg_name)
            m_reg_email = m_data.get("f_email", "")
            m_reg_adress = m_data.get("f_adress", "")
            m_reg_shopcode = m_data.get("f_shopcode", "")
            m_reg_phone = m_data.get("f_phone_number", "")
            m_reg_phone = m_reg_phone.replace('+', '')
            m_url_path = m_data.get("url_path", "")
            m_reg_birthday = m_data.get("f_date_birth", "")
            m_reg_id = m_data.get("f_idoc", "")
            print(m_reg_id)
            m_reg_password = f"{random.randrange(100, 999)}{random.randrange(100, 999)}{random.randrange(100, 999)}"

            # Validation of data
            val_dict = {'m_reg_name': m_reg_name,
                        'm_reg_phone': m_reg_phone,
                        'm_reg_id': m_reg_id
                        }

            is_valid, message = valid_values_registration(val_dict)
            is_valid_email_length = valid_email_length(m_reg_email)
            is_legal_input_age, message_age = is_legal_age(m_reg_birthday)

            if not is_legal_input_age:
                m_return['AnswerCod'] = '01'
                m_return['AnswerText'] = message_age
                print(message, "**")
                return Response(m_return)

            if is_valid_email_length:
                try:
                    validate_email(m_reg_email)
                except ValidationError:
                    m_return['AnswerCod'] = '01'
                    m_return['AnswerText'] = "Please enter correct email"
                    return Response(m_return)

            if not is_valid:
                m_return['AnswerCod'] = '01'
                m_return['AnswerText'] = message
                print(message, "*")
                return Response(m_return)
            print(m_reg_name)

            t_blogger_id = None
            if m_url_path != '':
                if Blogger.objects.filter(ref_hash=m_url_path).exists():
                    t_blogger_id = Blogger.objects.get(ref_hash=m_url_path).id

            logging.info(f'  m_reg_name             = {m_reg_name}')
            logging.info(f'  m_reg_shopcode         = {m_reg_shopcode}')
            logging.info(f'  m_reg_phone            = {m_reg_phone}')
            logging.info(f'  m_url_path             = {m_url_path}')
            logging.info(f'  m_reg_id             = {m_reg_id}')

        except Exception as ex:
            m_body_data = {}
            t_profile = None
            join_errors.append("data error")
            logging.info(f'  data error    = {ex}')

        print("11")
        print("11")
        print("11")
        if len(join_errors) == 0:
            # DO registartion
            # create token to login
            # check unic - m_reg_email  m_reg_phone  m_reg_id_doc
            # t_profile = None
            # if Profile.objects.filter(mobile=m_reg_phone, i_doc=m_reg_id_doc, user__email=m_reg_email ).exists():
            #    t_profile = Profile.objects.filter(mobile=m_reg_phone, i_doc=m_reg_id_doc, user__email=m_reg_email)[0]
            #   logging.info(f'  Profile exist')
            # else:
            #   logging.info(f'  Profile not exist')
            #  print("22")
            # print("22")
            ###
            # f_name: m_name,
            # if len(m_reg_name) < 1:
            #    join_errors.append(_("Please enter your Name."))
            #   logging.info(f'  error NAME')
            # f_phone: m_phone,
            # if len(m_reg_phone) < 1:
            #    join_errors.append(_("Please enter your phone."))
            #   logging.info(f'  error phone')
            # check phone unic
            # if Profile.objects.filter(mobile=m_reg_phone).exists():
            #    join_errors.append(_("User with this phone already exists."))
            #   logging.info(f'  error phone already exists')
            # logging.info(f'  step 3 len(join_errors)={len(join_errors)}')
            # print("33")

            if len(join_errors) == 0:
                user = User.objects.create_user(m_reg_email, m_reg_email, m_reg_password)
                try:
                    t_profile = Profile()
                    t_profile.user_id = user.id
                    t_profile.date_joined = datetime.now()
                    t_profile.name = m_reg_name
                    t_profile.mobile = m_reg_phone
                    t_profile.email = m_reg_email
                    t_profile.adress = m_reg_adress
                    t_profile.date_birthday = m_reg_birthday
                    t_profile.i_doc = m_reg_id
                    t_profile.settings['url_path'] = m_url_path
                    t_profile.settings['reg_pass'] = m_reg_password
                    t_profile.save()
                    t_game_history = Game_history()
                    t_game_history.shop_code = m_reg_shopcode
                    t_game_history.save()
                    user.profile_id = t_profile.id
                    user.last_login = datetime.now()
                    user.save()
                except Exception as ex:
                    logging.info(f'  error {ex}')
                    print("user.delete", ex)
                    user.delete()
                    t_profile = None
                    join_errors = []
                    logging.info(f'  An error create PROFILE')

        if len(join_errors) > 0:
            m_return = {}
            m_return["success"] = False
            m_return["error"] = join_errors
            m_return["url_login"] = ""
            logging.info(f'  len(join_errors) > 0')
        else:
            if t_profile is not None:
                m_return = {}
                m_return["AnswerCod"] = '00'
                m_return["error"] = []
                #
                t_profile.hash = binascii.hexlify(os.urandom(16)).decode('utf-8')
                t_profile.save()
                m_scheme = request.scheme
                m_domain_name = get_current_site(request).name
                l_return_url = f"{m_scheme}://{m_domain_name}/ticket"
                logging.info(f'  success  l_return_url')
                print(f"l_return_url = {l_return_url}")
                m_return["RedirectUrl"] = l_return_url
            else:
                m_return = {}
                m_return["AnswerCod"] = "01"
                join_errors = []
                join_errors.append(_("An error occurred while creating the user profile, please try again later."))
                logging.info(f'  An error occurred while creating the user profile, please try again later.')
                m_return["error"] = join_errors
                m_return["RedirectUrl"] = ""
        print(f"m_return = {m_return}")
        return Response(m_return)
