# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import binascii
import os
import json
import datetime
import random

from dateutil.relativedelta import relativedelta
import logging
import logging.config

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from .models import (Profile, List_external_company, APIExtPage, APIExtHash, IdConfirmation,
                     Ticket_history, Blogger)
from .service.dft import get_GlobalSettings
from .service.report.report_data import report_data
from .service.service import get_main_args, check_template_exists


class ExtApi_AccessPermission(permissions.BasePermission):
    message = 'ExtApi_Registration customers not allowed.'

    def has_permission(self, request, view):
        m_headers = request.headers
        m_token = m_headers.get("Token", "")
        m_external_company_list = List_external_company.objects.filter(api_token=m_token, verbal="ext_reg")
        
        print(m_external_company_list)
        if m_external_company_list.count() > 0:
            m_Devices_list = m_external_company_list[0]
            print("permission yes")
            return True
        else:
            print("permission no")
            return False


# @csrf_exempt
class ext_reg(APIView):
    permission_classes = [ExtApi_AccessPermission]

    def post(self, request):
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
            m_data = request.data
            logging.info(f'  m_data   = {m_data}')
            m_reg_param = json.loads(m_data.get("reg_param", ""))
            '''
            m_reg_param =  {
            "reg_name": "qwerty", 
            "reg_email": "22qwerty@gmail.com", 
            "reg_password": "123456", 
            "reg_repeat_password": "123456", 
            "reg_phone": "1234567891", 
            "reg_birthday": null, 
            "reg_day": "01", 
            "reg_month": "01", 
            "reg_year": "2004", 
            "reg_id_doc": "1234567891", 
            "reg_city": "qwerty", 
            "reg_street": "qwerty", 
            "reg_building": "qwerty", 
            "reg_apartments": "123456", 
            "reg_reklama": "1"
            }            
            '''

            m_reg_name = m_reg_param.get("reg_name", "")
            m_reg_email = m_reg_param.get("reg_email", "")
            m_reg_password = m_reg_param.get("reg_password", "")
            m_reg_repeat_password = m_reg_param.get("reg_repeat_password", "")
            m_reg_phone = m_reg_param.get("reg_phone", "")
            m_reg_birthday = m_reg_param.get("reg_birthday", "")
            m_reg_day = m_reg_param.get("reg_day", "")
            m_reg_month = m_reg_param.get("reg_month", "")
            m_reg_year = m_reg_param.get("reg_year", "")
            m_reg_id_doc = m_reg_param.get("reg_id_doc", "")
            m_reg_city = m_reg_param.get("reg_city", "")
            m_reg_street = m_reg_param.get("reg_street", "")
            m_reg_building = m_reg_param.get("reg_building", "")
            m_reg_apartments = m_reg_param.get("reg_apartments", "")
            m_reg_reklama = m_reg_param.get("reg_reklama", "")
            m_url_path = m_reg_param.get("url_path", "")
            t_blogger_id = None
            if m_url_path != '':
                if Blogger.objects.filter(ref_hash=m_url_path).exists():
                    t_blogger_id = Blogger.objects.get(ref_hash=m_url_path).id

            logging.info(f'  m_reg_name             = {m_reg_name}')
            logging.info(f'  m_reg_email            = {m_reg_email}')
            logging.info(f'  m_reg_password         = {m_reg_password}')
            logging.info(f'  m_reg_repeat_password  = {m_reg_repeat_password}')
            logging.info(f'  m_reg_phone            = {m_reg_phone}')
            logging.info(f'  m_reg_birthday         = {m_reg_birthday}')
            logging.info(f'  m_reg_day              = {m_reg_day}')
            logging.info(f'  m_reg_month            = {m_reg_month}')
            logging.info(f'  m_reg_year             = {m_reg_year}')
            logging.info(f'  m_reg_id_doc           = {m_reg_id_doc}')
            logging.info(f'  m_reg_city             = {m_reg_city}')
            logging.info(f'  m_reg_street           = {m_reg_street}')
            logging.info(f'  m_reg_building         = {m_reg_building}')
            logging.info(f'  m_reg_apartments       = {m_reg_apartments}')
            logging.info(f'  m_reg_reklama          = {m_reg_reklama}')
            logging.info(f'  m_url_path             = {m_url_path}')

        except Exception as ex:
            m_body_data = {}
            t_profile = None
            join_errors.append("data error")
            logging.info(f'  data error    = {ex}')

        print ("11")
        print ("11")
        print ("11")
        if len(join_errors) == 0:
            # DO registartion
            # create token to login
            # check unic - m_reg_email  m_reg_phone  m_reg_id_doc
            t_profile = None
            if Profile.objects.filter(mobile=m_reg_phone, i_doc=m_reg_id_doc, user__email=m_reg_email ).exists():
                t_profile = Profile.objects.filter(mobile=m_reg_phone, i_doc=m_reg_id_doc, user__email=m_reg_email)[0]
                logging.info(f'  Profile exist')
            else:
                logging.info(f'  Profile not exist')
                print("22")
                print("22")
                ###
                # f_name: m_name,
                if len(m_reg_name) < 1:
                    join_errors.append(_("Please enter your Name."))
                    logging.info(f'  error NAME')
                # f_email: m_email,
                try:
                    validate_email(m_reg_email)
                except ValidationError:
                    join_errors.append(_("Please enter your Email/Login."))
                    logging.info(f'  error LOGIN')
                # check reg_email unic
                if User.objects.filter(email=m_reg_email).exists():
                    join_errors.append(_("User with this E-mail already exists."))
                    logging.info(f'  error LOGIN exist')
                if len(User.objects.filter(username=m_reg_email)) != 0:
                    join_errors.append(_("The mail you specified is already in use."))
                if len(User.objects.filter(email=m_reg_email)) != 0:
                    join_errors.append(_("The mail you specified is already in use."))
                # f_password: m_password,
                if len(m_reg_password) < 6:
                    join_errors.append(_("Password cannot be less than 6 characters."))
                    logging.info(f'  error Password cannot be less than 6 characters')
                # f_re_password: m_re_password,
                if m_reg_password != m_reg_repeat_password:
                    join_errors.append(_("Password mismatch."))
                    logging.info(f'  error Password mismatch')
                # f_phone: m_phone,
                if len(m_reg_phone) < 1:
                    join_errors.append(_("Please enter your phone."))
                    logging.info(f'  error phone')
                # check phone unic
                if Profile.objects.filter(mobile=m_reg_phone).exists():
                    join_errors.append(_("User with this phone already exists."))
                    logging.info(f'  error phone already exists')
                # 'f_day': ['01'], 'f_month': ['January'], 'f_year': ['2004']
                m_reg_birthday = None
                try:
                    m_temp_18year = datetime.datetime.today() - relativedelta(years=18, hour=0, minute=0, second=0, microsecond=0)
                    m_temp_birthday = f"{m_reg_year}{m_reg_month}{m_reg_day}"
                    m_temp_birthday = datetime.datetime.strptime(m_temp_birthday , "%Y%m%d")
                    # проверить на 18 лет
                    if m_temp_birthday > m_temp_18year:
                        join_errors.append(_("Your not have 18 years."))
                        logging.info(f'  error Your not have 18 years')
                except Exception as ex:
                    print("birthday == ", ex)
                    join_errors.append(_("please enter the correct date of your birth."))
                    logging.info(f'  error please enter the correct date of your birth')
                # f_id: m_id,
                if len(m_reg_id_doc) < 1:
                    join_errors.append(_("Please enter your ID."))
                    logging.info(f'  error ID')
                # check ID unic
                if Profile.objects.filter(i_doc=m_reg_id_doc).exists():
                    join_errors.append(_("User with this ID already exists."))
                    logging.info(f'  error ID already exists')
                if len(m_reg_city) < 1:
                    join_errors.append(_("Please enter your City."))
                    logging.info(f'  error City')
                if len(m_reg_street) < 1:
                    join_errors.append(_("Please enter your Street."))
                    logging.info(f'  error Street')
                if len(m_reg_building) < 1:
                    join_errors.append(_("Please enter your Building."))
                    logging.info(f'  error Building')
                if len(m_reg_apartments) < 1:
                    join_errors.append(_("Please enter your Apartments."))
                    logging.info(f'  error Apartments')

                if m_reg_reklama == "1":
                    m_reg_reklama = True
                else:
                    m_reg_reklama = False

                logging.info(f'  step 3 len(join_errors)={len(join_errors)}')
                print("33")

                if len(join_errors) == 0:
                    user = User.objects.create_user(m_reg_email, m_reg_email, m_reg_password)
                    try:
                        t_profile = Profile()
                        t_profile.user_id = user.id
                        t_profile.date_joined = datetime.datetime.now()
                        t_profile.name = m_reg_name
                        t_profile.mobile = m_reg_phone
                        if m_reg_birthday is not  None:
                            t_profile.date_birthday = m_reg_birthday
                        t_profile.i_doc = m_reg_id_doc
                        t_profile.city = m_reg_city
                        t_profile.street = m_reg_street
                        t_profile.building = m_reg_building
                        t_profile.apartments = m_reg_apartments
                        t_profile.reklama = m_reg_reklama
                        t_profile.first_login = True
                        t_profile.mail_confirmed = True
                        if t_blogger_id:
                            t_profile.settings['ref_blogger_id'] = t_blogger_id
                        t_profile.settings['url_path'] = m_url_path
                        t_profile.save()
                        user.profile_id = t_profile.id
                        user.last_login = datetime.datetime.now()
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
                m_return["success"] = True
                m_return["error"] = []
                #
                t_profile.hash = binascii.hexlify(os.urandom(16)).decode('utf-8')
                t_profile.save()
                m_scheme = request.scheme
                m_domain_name = get_current_site(request).name
                l_return_url = f"{m_scheme}://{m_domain_name}/loginext/{t_profile.hash}/"
                logging.info(f'  success  l_return_url')
                print(f"l_return_url = {l_return_url}")
                m_return["url_login"] = l_return_url
            else:
                m_return = {}
                m_return["success"] = False
                join_errors = []
                join_errors.append(_("An error occurred while creating the user profile, please try again later."))
                logging.info(f'  An error occurred while creating the user profile, please try again later.')
                m_return["error"] = join_errors
                m_return["url_login"] = ""

        print ("m_return = ", m_return)
        return Response(m_return)


