import binascii
import os
import json
import requests
import random
from dateutil.relativedelta import relativedelta
from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from .models import Profile, Game_history, User
from .service.service import get_main_args, send_sms_01
from .views_ex_reg import valid_input


# def login_shop(request):
#     args = get_main_args(request)
#     m_return = {}
#     if request.POST:
#         print(request.POST)
#         m_id = request.POST.get('f_id', '').lower()
#         m_username = request.POST.get('f_id', '').lower()
#         m_phone = request.POST.get('f_phone', '')
#         user = auth.authenticate(m_username=m_username, password=m_phone)
#         print ("user = ", user )
#         print ("m_password = ", m_phone )
#         if user is not None:
#             print ("user not None")
#             auth.login(request, user)
#             m_return["AnswerCod"] = '00'
#             return m_return
def login_shop(request):
    args = get_main_args(request)
    m_return = {}
    if request.POST:
        print(request.POST)
        m_i_doc = request.POST.get('f_id', '').lower()
        m_phone = request.POST.get('f_phone', '')
        m_phone = m_phone.replace('+', '')
        print(m_phone)
        m_club_member = request.POST.get('f_clubcode', '')

        if m_i_doc or m_phone or m_club_member:
            _profile = Profile.objects.all()

            if m_phone and len(m_phone) == 12:
                print('**')
                _profile = _profile.filter(mobile=m_phone)
                m_profile = _profile.first()

                if not m_profile:
                    print(m_profile)
                    m_return['AnswerCod'] = '01'
                    m_return['AnswerText'] = 'You`re entered a wrong phone number'
                    return JsonResponse(m_return)

                phone_code_lst = [str(random.randrange(1, 9)) for i in range(4)]
                phone_code = ''.join(phone_code_lst)
                m_profile.phone_code = phone_code
                m_profile.save()

                m_receiver_phone_code = ""
                m_receiver_phone = m_phone
                m_sender_phone_from = args.get("GL_SMS_from", "")
                m_sms_text = f'Your code: {phone_code}'
                print(m_sms_text)
                m_sms_send, m_sms_answ = send_sms_01(m_receiver_phone_code, m_sender_phone_from, m_receiver_phone,
                                                     m_sms_text, args)
                print(m_sms_send)
                print(m_sms_answ)
                m_return['AnswerCod'] = '00'
                m_return['Profile_id'] = m_profile.id

                print(m_return)
                return JsonResponse(m_return)

            if m_i_doc:
                _profile = _profile.filter(i_doc=m_i_doc)
                m_profile = _profile.first()

                if not m_profile:
                    m_return['AnswerCod'] = '01'
                    m_return['AnswerText'] = 'You have entered a wrong id'
                    return JsonResponse(m_return)

                print(m_profile)
                m_return['AnswerCod'] = '01'
                m_return['AnswerText'] = 'Please enter your phone number'
                m_return['Profile_id'] = m_profile.id
                return JsonResponse(m_return)

            if m_club_member:
                _profile = _profile.filter(club_code=m_club_member)
                m_profile = _profile.first()

                if not m_profile:
                    m_return['AnswerCod'] = '01'
                    m_return['AnswerText'] = 'We haven`t got your club code'
                    return JsonResponse(m_return)

                m_return['AnswerCod'] = '01'
                m_return['AnswerText'] = 'We haven`t got your club code'
                m_return['Profile_id'] = m_profile.id
                return JsonResponse(m_return)


def phone_code_verification(request):
    m_return = {}
    m_answer_code = request.POST.get('f_phonecode', '')
    m_profile_id = request.POST.get('profile_id', '')
    profile = Profile.objects.filter(id=int(m_profile_id)).first()
    if m_answer_code == profile.phone_code:
        m_return['AnswerCod'] = '00'
        # auth.login(request, m_profile_id)
        return JsonResponse(m_return)
    m_return['AnswerCod'] = '01'
    return JsonResponse(m_return)

