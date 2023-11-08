#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path
from django.conf.urls import include, url
from django.views.i18n import JavaScriptCatalog
from django.conf.urls.static import static
from django.conf import settings

from .views_main import index, about, contact, p_footer, rules, feedback, download_applepay, \
    hishgadonline, download_manifest_json, download_firebase_messaging_sw
from .views_common import box_message, box_registration, cabs_nosms, cabs_nosmsconfirm

from .views_auth import login, logout, logout_timeout, register_user, check_username, \
    check_userlogin, confirmation, recovery, check_loginrecovery, forgot_password, set_password, \
    mobile_confirmed, login_ext
from .views_auth_shop import login_shop, phone_code_verification
from .views_cab import cabinet, cab_game_item, cab_cartpage, \
    cab_game_buy, cab_game_pay, cab_game_paybtn, cab_game_play, \
    cab_game_addnew, cab_game_order, cab_game_ticket_del, cab_game_play_info, \
    cab_game_play_ticket_info, cab_game_play_ticket_send_status, \
    cab_game_play_ticket_send_status_test, cab_game_gift_info

from .views_cab import cab_payout_save, cab_payout_ok, cab_payout_block, cab_payout_delete
from .views_cab import cab_payadd_save, cab_payadd_ok
from .views_cab import cab_cashadd_save, cab_cashadd_ok

from .views_cab import cab_profile_save, cab_pasw_save

from .views_boss import (cab_boss, cabb_balance_save,
                         cabb_payadd_info, cabb_payadd_conf, cabb_payout_info,
                         cabb_user_tickets, cabb_ticketcheck, cabb_ticketcheck_conf, cabb_user_tickets_action,
                         cabb_cashadd_btn,
                         cabb_feedbackbtninfo, cabb_feedbackbtnsave,
                         cabb_user_balance_oparation, cabb_user_payoperation_save,
                         cabb_user_payoperation,
                         cabb_user_block, cabb_blocklist_enable, cabb_blocklist_new, cabb_blocklist_save,
                         cabb_user_limit, cabb_ticketrestart, cabb_user_sms,
                         cabb_user_form, cabb_user_tickets_and_balops,
                         cabb_payout_form,
                         save_comment_callcenter
                         )

from .views_payment import cab_game_payment, trz_fail, trz_done, game_payment_fail, trz_notify, \
    game_payment_info
from .views_api_external import jellyfish_rezult
from .views_rest_report import Report_data_get
from .views_api_ext import ext_reg, ApiExtPage, ext_page

from .views_cabb_report import cabb_report, cabb_report_exp
from .views_task import cabs_task, cabs_newtask_save, cabs_task_users_list

from .views_payments_parser import upload_payment_answers_data
from .views_shop import shop_main
from .views_ex_reg import ext_shop


