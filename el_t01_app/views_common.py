# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os

from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _

from el_t01.settings import MEDIA_ROOT, BASE_DIR
from el_t01_app.service.service import get_main_args
from el_t01_app.models import Feedback
from el_t01_app.models import Profile, SmsToSend, EmailToSend


def box_registration(request, mess_param=None):
    print ("==p_footer==")
    args = get_main_args(request, section="main")
    # if not args['logged_in']:
    #     pass
    #     return redirect('/')
    # else:

    # поиск видио после регистрации
    m_movie_source = f"/media/prevideo/{args['GL_MainSkin']}/{args['GL_Movie_registr']}"
    m_movie_source_for_check = MEDIA_ROOT + f"/prevideo/{args['GL_MainSkin']}/{args['GL_Movie_registr']}"
    if os.path.exists(m_movie_source_for_check) and os.path.isfile(m_movie_source_for_check):
        args['movie_source'] = m_movie_source
        args['movie_source_type'] = "video/mp4"
        args['movie_poster'] = f"/media/prevideo/{args['GL_MainSkin']}/{args['GL_Movie_registr_poster']}"
        args['movie_link'] = f"{args['GL_Movie_registr_link']}"
    else:
        args['movie_source'] = None

    print ("m_movie_source_for_check = ", m_movie_source_for_check)
    print ("args['movie_source'] = ", args['movie_source'])

    args['cabinet_form'] = True
    args['page_caption'] = _("Registration completed")
    args['wait_source'] = "None"
    args['box_message_title'] = ""
    args['box_message_subtitle'] = 'חדש בישראל ! מגרדים חישגד בנייד!'
    args['box_message_text'] = "גירוד כרטיסי חישגד בנייד ! גרדו עכשיו והתחילו להרוויח !בבית , במשרד או בכל מקום שתבחרו …מגרדים כרטיסי חישגד ומקבלים כסף לחשבון הבנק!"
    args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/box_registration.html")
    args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"

    try:
        args['pixel'] = args['me'].profile.settings["get_param"]["pixel"]
        print("args['pixel'] = ", args['pixel'])
    except:
        print("args['pixel'] = ", "BRED")
        pass

    return render(request, args['main_tab'], args)


