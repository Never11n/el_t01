#! /usr/bin/env python
# -*- coding: utf-8 -*-
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
from .mail_service import send_mail_user
from .models import Profile, User, Blogger, Discount, DiscountHistory, DiscountList, Game_history, MessWhatsapp
from .service.service import get_main_args, send_sms_01
from .service.dft import (get_GlobalSettings)
from .bot_mess.message_send import message_send


def login(request):
    args = get_main_args(request)
    if args['logged_in']:
        return redirect('/')
    if request.POST:
        print(request.POST)
        m_username = request.POST.get('fl_email', '').lower()
        m_password = request.POST.get('fl_password', '')
        m_redirect_url =  request.POST.get('fl_redirect_url', '')
        user = auth.authenticate(username=m_username, password=m_password)
        if 'fl_remember_me' in request.POST:
            SESSION_EXPIRE_AT_BROWSER_CLOSE = False
        else:
            SESSION_EXPIRE_AT_BROWSER_CLOSE = True
        print ("user = ", user )
        print ("m_password = ", m_password )
        if user is not None:
            print ("user not None")
            m_ver_reg = 2
            if m_ver_reg == 1:
                if user.profile.mail_confirmed:
                    print("mail_confirmed")
                    profile = Profile.objects.get(id=user.profile.id)
                    profile.hash = ''
                    profile.save()
                    auth.login(request, user)
                    if args['globalset'].get("BoolMobConfirm","111") == "111":
                        if user.profile.mobile_confirmed:
                            return redirect('/cabinet')
                        else:
                            request.session['user_id'] = user.id
                            return redirect('/mobile-confirmed')
                    else:
                        return redirect('/cabinet')
                else:
                    return redirect('/')
            if m_ver_reg == 2:
                profile = Profile.objects.get(id=user.profile.id)
                profile.hash = ''
                profile.save()
                auth.login(request, user)
                m_game_gift_id = request.POST.get('game_gift_id_login', '')
                if m_game_gift_id != '':
                    try:
                        t_game_history = Game_history.objects.get(id=m_game_gift_id)
                        t_game_history.user_recipient = user
                        t_game_history.save()
                        return redirect(f'/cab-game-play/{t_game_history.id}/')
                    except:
                        pass
                if m_redirect_url == "":
                    return redirect('/cabinet')
                else:
                    return redirect(m_redirect_url)
        else:
            return redirect('/')
    else:
        return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')


def logout_timeout(request):
    auth.logout(request)
    answer = {"AnswerCod": "00"}
    return JsonResponse(answer)


def check_username(request):
    print ("check_username")
    try:
        user = User.objects.get(email=str(request.GET['u_name']))
        answer = {"AnswerCod": "01",
                  "AnswerText": _("exist")}
    except Exception as ex:
        answer = {"AnswerCod": "00",
                  "AnswerText": ""}
    print ("answer = ", answer)
    return JsonResponse(answer)


def register_user(request):
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
            profile.date_joined = datetime.now()
            profile.name = args['reg_name']
            profile.mobile = args['reg_phone']
            if args['reg_birthday'] is not None:
                profile.date_birthday = args['reg_birthday']
            profile.i_doc = args['reg_id_doc']
            profile.city = args['reg_city']
            profile.street = args['reg_street']
            profile.building = args['reg_building']
            profile.apartments = args['reg_apartments']
            profile.reklama = args['reg_reklama']
            profile.first_login = True
            profile.save()
            user.profile_id = profile.id
            user.last_login = datetime.now()
            user.save()

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
        return redirect('/')


