# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import json
from ipware import get_client_ip
from django.utils.translation import gettext
from django.shortcuts import render, redirect
from django.http import HttpResponse
from el_t01_app.service.service import get_main_args
from el_t01_app.models import Feedback, Faqtabl, Blogger, BloggerRef
from el_t01.settings import BASE_DIR
from .views_auth import register_add_blogger_and_discount

def index(request, login=False, loc_redirect_url=""):
    print ("index")
    print("loc_redirect_url=",loc_redirect_url)
    # print ("redirect")
    # return redirect('/hishgadonline')
    args = get_main_args(request, section="main")
    args['utm_code'] = request.GET.get('utm_campaign', '')
    print("args['utm_code'] = ", args['utm_code'])

    args['get_param'] = json.dumps(request.GET)
    print("args['get_param'] = ", args['get_param'])

    if args['utm_code'] != "":
        try:
            m_in_ip, m_in_is_routable = get_client_ip(request)
            t_blog_ref = BloggerRef()
            t_blog_ref.dt_add = datetime.datetime.now()
            t_blog_ref.utm_code = args['utm_code']
            if Blogger.objects.filter(ref_hash=args['utm_code']).exists():
                t_blog_ref.blogger_id = Blogger.objects.get(ref_hash=args['utm_code']).id
            t_blog_ref.u_ip = f'{m_in_ip} {m_in_is_routable}'
            t_blog_ref.http_referer = request.META.get('HTTP_REFERER', "")
            t_blog_ref.save()
        except Exception:
            pass

    if args['logged_in']:
        args['utm_code'] = request.GET.get('utm_campaign', '')
        print("args['utm_code'] = ", args['utm_code'])
        if args['utm_code'] != '':
            register_add_blogger_and_discount(args['me'].profile, args['utm_code'], profile_update=False)
        return redirect('/cabinet')
    else:

        args['bool_login'] = login
        args['redirect_url'] = loc_redirect_url
        if args['GL_PageMain'] == "login":  # "lending" "login"
            args['main_tab'] = f"{args['GL_MainSkin']}/index/index_login.html"
        else:
            args['box_message_title'] = gettext("Guiding video")
            args['box_message_subtitle'] = ""
            args['box_message_text'] = ""
            if args['GL_Movie_list'] != "-":
                args['video_source'] = f"/media/prevideo/{args['GL_Movie_list']}"
            else:
                args['video_source'] = ""
            args['video_source_type'] = "video/mp4"
            args['menu_item'] = 'nav-link_cabinet'
            args['main_tab'] = args['lf_index']
            args['menu_item'] = "nav-link_home"
        return render(request, args['main_tab'], args)

def hishgadonline(request):
    print ("hishgadonline")

    args = get_main_args(request, section="main")
    if args['logged_in']:
        ##
        print("== hishgadonline cabinet==")
        args['box_message_title'] = gettext("Guiding video")
        args['box_message_subtitle'] = ""
        args['box_message_text'] = ""
        args['video_source'] = f"/media/prevideo/{args['GL_Movie_list']}"
        args['video_source_type'] = "video/mp4"
        args['menu_item'] = 'nav-link_cabinet'
        args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_game_list.html")
        args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_video.html")
        if len(args['dict_partner']) > 0:
            args['l_body_list'].append(f"{args['GL_MainSkin']}/cabinet/cab_partner.html")

        args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
        return render(request, args['main_tab'], args)
        ##
        return redirect('/cabinet')
    else:
        if args['GL_PageMain'] == "login":  # "lending" "login"
            args['main_tab'] = f"{args['GL_MainSkin']}/index/index_login.html"
        else:
            args['box_message_title'] = gettext("Guiding video")
            args['box_message_subtitle'] = ""
            args['box_message_text'] = ""
            if args['GL_Movie_list'] != "-":
                args['video_source'] = f"/media/prevideo/{args['GL_Movie_list']}"
            else:
                args['video_source'] = ""
            args['video_source_type'] = "video/mp4"
            args['menu_item'] = 'nav-link_cabinet'
            args['main_tab'] = args['lf_index']
            args['menu_item'] = "nav-link_home"
        return render(request, args['main_tab'], args)

def rules(request):
    args = get_main_args(request, section="main")
    args['name_doc_short'] = "/static/foot/rules.pdf"
    args['main_tab'] = f"{args['GL_MainSkin']}/main/rules.html"
    return render(request, args['main_tab'], args)