urlpatterns = \
    [
        url(r'^i18n/', include('django.conf.urls.i18n')),
        path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
        path('check-username/', check_username, name='check_username'),
        path('register-user/', register_user, name='register_user'),
        path('confirmation/', confirmation, name='confirmation'),
        path('check-userlogin/', check_userlogin, name='check_userlogin'),
        path('login/', login, name='login'),
        path('login-shop/', login_shop, name='login-shop'),
        path('loginext/<str:verbal>/', login_ext, name='login_ext'),
        path('logout/', logout, name='logout'),
        path('logout_timeout', logout_timeout, name='logout_timeout'),
        path('mobile-confirmed', mobile_confirmed, name='mobile_confirmed'),
        # box_message
        path('registration-ok/', box_registration, name='registration-ok'),
        # path('registration-ok/', box_message, {'mess_param': 'registration_ok'}, name='registration-ok'),
        path('feedback-ok/', box_message, {'mess_param': 'feedback_ok'}, name='feedback-ok'),
        path('feedback-err/', box_message, {'mess_param': 'feedback_err'}, name='feedback-err'),
        path('payout-gift-ok/', box_message, {'mess_param': 'payout_gift_ok'}, name='payout-gift-ok'),
        path('payout-ok/', box_message, {'mess_param': 'payout_ok'}, name='payout-ok'),
        path('payout-err/', box_message, {'mess_param': 'payout_err'}, name='payout-err'),
        path('payout-err-sum/', box_message, {'mess_param': 'payout_err_sum'}, name='payout-err-sum'),
        path('payadd-ok/', box_message, {'mess_param': 'payadd_ok'}, name='payadd-ok'),
        path('payadd-err/', box_message, {'mess_param': 'payadd_err'}, name='payadd-err'),
        path('phone-code-verification/', phone_code_verification, name='phone-code-verification'),
        path('cashadd-ok/', box_message, {'mess_param': 'cashadd_ok'}, name='cashadd-ok'),
        path('cashadd-err/', box_message, {'mess_param': 'cashadd_err'}, name='cashadd-err'),
        path('cashadd-err-sum/', box_message, {'mess_param': 'cashadd_err_sum'}, name='cashadd-err-sum'),
        path('profile-ok/', box_message, {'mess_param': 'profile_ok'}, name='profile-ok'),
        path('profile-err/', box_message, {'mess_param': 'profile_err'}, name='profile-err'),
        path('cabpass-ok/', box_message, {'mess_param': 'cabpass_ok'}, name='cabpass-ok'),
        path('cabpass-err/', box_message, {'mess_param': 'cabpass_err'}, name='cabpass-err'),
        path('recovery-ok/', box_message, {'mess_param': 'recovery_ok'}, name='recovery-ok'),
        path('recovery-phone-ok/', box_message, {'mess_param': 'recovery_phone_ok'},
             name='recovery-phone-ok'),
        path('recovery-not-ok/', box_message, {'mess_param': 'recovery_not_ok'}, name='recovery-not-ok'),
        path('sms-stop/', box_message, {'mess_param': 'sms_stop'}, name='sms_stop'),
        path('sms-notstop/', box_message, {'mess_param': 'sms_notstop'}, name='sms_notstop'),
        path('gift-ok/', box_message, {'mess_param': 'gift-ok'}, name='gift-ok'),
        # end box_message
        path('check-loginrecovery/', check_loginrecovery, name='check_loginrecovery'),
        path('recovery', recovery, name='recovery'),
        path('forgot-password', forgot_password, name='forgot_password'),
        path('set_password', set_password, name='set_password'),
        # footer
        path('aboutus/', p_footer, {'foot_param': 'aboutus'}, name='aboutus'),  # 'About Us
        path('technology/', p_footer, {'foot_param': 'technology'}, name='technology'),  # 'Technology
        path('contact/', p_footer, {'foot_param': 'contact'}, name='contact'),  # 'Contact Us
        path('ppolicy/', p_footer, {'foot_param': 'ppolicy'}, name='ppolicy'),  # 'Privacy Policy
        path('maccount/', p_footer, {'foot_param': 'maccount'}, name='maccount'),  # 'Manage Your Account
        path('hdeposit/', p_footer, {'foot_param': 'hdeposit'}, name='hdeposit'),  # 'How to Deposit
        path('hwithdraw/', p_footer, {'foot_param': 'hwithdraw'}, name='hwithdraw'),  # 'How to Withdraw
        path('helpcentre/', p_footer, {'foot_param': 'helpcentre'}, name='helpcentre'),  # 'Help centre
        path('faq/', p_footer, {'foot_param': 'faq'}, name='faq'),  # 'FAQ
        path('quickstart/', p_footer, {'foot_param': 'quickstart'}, name='quickstart'),  # 'Quick Start Guide
        path('riskwarnings/', p_footer, {'foot_param': 'riskwarnings'}, name='riskwarnings'),
        # 'Risk Warnings
        path('privacynotice/', p_footer, {'foot_param': 'privacynotice'}, name='privacynotice'),
        # 'Privacy Notice
        path('security/', p_footer, {'foot_param': 'security'}, name='security'),  # 'Security
        path('termsservice/', p_footer, {'foot_param': 'termsservice'}, name='termsservice'),
        # 'Terms of Service
        path('termsuse/', p_footer, {'foot_param': 'termsuse'}, name='termsuse'),  # 'Terms Of Use
        path('gamble/', p_footer, {'foot_param': 'gamble'}, name='gamble'),  # 'Gamble
        path('aware/', p_footer, {'foot_param': 'aware'}, name='aware'),  # 'Aware
        path('feedback/', feedback, name='feedback'),
        # cabinet
        path('cabinet/', cabinet, {'cab_type': 'cab_cabinet'}, name='cabinet'),
        path('cabinet_gift/', cabinet, {'cab_type': 'cab_cabinet_gift'}, name='cabinet_gift'),
        path('cab_subs_history/', cabinet, {'cab_type': 'cab_subs_history'}, name='cab_subs_history'),
        path('cab-history/', cabinet, {'cab_type': 'cab_history'}, name='cab_history'),
        path('cab-payadd/', cabinet, {'cab_type': 'cab_payadd'}, name='cab_payadd'),
        path('cab_payadd_save/', cab_payadd_save, name='cab_payadd_save'),
        path('cab_payadd_ok/', cab_payadd_ok, name='cab_payadd_ok'),
        path('cab_cashadd/', cabinet, {'cab_type': 'cab_cashadd'}, name='cab_cashadd'),
        path('cab_cashadd_save/', cab_cashadd_save, name='cab_cashadd_save'),
        path('cab_cashadd_ok/', cab_cashadd_ok, name='cab_cashadd_ok'),
        path('cab-payout/', cabinet, {'cab_type': 'cab_payout'}, name='cab_payout'),
        path('cab_payout_save/', cab_payout_save, name='cab_payout_save'),
        path('cab_payout_delete/', cab_payout_delete, name='cab_payout_delete'),
        path('cab_payout_ok/', cab_payout_ok, name='cab_payout_ok'),
        path('cab_payout_block/', cab_payout_block, name='cab_payout_block'),
        path('cab_referrals/', cabinet, {'cab_type': 'cab_referrals'}, name='cab_referrals'),
        path('cab-contact/', p_footer, {'foot_param': 'contact'}, name='contact'),
        # path('cab-profile/', cabinet, {'cab_type': 'cab_profile'}, name='cab_profile'),
        path('cab-profile-save/', cab_profile_save, name='cab_profile_save'),
        path('cab-pasw/', cabinet, {'cab_type': 'cab_pasw'}, name='cab_pasw'),
        path('cab-pasw-save/', cab_pasw_save, name='cab_pasw_save'),
        path('cab-balance/', cabinet, {'cab_type': 'cab_balance'}, name='cab_balance'),
        path('cab-block/', cabinet, {'cab_type': 'cab_block'}, name='cab_block'),
        #
        path('cab-cartpage/', cab_cartpage, name='cab_cartpage'),
        path('cab-game-addnew/<str:verbal>/<str:addparam>/', cab_game_addnew, name='cab_game_addnew'),
        path('cab-game-item/<str:verbal>/<str:addparam>/', cab_game_item, name='cab_game_item'),
        path('cab-game-order/<str:verbal>/', cab_game_order, name='cab_game_order'),
        path('cab-game-buy/', cab_game_buy, name='cab_game_buy'),
        path('cab-game-gift-info/', cab_game_gift_info, name='cab_game_gift_info'),
        path('cab-game-pay/<str:verbal>/', cab_game_pay, name='cab_game_pay'),
        path('cab-game-ticket-del/<int:game_id>/<int:ticket_id>/', cab_game_ticket_del,
             name='cab_game_ticket_del'),
        path('cab-game-paybtn/', cab_game_paybtn, name='cab_game_paybtn'),
        path('cab-game-payment/<str:verbal>/', cab_game_payment, name='cab_game_payment'),
        path('cab-game-play/<str:verbal>/', cab_game_play, name='cab_game_play'),
        path('cab-game-play-info/', cab_game_play_info, name='cab_game_play_info'),
        path('cab-game-play-ticket-info/', cab_game_play_ticket_info, name='cab_game_play_ticket_info'),
        path('cab-game-play-ticket-send-status/', cab_game_play_ticket_send_status,
             name='cab_game_play_ticket_send_status'),
        path('cab-game-play-ticket-send-status_test/', cab_game_play_ticket_send_status_test,
             name='cab_game_play_ticket_send_status_test'),
        # jellyfish_rezult
        path('jellyfish_rezult/', jellyfish_rezult.as_view(), name='jellyfish_rezult'),
        #lotto result
        # path('lotto_result/', lotto_result.as_view(), name='lotto_result'),
        # cab_boss
        path('cabb_users/', cab_boss, {'cab_type': 'cabb_users'}, name='cabb_users'),
        path('cabb_games/', cab_boss, {'cab_type': 'cabb_games'}, name='cabb_games'),
        path('cabb_tickets/', cab_boss, {'cab_type': 'cabb_tickets'}, name='cabb_tickets'),
        path('cabb_tickets_check/', cab_boss, {'cab_type': 'cabb_tickets_check'}, name='cabb_tickets_check'),
        path('cabb_lotto_tickets_check/', cab_boss, {'cab_type': 'cabb_lotto_tickets_check'}, name='cabb_lotto_tickets_check'),
        path('cabb_ticketcheck/', cabb_ticketcheck, name='cabb_ticketcheck'),
        path('cabb_ticketcheck_conf/', cabb_ticketcheck_conf, name='cabb_ticketcheck_conf'),
        path('cabb-user-tickets/<int:user_id>/', cabb_user_tickets, name='cabb_user_tickets'),
        path('cabb-user-tickets-and-balops/<int:user_id>/', cabb_user_tickets_and_balops, name='cabb_user_tickets_and_balops'),
        path('cabb-user-tickets-action/', cabb_user_tickets_action, name='cabb_user_tickets_action'),
        path('cabb-user-payoperation/<int:user_id>/', cabb_user_payoperation, name='cabb_user_payoperation'),
        path('cabb_user_block/', cabb_user_block, name='cabb_user_block'),
        path('cabb_user_limit/', cabb_user_limit, name='cabb_user_limit'),
        path('cabb_user_sms/', cabb_user_sms, name='cabb_user_sms'),
        path('cabb_ticketrestart/', cabb_ticketrestart, name='cabb_ticketrestart'),
        path('cabb-user-form/', cabb_user_form, name='cabb_user_form'),
        path('cabb_cabala/', cab_boss, {'cab_type': 'cabb_cabala'}, name='cabb_cabala'),
        # path('cabb-user-payoparation/<int:user_id>/', cabb_user_payoparation, name='cabb_user_payoparation'),
        path('cabb_feedback_new/', cab_boss, {'cab_type': 'cabb_feedback_new'}, name='cabb_feedback_new'),
        path('cabb_feedback_ok/', cab_boss, {'cab_type': 'cabb_feedback_ok'}, name='cabb_feedback_ok'),
        path('cabb_feedback_block/', cab_boss, {'cab_type': 'cabb_feedback_block'},
             name='cabb_feedback_block'),
        path('cabb_feedback_btn_info/', cabb_feedbackbtninfo, name='cabb_feedbackbtninfo'),
        path('cabb_feedback_btn_save/', cabb_feedbackbtnsave, name='cabb_feedbackbtnsave'),
        path('cabb_payout_new/', cab_boss, {'cab_type': 'cabb_payout_new'}, name='cabb_payout_new'),
        path('cabb_payout_ok/', cab_boss, {'cab_type': 'cabb_payout_ok'}, name='cabb_payout_ok'),
        path('cabb_payout_reject/', cab_boss, {'cab_type': 'cabb_payout_reject'}, name='cabb_payout_reject'),
        path('cabb_payout_info/', cabb_payout_info, name='cabb_payout_info'),
        path('cabb_payout_form/', cabb_payout_form, name='cabb_payout_form'),
        # path('cabb_payadd_conf/', cabb_payadd_conf, name='cabb_payadd_conf'),
        path('cabb_payadd_new/', cab_boss, {'cab_type': 'cabb_payadd_new'}, name='cabb_payadd_new'),
        path('cabb_payadd_ok/', cab_boss, {'cab_type': 'cabb_payadd_ok'}, name='cabb_payadd_ok'),
        path('cabb_payadd_info/', cabb_payadd_info, name='cabb_payadd_info'),
        path('cabb_payadd_conf/', cabb_payadd_conf, name='cabb_payadd_conf'),
        path('cabb_cashadd_new/', cab_boss, {'cab_type': 'cabb_cashadd_new'}, name='cabb_cashadd_new'),
        path('cabb_cashadd_ok/', cab_boss, {'cab_type': 'cabb_cashadd_ok'}, name='cabb_cashadd_ok'),
        path('cabb_cashadd_block/', cab_boss, {'cab_type': 'cabb_cashadd_block'}, name='cabb_cashadd_block'),
        path('cabb_cashadd_btn/', cabb_cashadd_btn, name='cabb_cashadd_btn'),
        path('cab-game-user/', cab_boss, {'cab_type': 'boss_game_user'}, name='boss_game_user'),
        path('cab-game-type/', cab_boss, {'cab_type': 'boss_game_type'}, name='boss_game_type'),
        path('cabb_blist/', cab_boss, {'cab_type': 'cabb_blist'}, name='cabb_blist'),
        path('cabb_blocklist_enable/', cabb_blocklist_enable, name='cabb_blocklist_enable'),
        path('cabb_blocklist_new/', cabb_blocklist_new, name='cabb_blocklist_new'),
        path('cabb_blocklist_save/', cabb_blocklist_save, name='cabb_blocklist_save'),
        # path('cabb_subs_/', cab_boss, {'cab_type': 'cabb_subs'}, name='cabb_subs'),
        path('cabb_balance_save/', cabb_balance_save, name='cabb_balance_save'),
        path('cabb_user_balance_oparation/', cabb_user_balance_oparation, name='cabb_user_balance_oparation'),
        path('cabb_user_payoperation_save/', cabb_user_payoperation_save, name='cabb_user_payoperation_save'),
        path('cabb_user_payoperation_save/', cabb_user_payoperation_save, name='cabb_user_payoperation_save'),
        # cabb report
        path('cabb_reports/', cab_boss, {'cab_type': 'cabb_reports'}, name='cabb_reports'),
        path('cabb_report/<str:verbal>/', cabb_report, name='cabb_report'),
        path('cabb_report_exp/<str:verbal>/<str:r_type>/', cabb_report_exp, name='cabb_report_exp'),
        # payment
        # tranzila
        path('trz-fail/<str:verbal>/', trz_fail, name="trz_fail"),
        path('trz-done/<str:verbal>/', trz_done, name="trz_done"),
        path('trz-notify/<str:verbal>/', trz_notify, name="trz-notify"),
        path('game-payment-fail/<str:verbal>/', game_payment_fail, name="game_payment_fail"),
        path('game_payment_info/', game_payment_info, name="game_payment_info"),

        path('rules/', rules, name='rules'),
        # path('about/', about, name='about'),
        # path('contact/', contact, name='contact'),
        path('hishgadonline/', hishgadonline, name='hishgadonline'),
        path('index/', index, {'login': False}, name='index'),
        path('userlogin/', index, {'login': True}, name='userlogin'),
        path('', index, name='index'),
        # SMS system
        path('cabs_list/', cabs_task, {'cabs_type': 'cabs_list'}, name='cabs_list'),
        path('cabs_newtask/<str:task_type>/', cabs_task, {'cabs_type': 'cabs_newtask'}, name='cabs_newtask'),
        path('new_task_users_list/', cabs_task_users_list, name='new_task_users_list'),
        path('cabs_newtask_save/', cabs_newtask_save, name='cabs_newtask_save'),
        path('nosms/<str:verbal>/', cabs_nosms, name='cabs_nosms'),
        path('cabs_nosmsconfirm/<str:verbal>/', cabs_nosmsconfirm, name='cabs_nosmsconfirm'),
        # api report
        path('api-report-data/', Report_data_get.as_view(), name='report-data'),
        # api ext
        path('api-extreg/', ext_reg.as_view(), name='ext_reg'),
        path('api-extshop/', ext_shop.as_view(), name='ext_shop'),
        #   Для TV system
        path('api_ext_report/', ApiExtPage.as_view(), name='ext_page'),
        path('ext_page/<str:api_hash>/', ext_page, name='ext_page_show'),
        # Tranzila Apple Pay
        path('.well-known/apple-developer-merchantid-domain-association', download_applepay,
             name="download_applepay"),
        # Download manifest file https://scratch-win.co.il/manifest.json
        path('manifest.json', download_manifest_json, name="download_manifest_json"),
        path('firebase-messaging-sw.js', download_firebase_messaging_sw,
             name="download_firebase_messaging_sw"),
        # Upload csv data from tranzilla
        # path("parse-payment-table/", dump_payments_data_to_database),
        path("upload_payment_answers/", upload_payment_answers_data, name='upload_payment_answers'),
        path("payment_answers/", cab_boss, {'cab_type': 'payment_answers'}, name='payment_answers'),
        # сформировать билеты по подписке вручную
        # Bloggers
        path('cabb_bloggers/', cab_boss, {'cab_type': 'cabb_bloggers'}, name='cabb_bloggers'),
        # ID confirmation
        path('id_confirmation/', cab_boss, {'cab_type': 'id_confirmation'}, name='id_confirmation'),
        # path('game-check-id/<str:verbal>/', game_check_id, name='game_check_id'),
        # path('cabb-idconf-confirm/', cabb_idconf_confirm, name='cabb_idconf_confirm'),
        # path('cabb-idconf-form/', cabb_idconf_form, name='cabb_idconf_form'),
        # path('cabb-idconf-reject/', cabb_idconf_reject, name='cabb_idconf_reject'),
        path('shop-main/<str:company_code>', shop_main, name='shop_main')
    ] \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
