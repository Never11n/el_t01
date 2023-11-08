# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import decimal
import os
import json
import operator
import datetime
import logging
import logging.config
from functools import reduce
import requests
from dateutil.relativedelta import relativedelta

from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.utils.translation import gettext
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q, DecimalField, Count, Sum, F, Case, When, Value, CharField, Func, FloatField
from django.db.models.functions import Coalesce, Cast
from django.core import mail
from validate_email import validate_email
from el_t01_app.service.dft import get_GlobalSettings
from el_t01.settings import MEDIA_ROOT


from .service.service import (paginate,
                              get_main_args,
                              check_template_exists,
                              jellyfish_change_data,
                              generate_hash)
from .models import (BalanceOperation, Game_history, List_jellyfish, Profile, Ticket_history, Feedback, Payout, Payadd,
                     Cashadd, Type_balanceoperation_status, Blacklist, Type_blacklist, Subscription, Blogger, SubsBonus,
                     IdConfirmation, Ticket_type, Report_list, PaymentAnswer,
                     Discount, DiscountList, DiscountHistory, DiscountSet,
                     NotificationSystem, GameLottoProfit, GameLottoResults, EmailToSend, Type_game_status,
                     CommentCallcenter,
                     LottoSubscription)
from .mail_service import send_mail_user
from .views_cab import make_pay_operation
from .views_cab import balance_recalculate
from .views_boss_export import boss_page_export


