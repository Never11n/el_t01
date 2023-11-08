#! /usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import os

from django.contrib.auth.models import User
# from django.core import mail
from django.core.mail import send_mail, get_connection, EmailMultiAlternatives
from django.template.loader import get_template
from django.utils import translation
from django.utils.translation import gettext
from django.contrib.sites.shortcuts import get_current_site
from validate_email import validate_email

from el_t01_app.models import EmailToSend, EmailSettings, Payout, Ticket_history
from el_t01_app.service.service import generate_hash
from el_t01_app.service.service import get_main_args
from el_t01_app.service.dft import get_GlobalSettings


def send_mail_user(request=None, user_id=None, type_mess=None, l_email=None, l_text=None, l_password=None,
                   l_payout_id=None, l_ticket_id=None):
    d_globalset = get_GlobalSettings()
    m_current_site_for_send = str(get_current_site(request)) if request else None
    mail_args = {
        "EMAIL_DEFAULT_FROM_EMAIL": d_globalset.get('GL_EMAIL_DEFAULT_FROM_EMAIL'),
        "EMAIL_HOST_USER_NAME": d_globalset.get('GL_EMAIL_HOST_USER_NAME'),
        "EMAIL_SERVICE_NAME": d_globalset.get('GL_EMAIL_SERVICE_NAME'),
        "EMAIL_LOGO_FOR_MAIL": d_globalset.get('GL_EMAIL_LOGO_FOR_MAIL'),
        "EMAIL_LINKS_SOCIAL_MEDIA": d_globalset.get('GL_EMAIL_LINKS_SOCIAL_MEDIA'),
        "EMAIL_LINK_INSTAGRAM": d_globalset.get('GL_EMAIL_LINK_INSTAGRAM'),
        "EMAIL_LINK_FACEBOOK": d_globalset.get('GL_EMAIL_LINK_FACEBOOK'),
        "EMAIL_LINK_YOUTUBE": d_globalset.get('GL_EMAIL_LINK_YOUTUBE'),
        "DOMAIN_OUTER": m_current_site_for_send
    }

    if user_id is not None:
        user = User.objects.get(id=user_id)
        m_recipient = user.email
    else:
        m_recipient = l_email
    email_is_valid = validate_email(m_recipient, verify=True)
    if not email_is_valid or not EmailSettings.objects.filter(verbal=type_mess).exists():
        return
    t_email_settings = EmailSettings.objects.get(verbal=type_mess)
    m_subject = t_email_settings.subject
    m_templ = f"{d_globalset.get('GL_MainSkin')}/{t_email_settings.mail_template}"
    m_text = t_email_settings.text
    m_layout_templ = t_email_settings.layout_template
    if m_layout_templ and m_layout_templ != '':
        m_layout_templ = f"{d_globalset.get('GL_MainSkin')}/{m_layout_templ}"
    else:
        m_layout_templ = f"{d_globalset.get('GL_MainSkin')}/mail/mail_layout.html"
    mail_args['layout_template'] = m_layout_templ
    m_attach_file = None
    if type_mess == "registration":
        mail_args['url'] = m_current_site_for_send + '/confirmation?h=' + str(user.profile.hash)
        mail_args['profile'] = user.profile

    elif type_mess == "recovery":
        m_subject = f"{d_globalset.get('GL_Name_Company')} - {m_subject}"
        mail_args['password'] = l_password
        mail_args['profile'] = user.profile

    elif type_mess == "feedback_replay":
        m_subject = f"{d_globalset.get('GL_Name_Company')} - {m_subject}"
        mail_args['text_replay'] = l_text

    elif type_mess == 'payout':
        t_payout = Payout.objects.get(id=l_payout_id)
        m_title = f"{t_payout.user_id.profile.name} שלום"
        m_link_site = d_globalset.get("GL_SMS_domen", "")
        m_image = t_payout.photo if t_payout.photo else None
        if m_image:
            m_image = f'{m_link_site}media/{m_image}'
        mail_args['m_image'] = m_image
        mail_args['m_link_site'] = m_link_site
        mail_args['m_title'] = m_title
    elif type_mess == 'cancel_lotto':
        t_ticket = Ticket_history.objects.get(id=l_ticket_id)
        m_title = f"{t_ticket.games_id.user_id.profile.name} שלום"
        mail_args['m_title'] = m_title
        m_link_site = d_globalset.get("GL_SMS_domen", "")
        mail_args['m_link_site'] = m_link_site
        m_attach_file = t_ticket.img_06
    elif type_mess == 'win_lotto':
        t_ticket = Ticket_history.objects.get(id=l_ticket_id)
        m_title = f"{t_ticket.games_id.user_id.profile.name} שלום"
        mail_args['m_title'] = m_title
        m_link_site = d_globalset.get("GL_SMS_domen", "")
        mail_args['m_link_site'] = m_link_site
    elif type_mess == 'lotto_subscription_ended':
        mail_args['m_title'] = 'lotto_subscription_ended'
    elif type_mess == 'lotto_subscription_payment_fail':
        mail_args['m_title'] = 'lotto_subscription_payment_fail'
    elif type_mess == 'lotto_subscription_payment_ok':
        mail_args['m_title'] = 'lotto_subscription_payment_ok'
    elif type_mess == 'add_extra':
        t_ticket = Ticket_history.objects.get(id=l_ticket_id)
        m_attach_file = t_ticket.img_06
        mail_args['m_title'] = 'Your ticket have extra!!!'
    else:
        return
    mail_args['m_text'] = m_text
    if m_attach_file:
        save_and_send_email(request, m_recipient, m_subject, m_templ, mail_args, attach_file=m_attach_file)
    else:
        save_and_send_email(request, m_recipient, m_subject, m_templ, mail_args)