# Для TV system
class ApiExtPagePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        m_token = request.headers.get("Token", "")
        m_page = request.headers.get('page')
        if not List_external_company.objects.filter(api_token=m_token).exists():
            return False
        m_company_verbal = List_external_company.objects.get(api_token=m_token).verbal
        if APIExtPage.objects.filter(caption=m_page).exists() and m_company_verbal in \
                APIExtPage.objects.get(caption=m_page).allowed_companies:
            return True
        return False


class ApiExtPage(APIView):
    permission_classes = [ApiExtPagePermission]

    def get(self, request):
        m_page = request.headers.get('page')
        m_GL_LIST = get_GlobalSettings()
        m_scheme = m_GL_LIST.get("GL_Subs_return_url_sh", "")
        m_domain_name = m_GL_LIST.get("GL_Subs_return_url_dom", "")
        t_api_ext_hash = APIExtHash()
        t_api_ext_hash.api_hash = ''.join([str(random.randrange(1, 9)) for i in range(6)])
        t_api_ext_hash.page = APIExtPage.objects.get(caption=m_page)
        t_api_ext_hash.dt_add = datetime.datetime.now()
        t_api_ext_hash.api_link = f'{m_scheme}://{m_domain_name}/ext_page/{t_api_ext_hash.api_hash}/'
        t_api_ext_hash.save()
        return Response({'link': t_api_ext_hash.api_link})