def register_add_blogger_and_discount(profile, url_path, profile_update=True):
    t_blogger_id = None
    t_blogger_last_discount = None
    if Blogger.objects.filter(ref_hash=url_path).exists():
        t_blogger_id = Blogger.objects.get(ref_hash=url_path).id
        t_blogger_discount_lists = DiscountList.objects.filter(
            enabled=True, owner__verbal='bloger', id_owner=t_blogger_id).order_by('-id')
        if t_blogger_discount_lists.exists():
            t_blogger_last_discount = t_blogger_discount_lists[0]
    if t_blogger_id is not None:
        if profile_update:
            profile.settings['ref_blogger_id'] = t_blogger_id
            profile.save()
        if t_blogger_last_discount is not None:
            t_discount_history = DiscountHistory()
            t_discount_history.discount = t_blogger_last_discount.discount
            t_discount_history.all_users = False
            t_discount_history.user = profile.user
            t_discount_history.start_date = datetime.now()
            discount_hours = t_blogger_last_discount.duration_hours
            t_discount_history.stop_date = datetime.now() + relativedelta(hours=discount_hours)
            t_discount_history.save()


def register_add_get_param(profile, get_param):
    try:
        get_param = json.loads(get_param)
        profile.settings['get_param'] = get_param
        profile.save()
        m_sub_1 = profile.settings['get_param'].get("sub_1", "")
        if m_sub_1:
            url = f"https://qualityleadskeitaro.website/f604f2a/postback?subid={m_sub_1}&status=lead&from=scratch-win_sem4ik"
            response = requests.request("GET", url)
            profile.settings['response_vadim_1'] = [response.status_code, response.text]
            url = f"https://hishline.fun/3b35be8/postback?subid={m_sub_1}&status=lead&from=scratch-win_sem4ik"
            response = requests.request("GET", url)
            profile.settings['response_vadim_2'] = [response.status_code, response.text]
            profile.save()
    except:
        pass


def register_add_whatsapp_instance(profile):
    whatsapp_instances = MessWhatsapp.objects.filter(enabled=True)
    correct_instance = None
    for instance in whatsapp_instances:
        if instance.mess_whatsapp_users.count() < instance.max_users:
            correct_instance = instance
            break
        else:
            continue
    if correct_instance:
        profile.mess_whatsapp = correct_instance
        profile.save()
    else:
        d_globalset = get_GlobalSettings()
        data_for_bot_sms = {
            "company": d_globalset.get("GL_Name_Company", ""),
            "client_name": profile.name,
            "client_email": profile.user.email,
            "client_phone": profile.mobile,
            "messenger": "telegram",
            "message_type": "fail_set_whatsapp_instance",
        }
        try:
            message_send(data_for_bot_sms)
        except:
            pass


def register_check_gift_game(user, game_gift_id):
    try:
        t_game_history = Game_history.objects.get(id=game_gift_id)
        t_game_history.user_recipient = user
        t_game_history.save()
        answer = {'AnswerCod': '00gift', 'RedirectUrl': f'/cab-game-play/{t_game_history.id}/'}
        return answer
    except:
        return False


def check_userlogin(request):
    if request.GET:
        m_username = request.GET.get('fl_email', '').lower()
        m_password = request.GET.get('fl_password', '')
        user = auth.authenticate(username=m_username, password=m_password)
        try:
            if user is not None:
                answer = {"AnswerCod": "00",
                          "AnswerText": ""}
            else:
                answer = {"AnswerCod": "01",
                          "AnswerText": _("Incorrect e-mail and/or password.")}
        except:
            answer = {"AnswerCod": "01",
                      "AnswerText": _("Incorrect e-mail and/or password.")}

        return JsonResponse(answer)
    else:
        return redirect('/')


def confirmation(request):
    _hash = request.GET.get('h', '')
    _hash_clear = request.GET.get('h_cl', '')
    if _hash != '':
        try:
            profile = Profile.objects.get(hash=_hash)
        except:
            return redirect('/')
        profile.mail_confirmed = True
        profile.save()
        user = User.objects.get(id=profile.user_id)
        auth.login(request, user)
        return redirect('/cabinet/')
        # return redirect('/settings')
    if _hash_clear != '':
        try:
            profile = Profile.objects.get(hash=_hash_clear)
            profile.hash = ''
            profile.save()
            return HttpResponse("ok", content_type='text/plain')
        except:
            return HttpResponse("er", content_type='text/plain')