def cab_boss(request, cab_type=None):
    print("cab_boss")
    print("cab_type ", cab_type)
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if args['me'].profile.is_boss or args['me'].profile.is_manager or args['me'].profile.is_moderator:
            args['l_head_list'] = []
            args['l_header_list'] = []
            args['l_footer_list'] = []
            args['l_script_list'] = []
            args['l_modal_list'] = []
            args['l_body_list'] = []
            args['lf_language'] = check_template_exists("common/section_language_02.html")
            args['l_layout_file'] = check_template_exists("cab_boss/layout.html")
            args['l_head_list'].append(check_template_exists("cab_boss/l_head_01.html"))
            args['l_header_list'].append(check_template_exists("cab_boss/l_header.html"))
            args['l_script_list'].append(check_template_exists("cab_boss/l_script_01.html"))
            if cab_type == "cabb_users":
                m_uName = request.GET.get('uName', "")
                m_uEmail = request.GET.get('uEmail', "")
                m_uPhone = request.GET.get('uPhone', "")
                _list_users = Profile.objects.all().annotate(
                    num_tickets=Count('user__game_user__games_id_history')).order_by("-date_joined")

                values_by_dates = Profile.objects.values('date_joined__date').annotate(
                    joined=Count('id', distinct=True),
                    played=Count('user__game_user__user_id', filter=Q(user__game_user__t_status__verbal='start'),
                                 distinct=True),
                    tickets=Count('user__game_user__games_id_history')
                ).order_by('-date_joined__date')
                args['values_by_dates'] = {datetime.datetime.strftime(i['date_joined__date'], "%d.%m.%Y"): i for i in values_by_dates}
                # args['values_by_dates'] = {i['date_joined__date']: i for i in values_by_dates}

                args['m_addTitle'] = ""
                if 'm_uName' != "":
                    args['m_uName'] = m_uName
                    args['m_addTitle'] = f"name={m_uName}"
                    _list_users = _list_users.filter(name__icontains=m_uName)
                if m_uEmail != "":
                    args['m_uEmail'] = m_uEmail
                    args['m_addTitle'] += f" email={m_uName}"
                    _list_users = _list_users.filter(user__email__icontains=m_uEmail)
                if m_uPhone != "":
                    args['m_uPhone'] = m_uPhone
                    args['m_addTitle'] += f" phone={m_uPhone}"
                    _list_users = _list_users.filter(mobile__icontains=m_uPhone)
                m_list_per_page = args['GL_CabbNumberInPage']
                p = 1
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                p, args['list_users'] = paginate(_list_users, p, m_list_per_page)
                args['pagin_list_all'] = _list_users.count()
                args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                args['pagin_list_02'] = m_list_per_page * p
                if args['pagin_list_02'] > args['pagin_list_all']:
                    args['pagin_list_02'] = args['pagin_list_all']
                args['pagin_url'] = "/cabb_users"
                args['pagin_list'] = args['list_users']
                args['menu_item'] = 'nav-link_cabb_users'
                args['menu_user_item'] = 'nav-link_users'
                args['l_pagination'] = f"{args['GL_MainSkin']}/common/_pagination.html"
                args['l_find'] = check_template_exists("cab_boss/_cab_find_01.html")
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_users.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/cabb_modal_editbalance.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_userprofileedit.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))

            elif cab_type == "cabb_games":
                _list_games = Game_history.objects.all().order_by("-dt_add")

                m_list_per_page = args['GL_CabbNumberInPage']
                p = 1
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                p, args['list_games'] = paginate(_list_games, p, m_list_per_page)
                args['pagin_list_all'] = _list_games.count()
                args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                args['pagin_list_02'] = m_list_per_page * p
                if args['pagin_list_02'] > args['pagin_list_all']:
                    args['pagin_list_02'] = args['pagin_list_all']
                args['pagin_url'] = "/cabb_games"
                args['pagin_list'] = args['list_games']

                args['menu_item'] = 'nav-link_cabb_games'
                args['l_pagination'] = f"{args['GL_MainSkin']}/common/_pagination.html"
                args['l_find'] = check_template_exists("cab_boss/_cab_find_game.html")
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_games.html"))
            elif cab_type == "cabb_tickets":
                mm_time_1 = datetime.datetime.now()

                _list_tickets = Ticket_history.objects.all().order_by("-req_dt")
                m_uTicket = request.GET.get('uTicket', "")
                args['m_addTitle'] = ""
                if m_uTicket != "":
                    args['m_uTicket'] = m_uTicket
                    args['m_addTitle'] = f"name={m_uTicket}"
                    _list_tickets = _list_tickets.filter(answ_nom__icontains=m_uTicket)
                m_list_per_page = args['GL_CabbNumberInPage']
                p = 1
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                p, args['list_tickets'] = paginate(_list_tickets, p, m_list_per_page)
                args['pagin_list_all'] = _list_tickets.count()
                args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                args['pagin_list_02'] = m_list_per_page * p
                if args['pagin_list_02'] > args['pagin_list_all']:
                    args['pagin_list_02'] = args['pagin_list_all']
                args['pagin_url'] = "/cabb_tickets"
                args['pagin_list'] = args['list_tickets']
                args['menu_item'] = 'nav-link_cabb_tickets'
                args['l_pagination'] = f"{args['GL_MainSkin']}/common/_pagination.html"
                args['l_find'] = check_template_exists("cab_boss/_cab_find_tickets.html")
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_tickets.html"))
                args['l_tickets_body'] = check_template_exists("cab_boss/cabb_tickets_body.html")
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_ticketcheck.html"))
                # args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_ticketcheck_lotto.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_blank.html"))
                mm_time_2 = datetime.datetime.now()
                print(f"time = {mm_time_1} {mm_time_2}")
                print(f"time = {mm_time_2 - mm_time_1}")
            elif cab_type == "cabb_tickets_check":
                mm_time_1 = datetime.datetime.now()

                _list_tickets = Ticket_history.objects.all().order_by("-req_dt")
                m_uTicket = request.GET.get('uTicket', "")
                args['m_addTitle'] = ""
                if m_uTicket != "":
                    args['m_uTicket'] = m_uTicket
                    args['m_addTitle'] = f"name={m_uTicket}"
                    _list_tickets = _list_tickets.filter(answ_nom__icontains=m_uTicket)
                # m_list_per_page = args['GL_CabbNumberInPage']
                # p = 1
                # if 'page' in request.GET:
                #     p = int(request.GET['page'])
                # p, args['list_tickets'] = paginate(_list_tickets, p, m_list_per_page)

                args['list_tickets'] = _list_tickets[:50]

                # args['pagin_list_all'] = _list_tickets.count()
                # args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                # args['pagin_list_02'] = m_list_per_page * p
                # if args['pagin_list_02'] > args['pagin_list_all']:
                #     args['pagin_list_02'] = args['pagin_list_all']
                # args['pagin_url'] = "/cabb_tickets"
                # args['pagin_list'] = args['list_tickets']
                args['menu_item'] = 'nav-link_cabb_tickets_check'
                # args['l_pagination'] = f"{args['GL_MainSkin']}/common/_pagination.html"
                args['l_find'] = check_template_exists("cab_boss/_cab_find_tickets.html")
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_tickets.html"))
                args['l_tickets_body'] = check_template_exists("cab_boss/cabb_tickets_body.html")
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_ticketcheck.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_blank.html"))
                mm_time_2 = datetime.datetime.now()

            elif cab_type == "cabb_lotto_tickets_check":
                m_type_ticket = request.GET.get('ticket', "all")
                if m_type_ticket == "all":
                    _list_tickets = Ticket_history.objects.filter(~Q(game_type__t_type__verbal='old')).order_by("-req_dt")
                else:
                    _list_tickets = Ticket_history.objects.filter(game_type__t_type__verbal=m_type_ticket).order_by("-req_dt")
                # args['list_tickets'] = _list_tickets
                m_list_per_page = args['GL_CabbNumberInPage']

                p = 1
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                p, args['list_tickets'] = paginate(_list_tickets, p, m_list_per_page)

                now = timezone.now()
                args['less_15_min_left'] = []
                args['draw_is_over'] = []
                for ticket in args['list_tickets']:
                    if ticket.lotto_result:
                        try:
                            if ticket.lotto_result.draw_date:
                                # if now < ticket.lotto_result.draw_date:
                                delta = ticket.lotto_result.draw_date - now
                                delta_minutes = round(delta.total_seconds() / 60)
                                if 15 >= delta_minutes > 0:
                                    print(ticket, delta_minutes)
                                    args['less_15_min_left'].append(ticket.id)
                                elif delta_minutes < 0 and ticket.games_id.t_status.verbal != 'finish':
                                    print(ticket, delta_minutes)
                                    args['draw_is_over'].append(ticket.id)
                        except Exception:
                            continue

                args['pagin_list_all'] = _list_tickets.count()
                args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                args['pagin_list_02'] = m_list_per_page * p
                if args['pagin_list_02'] > args['pagin_list_all']:
                    args['pagin_list_02'] = args['pagin_list_all']
                args['pagin_url'] = "/cabb_tickets"
                args['pagin_list'] = args['list_tickets']
                args['l_pagination'] = f"{args['GL_MainSkin']}/common/_pagination.html"
                args['menu_item'] = f'nav-link_cabb_lotto_tickets_check-{m_type_ticket}'

                args['l_body_list'].append(check_template_exists("cab_boss/cabb_tickets.html"))
                args['l_tickets_body'] = check_template_exists("cab_boss/cabb_tickets_body_lotto.html")
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_ticketcheck.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_blank.html"))
            elif cab_type == "boss_game_type":
                args['menu_item'] = 'nav-link_profile'
                args['l_body_list'].append(check_template_exists("cab_boss/boss_pasw.html"))
            elif cab_type == "cabb_feedback_new":
                args['list_feedback'] = Feedback.objects.filter(status="00").order_by('-created')
                args['menu_item'] = 'nav-link_cabb_feedback'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_feedback_new.html"))
                # args['l_script_list'].append('')
                # args['l_modal_list'].append(check_template_exists("cab_boss/cabb_modal_feedback_replay.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_feedback.html"))
            elif cab_type == "cabb_feedback_ok":
                args['list_feedback'] = Feedback.objects.filter(status="01").order_by('-created')
                args['menu_item'] = 'nav-link_cabb_feedback'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_feedback_ok.html"))
                # args['l_modal_list'].append(check_template_exists("cab_boss/cabb_modal_feedback_replay.html"))
            elif cab_type == "cabb_feedback_block":
                args['list_feedback'] = Feedback.objects.filter(status="02").order_by('-created')
                args['menu_item'] = 'nav-link_cabb_feedback'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_feedback_block.html"))
                # args['l_modal_list'].append(check_template_exists("cab_boss/cabb_modal_feedback_replay.html"))
            elif cab_type == "cabb_payout_new":
                args['list_payout'] = Payout.objects.filter(status__in=["00", "04"]).order_by('-created')
                args['menu_item'] = 'nav-link_cabb_payout'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_payout_new.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))
                # args['l_script_list'].append('')
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_payout.html"))
            elif cab_type == "cabb_payout_ok":
                args['list_payout'] = Payout.objects.filter(status="01").order_by('-created')
                args['menu_item'] = 'nav-link_cabb_payout'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_payout_ok.html"))
                # args['l_modal_list'].append('cab_boss/cabb_modal_feedback_replay.html')
            elif cab_type == "cabb_payout_reject":
                args['list_payout'] = Payout.objects.filter(status="02").order_by('-created')
                args['menu_item'] = 'nav-link_cabb_payout'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_payout_reject.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))
            elif cab_type == "cabb_payadd_new":
                args['list_payadd'] = Payadd.objects.filter(status="00").order_by('-created')
                args['menu_item'] = 'nav-link_cabb_payadd'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_payadd_new.html"))
                # args['l_script_list'].append('')
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_payadd.html"))
            elif cab_type == "cabb_payadd_ok":
                args['list_payadd'] = Payadd.objects.filter(Q(status='01') | Q(status='02')).order_by('-created')
                args['menu_item'] = 'nav-link_cabb_payadd'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_payadd_ok.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_payadd.html"))
            elif cab_type == "cabb_cashadd_new":
                args['list_cashadd'] = Cashadd.objects.filter(status="00").order_by('-created')
                args['menu_item'] = 'nav-link_cabb_cashadd'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_cashadd_new.html"))
                # args['l_script_list'].append('')
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_cashadd.html"))
            elif cab_type == "cabb_cashadd_ok":
                args['list_cashadd'] = Cashadd.objects.filter(status='01').order_by('-created')
                args['menu_item'] = 'nav-link_cabb_cashadd'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_cashadd_ok.html"))
                # args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_cashadd.html"))
            elif cab_type == "cabb_cashadd_block":
                args['list_cashadd'] = Cashadd.objects.filter(status='02').order_by('-created')
                args['menu_item'] = 'nav-link_cabb_cashadd'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_cashadd_block.html"))
                # args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_cashadd.html"))
            elif cab_type == "cabb_cabala":
                _list_games = Game_history.objects.all().order_by("-dt_add")

                m_list_per_page = args['GL_CabbNumberInPage']
                p = 1
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                p, args['list_games'] = paginate(_list_games, p, m_list_per_page)
                args['pagin_list_all'] = _list_games.count()
                args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                args['pagin_list_02'] = m_list_per_page * p
                if args['pagin_list_02'] > args['pagin_list_all']:
                    args['pagin_list_02'] = args['pagin_list_all']
                args['pagin_url'] = "/cabb_games"
                args['pagin_list'] = args['list_games']

                args['menu_item'] = 'nav-link_cabb_games'
                args['l_find'] = check_template_exists("cab_boss/_cab_find_game.html")
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_cabala.html"))
            elif cab_type == "cabb_blist":
                _list_blacklist = Blacklist.objects.all().order_by("-created")

                m_list_per_page = args['GL_CabbNumberInPage']
                p = 1
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                p, args['list_blacklist'] = paginate(_list_blacklist, p, m_list_per_page)
                args['pagin_list_all'] = _list_blacklist.count()
                args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                args['pagin_list_02'] = m_list_per_page * p
                if args['pagin_list_02'] > args['pagin_list_all']:
                    args['pagin_list_02'] = args['pagin_list_all']
                args['pagin_url'] = "/cabb_blist"
                args['pagin_list'] = args['list_blacklist']

                args['menu_item'] = 'nav-link_cabb_users'
                args['menu_user_item'] = 'nav-link_cabb_blist'
                args['l_pagination'] = f"{args['GL_MainSkin']}/common/_pagination.html"
                # args['l_find'] = check_template_exists("cab_boss/_cab_find_game.html")
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_blist.html"))
            elif cab_type == "cabb_subs":
                m_uEmail = request.GET.get('uEmail', "")
                m_active = request.GET.get('active', "")
                m_daterange_create = request.GET.get('daterange', '')
                m_daterange_active = request.GET.get('daterange_2', '')
                m_weekdays = request.GET.get('weekdays', '')
                _list_subscription = Subscription.objects.all().order_by("-dt_add")
                if m_uEmail != "":
                    args['m_uEmail'] = m_uEmail
                    _list_subscription = _list_subscription.filter(user_id__email__icontains=m_uEmail)
                if m_active == '1':
                    args['m_active'] = m_active
                    _list_subscription = _list_subscription.filter(enabled=True)
                if m_daterange_create != '':
                    args['date_range'] = m_daterange_create
                    m_daterange_create_list = m_daterange_create.split("-")
                    try:
                        m_date_start = datetime.datetime.strptime(m_daterange_create_list[0].strip(), "%d.%m.%Y")
                        m_date_finish = datetime.datetime.strptime(m_daterange_create_list[1].strip(), "%d.%m.%Y")
                        _list_subscription = _list_subscription.filter(dt_add__range=[m_date_start, m_date_finish])
                    except Exception:
                        _list_subscription = _list_subscription
                if m_daterange_active != '':
                    args['date_range_2'] = m_daterange_active
                    m_daterange_active_list = m_daterange_active.split("-")
                    try:
                        m_date_start = datetime.datetime.strptime(m_daterange_active_list[0].strip(), "%d.%m.%Y")
                        m_date_finish = datetime.datetime.strptime(m_daterange_active_list[1].strip(), "%d.%m.%Y")
                        _list_subscription = _list_subscription.filter(
                            (Q(dt_start__range=[m_date_start, m_date_finish]) | Q(dt_start__lt=m_date_start) &
                             (Q(dt_stop__range=[m_date_start, m_date_finish]) | Q(dt_stop__gt=m_date_finish))
                             )
                        )
                    except Exception:
                        _list_subscription = _list_subscription

                if m_weekdays != '':
                    weekdays = [f'day_{i}' for i in m_weekdays]
                    argument_list = []
                    for day in weekdays:
                        argument_list.append(Q(**{day: True}))
                    _list_subscription = _list_subscription.filter(reduce(operator.or_, argument_list))
                args['weekdays'] = '1234567' if m_weekdays == '' else m_weekdays
                m_list_per_page = args['GL_CabbNumberInPage']
                p = 1
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                p, args['list_subscription'] = paginate(_list_subscription, p, m_list_per_page)

                args['pagin_list_all'] = _list_subscription.count()
                args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                args['pagin_list_02'] = m_list_per_page * p
                if args['pagin_list_02'] > args['pagin_list_all']:
                    args['pagin_list_02'] = args['pagin_list_all']
                args['pagin_url'] = "/cabb_subs"
                args['pagin_list'] = args['list_subscription']

                args['menu_item'] = 'nav-link_cabb_users'
                args['menu_user_item'] = 'nav-link_cabb_subs'
                args['l_pagination'] = f"{args['GL_MainSkin']}/common/_pagination.html"
                args['l_find'] = check_template_exists("cab_boss_subs/_cab_find_subs.html")
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))
                args['l_body_list'].append(check_template_exists("cab_boss_subs/cabb_subs.html"))
            elif cab_type == "cabb_bloggers":
                _bloggers_list = Blogger.objects.values(
                    'id', 'name', 'ref_hash', 'ref_link', 'accounts', 'phone', 'notes', 'b_type__caption'
                ).order_by('-id')
                for blogger in _bloggers_list:
                    profiles = Profile.objects.filter(settings__has_key="ref_blogger_id").filter(
                        settings__ref_blogger_id=blogger['id']).count()
                    blogger['count_profiles'] = profiles
                args['bloggers_list'] = _bloggers_list
                args['menu_item'] = 'nav-link_cabb_users'
                args['menu_user_item'] = 'nav-link_bloggers'
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))
                args['l_body_list'].append(check_template_exists("cab_boss_bloggers/cabb_bloggers.html"))
            elif cab_type == "id_confirmation":
                m_statuses = request.GET.get('status')
                if not m_statuses:
                    _confirmations_list = IdConfirmation.objects.filter(status__verbal__in=['wait', 'repeat']).order_by('-id')
                else:
                    _confirmations_list = IdConfirmation.objects.all().order_by('-id')
                m_uName = request.GET.get('uName')
                m_uEmail = request.GET.get('uEmail')
                m_uPhone = request.GET.get('uPhone')
                m_idcard = request.GET.get('uIdcard')
                if m_statuses:
                    m_statuses_list = [i for i in m_statuses.split('-') if i != '']
                    _confirmations_list = _confirmations_list.filter(status__verbal__in=m_statuses_list)
                args['statuses'] = ['wait', 'repeat'] if not m_statuses else m_statuses
                if m_uName:
                    args['m_uName'] = m_uName
                    _confirmations_list = _confirmations_list.filter(user__profile__name__icontains=m_uName)
                if m_uEmail:
                    args['m_uEmail'] = m_uEmail
                    _confirmations_list = _confirmations_list.filter(user__email__icontains=m_uEmail)
                if m_uPhone:
                    args['m_uPhone'] = m_uPhone
                    _confirmations_list = _confirmations_list.filter(user__profile__mobile__icontains=m_uPhone)
                if m_idcard:
                    args['m_idcard'] = m_idcard
                    _confirmations_list = _confirmations_list.filter(user__profile__i_doc__icontains=m_idcard)
                if request.GET.get('is_export', 'false') == 'true':
                    columns = ['Request id', 'Status', 'Date add', 'User id', 'Email', 'Name',
                               'Date joined', 'Phone', 'Birthday', 'ID number']
                    values = {1: 'id', 2: ['status', 'caption'], 3: 'dt_add',
                              4: ['user', 'id'], 5: ['user', 'email'], 6: ['user', 'profile', 'name'],
                              7: ['user', 'profile', 'date_joined'], 8: ['user', 'profile', 'mobile'],
                              9: ['user', 'profile', 'date_birthday'], 10: ['user', 'profile', 'i_doc']}
                    return boss_page_export(columns, values, _confirmations_list, 'Id confirmations')
                # args['conf_list'] = _confirmations_list
                m_list_per_page = args['GL_CabbNumberInPage']
                p = 1
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                p, args['conf_list'] = paginate(_confirmations_list, p, m_list_per_page)
                args['pagin_list_all'] = _confirmations_list.count()
                args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                args['pagin_list_02'] = m_list_per_page * p
                if args['pagin_list_02'] > args['pagin_list_all']:
                    args['pagin_list_02'] = args['pagin_list_all']
                args['pagin_url'] = "/id_confirmation"
                args['pagin_list'] = args['conf_list']
                args['l_pagination'] = f"{args['GL_MainSkin']}/common/_pagination.html"

                args['menu_item'] = 'nav-link_cabb_users'
                args['menu_user_item'] = 'nav-link_confs'
                args['l_find'] = check_template_exists("cab_boss/_cab_find_multi.html")
                args['l_find_uphone'] = True
                args['l_find_name'] = True
                args['l_find_uemail'] = True
                args['l_find_id_confirmation'] = True
                args['l_body_list'].append(check_template_exists("cab_boss_id_conf/id_conf_admin.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))

            elif cab_type == "cabb_reports":
                list_reports = Report_list.objects.filter(enabled=True).order_by("verbal")
                args['list_reports'] = list_reports
                args['menu_item'] = 'nav-link_cabb_reports'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_reports.html"))
            elif cab_type == "payment_answers":
                today = datetime.datetime.now().date()
                _list_answers = PaymentAnswer.objects.filter(created_date__date=today).order_by("-created_date")
                m_daterange_create = request.GET.get('daterange', '')
                if m_daterange_create != '':
                    args['date_range'] = m_daterange_create
                    m_daterange_create_list = m_daterange_create.split("-")
                    try:
                        m_date_start = datetime.datetime.strptime(m_daterange_create_list[0].strip(), "%d.%m.%Y")
                        m_date_finish = datetime.datetime.strptime(m_daterange_create_list[1].strip(), "%d.%m.%Y")
                        _list_answers = PaymentAnswer.objects.filter(created_date__range=[m_date_start, m_date_finish])
                    except Exception:
                        _list_answers = _list_answers
                m_list_per_page = args['GL_CabbNumberInPage']
                p = 1
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                p, args['list_answers'] = paginate(_list_answers, p, m_list_per_page)
                args['pagin_list_all'] = _list_answers.count()
                args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                args['pagin_list_02'] = m_list_per_page * p
                if args['pagin_list_02'] > args['pagin_list_all']:
                    args['pagin_list_02'] = args['pagin_list_all']
                args['pagin_url'] = "/payment_answers"
                args['pagin_list'] = args['list_answers']
                args['menu_item'] = 'nav-link_cabb_payout'
                args['l_pagination'] = f"{args['GL_MainSkin']}/common/_pagination.html"
                args['l_find'] = check_template_exists("cab_boss/_cab_find_multi.html")
                args['l_find_date_range'] = True
                args['l_body_list'].append(check_template_exists("cab_boss/uploaded_payment_answers.html"))
            elif cab_type == "cabb_subs_bonuses":
                list_bonuses = SubsBonus.objects.all().order_by("ticket_type", "max_days", "type_payment")
                args['list_bonuses'] = list_bonuses
                args['menu_item'] = 'nav-link_cabb_users'
                args['menu_user_item'] = 'nav-link_cabb_bonuses'
                args['l_body_list'].append(check_template_exists("cab_boss_subs/cabb_subs_bonuses.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))
            elif cab_type == "cabb_discounts":
                list_discounts = Discount.objects.values(
                    'id', 'verbal', 'enabled', 'caption', 'caption_user', 'start_date', 'stop_date').order_by('-id')
                for disc in list_discounts:
                    disc_sets = DiscountSet.objects.filter(disc_id=disc['id'])
                    disc.update({'disc_sets': disc_sets})
                args['list_discounts'] = list_discounts
                args['menu_item'] = 'nav-link_cabb_users'
                args['menu_user_item'] = 'nav-link_discounts'
                args['l_body_list'].append(check_template_exists("cab_boss_discounts/cabb_discounts.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))
            elif cab_type == "cabb_discount_lists":
                discount_lists = DiscountList.objects.all().order_by('-id')
                args['discount_lists'] = discount_lists
                args['menu_item'] = 'nav-link_cabb_users'
                args['menu_user_item'] = 'nav-link_discount_lists'
                args['l_body_list'].append(check_template_exists("cab_boss_discounts/cabb_discount_lists.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))
            elif cab_type == "cabb_discount_histories":
                discount_histories = DiscountHistory.objects.all().order_by('-id')
                m_uEmail = request.GET.get('uEmail')
                if m_uEmail:
                    args['m_uEmail'] = m_uEmail
                    discount_histories = discount_histories.filter(user__email__icontains=m_uEmail)
                args['discount_histories'] = discount_histories
                args['l_find'] = check_template_exists("cab_boss/_cab_find_multi.html")
                args['l_find_uemail'] = True
                args['menu_item'] = 'nav-link_cabb_users'
                args['menu_user_item'] = 'nav-link_discount_histories'
                args['l_body_list'].append(check_template_exists("cab_boss_discounts/cabb_discount_histories.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))
            elif cab_type == "cabb_system_notifications":
                list_notifications = NotificationSystem.objects.all().order_by('-id')
                args['list_notifications'] = list_notifications
                args['menu_item'] = 'nav-link_cabb_users'
                args['menu_user_item'] = 'nav-link_notifications_list'
                args['l_body_list'].append(check_template_exists("cab_boss_notifications/notifications_list.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))
            elif cab_type == "cabb_lotto_profits":
                list_lotto_profits = GameLottoProfit.objects.all().order_by('ticket_type', 'sum_from')
                args['list_lotto_profits'] = list_lotto_profits
                args['menu_item'] = 'nav-link_lotto_profits'
                args['l_body_list'].append(check_template_exists("cab_boss_lotto/cabb_lotto_profits.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))
            elif cab_type == "cabb_lotto_results":
                list_lotto_results = GameLottoResults.objects.all().order_by('lotto_type', 'ticket_type', '-lottery_number')
                args['list_lotto_profits'] = list_lotto_results
                args['menu_item'] = 'nav-link_lotto_results'
                args['l_body_list'].append(check_template_exists("cab_boss_lotto/cabb_lotto_results.html"))
                args['l_modal_list'].append(check_template_exists("cab_boss/_m_cabb_form.html"))
            elif cab_type == "cabb_list_tickets":
                args['menu_item'] = 'nav-link_list_tickets'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_list_tickets.html"))
            elif cab_type == "cabb_callcenter":
                args['l_find'] = check_template_exists("cab_boss/_cab_find_01.html")
                args['menu_item'] = 'nav-link_callcenter_menu'
                args['l_body_list'].append(check_template_exists("cab_boss/cabb_callcenter.html"))
                m_uName = request.GET.get('uName', "")
                m_uEmail = request.GET.get('uEmail', "")
                m_uPhone = request.GET.get('uPhone', "")
                m_uId = request.GET.get('uId', "")
                m_daterange = request.GET.get('daterange', "")

                filters = {}
                if m_uName != "":
                    filters['name__icontains'] = m_uName
                    args['m_uName'] = m_uName
                if m_uEmail != "":
                    filters['user__email__icontains'] = m_uEmail
                    args['m_uEmail'] = m_uEmail
                if m_uPhone != "":
                    filters['mobile__icontains'] = m_uPhone
                    args['m_uPhone'] = m_uPhone
                if len(filters) > 0:
                    profiles = Profile.objects.filter(**filters)
                    if profiles.count() > 0:
                        args['users_list'] = profiles
                    else:
                        args['not_user_with_params'] = True
                if len(filters) == 0 and m_uId == "" and m_daterange == '':
                    args['select_params'] = True
                if m_daterange != '':
                    args['date_range_comment'] = m_daterange
                    m_find_daterange_1 = m_daterange.split("-")
                    m_date_start_txt = m_find_daterange_1[0].strip()[:10]
                    m_date_finish_txt = m_find_daterange_1[1].strip()[:10]
                    m_date_start = datetime.datetime.strptime(m_date_start_txt, "%d.%m.%Y")
                    m_date_finish = datetime.datetime.strptime(m_date_finish_txt, "%d.%m.%Y")
                    comment_list = CommentCallcenter.objects.filter(date_return__range=[m_date_start.date(), m_date_finish.date()])
                    if comment_list.count() > 0:
                        args['comment_list'] = comment_list
                    else:
                        args['comment_list_empty'] = True
                if m_uId != "":
                    args['user_slides'] = True
                    profile = Profile.objects.get(id=m_uId)
                    now = timezone.now()
                    previous_month = (now - relativedelta(months=1)).month
                    previous_year = (now - relativedelta(months=1)).year
                    args['previous_month'] = f'{previous_month}/{str(previous_year)[2:]}'
                    previous_previous_month = (now - relativedelta(months=2)).month
                    previous_previous_year = (now - relativedelta(months=2)).year
                    args['previous_previous_month'] = f'{previous_previous_month}/{str(previous_previous_year)[2:]}'
                    user_bday = profile.date_birthday
                    if user_bday:
                        user_age = now.year - user_bday.year - ((now.month, now.day) < (user_bday.month,user_bday.day))
                    else:
                        user_age = 'Unknown'
                    args['user_info'] = {
                        'name': profile.name, 'phone': profile.mobile, 'email': profile.user.email,
                        'age': user_age, 'register': profile.date_joined, 'profile_id': profile.id
                    }

                    user_tickets_previous_month = Ticket_history.objects.filter(
                        games_id__user_id=profile.user,
                        req_dt__month=previous_month, req_dt__year=previous_year).annotate(win_as_int=Case(
                            When(answ_win_sum='', then=Value(0)),
                            When(answ_win_sum=None, then=Value(0)),
                            default=Cast('answ_win_sum', DecimalField(max_digits=15, decimal_places=2)),
                            output_field=DecimalField(max_digits=15, decimal_places=2)))
                    previous_month_tickets_by_type = user_tickets_previous_month.values(
                        'game_type__caption').distinct().annotate(tickets=Count('id'))
                    args['previous_month_labels'] = []
                    args['previous_month_values'] = []
                    for ticket_type in previous_month_tickets_by_type:
                        args['previous_month_labels'].append(ticket_type['game_type__caption'])
                        args['previous_month_values'].append(ticket_type['tickets'])
                    args['sorted_previous_tickets'] = sorted(
                        list(previous_month_tickets_by_type), key=lambda d: (d['tickets']), reverse=True)

                    previous_month_aggs = user_tickets_previous_month.aggregate(
                        amount=Coalesce(Sum('cost_2'), 0, output_field=DecimalField()),
                        count=Count('id', distinct=True),
                        amount_subs=Coalesce(Sum('cost_2',
                                                 filter=Q(games_id__t_subs__isnull=False) | Q(games_id__t_lotto_subs__isnull=False)),
                                             0, output_field=DecimalField()),
                        total_win=Sum('win_as_int'),
                        subs_win=Coalesce(Sum('win_as_int',
                                              filter=Q(games_id__t_subs__isnull=False) | Q(games_id__t_lotto_subs__isnull=False)),
                                          0, output_field=DecimalField()))
                    args['user_info']['previous_month_agg_amount'] = previous_month_aggs['amount']
                    args['user_info']['previous_month_agg_count'] = previous_month_aggs['count']
                    args['user_info']['previous_month_agg_amount_subs'] = previous_month_aggs['amount_subs']
                    args['user_info']['previous_month_agg_win_sub'] = previous_month_aggs['subs_win']
                    args['user_info']['previous_month_agg_total_win'] = previous_month_aggs['total_win']
                    user_tickets_previous_previous_month = Ticket_history.objects.filter(
                        games_id__user_id=profile.user,
                        req_dt__month=previous_previous_month, req_dt__year=previous_previous_year
                    ).annotate(win_as_int=Case(
                            When(answ_win_sum='', then=Value(0)),
                            When(answ_win_sum=None, then=Value(0)),
                            default=Cast('answ_win_sum', DecimalField(max_digits=15, decimal_places=2)),
                            output_field=DecimalField(max_digits=15, decimal_places=2)))
                    previous_previous_tickets_by_type = user_tickets_previous_previous_month.values(
                        'game_type__caption').distinct().annotate(tickets=Count('id'))
                    args['sorted_previous_previous_tickets'] = sorted(
                        list(previous_previous_tickets_by_type), key=lambda d: (d['tickets']), reverse=True)
                    args['previous_previous_month_labels'] = []
                    args['previous_previous_month_values'] = []
                    for ticket_type in previous_previous_tickets_by_type:
                        args['previous_previous_month_labels'].append(ticket_type['game_type__caption'])
                        args['previous_previous_month_values'].append(ticket_type['tickets'])
                    previous_previous_aggs = user_tickets_previous_previous_month.aggregate(
                        amount=Coalesce(Sum('cost_2'), 0, output_field=DecimalField()),
                        count=Count('id', distinct=True),
                        amount_subs=Coalesce(Sum('cost_2',
                                                 filter=Q(games_id__t_subs__isnull=False) | Q(
                                                     games_id__t_lotto_subs__isnull=False)),
                                             0, output_field=DecimalField()),
                        total_win=Sum('win_as_int'),
                        subs_win=Coalesce(Sum('win_as_int',
                                              filter=Q(games_id__t_subs__isnull=False) | Q(
                                                  games_id__t_lotto_subs__isnull=False)),
                                          0, output_field=DecimalField()))
                    args['user_info']['previous_previous_month_agg_amount'] = previous_previous_aggs['amount']
                    args['user_info']['previous_previous_month_agg_count'] = previous_previous_aggs['count']
                    args['user_info']['previous_previous_month_agg_amount_subs'] = previous_previous_aggs['amount_subs']
                    args['user_info']['previous_previous_month_agg_win_sub'] = previous_previous_aggs['subs_win']
                    args['user_info']['previous_previous_month_agg_total_win'] = previous_previous_aggs['total_win']
                    delta = relativedelta(now, profile.date_joined)
                    args['user_info']['months_on_site'] = delta.months + (delta.years * 12)

                    users_months_activity = Ticket_history.objects.filter(games_id__user_id=profile.user).values(
                        'games_id__user_id_id__email', 'games_id__user_id_id__profile__name',
                        'games_id__user_id_id__profile__mobile',
                        'games_id__user_id_id__profile__date_joined__date').distinct().annotate(
                        month_count=Count(
                            Func(F('req_dt'), Value('MM.yyyy'), function='to_char', output_field=CharField()),
                            distinct=True),
                        tickets_count=Count('id'),
                        amount_sum=Sum('cost_2'),
                        avg_tickets=Case(
                            When(month_count__gt=0, then=F('tickets_count') * 1.0 / F('month_count')),
                            default=None,
                            output_field=FloatField()
                        ),
                        avg_amount=Case(
                            When(month_count__gt=0, then=F('amount_sum') * 1.0 / F('month_count')),
                            default=None,
                            output_field=FloatField()
                        )
                    ).order_by('-month_count')
                    args['activity_labels'] = []
                    args['activity_values'] = []
                    if users_months_activity.count() > 0:
                        args['user_info']['users_months_activity_month_count'] = users_months_activity[0]['month_count']
                        args['user_info']['users_months_activity_avg_tickets'] = int(users_months_activity[0]['avg_tickets'])
                        args['user_info']['users_months_activity_avg_amount'] = round(users_months_activity[0]['avg_amount'], 0)
                        args['activity_labels'] = ['active month', 'not active']
                        not_active_month = args['user_info']['months_on_site'] - users_months_activity[0]['month_count']
                        args['activity_values'] = [users_months_activity[0]['month_count'], not_active_month]
                        if args['user_info']['months_on_site']:
                            args['activity_percent'] = round((users_months_activity[0]['month_count'] * 100) / args['user_info']['months_on_site'], 2)
                        else:
                            args['activity_percent'] = 0
                    if CommentCallcenter.objects.filter(user_profile=profile).exists():
                        last_comment = CommentCallcenter.objects.filter(user_profile=profile).order_by('-date_created')[0]
                        date_return = datetime.datetime.strftime(last_comment.date_return, "%d.%m.%Y") if last_comment.date_return else None
                        args['last_comment'] = f'Last Comment: {last_comment.text} '
                        args['last_comment'] += f'Date: {date_return}' if date_return else ''
            elif cab_type == "cabb_lotto_subs":
                m_uEmail = request.GET.get('uEmail', "")
                m_active = request.GET.get('active', "")
                m_daterange_create = request.GET.get('daterange', '')
                _list_subscription = LottoSubscription.objects.all().order_by("-date_created")
                if m_uEmail != "":
                    args['m_uEmail'] = m_uEmail
                    _list_subscription = _list_subscription.filter(user_owner__email__icontains=m_uEmail)
                if m_active == '1':
                    args['m_active'] = m_active
                    _list_subscription = _list_subscription.filter(enabled=True)
                if m_daterange_create != '':
                    args['date_range'] = m_daterange_create
                    m_daterange_create_list = m_daterange_create.split("-")
                    try:
                        m_date_start = datetime.datetime.strptime(m_daterange_create_list[0].strip(), "%d.%m.%Y")
                        m_date_finish = datetime.datetime.strptime(m_daterange_create_list[1].strip(), "%d.%m.%Y")
                        _list_subscription = _list_subscription.filter(date_created__range=[m_date_start, m_date_finish])
                    except Exception:
                        _list_subscription = _list_subscription
                m_list_per_page = args['GL_CabbNumberInPage']
                p = 1
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                p, args['list_subscription'] = paginate(_list_subscription, p, m_list_per_page)

                args['pagin_list_all'] = _list_subscription.count()
                args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                args['pagin_list_02'] = m_list_per_page * p
                if args['pagin_list_02'] > args['pagin_list_all']:
                    args['pagin_list_02'] = args['pagin_list_all']
                args['pagin_url'] = "/cabb_lotto_subs"
                args['pagin_list'] = args['list_subscription']

                args['menu_item'] = 'nav-link_cabb_users'
                args['menu_user_item'] = 'nav-link_cabb_lotto_subs'
                args['l_pagination'] = f"{args['GL_MainSkin']}/common/_pagination.html"
                args['l_find'] = check_template_exists("cab_boss_lotto/_cab_find_lotto_subs.html")
                args['l_body_list'].append(check_template_exists("cab_boss_lotto/cabb_lotto_subs.html"))
            else:  # cab_type == "boss_cabinet":
                args['menu_item'] = 'nav-link_cabinet'
                args['l_body_list'].append(check_template_exists("cab_boss/cab_game_list.html"))

            # args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
            args['main_tab'] = check_template_exists("cab_boss/cabinet.html")
            return render(request, args['main_tab'], args)
        else:
            return redirect('/')


def cabb_balance_save(request):
    print("cabb_balance_save")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    if not args['me'].profile.is_moderator:
        return redirect('/')

    if request.POST:
        # m_feedback_lang = request.POST.get('feedback_lang', "")
        m_balance_id = request.POST.get('balance_id', "")
        m_balance_num = request.POST.get('balance_num', "")
        try:
            print("save 1")
            t_profile = Profile.objects.get(id=m_balance_id)
            t_profile.balance = m_balance_num
            t_profile.save()
            return_data = {"AnswerCod": "01"}
        except:
            return_data = {"AnswerCod": "00"}
    else:
        return_data = {"AnswerCod": "00"}
    return JsonResponse(return_data)


def cabb_payadd_info(request):
    print("= cabb_payadd_info =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.POST:
            print("request.POST = ", request.POST)
            m_payadd_id = request.POST.get('f_payadd_id', '')
            args['item_payadd'] = Payadd.objects.get(id=m_payadd_id)
            template_name = check_template_exists("cab_boss/_templ_payadd_info.html")
            m_template = get_template(template_name)
            return HttpResponse(m_template.render(args))
        return HttpResponse("ERROR")


def cabb_payadd_conf(request):
    print("= cabb_payadd_conf =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    # ToDo check ADMIN
    if not args['me'].profile.is_boss:
        return redirect('/')
    else:
        if True:
            pass
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                print("POST = ", request.POST)
                try:
                    m_user_id = args['me'].id
                    m_payadd_id = request.POST.get('f_payadd_id', "")
                    m_payadd_conf = request.POST.get('f_payadd_conf', "")
                    print("m_payadd_id   = ", m_payadd_id)
                    print("m_payadd_conf = ", m_payadd_conf)
                    m_balanceoperation_status_verbal = "01"
                    if m_payadd_conf == "01":
                        m_balanceoperation_status_verbal = "04"
                        m_payadd_status = "01"

                    if m_payadd_conf == "02":
                        m_balanceoperation_status_verbal = "02"
                        m_payadd_status = "02"

                    t_payadd = Payadd.objects.get(id=m_payadd_id)
                    t_payadd.status = m_payadd_status
                    t_payadd.t_check = True
                    t_payadd.t_check_user_id = m_user_id
                    t_payadd.t_check_dt = timezone.now()
                    t_payadd.save()

                    m_type_balanceoperation_status_id = Type_balanceoperation_status.objects.get(
                        verbal=m_balanceoperation_status_verbal).id
                    pay_operation = BalanceOperation.objects.get(id=t_payadd.bal_oper_id)
                    pay_operation.status_id = m_type_balanceoperation_status_id
                    pay_operation.save()
                    answer = {"AnswerCod": "01",
                              "AnswerText": ""}
                except:
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cabb_payout_form(request):
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    if not args['me'].profile.is_boss:
        return redirect('/')
    else:
        answer = {"AnswerCod": "00",
                  "AnswerText": gettext("ERROR")}
        if request.GET:
            print("request.GET = ", request.GET)
            m_id = request.GET.get('f_id', "")
            m_typeform = request.GET.get('f_typeform', "")
            m_rejected_payouts = request.GET.get('f_rejected_payouts', "")
            args['rejected_payouts'] = True if m_rejected_payouts == 'true' else False
            try:
                t_payout = Payout.objects.get(id=m_id)
                args['payout'] = t_payout
                args['typeform'] = m_typeform
                m_template_name = check_template_exists("cab_boss/cabb_payout_form.html")
                m_template = get_template(m_template_name)
                m_html = m_template.render(args)
                answer = {"AnswerCod": "01",
                          "AnswerText": "ok",
                          "html": m_html
                          }
            except:
                answer = {"AnswerCod": "00",
                          "AnswerText": gettext("ERROR")}
        if request.POST:
            print("request.POST = ", request.POST)
            m_id = request.POST.get('f_id', "")
            m_action = request.POST.get('f_action', "")
            m_reject_reason = request.POST.get('f_reject_reason', "")
            m_notes = request.POST.get('f_notes', "")
            m_amount = request.POST.get('f_payout_amount', "")
            t_payout = Payout.objects.get(id=m_id)
            if m_action in ['confirm', 'reject', 'save', 'in_process']:
                t_payout.t_check = True
                t_payout.t_check_user_id = args['me'].id
                t_payout.t_check_dt = timezone.now()
                t_payout.reject_reason = m_reject_reason
                t_payout.description = m_notes
                t_payout.amount = decimal.Decimal(m_amount)
                t_payout.save()
                if m_action == "confirm":
                    t_payout.status = '01'
                    t_payout.save()
                    d_globalset = get_GlobalSettings()
                    if d_globalset.get("GL_MES_u_payout", False):
                        send_mail_user(user_id=t_payout.user_id.id, type_mess='payout', l_payout_id=t_payout.id)
                        # if True:
                        #     user_email = t_payout.user_id.email
                        #     email_is_valid = validate_email(user_email, verify=True)
                        #     if email_is_valid:
                        #         m_receiver_email = user_email
                        #         m_title = f"{t_payout.user_id.profile.name} שלום"
                        #         m_link_domen = d_globalset.get("GL_SMS_domen", "")
                        #         m_link_site = m_link_domen
                        #         # m_text = d_globalset.get("GL_MES_u_payout_text", "")
                        #         m_text = None
                        #         m_image = t_payout.photo if t_payout.photo else None
                        #         if m_image:
                        #             m_image = f'{m_link_domen}media/{m_image}'
                        #         email = EmailToSend()
                        #         email.hash = generate_hash(50)
                        #         email.save()
                        #         d_globalset = get_GlobalSettings()

                                # mail_args = {
                                #     "EMAIL_DEFAULT_FROM_EMAIL": d_globalset.get('GL_EMAIL_DEFAULT_FROM_EMAIL'),
                                #     "EMAIL_HOST_USER_NAME": d_globalset.get('GL_EMAIL_HOST_USER_NAME'),
                                #     "EMAIL_SERVICE_NAME": d_globalset.get('GL_EMAIL_SERVICE_NAME'),
                                #     "EMAIL_LOGO_FOR_MAIL": d_globalset.get('GL_EMAIL_LOGO_FOR_MAIL'),
                                #     "EMAIL_LINKS_SOCIAL_MEDIA": d_globalset.get('GL_EMAIL_LINKS_SOCIAL_MEDIA'),
                                #     "EMAIL_LINK_INSTAGRAM": d_globalset.get('GL_EMAIL_LINK_INSTAGRAM'),
                                #     "EMAIL_LINK_FACEBOOK": d_globalset.get('GL_EMAIL_LINK_FACEBOOK'),
                                #     "EMAIL_LINK_YOUTUBE": d_globalset.get('GL_EMAIL_LINK_YOUTUBE'),
                                #     "m_text": m_text,
                                #     "m_image": m_image,
                                #     "m_link_site": m_link_site,
                                #     "m_title": m_title
                                # }
                                # subject = d_globalset.get('GL_MES_u_payout_subject')
                                # template = get_template(f"{d_globalset.get('GL_MainSkin')}/mail/payout.html")
                                # email_body = template.render(mail_args)
                                # email.subject = subject
                                # email.recipient = m_receiver_email
                                # email.html_message = email_body
                                # email.save()
                                # m_email_host_user = f"{d_globalset.get('GL_EMAIL_HOST_USER_NAME')} <{d_globalset.get('GL_EMAIL_DEFAULT_FROM_EMAIL')}>"
                                # mail_connection = mail.get_connection(
                                #     host=d_globalset.get('GL_EMAIL_HOST'),
                                #     port=d_globalset.get('GL_EMAIL_PORT'),
                                #     username=d_globalset.get('GL_EMAIL_HOST_USER'),
                                #     password=d_globalset.get('GL_EMAIL_HOST_PASSWORD'),
                                #     use_tls=d_globalset.get('GL_EMAIL_USE_TLS')
                                # )
                                # mail_connection.open()
                                # mail.send_mail(subject=subject,
                                #                message="",
                                #                from_email=m_email_host_user,
                                #                recipient_list=[m_receiver_email],
                                #                html_message=email_body,
                                #                connection=mail_connection)
                                # mail_connection.close()
                        # except Exception:
                        #     pass
                elif m_action == "reject":
                    t_payout.status = '02'
                elif m_action == "in_process":
                    t_payout.status = '04'
            elif m_action == 'add_photo':
                if 'photo' in request.FILES:
                    t_payout.photo = request.FILES['photo']
            t_payout.save()
            answer = {"AnswerCod": "01",
                      "AnswerText": "ok"}
        return JsonResponse(answer)


def cabb_payout_info(request):
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.POST:
            m_payout_id = request.POST.get('f_payout_id', '')
            args['item_payadd'] = Payout.objects.get(id=m_payout_id)
            template_name = "cab_boss/_templ_payout_info.html"
            m_template = get_template(template_name)
            return HttpResponse(m_template.render(args))
        return HttpResponse("ERROR")


def cabb_payout_conf(request):
    print("= cabb_payout_conf =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    # ToDo check ADMIN
    if not args['me'].profile.is_boss:
        return redirect('/')
    else:
        if True:
            pass
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                print("POST = ", request.POST)
                try:
                    m_user_id = args['me'].id
                    m_payadd_id = request.POST.get('f_payadd_id', "")
                    m_payadd_conf = request.POST.get('f_payadd_conf', "")
                    print("m_payadd_id   = ", m_payadd_id)
                    print("m_payadd_conf = ", m_payadd_conf)
                    m_balanceoperation_status_verbal = "01"
                    if m_payadd_conf == "01":
                        m_balanceoperation_status_verbal = "04"
                        m_payadd_status = "01"

                    if m_payadd_conf == "02":
                        m_balanceoperation_status_verbal = "02"
                        m_payadd_status = "02"

                    t_payadd = Payadd.objects.get(id=m_payadd_id)
                    t_payadd.status = m_payadd_status
                    t_payadd.t_check = True
                    t_payadd.t_check_user_id = m_user_id
                    t_payadd.t_check_dt = timezone.now()
                    t_payadd.save()

                    m_type_balanceoperation_status_id = Type_balanceoperation_status.objects.get(
                        verbal=m_balanceoperation_status_verbal).id
                    pay_operation = BalanceOperation.objects.get(id=t_payadd.bal_oper_id)
                    pay_operation.status_id = m_type_balanceoperation_status_id
                    pay_operation.save()
                    answer = {"AnswerCod": "01",
                              "AnswerText": ""}
                except:
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cabb_user_tickets(request, user_id=0):
    print("cabb_user_tickets")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if args['me'].profile.is_boss or args['me'].profile.is_manager or args['me'].profile.is_moderator:
            print("user_id = ", user_id)
            args['filter_user_id'] = user_id
            args['l_head_list'] = []
            args['l_header_list'] = []
            args['l_footer_list'] = []
            args['l_script_list'] = []
            args['l_modal_list'] = []
            args['l_body_list'] = []
            args['l_layout_file'] = check_template_exists("cab_boss/layout.html")
            args['l_head_list'].append(check_template_exists("cab_boss/l_head_01.html"))
            args['l_header_list'].append(check_template_exists("cab_boss/l_header.html"))
            args['l_script_list'].append(check_template_exists("cab_boss/l_script_01.html"))
            # _list_tickets = Ticket_history.objects.filter(games_id__user_id__id=user_id).order_by("-req_dt")
            _list_tickets = Ticket_history.objects.filter(
                Q(games_id__user_id__id=user_id) | Q(games_id__user_recipient_id=user_id)
            ).order_by("-req_dt")

            for ItemList in _list_tickets:
                m_tmp_game = ItemList.games_id_id
                m_last_4 = ""
                m_card_mask = ""

                try:
                    m_BalanceOperation = BalanceOperation.objects.get(games_id_id=m_tmp_game)
                    if m_BalanceOperation.type_balanceoperation_id == 7:
                        m_pay_response = m_BalanceOperation.pay_response.replace("\n", "").split("QueryDict:")[
                                             -1].strip()[:-1].replace("'", '"')
                        # print("1 m_pay_response  = ", m_pay_response)
                        m_pay_response = json.loads(m_pay_response)
                        # print("2 m_pay_response  = ", m_pay_response)
                        m_last_4 = m_pay_response.get("last_4", "")
                        m_card_mask = m_pay_response.get("card_mask", "")
                except:
                    m_last_4 = ""

                ItemList.last_4 = m_last_4
                ItemList.card_mask = m_card_mask

            if _list_tickets.count() > 0:
                m_list_per_page = args['GL_CabbNumberInPage']
                p = 1
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                p, args['list_tickets'] = paginate(_list_tickets, p, m_list_per_page)
                args['pagin_list_all'] = _list_tickets.count()
                args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                args['pagin_list_02'] = m_list_per_page * p
                if args['pagin_list_02'] > args['pagin_list_all']:
                    args['pagin_list_02'] = args['pagin_list_all']
                args['pagin_url'] = "/cabb_tickets"
                args['pagin_list'] = args['list_tickets']
            else:
                args['pagin_list'] = _list_tickets

            args['l_pagination'] = f"{args['GL_MainSkin']}/common/_pagination.html"
            args['menu_item'] = 'nav-link_cabb_tickets'
            args['l_body_list'].append(check_template_exists("cab_boss/cabb_user_tickets.html"))

            args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
            return render(request, args['main_tab'], args)
        else:
            return redirect('/')


def cabb_user_tickets_and_balops(request, user_id=0):
    print("cabb_user_tickets_and_balops")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if args['me'].profile.is_boss or args['me'].profile.is_manager or args['me'].profile.is_moderator:
            args['filter_user_id'] = user_id
            args['l_head_list'] = []
            args['l_header_list'] = []
            args['l_footer_list'] = []
            args['l_script_list'] = []
            args['l_modal_list'] = []
            args['l_body_list'] = []
            args['l_layout_file'] = check_template_exists("cab_boss/layout.html")
            args['l_head_list'].append(check_template_exists("cab_boss/l_head_01.html"))
            args['l_header_list'].append(check_template_exists("cab_boss/l_header.html"))
            args['l_script_list'].append(check_template_exists("cab_boss/l_script_01.html"))
            _list_all_operations = []
            _list_tickets = Ticket_history.objects.filter(
                Q(games_id__user_id__id=user_id) | Q(games_id__user_recipient_id=user_id)
            ).order_by("-req_dt", "-id")
            for ticket in _list_tickets:
                ticket_dict = {'type': 'Ticket', 'id': ticket.id, 'dt': ticket.req_dt, 'obj': ticket}
                if BalanceOperation.objects.filter(games_id_id=ticket.games_id_id).exists():
                    print ("ticket.games_id_id = ", ticket.games_id_id)
                    # Entry.objects.exclude(
                    # balance_op = BalanceOperation.objects.get(status__verbal_="01", games_id_id=ticket.games_id_id)
                    # balance_op = BalanceOperation.objects.get(status__verbal__in=["02", "03", "04"], games_id_id=ticket.games_id_id)
                    balance_op = BalanceOperation.objects.filter(status__verbal__in=["02", "03", "04"], games_id_id=ticket.games_id_id)
                    balance_op = balance_op[0]

                    if balance_op.type_balanceoperation_id == 7:
                        m_pay_response = balance_op.pay_response.replace("\n", "").split("QueryDict:")[-1].strip()[:-1].replace("'", '"')
                        try:
                            m_pay_response = json.loads(m_pay_response)
                            m_last_4 = m_pay_response.get("last_4")
                            m_card_mask = m_pay_response.get("card_mask")
                            if m_last_4 or m_card_mask:
                                ticket_dict['card'] = [m_last_4, m_card_mask]
                        except Exception:
                            pass
                _list_all_operations.append(ticket_dict)
            _list_operations = BalanceOperation.objects.filter(
                user_id=user_id, status__verbal='04', type_balanceoperation__verbal__in=['payout', 'cashadd', 'add_money', 'cut_money']
            ).order_by("-t_create_dt")
            for operation in _list_operations:
                if operation.t_create_user:
                    m_create_user_name = operation.t_create_user.profile.name
                    m_create_user_email = operation.t_create_user.email
                else:
                    m_create_user_name = 'system'
                    m_create_user_email = ''

                _list_all_operations.append({'type': operation.type_balanceoperation.caption,
                                             'id': operation.id, 'dt': operation.created, 'obj': operation,
                                             't_create_user_name': m_create_user_name,
                                             't_create_user_email': m_create_user_email,
                                             })
            _list_all_operations = sorted(_list_all_operations, key=lambda d: (d['dt'], d['id']))

            comparing_balance = 0
            for item in _list_all_operations:
                if item['type'] == 'Ticket':
                    if item['obj'].games_id.game_type.verbal in ['game', 'game_lotto']:
                        if item['obj'].balance_01 != comparing_balance:
                            item['error'] = True
                        comparing_balance = item['obj'].balance_02
                    elif item['obj'].games_id.game_type.verbal in ['game_gift', 'game_lotto_gift']:
                        if item['obj'].games_id.user_recipient_id == user_id:
                            if item['obj'].recipient_balance_01 != comparing_balance:
                                item['error'] = True
                            comparing_balance = item['obj'].recipient_balance_02
                        elif item['obj'].games_id.user_id_id == user_id:
                            if item['obj'].balance_01 != comparing_balance:
                                item['error'] = True
                            comparing_balance = item['obj'].balance_02
                else:
                    if item['obj'].type_balanceoperation.verbal == 'payout':
                        comparing_balance -= item['obj'].amount
                    elif item['obj'].type_balanceoperation.verbal in ['cashadd', 'add_money']:
                        comparing_balance += item['obj'].amount

            _list_all_operations = sorted(_list_all_operations, key=lambda d: (d['dt'], d['id']), reverse=True)
            if len(_list_all_operations) > 0:
                m_list_per_page = 150
                p = 1
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                p, args['list_operations'] = paginate(_list_all_operations, p, m_list_per_page)
                args['pagin_list_all'] = len(_list_all_operations)
                args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                args['pagin_list_02'] = m_list_per_page * p
                if args['pagin_list_02'] > args['pagin_list_all']:
                    args['pagin_list_02'] = args['pagin_list_all']
                args['pagin_url'] = "/cabb_tickets"
                args['pagin_list'] = args['list_operations']
            else:
                args['pagin_list'] = _list_all_operations

            args['l_pagination'] = f"{args['GL_MainSkin']}/common/_pagination.html"
            args['menu_item'] = 'nav-link_cabb_tickets'
            args['l_body_list'].append(check_template_exists("cab_boss/cabb_user_tickets_and_balops.html"))

            args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
            return render(request, args['main_tab'], args)
        else:
            return redirect('/')


def cabb_user_tickets_action(request):
    print("cabb_user_tickets_action")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        answer = {"AnswerCod": "00",
                  "AnswerText": gettext("ERROR")}
        if request.POST:
            print("POST = ", request.POST)
            try:
                m_type_action = request.POST.get('type_action', "")
                m_ticket_id = request.POST.get('ticket_id', "")
                m_user_id = request.POST.get('user_id', "")
                if m_type_action == "recalculate":
                    balance_recalculate(m_user_id, m_ticket_id)
                elif  m_type_action == "":
                    pass
                else:
                    pass
                answer = {"AnswerCod": "01",
                          "AnswerText": ""}
            except Exception as ex:
                print("ex = ", ex)
                answer = {"AnswerCod": "00",
                          "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cabb_user_payoperation(request, user_id=0):
    print("cabb_user_payoperation")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if args['me'].profile.is_boss or args['me'].profile.is_manager or args['me'].profile.is_moderator:
            print("user_id = ", user_id)

            args['l_head_list'] = []
            args['l_header_list'] = []
            args['l_footer_list'] = []
            args['l_script_list'] = []
            args['l_modal_list'] = []
            args['l_body_list'] = []
            args['l_layout_file'] = check_template_exists("cab_boss/layout.html")
            args['l_head_list'].append(check_template_exists("cab_boss/l_head_01.html"))
            args['l_header_list'].append(check_template_exists("cab_boss/l_header.html"))
            args['l_script_list'].append(check_template_exists("cab_boss/l_script_01.html"))
            # args[""]
            _list_balanceOperation = BalanceOperation.objects.filter(user_id_id=user_id).order_by("-created")
            if _list_balanceOperation.count() > 0:
                m_list_per_page = args['GL_CabbNumberInPage']
                p = 1
                if 'page' in request.GET:
                    p = int(request.GET['page'])
                p, args['list_balanceOperation'] = paginate(_list_balanceOperation, p, m_list_per_page)
                args['pagin_list_all'] = _list_balanceOperation.count()
                args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
                args['pagin_list_02'] = m_list_per_page * p
                if args['pagin_list_02'] > args['pagin_list_all']:
                    args['pagin_list_02'] = args['pagin_list_all']
                args['pagin_url'] = "/cabb_tickets"
                args['pagin_list'] = args['list_balanceOperation']
            else:
                args['pagin_list'] = _list_balanceOperation

            args['l_pagination'] = f"{args['GL_MainSkin']}/common/_pagination.html"
            args['menu_item'] = 'nav-link_cabb_tickets'
            args['l_body_list'].append(check_template_exists("cab_boss/cabb_user_payoperation.html"))

            args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
            return render(request, args['main_tab'], args)
        else:
            return redirect('/')


# def cabb_user_payoperation(request, user_id=0):
#     print("cabb_user_payoperation")
#     args = get_main_args(request, section="main")
#     if not args['logged_in']:
#         return redirect('/')
#     else:
#         if args['me'].profile.is_boss or args['me'].profile.is_manager or args['me'].profile.is_moderator:
#             print ("user_id = ", user_id)
#             # args['l_head_list'] = []
#             # args['l_header_list'] = []
#             # args['l_footer_list'] = []
#             # args['l_script_list'] = []
#             # args['l_modal_list'] = []
#             # args['l_body_list'] = []
#             args['l_layout_file'] = 'cab_boss/layout.html'
#             args['l_head_list'].append('cab_boss/l_head_01.html')
#             args['l_header_list'].append('cab_boss/l_header.html')
#             args['l_script_list'].append('cab_boss/l_script_01.html')
#             # args[""]
#
#             _list_tickets = Ticket_history.objects.filter(games_id__user_id__id=user_id).order_by("-req_dt")
#
#             t_balanceOperation = BalanceOperation.objects.filter(user_id_id=user_id).order_by("-created")
#             args['balanceOperation'] = t_balanceOperation
#
#             if _list_tickets.count() > 0:
#                 m_list_per_page = args['GL_CabbNumberInPage']
#                 p = 1
#                 if 'page' in request.GET:
#                     p = int(request.GET['page'])
#                 p, args['list_tickets'] = paginate(_list_tickets, p, m_list_per_page)
#                 args['pagin_list_all'] = _list_tickets.count()
#                 args['pagin_list_01'] = (m_list_per_page * p) - m_list_per_page + 1
#                 args['pagin_list_02'] = m_list_per_page * p
#                 if args['pagin_list_02'] > args['pagin_list_all']:
#                     args['pagin_list_02'] = args['pagin_list_all']
#                 args['pagin_url'] = "/cabb_tickets"
#                 args['pagin_list'] = args['list_tickets']
#             else:
#                 args['pagin_list'] = _list_tickets
#
#             args['menu_item'] = 'nav-link_cabb_tickets'
#             args['l_body_list'].append('cab_boss/cabb_user_payoperation.html')
#
#             args['main_tab'] = 'cabinet/cabinet.html'
#             return render(request, args['main_tab'], args)
#         else:
#             return redirect('/')


def cabb_ticketcheck(request):
    print("cabb_ticketcheck")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.POST:
            m_ticket_id = request.POST.get('ticket_id', '')
            m_type = request.POST.get('f_type', '01')
            print("m_type = ", m_type)
            args['item_ticket'] = Ticket_history.objects.get(id=m_ticket_id)
            if args['item_ticket'].game_type.t_type.verbal == 'old':
                m_ticket_type = args['item_ticket'].game_type.verbal
                print("m_ticket_type = ", m_ticket_type)
                args['template_result_name'] = check_template_exists(f"result_game/result_{m_ticket_type}.html")

                if m_type == "02":
                    template_name = check_template_exists("cab_boss/_templ_ticketcheck_02.html")
                else:
                    template_name = check_template_exists("cab_boss/_templ_ticketcheck.html")
            else:
                args['statuses'] = Type_game_status.objects.all()
                results = GameLottoResults.objects.filter(lottery_number=args['item_ticket'].answ_lottery_number)
                args['result'] = results[0] if len(results) > 0 else None
                args['m_current_site'] = f"{request.scheme}://{str(get_current_site(request))}"
                args['template_result_name'] = check_template_exists(
                    f"result_game/result_{args['item_ticket'].game_type.t_type.verbal}.html")
                template_name = check_template_exists("cab_boss/_templ_ticketcheck_lotto.html")
            m_template = get_template(template_name)
            print("OK")
            return HttpResponse(m_template.render(args))
        print("ERROR")
        return HttpResponse("ERROR")


def cabb_ticketcheck_conf(request):
    print("= cabb_ticketcheck_conf =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    # ToDo check ADMIN
    if not args['me'].profile.is_boss:
        return redirect('/')
    else:
        if True:
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                print("POST = ", request.POST)
                try:
                    m_user_id = args['me'].id
                    m_ticket_id = request.POST.get('f_id', "")
                    m_param = request.POST.get('f_param', "")
                    m_answ_nom = request.POST.get('f_answ_nom', "")
                    m_answ_win_sum = request.POST.get('f_answ_win_sum', "")

                    print("m_ticket_id = ", m_ticket_id)
                    print("m_param     = ", m_param)
                    if m_param == "01":
                        m_ticket_item = Ticket_history.objects.get(id=m_ticket_id)
                        m_ticket_item.t_check = True
                        m_ticket_item.t_check_user_id = m_user_id
                        m_ticket_item.t_check_dt = timezone.now()
                        m_ticket_item.save()

                    if m_param == "0101":
                        m_ticket_item = Ticket_history.objects.get(id=m_ticket_id)
                        if m_answ_nom != "" and m_answ_win_sum != "":
                            m_answ_nom_change = False
                            m_answ_win_sum_change = False
                            if m_ticket_item.answ_nom != m_answ_nom:
                                m_answ_nom_change = True
                                m_ticket_item.answ_nom = m_answ_nom
                            if m_ticket_item.answ_win_sum != m_answ_win_sum:
                                m_answ_win_sum_change = True
                                m_ticket_item.answ_win_sum = m_answ_win_sum
                                try:
                                    if int(m_ticket_item.answ_win_sum) > 0:
                                        m_ticket_item.answ_win = True
                                    else:
                                        m_ticket_item.answ_win = False
                                except:
                                    m_ticket_item.answ_win = False
                                    m_ticket_item.answ_win_sum = "0"
                            m_ticket_item.t_check = True
                            m_ticket_item.t_check_user_id = m_user_id
                            m_ticket_item.t_check_dt = timezone.now()
                            if m_ticket_item.status == "02" or m_ticket_item.status == "03":
                                m_ticket_item.status = "01"
                            m_ticket_item.save()

                            if m_answ_nom_change or m_answ_win_sum_change:
                                jellyfish_change_data(m_ticket_item.req_id, m_answ_nom, m_answ_win_sum)

                            if m_answ_win_sum_change:
                                balance_recalculate(m_ticket_item.games_id.user_id_id, m_ticket_item.id)

                            answer = {"AnswerCod": "01",
                                      "AnswerText": ""}
                        else:
                            answer = {"AnswerCod": "00",
                                      "AnswerText": gettext("Number and amount must not be empty")}
                    if m_param == "02":
                        m_balanceoperation_status_verbal = "02"
                        m_payadd_status = "02"
                    if m_param == "change_game_status":
                        print("change_game_status", request.POST)
                        m_status = request.POST.get('f_status', "")
                        m_ticket_item = Ticket_history.objects.get(id=m_ticket_id)
                        m_game = m_ticket_item.games_id
                        m_new_status = Type_game_status.objects.get(verbal=m_status)
                        m_game.t_status = m_new_status
                        m_game.save()
                        answer = {"AnswerCod": "01",
                                  "AnswerText": ""}
                    if m_param == "change_extra":
                        print("change extra", request.POST)
                        extra_list = []
                        for num in range(1, 7):
                            extra_num = request.POST.get(f'extra_{num}', '')
                            if extra_num == '' or not extra_num.isdigit():
                                return JsonResponse({"AnswerCod": "00",
                                                     "AnswerText": gettext("Extra must be numbers and filled in completely")})
                            elif int(extra_num) not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                                return JsonResponse({"AnswerCod": "00",
                                                     "AnswerText": gettext(
                                                         "Extra must be a number from 0 to 9")})
                            else:
                                extra_list.append(int(extra_num))
                        m_ticket_item = Ticket_history.objects.get(id=m_ticket_id)
                        m_ticket_item.answ_tabl['lotto_ticket_info']['extra_list'] = extra_list
                        m_ticket_item.save()
                        answer = {"AnswerCod": "01",
                                  "AnswerText": str(m_ticket_item.answ_tabl['lotto_ticket_info']['extra_list'])}
                        send_mail_user(user_id=m_ticket_item.games_id.user_id.id, type_mess='add_extra',
                                       l_ticket_id=m_ticket_item.id)
                    if m_param == "change_6th":
                        print("change_6th", request.POST)
                        sixth_num = request.POST.get('f_6th_number', '')
                        if sixth_num == '' or not sixth_num.isdigit():
                            return JsonResponse({"AnswerCod": "00",
                                                 "AnswerText": gettext("6Th must be numbers and filled in completely")})
                        elif int(sixth_num) > 37 or int(sixth_num) < 1:
                            return JsonResponse({"AnswerCod": "00", "AnswerText": gettext(
                                "Additional 6th number must be a number from 1 to 37")})

                        m_ticket_item = Ticket_history.objects.get(id=m_ticket_id)
                        m_ticket_item.answ_tabl['lotto_ticket_info']['6th_number'] = sixth_num
                        m_ticket_item.save()
                        answer = {"AnswerCod": "01",
                                  "AnswerText": sixth_num}
                    if m_param == "change_cabala_date":
                        print("change_cabala_date", request.POST)
                        m_date = request.POST.get('f_cabala_dt', "")
                        try:
                            m_new_datetime = datetime.datetime.strptime(m_date, '%d.%m.%Y %H:%M')
                        except Exception:
                            return JsonResponse({"AnswerCod": "00", "AnswerText": _("Not correct datetime")})
                        m_ticket_item = Ticket_history.objects.get(id=m_ticket_id)
                        m_ticket_item.t_cabala_dt = m_new_datetime
                        m_ticket_item.save()
                        answer = {"AnswerCod": "01",
                                  "AnswerText": f"&#9989; Succesfully change cabala date to {m_date}"}
                    elif m_param == 'change_cabala_photo':
                        if 'photo1' in request.FILES:
                            m_ticket_item = Ticket_history.objects.get(id=m_ticket_id)
                            str_now = datetime.datetime.strftime(timezone.now(), '%Y%m%d%H%M%S')
                            file_extension = request.FILES['photo1'].content_type.split('/')[1]
                            file_name = MEDIA_ROOT + f"/lotto_tickets/l_{m_ticket_item.id}_{str_now}.{file_extension}"
                            with open(file_name, 'wb+') as f:
                                f.write(request.FILES['photo1'].read())
                            m_ticket_item.img_06 = f"media/lotto_tickets/l_{m_ticket_item.id}_{str_now}.{file_extension}"
                            m_ticket_item.save()
                            answer = {"AnswerCod": "01",
                                      "AnswerText": m_ticket_item.img_06}
                        else:
                            return JsonResponse({"AnswerCod": "00", "AnswerText": _("Not correct file. Try to select another one")})
                except:
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cabb_cashadd_btn(request):
    print("= cabb_cashadd_btn =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    # ToDo check ADMIN
    if not args['me'].profile.is_boss:
        return redirect('/')
    else:
        if True:
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                print("POST = ", request.POST)
                try:
                    m_user_id = args['me'].id
                    m_cash_id = request.POST.get('f_cash_id', "")
                    m_cash_action = request.POST.get('f_cash_action', "")
                    print("m_cash_id     = ", m_cash_id)
                    print("m_cash_action = ", m_cash_action)

                    m_balanceoperation_status_verbal = "01"
                    m_payadd_status = "02"
                    if m_cash_action == "01":
                        m_balanceoperation_status_verbal = "04"
                        m_payadd_status = "01"
                    if m_cash_action == "02":
                        m_balanceoperation_status_verbal = "02"
                        m_payadd_status = "02"

                    t_cash = Cashadd.objects.get(id=m_cash_id)
                    t_cash.status = m_payadd_status
                    t_cash.t_check = True
                    t_cash.t_check_user_id = m_user_id
                    t_cash.t_check_dt = timezone.now()
                    t_cash.save()

                    m_type_balanceoperation_status_id = Type_balanceoperation_status.objects.get(
                        verbal=m_balanceoperation_status_verbal).id
                    pay_operation = BalanceOperation.objects.get(id=t_cash.bal_oper_id)
                    pay_operation.status_id = m_type_balanceoperation_status_id
                    pay_operation.save()

                    # ToDo  change balace

                    answer = {"AnswerCod": "01",
                              "AnswerText": ""}
                except:
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cabb_feedbackbtninfo(request):
    print("= cabb_feedbackbtninfo =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.POST:
            print("request.POST = ", request.POST)
            m_feedback_id = request.POST.get('f_feedback_id', '')
            args['item_feedback'] = Feedback.objects.get(id=m_feedback_id)
            template_name = check_template_exists("cab_boss/_templ_feedback_info.html")
            m_template = get_template(template_name)
            return HttpResponse(m_template.render(args))
        return HttpResponse("ERROR")


def cabb_feedbackbtnsave(request):
    print("= cabb_feedbackbtnsave =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    # ToDo check ADMIN
    if not args['me'].profile.is_boss:
        return redirect('/')
    else:
        if True:
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                print("POST = ", request.POST)
                m_user_id = args['me'].id
                m_feedback_id = request.POST.get('feedback_id', "")
                m_feedback_btn = request.POST.get('feedback_btn', "")
                m_feedback_text = request.POST.get('feedback_text', "")
                print("m_feedback_id   = ", m_feedback_id)
                print("m_feedback_btn  = ", m_feedback_btn)
                print("m_feedback_text = ", m_feedback_text)
                try:
                    m_feedback_item = Feedback.objects.get(id=m_feedback_id)
                    m_feedback_item.reply_text = m_feedback_text
                    m_feedback_item.reply_date = datetime.datetime.now()
                    print("m_feedback_btn = ", m_feedback_btn)
                    if m_feedback_btn == "01":
                        #
                        m_type_mess = "feedback_replay"
                        m_text = m_feedback_item.reply_text
                        if m_feedback_item.user_id_id is None:
                            m_user_id = None
                            m_email = m_feedback_item.u_email
                        else:
                            m_user_id = m_feedback_item.user_id_id
                            m_email = None
                        send_mail_user(request, user_id=m_user_id, type_mess=m_type_mess, l_email=m_email,
                                       l_text=m_text)
                        m_feedback_item.status = "01"
                    if m_feedback_btn == "02":
                        m_feedback_item.status = "02"
                    m_feedback_item.save()
                    answer = {"AnswerCod": "01",
                              "AnswerText": ""}
                except Exception as ex:
                    print("ex = ", ex)
                    m_feedback_item = Feedback.objects.get(id=m_feedback_id)
                    m_feedback_item.status = "00"
                    m_feedback_item.save()
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cabb_user_balance_oparation(request):
    print("= cabb_user_balance_oparation =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.POST:
            print("request.POST = ", request.POST)
            m_user_id = request.POST.get('f_user_id', "")
            args['m_user'] = Profile.objects.get(id=m_user_id)

            args['m_range_hours'] = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                                     '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                                     '20', '21', '22', '23'
                                     ]
            args['m_range_minut'] = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                                     '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                                     '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                                     '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
                                     '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
                                     '50', '51', '52', '53', '54', '55', '56', '57', '58', '59'
                                     ]
            args['m_date'] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
            args['m_hour'] = str(datetime.datetime.strftime(datetime.datetime.now(), "%H"))
            args['m_minut'] = str(datetime.datetime.strftime(datetime.datetime.now(), "%M"))

            template_name = check_template_exists("cab_boss/_templ_payoparation.html")
            m_template = get_template(template_name)
            return HttpResponse(m_template.render(args))
        return HttpResponse("ERROR")


def cabb_user_payoperation_save(request):
    print("= cabb_user_payoperation_save =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if True:
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                print("POST = ", request.POST)
                m_user_id = args['me'].id
                m_oper_user_id = request.POST.get('user_id', "")
                m_oper_amount = request.POST.get('t_amount', "")
                m_oper_typeoperation = request.POST.get('t_typeoperation', "")
                m_oper_data = request.POST.get('t_data', "")
                m_oper_hours = request.POST.get('t_hours', "")
                m_oper_minut = request.POST.get('t_minut', "")
                m_oper_description = request.POST.get('t_description', "")

                print("m_oper_user_id       = ", m_oper_user_id)
                print("m_oper_amount        = ", m_oper_amount)
                print("m_oper_typeoperation = ", m_oper_typeoperation)
                print("m_oper_data          = ", m_oper_data)
                print("m_oper_hours         = ", m_oper_hours)
                print("m_oper_minut         = ", m_oper_minut)
                print("m_oper_description   = ", m_oper_description)

                try:
                    m_oper_amount = decimal.Decimal(m_oper_amount)
                except:
                    m_oper_amount = 0

                try:
                    t_profile = Profile.objects.get(id=m_oper_user_id)

                    print("t_profile.user_id = ", t_profile.user_id)

                    m_pay_operation_id = make_pay_operation(l_user_id=t_profile.user_id,
                                                            l_sum=m_oper_amount,
                                                            # l_game_id=args['item_game_user'].id,
                                                            l_game_id=None,
                                                            l_status_verbal="04",
                                                            l_type_verbal=m_oper_typeoperation,
                                                            l_description=m_oper_description,
                                                            l_create_user=m_user_id
                                                            )

                    t_profile.balance += m_oper_amount
                    t_profile.save()

                    # m_feedback_item = Feedback.objects.get(id=m_feedback_id)
                    # m_feedback_item.reply_text = m_feedback_text
                    # m_feedback_item.reply_date = datetime.datetime.now()
                    # print ("m_feedback_btn = ", m_feedback_btn)
                    # if m_feedback_btn == "01":
                    #     #
                    #     m_type_mess = "feedback_replay"
                    #     m_text = m_feedback_item.reply_text
                    #     if m_feedback_item.user_id_id is None:
                    #         m_user_id = None
                    #         m_email = m_feedback_item.u_email
                    #     else:
                    #         m_user_id = m_feedback_item.user_id_id
                    #         m_email = None
                    #     send_mail_user(request, user_id=m_user_id, type_mess=m_type_mess, l_email=m_email,
                    #                    l_text=m_text)
                    #     m_feedback_item.status = "01"
                    # if m_feedback_btn == "02":
                    #     m_feedback_item.status = "02"
                    # m_feedback_item.save()
                    answer = {"AnswerCod": "01",
                              "AnswerText": ""}
                except Exception as ex:
                    print("ex = ", ex)
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cabb_user_block(request):
    print("= cabb_user_block =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if True:
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                user_id = request.POST.get('user_id', "")

                try:
                    t_profile = Profile.objects.get(id=user_id)
                    if t_profile.user.is_active:
                        t_profile.user.is_active = False
                    else:
                        t_profile.user.is_active = True
                    t_profile.user.save()
                    answer = {"AnswerCod": "01",
                              "AnswerText": ""}
                except Exception as ex:
                    print("ex = ", ex)
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cabb_user_sms(request):
    print("= cabb_user_sms =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if True:
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                user_id = request.POST.get('user_id', "")

                try:
                    t_profile = Profile.objects.get(id=user_id)
                    if t_profile.reklama:
                        t_profile.reklama = False
                    else:
                        t_profile.reklama = True
                    t_profile.save()
                    answer = {"AnswerCod": "01",
                              "AnswerText": ""}
                except Exception as ex:
                    print("ex = ", ex)
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cabb_user_limit(request):
    print("= cabb_user_limit =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if True:
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                user_id = request.POST.get('user_id', "")
                try:
                    t_profile = Profile.objects.get(id=user_id)
                    if t_profile.max_sum_m >= 0:
                        t_profile.max_sum_m = -1
                    else:
                        t_profile.max_sum_m = 0
                    t_profile.save()
                    answer = {"AnswerCod": "01",
                              "AnswerText": ""}
                except Exception as ex:
                    print("ex = ", ex)
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cabb_blocklist_enable(request):
    print("= cabb_blocklist_enable =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if True:
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                blist_id = request.POST.get('blist_id', "")
                try:
                    t_blacklist = Blacklist.objects.get(id=blist_id)
                    if t_blacklist.enabled:
                        t_blacklist.enabled = False
                    else:
                        t_blacklist.enabled = True
                    t_blacklist.save()
                    answer = {"AnswerCod": "01",
                              "AnswerText": ""}
                except Exception as ex:
                    print("ex = ", ex)
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cabb_blocklist_new(request):
    print("= cabb_blocklist_new =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.POST:
            print("request.POST = ", request.POST)
            # m_user_id = request.POST.get('f_user_id', "")
            # args['m_user'] = Profile.objects.get(id=m_user_id)

            args['m_range_hours'] = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                                     '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                                     '20', '21', '22', '23'
                                     ]
            args['m_range_minut'] = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                                     '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                                     '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                                     '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
                                     '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
                                     '50', '51', '52', '53', '54', '55', '56', '57', '58', '59'
                                     ]
            args['m_date'] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
            args['m_hour'] = str(datetime.datetime.strftime(datetime.datetime.now(), "%H"))
            args['m_minut'] = str(datetime.datetime.strftime(datetime.datetime.now(), "%M"))

            template_name = check_template_exists("cab_boss/_templ_blacklist_new.html")
            m_template = get_template(template_name)
            return HttpResponse(m_template.render(args))
        return HttpResponse("ERROR")


def cabb_blocklist_save(request):
    print("= cabb_blocklist_save =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if True:
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                print("POST = ", request.POST)
                m_user_id = args['me'].id

                m_type = request.POST.get('t_type', "")
                m_text = request.POST.get('t_text', "")
                m_description = request.POST.get('t_description', "")

                print("m_type        = ", m_type)
                print("m_text        = ", m_text)
                print("m_description = ", m_description)

                try:
                    m_type_id = Type_blacklist.objects.get(verbal=m_type).id
                    t_blacklist = Blacklist()
                    t_blacklist.created = timezone.now()
                    t_blacklist.create_user_id = m_user_id
                    t_blacklist.type_blacklist_id = m_type_id
                    t_blacklist.text = m_text
                    t_blacklist.enabled = True
                    t_blacklist.description = m_description
                    t_blacklist.save()
                    answer = {"AnswerCod": "01",
                              "AnswerText": ""}
                except Exception as ex:
                    print("ex = ", ex)
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("ERROR")}
        return JsonResponse(answer)


def cabb_ticketrestart(request):
    print("= cabb_ticketrefresh =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if True:
            answer = {"AnswerCod": "00",
                      "AnswerText": gettext("ERROR")}
            if request.POST:
                m_ticket_id = request.POST.get('ticket_id', "")
                try:
                    m_ticket_item = Ticket_history.objects.get(id=m_ticket_id)
                    '''
                    ('00', 'start'),
                    ('01', 'ready'),
                    ('02', 'wait confirm'),
                    ('03', 'error SOD'),
                    # ('04', 'step 4'),
                    # ('05', 'step 5'),
                    ('30', 'error'),
                    ('33', 'finish game'),
                    '''

                    if m_ticket_item.status == "00":
                        answer = cabb_jellyfish_game_restart(request, l_ticket=m_ticket_item, args=args)
                        #
                        # answer = {"AnswerCod": "01",
                        #           "AnswerText": gettext("Ticket successfully restarted")}
                    elif m_ticket_item.status == "01":
                        answer = {"AnswerCod": "01",
                                  "AnswerText": gettext("ready")}
                    elif m_ticket_item.status == "02":
                        answer = {"AnswerCod": "01",
                                  "AnswerText": gettext("wait confirm")}
                    elif m_ticket_item.status == "03":
                        answer = cabb_jellyfish_game_restart(request, l_ticket=m_ticket_item, args=args)
                    elif m_ticket_item.status == "30":
                        answer = {"AnswerCod": "01",
                                  "AnswerText": gettext("Ticket ERROR")}
                    elif m_ticket_item.status == "33":
                        answer = {"AnswerCod": "01",
                                  "AnswerText": gettext("The game is over")}
                    else:
                        answer = {"AnswerCod": "00",
                                  "AnswerText": gettext("Error ticket restarted. Please try again later.")}

                except Exception as ex:
                    print("ex = ", ex)
                    answer = {"AnswerCod": "00",
                              "AnswerText": gettext("Error ticket restarted. Please try again later.")}
        return JsonResponse(answer)


# в cabb_  такаяже функция запуска РЕСТАРТ БИЛЕТА jellyfish_game_restart
#   l_game_id    , l_tickets
def cabb_jellyfish_game_restart(request, l_ticket, args={}):
    m_dirlog_short = '../log/log_jellyfish_game_restart'
    if not os.path.exists(m_dirlog_short):
        os.makedirs(m_dirlog_short)
    m_log_file = os.path.join(m_dirlog_short, 'log_jellyfish_game_restart.log')
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
    logging.info('*********************************')
    logging.info('***** jellyfish_game_start ******')
    mr_code, mr_text = "00", "ERROR"
    try:
        # проверить доступна МЕДУЗА или нет
        t_jellyfish = List_jellyfish.objects.filter(enabled=True).order_by("order")
        logging.info(f" jellyfish count = {t_jellyfish.count()}")
        ##
        m_current_site_for_send = str(get_current_site(request))
        # logging.info(f" url for answer = {m_current_site_for_send}")
        m_scheme = request.scheme
        m_domain_name = get_current_site(request).name
        l_return_url = f"{m_scheme}://{m_domain_name}/jellyfish_rezult"

        if t_jellyfish.count() > 0:
            logging.info(f" check_jellyfish_game")
            # вічислить новый код
            if len(l_ticket.error_job) > 0:
                l_ticket.error_job += "\n"
            l_ticket.error_job += f"RESTART \n dt={l_ticket.req_dt} id={l_ticket.req_id} \n user={args['me'].id}"
            l_ticket.req_id += ".1"
            l_ticket.req_dt = timezone.now()
            l_ticket.save()

            jf_game_id = l_ticket.game_type.verbal_jellyfish
            jf_tickets = []
            jf_tickets.append({"ticket_id": l_ticket.req_id})
            # готовим данные для запроса
            item_jellyfish = t_jellyfish[0]
            # id enabled verbal caption order ipadres api_token
            m_url_1 = item_jellyfish.ipadres
            m_url_2 = "" if m_url_1.strip()[-1] == "/" else "/"
            m_url_3 = "api/v07/external/new_game"
            url = f"{m_url_1}{m_url_2}{m_url_3}"
            m_payload = {
                "game_id": jf_game_id,
                "tickets": jf_tickets,
                "return_url": l_return_url
            }
            payload = json.dumps(m_payload)
            headers = {
                'Token': item_jellyfish.api_token,
                'Content-Type': 'application/json'
            }
            # logging.info(f" game_id   = {jf_game_id}")
            # logging.info(f" l_tickets = {jf_tickets}")
            # logging.info(f" url       = {url}")
            logging.info(f" headers   = {headers}")
            logging.info(f" payload   = {payload}")
            m_CountRetry = 6
            for itemRequests in range(m_CountRetry):
                response = requests.request("POST", url, headers=headers, data=payload)
                logging.info(f" itemRequests = {itemRequests}, response.status_code = {response.status_code}")
                logging.info(f" itemRequests = {itemRequests}, response.text        = {response.text}")
                if response.status_code == 200:
                    try:
                        mj_response = json.loads(response.text)
                        if mj_response["success"] == True:
                            logging.info(f" check_jellyfish_game status start OK")
                            m_Text01 = gettext("We are preparing your game, the approximate waiting time is")
                            m_Text02 = mj_response.get("approximate_waiting_time_sec", "--")
                            m_Text03 = gettext("sec.")
                            m_ReturnText = f"{m_Text01} {m_Text02} {m_Text03}"
                            mr_code, mr_text = "01", m_ReturnText
                        else:
                            mr_code, mr_text = "00", f" jellyfish response error. {mj_response['error']}"
                    except Exception as ex:
                        mr_code, mr_text = "00", f" Error jellyfish_game status except. ex = {ex}"
                    break
                else:
                    mr_code, mr_text = "00", f" Unable to start the game. Try later. status={response.status_code}"
        else:
            mr_code, mr_text = "00", f" Error jellyfish not available. Try later."
    except Exception as ex:
        mr_code, mr_text = "00", gettext("Error to start the game. Try later.") + f"ex = {ex}"

    logging.info(mr_text)
    logging.info(f"--- FINISH ---")
    m_Return = {"AnswerCod": mr_code,
                "AnswerText": mr_text}
    return (m_Return)


def cabb_user_form(request):
    print("= cabb_user_form =")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        answer = {"AnswerCod": "00",
                  "AnswerText": gettext("ERROR")}
        if request.POST:
            print("request.POST = ", request.POST)
            m_user_id = request.POST.get('f_user_id', "")
            m_form_name = request.POST.get('f_form_name', "")
            m_form_type = request.POST.get('f_form_type', "show")
            if m_form_name == "user_edit":
                print("m_form_name == user_edit")
                args['t_user_profile'] = Profile.objects.get(id=m_user_id)
                print("user_profile = ", args['t_user_profile'].name)
                if m_form_type == "show":
                    print("m_form_name == show")
                    m_template_name = check_template_exists("cab_boss/_templ_useredit.html")
                    m_template = get_template(m_template_name)
                    gl_permissions = args.get("GL_Permission_list", "")
                    args['all_permissions'] = [perm.strip() for perm in gl_permissions.split(',')]
                    user_has_permissions = args['t_user_profile'].settings.get('permit_cabb')
                    if user_has_permissions:
                        args['user_permissions'] = [k for k, v in args['t_user_profile'].settings['permit_cabb'].items() if v is True]
                    m_html = m_template.render(args)
                    answer["AnswerCod"] = "01"
                    answer["AnswerText"] = "ok"
                    answer["html"] = m_html

                if m_form_type == "save":
                    list_errors = []
                    # tab limits
                    if args['me'].profile.settings['permit_cabb'].get('user_edit_limits'):
                        m_limits = {'max_ticket_d': request.POST.get('f_max_ticket_d'),
                                    'max_ticket_w': request.POST.get('f_max_ticket_w'),
                                    'max_ticket_m': request.POST.get('f_max_ticket_m'),
                                    'max_sum_d': request.POST.get('f_max_sum_d'),
                                    'max_sum_w': request.POST.get('f_max_sum_w'),
                                    'max_sum_m': request.POST.get('f_max_sum_m')}
                        if args['t_user_profile'].settings.get("limit") is None:
                            args['t_user_profile'].settings["limit"] = {}
                        for key, value in m_limits.items():
                            if args['t_user_profile'].settings["limit"].get(key):
                                args['t_user_profile'].settings["limit"][key] = value
                            elif not args['t_user_profile'].settings["limit"].get(key) and value != '':
                                args['t_user_profile'].settings["limit"][key] = value
                            else:
                                continue
                    # tab set blogger
                    if args['me'].profile.settings['permit_cabb'].get('user_edit_set_blogger'):
                        m_blogger_ref_hash = request.POST.get('f_user_blogger_ref', '')
                        if m_blogger_ref_hash.strip() != '':
                            if not Blogger.objects.filter(ref_hash=m_blogger_ref_hash).exists():
                                list_errors.append(f"Blogger with ref hash {m_blogger_ref_hash } does not exists")
                            else:
                                args['t_user_profile'].settings['i_am_blogger'] = m_blogger_ref_hash
                        else:
                            args['t_user_profile'].settings['i_am_blogger'] = ''
                    # tab profile
                    new_email = None
                    new_password = None
                    if args['me'].profile.settings['permit_cabb'].get('user_edit_profile'):
                        m_name = request.POST.get('f_user_name')
                        m_email = request.POST.get('f_user_email')
                        m_phone = request.POST.get('f_user_phone')
                        m_user_id_doc = request.POST.get('f_user_id_doc')
                        m_user_date_birthday = request.POST.get('f_user_date_birthday')
                        m_password = request.POST.get('f_user_password')

                        if m_user_id_doc:
                            if m_user_id_doc.strip() == '':
                                list_errors.append("ID document can't be empty!")
                            else:
                                args['t_user_profile'].i_doc = m_user_id_doc
                        if m_name:
                            if m_name.strip() == '':
                                list_errors.append("Name can't be empty!")
                            else:
                                args['t_user_profile'].name = m_name
                        if m_phone:
                            if m_phone == '':
                                list_errors.append("Phone can't be empty!")
                            else:
                                args['t_user_profile'].mobile = m_phone
                        if m_user_date_birthday:
                            try:
                                m_date_birthday_convert = datetime.datetime.strptime(m_user_date_birthday, '%d.%m.%Y')
                                m_temp_18year = datetime.datetime.today() - relativedelta(years=18, hour=0, minute=0,
                                                                                          second=0, microsecond=0)
                                if m_date_birthday_convert > m_temp_18year:
                                    list_errors.append("Not correct date of birth. User must be over 18 years old.")
                                else:
                                    args['t_user_profile'].date_birthday = m_date_birthday_convert
                            except Exception:
                                list_errors.append("Not correct date of birth")
                        else:
                            list_errors.append("Date of birth can't be empty!")
                        if m_email:
                            new_email = m_email.strip()
                            if new_email == '' or '@' not in new_email:
                                list_errors.append("Email can't be empty and must include '@'")
                        if m_password:
                            new_password = m_password.strip()
                            if new_password == '' or len(new_password) < 8:
                                list_errors.append("Password can't be empty and must be at least 8 characters!")
                    if len(list_errors) > 0:
                        return JsonResponse({"AnswerCod": "00", "AnswerText": list_errors[0]})

                    if new_email and args['t_user_profile'].user.email != new_email:
                        user = args['t_user_profile'].user
                        user.email = new_email
                        user.username = new_email
                        user.save()
                    if new_password:
                        user = args['t_user_profile'].user
                        user.set_password(new_password)
                        user.save()
                    # Tab ID photo
                    if args['me'].profile.settings['permit_cabb'].get('user_edit_photo'):
                        if 'photo1' in request.FILES:
                            args['t_user_profile'].i_foto = request.FILES['photo1']
                        if 'photo2' in request.FILES:
                            args['t_user_profile'].i_photo_face = request.FILES['photo2']
                    # Tab permissions
                    if args['me'].profile.settings['permit_cabb'].get('user_add_permissions'):
                        m_perms = request.POST.get('f_perms')
                        if m_perms:
                            if m_perms == 'del_all':
                                if args['t_user_profile'].settings.get('permit_cabb'):
                                    args['t_user_profile'].settings['permit_cabb'] = {}
                            else:
                                args['t_user_profile'].settings['permit_cabb'] = {perm: True for perm in m_perms.split(',')}

                    args['t_user_profile'].save()

                    answer["AnswerCod"] = "01"
                    answer["AnswerText"] = "ok"

        return JsonResponse(answer)


def save_comment_callcenter(request):
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        if request.POST:
            print(request.POST)
            m_id = request.POST.get('f_id')
            m_text = request.POST.get('f_text')
            m_date_return = request.POST.get('f_date_return')
            if not m_id:
                return JsonResponse({"AnswerCod": "00", "AnswerText": gettext("User is undefined")})
            if not m_text or m_text.strip() == '':
                return JsonResponse({"AnswerCod": "00", "AnswerText": gettext("Please enter a text")})
            if m_date_return and m_date_return != '':
                try:
                    m_date_return_convert = datetime.datetime.strptime(m_date_return, '%d.%m.%Y')
                except Exception:
                    return JsonResponse({"AnswerCod": "00", "AnswerText": gettext("Not correct return date")})
            try:
                new_comment = CommentCallcenter()
                new_comment.text = m_text
                if m_date_return:
                    new_comment.date_return = m_date_return_convert
                new_comment.user_profile = Profile.objects.get(id=m_id)
                new_comment.creator = args['me'].profile
                new_comment.date_created = datetime.datetime.now()
                new_comment.save()
                answer_text = f'Last Comment: {new_comment.text} '
                date_return = datetime.datetime.strftime(new_comment.date_return,
                                                         "%d.%m.%Y") if new_comment.date_return else None
                answer_text += f'Date: {date_return}' if date_return else ''
                return JsonResponse({"AnswerCod": "01", "AnswerText": answer_text})
            except Exception:
                return JsonResponse({"AnswerCod": "00", "AnswerText": gettext("An error occured. Please try again later")})
