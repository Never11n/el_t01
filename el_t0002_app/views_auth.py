import binascii
import os
import json
import requests
import random
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.contrib import auth
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from el_t01_app.models import Profile, User, Blogger, Discount, DiscountHistory, DiscountList, Game_history, MessWhatsapp
from el_t01_app.service.service import get_main_args, send_sms_01
from el_t01_app.service.dft import (get_GlobalSettings)

def reg_shop_user(request):
    print("register_user")
    args = get_main_args(request, section="main")
    join_errors = []
    if request.method == 'POST':
        print ('POST = ', request.POST)
        # f_name: m_name,
        args['reg_name'] = request.POST.get('f_name', '').strip()
        if len(args['reg_name']) < 1:
            join_errors.append(_("Please enter your Name."))
        # f_email: m_email,
        args['reg_email'] = request.POST.get('f_email', '').replace(' ', '').lower()
        # f_shopcode : m_shopcode
        args['reg_shopcode'] = request.POST.get('f_shopcode', '')
        print(args['reg_shopcode'])
        try:
            validate_email(args['reg_email'])
        except ValidationError:
            join_errors.append(_("Please enter your Email/Login."))
        # check reg_email unic
        if User.objects.filter(email=args['reg_email']).exists():
            join_errors.append(_("User with this E-mail already exists."))

        # f_password: m_password,
        args['reg_password'] = str(request.POST.get('f_password', '')).strip()
        if len(args['reg_password']) < 6:
            join_errors.append(_("Password cannot be less than 6 characters."))
        # f_re_password: m_re_password,
        args['reg_repeat_password'] = str(request.POST.get('f_re_password', '')).strip()
        if args['reg_password'] != args['reg_repeat_password']:
            join_errors.append(_("Password mismatch."))
        if len(User.objects.filter(username=args['reg_email'])) != 0:
            join_errors.append(_("The mail you specified is already in use."))
        if len(User.objects.filter(email=args['reg_email'])) != 0:
            join_errors.append(_("The mail you specified is already in use."))
        # f_phone: m_phone,
        args['reg_phone'] = request.POST.get('f_phone', '').strip()
        if len(args['reg_phone']) < 1:
            join_errors.append(_("Please enter your phone."))
        # 'f_day': ['01'], 'f_month': ['January'], 'f_year': ['2004']
        # check phone unic
        if Profile.objects.filter(mobile=args['reg_phone']).exists():
            join_errors.append(_("User with this phone already exists."))

        args['reg_birthday'] = None
        args['reg_day'] = request.POST.get('f_day', '').strip()
        args['reg_month'] = request.POST.get('f_month', '').strip()
        args['reg_year'] = request.POST.get('f_year', '').strip()

        m_temp_18year = datetime.today() - relativedelta(years=18, hour=0, minute=0, second=0, microsecond=0)
        print ("m_temp_18year = ", m_temp_18year)
        m_temp_birthday = f"{args['reg_year']}{args['reg_month']}{args['reg_day']}"
        print ("m_temp_birthday = ", m_temp_birthday )
        # m_temp_birthday = f"{'2022'}{'01'}{'29'}"
        m_temp_birthday = datetime.strptime(m_temp_birthday, "%Y%m%d")
        print("m_temp_birthday = ", m_temp_birthday)
        args['reg_birthday'] = m_temp_birthday
        # проверить на 18 лет
        if m_temp_birthday > m_temp_18year:
            print ("m_temp_birthday > m_temp_18year")
        try:
            m_temp_18year = datetime.today() - relativedelta(years=18, hour=0, minute=0, second=0, microsecond=0)
            m_temp_birthday = f"{args['reg_year']}{args['reg_month']}{args['reg_day']}"
            # m_temp_birthday = f"{'2022'}{'01'}{'29'}"
            m_temp_birthday = datetime.strptime(m_temp_birthday , "%Y%m%d")
            args['reg_birthday'] = m_temp_birthday
            # проверить на 18 лет
            if m_temp_birthday > m_temp_18year:
                join_errors.append(_("Your not have 18 years."))
        except Exception as ex:
            print("birthday == ", ex)
            join_errors.append(_("please enter the correct date of your birth."))
        # f_id: m_id,
        args['reg_id_doc'] = request.POST.get('f_id', '').strip()
        if len(args['reg_id_doc']) < 1:
            join_errors.append(_("Please enter your ID."))
        # check ID unic
        if Profile.objects.filter(i_doc=args['reg_id_doc']).exists():
            join_errors.append(_("User with this ID already exists."))

        args['reg_city'] = request.POST.get('f_city', '').strip()
        if len(args['reg_city']) < 1:
            join_errors.append(_("Please enter your City."))
        args['reg_street'] = request.POST.get('f_street', '').strip()
        if len(args['reg_street']) < 1:
            join_errors.append(_("Please enter your Street."))
        args['reg_building'] = request.POST.get('f_building', '').strip()
        if len(args['reg_building']) < 1:
            join_errors.append(_("Please enter your Building."))
        args['reg_apartments'] = request.POST.get('f_apartments', '').strip()
        if len(args['reg_apartments']) < 1:
            join_errors.append(_("Please enter your Apartments."))

        args['reg_reklama'] = request.POST.get('f_reklama', '0').strip()
        print ("args['reg_reklama'] = ", args['reg_reklama'])
        if args['reg_reklama'] == "1":
            args['reg_reklama'] = True
        else:
            args['reg_reklama'] = False
        print("args['reg_reklama'] = ", args['reg_reklama'])
        if len(join_errors) > 0:
            print ("join_errors = ", join_errors)
            answer = {"AnswerCod": "01",
                      "AnswerText": join_errors[0]}
            return JsonResponse(answer)
        m_url_path = request.POST.get('f_url_path', '')
        m_get_param = request.POST.get('f_get_param', '')
        m_game_gift_id = request.POST.get('f_game_gift_id', '')
        user = User.objects.create_user(args['reg_email'], args['reg_email'], args['reg_password'])
        try:
            profile = Profile()
            profile.hash = binascii.hexlify(os.urandom(16)).decode('utf-8')
            profile.user_id = user.id
            profile.name = args['reg_name']
            profile.mobile = args['reg_phone']
            profile.save()
            user.profile_id = profile.id
            user.last_login = datetime.now()
            user.save()

            game_history = Game_history()
            game_history.shop_code = args['reg_shopcode']
            game_history.t_status_id = 1 
            game_history.save()

            profile.mail_confirmed = True
            profile.save()
            auth.login(request, user)

            if m_url_path != '':
                register_add_blogger_and_discount(profile, m_url_path, True)
            register_add_get_param(profile, m_get_param)
            if profile.reklama is True:
                register_add_whatsapp_instance(profile)
            if m_game_gift_id != '':
                answer = register_check_gift_game(user, m_game_gift_id)
                if answer:
                    return JsonResponse(answer)

            if args['GL_CONFIRMATION_REGISTRATION']:
                # send_mail_user(request, user.id, "registration")
                answer = {"AnswerCod": "00",
                          "AnswerText": _("Для подтверждения своей учётной записи следуйте инструкциям на Вашей почте.")}
            else:
                answer = {"AnswerCod": "00",
                          "AnswerText": _("Ожидайте подтверждения Вашей учётной записи.")}
            return JsonResponse(answer)
        except Exception as ex:
            print("user.delete", ex)
            user.delete()
            join_errors.append('server_error')
            args['register_page_guest'] = True
            answer = {"AnswerCod": "01",
                      "AnswerText": _("Во время создания профиля пользователя произошла ошибка, повторите попытку позже.")}
            return JsonResponse(answer)
    else:
        return render(request, '002/registr.html')