# def recovery(request):
#     args = get_main_args(request, section="main")
#     if request.method == 'POST':
#         m_fl_email_recovery = request.POST.get('fl_email_recovery', '').replace(' ', '').lower()
#         try:
#             user = User.objects.get(email=m_fl_email_recovery)
#             profile = Profile.objects.get(id=user.profile.id)
#             profile.hash = binascii.hexlify(os.urandom(16)).decode('utf-8')
#             profile.save()
#             user.profile = profile
#             args['user'] = user
#             send_mail_user(request, user.id, "recovery")
#             return redirect('/recovery-ok/')
#         except Exception as ex:
#             return redirect('/')
#     else:
#         return redirect('/')


def recovery(request):
    args = get_main_args(request, section="main")
    if request.method == 'POST':
        m_recovery_type = request.POST.get('recoveryType', '')
        if m_recovery_type == 'email':
            m_email = request.POST.get('fl_email_recovery', '').replace(' ', '').lower()
            user = User.objects.get(email=m_email)
            new_pass = m_email[:4] + ''.join(([str(random.randrange(1, 9)) for i in range(6)]))
            user.set_password(new_pass)
            user.save()
            send_mail_user(request, user_id=user.id, type_mess='recovery', l_password=new_pass)
            return redirect('/recovery-ok/')

        elif m_recovery_type == 'phone':
            m_phone = request.POST.get('fl_phone_recovery', '').replace(' ', '')
            profile = Profile.objects.get(mobile=m_phone)
            user = User.objects.get(profile=profile)
            new_pass = user.email[:4] + ''.join(([str(random.randrange(1, 9)) for i in range(6)]))

            m_receiver_phone_code = ""
            m_receiver_phone = m_phone
            m_sender_phone_from = args.get("GL_SMS_from", "")
            m_sms_text = f'Your login: {user.email} \n New password: {new_pass}'
            m_sms_send, m_sms_answ = send_sms_01(m_receiver_phone_code, m_receiver_phone, m_sender_phone_from,
                                                 m_sms_text, args)
            print(m_sms_send)
            print(m_sms_answ)
            if 'SUCCESS' in m_sms_answ:
                user.set_password(new_pass)
                user.save()
                return redirect('/recovery-phone-ok/')
        else:
            return redirect('/recovery-not-ok/')
    else:
        return redirect('/recovery-not-ok/')


def check_loginrecovery(request):
    args = get_main_args(request)
    answer = {"AnswerCod": "00", "AnswerText": ""}
    email = request.GET.get('fl_email')
    phone = request.GET.get('fl_phone')
    if email:
        email = email.replace(' ', '').lower()
        if not User.objects.filter(email=email).exists():
            answer = {"AnswerCod": "01", "AnswerText": _("User with the specified e-mail does not exist.")}
    if phone:
        phone = phone.replace(' ', '')
        if not Profile.objects.filter(mobile=phone).exists():
            answer = {"AnswerCod": "01", "AnswerText": _("User with the specified phone does not exist.")}
    return JsonResponse(answer)


def forgot_password(request):
    args = get_main_args(request)
    try:
        _hash = str(request.GET.get('h'))
        args['profile'] = Profile.objects.get(hash=_hash)
        args['hash'] = _hash
        args['menu_item'] = ""
        args['l_body_list'].append(f"{args['GL_MainSkin']}/auth/set_password.html")
        args['main_tab'] = f"{args['GL_MainSkin']}/auth/auth.html"
        return render(request, args['main_tab'], args)
    except:
        print("_hash = 5")
        return redirect('/')


def set_password(request):
    print ("set_password")
    args = get_main_args(request)
    if request.POST:
        try:
            m_hash = str(request.POST.get('hash'))
            m_password_1 = str(request.POST.get('fl_set_password1'))
            m_password_2 = str(request.POST.get('fl_set_password2'))
            m_profile = Profile.objects.get(hash=m_hash)
            m_profile.hash = ""
            m_profile.save()
            user = User.objects.get(id=m_profile.user_id)
            user.set_password(m_password_1)
            user.save()
            auth.login(request, user)
        except:
            pass
    return redirect('/')