def about(request):
    args = get_main_args(request, section="main")
    if args['logged_in']:
        return redirect('/cabinet')
    else:
        args['main_tab'] = args['lf_about']
        args['menu_item'] = "nav-link_about"
        return render(request, args['main_tab'], args)


def contact(request):
    args = get_main_args(request, section="main")
    if args['logged_in']:
        return redirect('/cabinet')
    else:
        args['main_tab'] = args['lf_contact']
        args['menu_item'] = "nav-link_contact"
        return render(request, args['main_tab'], args)


def p_footer(request, foot_param=None):
    print ("==p_footer==", foot_param)
    args = get_main_args(request, section="main")
    # if not args['logged_in']:
    #     pass
    #     return redirect('/')
    # else:

    if foot_param == "aboutus":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_aboutus.html")
    elif foot_param == "contact":
        print ("contact")
        if not args['logged_in']:
            args['m_fullname'] = ""
            args['m_email'] = ""
        else:
            args['m_fullname'] = args['me'].profile.name
            args['m_email'] = args['me'].email
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_contact.html")
    elif foot_param == "ppolicy":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_ppolicy.html")
    elif foot_param == "maccount":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_maccount.html")
    elif foot_param == "hdeposit":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_hdeposit.html")
    elif foot_param == "hwithdraw":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_hwithdraw.html")
    elif foot_param == "helpcentre":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_helpcentre.html")
    elif foot_param == "faq":
        args['faqtabl'] = Faqtabl.objects.filter(faq_enable=True).order_by("faq_order")
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_faq.html")
    elif foot_param == "quickstart":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_quickstart.html")
    elif foot_param == "riskwarnings":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_riskwarnings.html")
    elif foot_param == "privacynotice":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_privacynotice.html")
    elif foot_param == "security":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_security.html")
    elif foot_param == "termsservice":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_termsservice.html")
    elif foot_param == "termsuse":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_termsuse.html")
    elif foot_param == "gamble":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_gamble.html")
    elif foot_param == "aware":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_aware.html")
    elif foot_param == "technology":
        args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/foot_technology.html")
    else:
        return redirect('/')
    args['main_tab'] = f"{args['GL_MainSkin']}/footer/footer.html"
    return render(request, args['main_tab'], args)


def error403(request, reason=""):
    return redirect('/')


def feedback(request):
    print ("feedback")
    args = get_main_args(request, section="main")
    if args['logged_in']:
        if request.POST:
            print ("POST = ", request.POST)
            try:
                m_user_id = None
                if args['logged_in']:
                    m_user_id = args['me'].id

                print("request.POST = ", request.POST)
                m_fullname = request.POST.get('f_fullname', "")
                m_email = request.POST.get('f_email', "")
                m_text = request.POST.get('f_text', "")

                t_feedback = Feedback()
                t_feedback.created = datetime.datetime.now()
                t_feedback.u_name = m_fullname
                t_feedback.u_email = m_email
                t_feedback.text = m_text
                t_feedback.status = '00'
                if m_user_id is not None:
                    t_feedback.user_id_id = m_user_id
                # t_feedback.reply_text = ""
                # t_feedback.reply_date = datetime.datetime.now()
                # t_feedback.reply_lang = ""
                t_feedback.save()
                return redirect('/feedback-ok')

            except Exception as ex:
                return redirect('/feedback-err')
        else:
            return redirect('/')
    else:
        return redirect('/')

def download_applepay(request):
    from django.views.static import serve
    filepath = os.path.join(BASE_DIR, 'el_t01_app', 'static', 'apple-developer-merchantid-domain-association.txt')

    # f = open(filepath, 'r')
    # file_content = f.read()
    # f.close()
    # return HttpResponse(file_content, content_type="text/plain")

    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


def download_manifest_json(request):
    args = get_main_args(request, section="main")
    from django.views.static import serve
    filepath = os.path.join(BASE_DIR, 'el_t01_app', 'static', 'main', f"{args['GL_MainSkin']}", 'manifest.json')
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


def download_firebase_messaging_sw(request):
    args = get_main_args(request, section="main")
    from django.views.static import serve
    filepath = os.path.join(BASE_DIR, 'el_t01_app', 'static', 'main', f"{args['GL_MainSkin']}", 'firebase-messaging-sw.js')
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