def get_add_api_dict(t_page_item):
    t_page_params = t_page_item.add_param
    today_date = datetime.datetime.now().date()
    add_api_dict = {}
    if 'default_daterange_1' in t_page_params:
        date_start_range_1 = today_date + relativedelta(days=-t_page_params.get('default_daterange_1'))
        dr_1_text = (f'{datetime.datetime.strftime(date_start_range_1, "%d.%m.%Y")}'
                     f'-{datetime.datetime.strftime(today_date, "%d.%m.%Y")}')
        add_api_dict['daterange_1'] = dr_1_text
    if 'default_daterange_2' in t_page_params:
        date_start_range_2 = today_date + relativedelta(days=-t_page_params.get('default_daterange_2'))
        dr_2_text = (f'{datetime.datetime.strftime(date_start_range_2, "%d.%m.%Y")}'
                     f'-{datetime.datetime.strftime(today_date, "%d.%m.%Y")}')
        add_api_dict['daterange_2'] = dr_2_text
    if 'default_lang' in t_page_params:
        add_api_dict['lang'] = t_page_params.get('default_lang')
    return add_api_dict


def get_page_args(page_name=None):
    args = {}
    if page_name == 'users':
        args['list_users'] = Profile.objects.all().annotate(num_tickets=Count('user__game_user__games_id_history')
                                                            ).order_by("-date_joined")
        args['without_buttons'] = True
    elif page_name == 'id_confirmations':
        args['conf_list'] = IdConfirmation.objects.all().order_by('-id')
    elif page_name == 'tickets':
        _list_tickets = Ticket_history.objects.all().order_by("-req_dt")[:20]
        args['list_tickets'] = _list_tickets
        # args['l_body_list'].append(check_template_exists("cab_boss/cabb_tickets.html"))
        args['l_tickets_body'] = check_template_exists("cab_boss/cabb_tickets_body.html")
    args['without_buttons'] = True
    return args


def ext_page(request, api_hash=None):
    args = get_main_args(request, section="main")
    args['l_head_list'] = [check_template_exists("api_ext_pages/l_head.html")]
    args['l_script_list'] = [check_template_exists("api_ext_pages/l_script.html")]
    args['l_layout_file'] = check_template_exists("api_ext_pages/layout.html")
    args['main_tab'] = check_template_exists("cab_boss/cabinet.html")
    args['l_body_list'] = [check_template_exists(f"api_ext_pages/error_2319.html")]
    if APIExtHash.objects.filter(api_hash=api_hash, enabled=True).exists():
        page_to_show = APIExtHash.objects.get(api_hash=api_hash).page
        try:
            if 'Rep' in page_to_show.caption:
                args['report_list'], args_add = report_data(request, verbal=page_to_show.caption,
                                                            add_api=get_add_api_dict(page_to_show))
                args.update(args_add)
            else:
                args.update(get_page_args(page_to_show.caption))
            status_code = 200
            args['l_body_list'] = [check_template_exists(page_to_show.template)]
        except:
            status_code = 500
        api_hash = APIExtHash.objects.get(api_hash=api_hash)
        api_hash.enabled = False
        api_hash.save()
    else:
        status_code = 500
    return render(request, args['main_tab'], args, status=status_code)