def mobile_confirmed(request):
    print ("mobile_confirmed")
    # print ("request.session['email'] = ", request.session['user_id'])
    # m_user_id = request.session.get('user_id',None)
    args = get_main_args(request, section="main")
    print("args['lang'] = ", args['lang'])
    if not args['logged_in']:
        return redirect('/')
    else:
        args['menu_item'] = ""
        args['l_body_list'].append('auth/mobile_confirmed.html')
        args['main_tab'] = 'auth/auth.html'
        return render(request, args['main_tab'], args)


    # if m_user_id == None:
    #     return redirect('/')
    # else:
    #     try:
    #         args['profile'] = Profile.objects.get(user_id=m_user_id)
    #     except Exception as ex:
    #         print ("ex = ", ex)
    #


    # _code = str(request.GET.get('h'))
    # _code = "3569"
    # loc_tel_code = "972"
    # loc_tel = "0543139995"
    # loc_tel_from = "0528373418"
    # loc_tel_from = "WinWin-HISHGAD"
    # loc_txt = f"your verification code {_code}"
    # m_payload, m_response_text = send_sms_01(loc_tel_code, loc_tel, loc_tel_from, loc_txt)
    # print ("m_payload, m_response_text = ", m_payload, m_response_text)


    # args['profile'] = Profile.objects.get(hash=_hash)
    # args['hash'] = _hash
    #
    # try:
    #     _hash = str(request.GET.get('h'))
    #     args['profile'] = Profile.objects.get(hash=_hash)
    #     args['hash'] = _hash
    #     args['menu_item'] = ""
    #     args['l_body_list'].append('auth/set_password.html')
    #     args['main_tab'] = 'auth/auth.html'
    #     return render(request, args['main_tab'], args)
    # except:
    #     print("_hash = 5")
    #     return redirect('/')

def mobile_confirmed_code(request):
    print ("mobile_confirmed_code")
    # print ("request.session['email'] = ", request.session['user_id'])
    # m_user_id = request.session.get('user_id',None)
    # args = get_main_args(request, section="main")
    # print("args['lang'] = ", args['lang'])
    # if not args['logged_in']:
    #     return redirect('/')
    # else:
    #     args['menu_item'] = ""
    #     args['l_body_list'].append('auth/mobile_confirmed.html')
    #     args['main_tab'] = 'auth/auth.html'
    #     return render(request, args['main_tab'], args)


def mobile_confirmed_confirm(request):
    print ("mobile_confirmed_confirm")
    # print ("request.session['email'] = ", request.session['user_id'])
    # m_user_id = request.session.get('user_id',None)
    # args = get_main_args(request, section="main")
    # print("args['lang'] = ", args['lang'])
    # if not args['logged_in']:
    #     return redirect('/')
    # else:
    #     args['menu_item'] = ""
    #     args['l_body_list'].append('auth/mobile_confirmed.html')
    #     args['main_tab'] = 'auth/auth.html'
    #     return render(request, args['main_tab'], args)

def contact_save(request):
    print ("mobile_confirmed_confirm")
    if request.POST:
        m_username = request.POST.get('fl_email', '').lower()
        m_password = request.POST.get('fl_password', '')
        m_password = request.POST.get('fl_password', '')

        try:
            if user is not None:
                answer = {"AnswerCod": "00",
                          "AnswerText": ""}
            else:
                answer = {"AnswerCod": "01",
                          "AnswerText": _("Incorrect e-mail and/or password.")}
        except:
            answer = {"AnswerCod": "01",
                      "AnswerText": _("Incorrect e-mail and/or password.")}

        return JsonResponse(answer)
    else:
        return redirect('/')


def login_ext(request, verbal=None):
    print ("verbal = ", verbal)
    args = get_main_args(request, section="main")
    args['verbal'] = verbal

    t_profile = Profile.objects.filter(hash=verbal)
    if len(t_profile) == 1:
        t_profile = t_profile[0]
        t_profile.hash = ""
        t_profile.save()
        t_profile.save()
        user = User.objects.get(id=t_profile.user_id)
        auth.login(request, user)
        return redirect('/cabinet/')
    else:
        return redirect('/')