def save_and_send_email(request, recipient, subject, template, context, loc_lang='', attach_file=None):
    print("save_and_send_email")
    m_old_lang = translation.get_language()
    if loc_lang != '':
        translation.activate(loc_lang)
    email = EmailToSend()
    email.hash = generate_hash(50)
    email.save()
    if loc_lang != '':
        translation.activate(m_old_lang)
    try:
        recipient_provider = str(recipient).split('@')[1]
        # recipient_provider_is_blocked = recipient_provider in BLOCKED_EMAIL_PROVIDERS
        recipient_provider_is_blocked = recipient_provider in ""
    except:
        recipient_provider_is_blocked = False
    if not recipient_provider_is_blocked:
        try:
            d_globalset = get_GlobalSettings()
            EMAIL_HOST = d_globalset.get('GL_EMAIL_HOST')
            EMAIL_PORT = d_globalset.get('GL_EMAIL_PORT')
            EMAIL_HOST_USER = d_globalset.get('GL_EMAIL_HOST_USER')
            EMAIL_HOST_PASSWORD = d_globalset.get('GL_EMAIL_HOST_PASSWORD')
            EMAIL_USE_TLS = d_globalset.get('GL_EMAIL_USE_TLS')

            EMAIL_DEFAULT_FROM_EMAIL = context['EMAIL_DEFAULT_FROM_EMAIL']
            EMAIL_HOST_USER_NAME = context['EMAIL_HOST_USER_NAME']

            if len(subject.replace(' ', '')) == 0:
                subject = 'Notification'
            t = get_template(template)
            email_body = t.render(context)
            email.subject = subject
            email.recipient = recipient
            email.html_message = email_body
            email.save()
            m_email_host_user = f"{EMAIL_HOST_USER_NAME} <{EMAIL_DEFAULT_FROM_EMAIL}>"

            mail_connection = get_connection(
                host=EMAIL_HOST,
                port=EMAIL_PORT,
                username=EMAIL_HOST_USER,
                password=EMAIL_HOST_PASSWORD,
                use_tls=EMAIL_USE_TLS
            )
            mail_connection.open()
            if attach_file:
                message = EmailMultiAlternatives(subject=subject, body='', from_email=m_email_host_user,
                                                 to=[recipient], connection=mail_connection)
                message.attach_file(attach_file)
                message.attach_alternative(email_body, "text/html")
                message.send()
            else:
                send_mail(subject=subject,
                          message="",
                          from_email=m_email_host_user,
                          recipient_list=[recipient],
                          html_message=email_body,
                          connection=mail_connection,
                          )
            mail_connection.close()
        except Exception as ex:
            print('save_and_send_email = ERROR = ', ex)
        print ("send_email 4")
        if email.id:
            email.sent = True
            email.save()


def send_mail_password_reset(user):
    save_and_send_email(user.email,
                        u'СтройБук - Восстановление доступа',
                        'mail/password_has_been_reset.html',
                        {'user': user}
                        )