def box_message(request, mess_param=None):
    print ("==p_footer==")
    print ("mess_param = ", mess_param)
    args = get_main_args(request, section="main")
    # if not args['logged_in']:
    #     pass
    #     return redirect('/')
    # else:
    args['box_message_title'] = ""
    args['box_message_subtitle'] = ""
    args['box_message_text'] = ""
    args['cabinet_form'] = True
    if mess_param == "registration_ok":
        args['page_caption'] = _("Registration completed")
        # args['box_message_title'] = _("Registration completed")
        # args['box_message_subtitle'] = _('Registration completed successfully, follow the instructions in the mail')
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "feedback_ok":
        args['page_caption'] = _("Feedback")
        # args['box_message_title'] = _("Feedback")
        args['box_message_subtitle'] = _("Your appeal has been accepted and will be processed as soon as possible.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "feedback_err":
        args['page_caption'] = _("Feedback")
        args['box_message_title'] = _("Feedback")
        args['box_message_subtitle'] = _("An error occured, please try again later.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "payout_gift_ok":
        args['page_caption'] = _("Cash Withdrawal")
        # args['box_message_title'] = _("Cash Withdrawal")
        args['box_message_subtitle'] = _("We'll review and you will receive money soon.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "payout_ok":
        args['page_caption'] = _("Cash Withdrawal")
        args['box_message_title'] = _("Cash Withdrawal")
        args['box_message_subtitle'] = _("We'll review and update your account soon.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "payout_err":
        args['page_caption'] = _("Cash Withdrawal")
        # args['box_message_title'] = _("Cash Withdrawal")
        args['box_message_subtitle'] = _("An error occured, please try again later.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "payout_err_sum":
        args['page_caption'] = _("Cash Withdrawal")
        # args['box_message_title'] = _("Cash Withdrawal")
        args['box_message_subtitle'] = _("You don't have enough money.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "cashadd_ok":
        args['page_caption'] = _("Cash Payment")
        # args['box_message_title'] = _("Cash Payment")
        args['box_message_subtitle'] = _("We'll review and update your account soon.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "cashadd_err":
        args['page_caption'] = _("Cash Payment")
        # args['box_message_title'] = _("Cash Payment")
        args['box_message_subtitle'] = _("An error occured, please try again later.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "cashadd_err_sum":
        args['page_caption'] = _("Cash Payment")
        # args['box_message_title'] = _("Cash Payment")
        args['box_message_subtitle'] = _("Enter the correct amount.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "payadd_ok":
        args['page_caption'] = _("Bank Transfer")
        # args['box_message_title'] = _("Bank Transfer")
        args['box_message_subtitle'] = _("We'll review and update your account soon.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "payadd_err":
        args['page_caption'] = _("Bank Transfer")
        # args['box_message_title'] = _("Bank Transfer")
        args['box_message_subtitle'] = _("An error occured, please try again later.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "cabpass_ok":
        args['page_caption'] = _("Change pasword")
        # args['box_message_title'] = _("Change pasword")
        args['box_message_subtitle'] = _("Your changes have been saved successfully.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "cabpass_err":
        args['page_caption'] = _("Change pasword")
        # args['box_message_title'] = _("Change pasword")
        args['box_message_subtitle'] = _("your changes were not saved.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    # elif mess_param == "recovery_ok":
    #     args['page_caption'] = _("Recovery password")
    #     # args['box_message_title'] = _("Recovery password")
    #     args['box_message_subtitle'] = _("Follow the instructions in the mail.")
    #     # args['box_message_subtitle'] = ''
    #     # args['box_message_text'] = ""
    elif mess_param == "recovery_ok":
        args['page_caption'] = _("Recovery password")
        # args['box_message_title'] = _("Recovery password")
        args['box_message_subtitle'] = _("We have sent you a new password to your email address.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "recovery_phone_ok":
        args['page_caption'] = _("Recovery password")
        # args['box_message_title'] = _("Recovery password")
        args['box_message_subtitle'] = _("We have sent you a new password to your phone number.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "recovery_not_ok":
        args['page_caption'] = _("Recovery password")
        # args['box_message_title'] = _("Recovery password")
        args['box_message_subtitle'] = _("Something was wrong. Please try again later.")
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "sms_stop":
        args['page_caption'] = _("Sms Stop")
        args['box_message_title'] = _("The number has been removed from the mailing list.")
        args['box_message_subtitle'] = ""
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "sms_notstop":
        args['page_caption'] = _("Sms Stop")
        args['box_message_title'] = _("Thank you for choosing to stay!")
        args['box_message_subtitle'] = ""
        # args['box_message_subtitle'] = ''
        # args['box_message_text'] = ""
    elif mess_param == "gift-ok":
        args['page_caption'] = _("Hooray!")
        args['box_message_title'] = _("We prepared the HishGad lottery ticket as a gift")
        args['box_message_subtitle'] = _("The gift will be sent at the time you specified")
        args['box_message_text'] = _("Thank you for choosing our company!")
    elif mess_param == "subs_pay_ok":
        args['page_caption'] = _("Subscription completed!")
        args['box_message_title'] = _("Subscription completed successfully!")
        args['box_message_subtitle'] = _("The subscription will start from the date you specified, wait for the SMS with the ticket")
    elif mess_param == "subs_pay_fail":
        args['page_caption'] = _("Subscription not completed")
        args['box_message_title'] = _("Unfortunately, the subscription is not completed because your payment failed")
        args['box_message_subtitle'] = _("Please try again or contact us")
    else:
        return redirect('/')

    args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/box_message.html")
    args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
    return render(request, args['main_tab'], args)


def p_footer(request, foot_param=None):
    print ("==p_footer==")
    print ("foot_param = ", foot_param)
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
    else:
        return redirect('/')

    args['main_tab'] = f"{args['GL_MainSkin']}/footer/footer.html"
    return render(request, args['main_tab'], args)

def cabs_nosms(request, verbal=None):
    print ("==p_footer==")
    print ("verbal = ", verbal)
    args = get_main_args(request, section="main")
    args['verbal'] = verbal
    args['box_message_title'] = _("Remove mail")
    args['box_message_subtitle'] = _('Remove the number phone from the mailing list?')
    # args['box_message_text'] = _("Do you really want to stop receiving our news?")
    args['l_body_list'].append(f"{args['GL_MainSkin']}/footer/cabs_nosms.html")
    args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
    return render(request, args['main_tab'], args)


def cabs_nosmsconfirm(request, verbal=None):
    print("==cabs_nosmsconfirm==")
    print("verbal = ", verbal)
    verbal = verbal.strip()
    print("verbal = ", verbal)

    args = get_main_args(request, section="main")
    if request.POST:
        print("POST = ", request.POST)
        m_btn = request.POST.get("btn", "")
        print ("m_btn = ", m_btn)
        if m_btn == "stop":
            try:
                if EmailToSend.objects.filter(hash=verbal).exists():
                    t_EmailToSend = EmailToSend.objects.filter(hash=verbal)[0]
                    if t_EmailToSend.user_id is None:
                        m_user_mail = t_EmailToSend.recipient
                        t_profile = Profile.objects.filter(user__email=m_user_mail)
                        if t_profile.count() > 0:
                            t_profile = t_profile[0]
                            t_profile.reklama = False
                            t_profile.save()
                    else:
                        t_EmailToSend.user_id.profile.reklama = False
                        t_EmailToSend.user_id.profile.save()

                if SmsToSend.objects.filter(hash=verbal).exists():
                    t_SmsToSend = SmsToSend.objects.filter(hash=verbal)[0]
                    t_SmsToSend.user_id.profile.reklama = False
                    t_SmsToSend.user_id.profile.save()
                return redirect('/sms-stop/')
            except:
                return redirect('/sms-notstop/')
        else:
            return redirect('/sms-notstop/')

