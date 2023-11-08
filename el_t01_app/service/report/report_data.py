# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import decimal
import json
from dateutil import tz
from dateutil.rrule import rrule, MONTHLY
from dateutil.relativedelta import relativedelta
from datetime import timedelta, time
from django.contrib.auth.models import User
from django.utils.translation import gettext
from django.utils import translation, timezone
from django.db.models import Q, Count, Sum, F, IntegerField, FloatField, Case, When, DecimalField, \
    Value, CharField, DateTimeField, BigIntegerField, Min, ExpressionWrapper, DurationField, Func
from django.db.models.functions import Coalesce, Cast, ExtractMonth
from el_t01_app.models import (Profile, Report_list, BalanceOperation, Ticket_history,
                              Payout, Game_history, Ticket_type, SubsSmsToSend, Subscription,
                              PaymentAnswer, Type_balanceoperation, Blogger, BloggerType,
                              IdConfirmation,
                              Task_history, SmsToSend,
                              SubsManager, SubsAutoPay,
                              TypeTicketType, GameLottoResults
                              )
from el_t01_app.service.dft import get_report_list, get_game_verbal_list, get_GlobalSettings


def prep_date_iner(request):
    # 05/02/2021 12:00 AM - 05/22/2021 11:00 PM
    m_find_date = request.GET.get('date', '')
    m_zvit_date_txt = m_find_date
    m_find_daterange_1 = request.GET.get('daterange', '').split("-")
    # print("m_find_daterange_1 = ", m_find_daterange_1)
    m_find_daterange_2 = request.GET.get('daterange_2', '').split("-")
    # print("m_find_daterange_2 = ", m_find_daterange_2)
    # m_report_lang = "he"
    # FOR TESTS
    m_report_lang = "en"
    try:
        m_zvit_date_1_start_txt = m_find_daterange_1[0].strip()[:10]
        m_zvit_date_1_finish_txt = m_find_daterange_1[1].strip()[:10]
        m_zvit_date_1_start_txt = datetime.datetime.strptime(m_zvit_date_1_start_txt, "%d.%m.%Y")
        m_zvit_date_1_finish_txt = datetime.datetime.strptime(m_zvit_date_1_finish_txt, "%d.%m.%Y")
    except:
        m_zvit_date_1_start_txt = datetime.datetime.now()
        m_zvit_date_1_finish_txt = datetime.datetime.now()

    try:
        m_zvit_date_2_start_txt = m_find_daterange_2[0].strip()[:10]
        m_zvit_date_2_finish_txt = m_find_daterange_2[1].strip()[:10]
        m_zvit_date_2_start_txt = datetime.datetime.strptime(m_zvit_date_2_start_txt, "%d.%m.%Y")
        m_zvit_date_2_finish_txt = datetime.datetime.strptime(m_zvit_date_2_finish_txt, "%d.%m.%Y")
    except:
        m_zvit_date_2_start_txt = datetime.datetime.now()
        m_zvit_date_2_finish_txt = datetime.datetime.now()
    try:
        m_zvit_date = datetime.datetime.strptime(m_find_date, "%d.%m.%Y")
    except:
        m_zvit_date = datetime.datetime.now().date()
    return (
        m_zvit_date_1_start_txt, m_zvit_date_1_finish_txt, m_zvit_date_2_start_txt, m_zvit_date_2_finish_txt,
        m_report_lang, m_zvit_date, m_zvit_date_txt)


def prep_date_api(l_add_api={}):
    m_find_date = l_add_api.get('date', '')
    m_zvit_date_txt = m_find_date
    m_find_daterange_1 = l_add_api.get('daterange_1', '').split("-")
    # print("m_find_daterange_1 = ", m_find_daterange_1)
    m_find_daterange_2 = l_add_api.get('daterange_2', '').split("-")
    # print("m_find_daterange_2 = ", m_find_daterange_2)
    m_report_lang = l_add_api.get('lang', 'he')
    try:
        m_zvit_date_1_start_txt = m_find_daterange_1[0].strip()[:10]
        m_zvit_date_1_finish_txt = m_find_daterange_1[1].strip()[:10]
        m_zvit_date_1_start_txt = datetime.datetime.strptime(m_zvit_date_1_start_txt, "%d.%m.%Y")
        m_zvit_date_1_finish_txt = datetime.datetime.strptime(m_zvit_date_1_finish_txt, "%d.%m.%Y")
    except:
        m_zvit_date_1_start_txt = datetime.datetime.now()
        m_zvit_date_1_finish_txt = datetime.datetime.now()
    try:
        m_zvit_date_2_start_txt = m_find_daterange_2[0].strip()[:10]
        m_zvit_date_2_finish_txt = m_find_daterange_2[1].strip()[:10]

        m_zvit_date_2_start_txt = datetime.datetime.strptime(m_zvit_date_2_start_txt, "%d.%m.%Y")
        m_zvit_date_2_finish_txt = datetime.datetime.strptime(m_zvit_date_2_finish_txt, "%d.%m.%Y")
    except:
        m_zvit_date_2_start_txt = datetime.datetime.now()
        m_zvit_date_2_finish_txt = datetime.datetime.now()
    try:
        m_zvit_date = datetime.datetime.strptime(m_find_date, "%d.%m.%Y")
    except:
        m_zvit_date = datetime.datetime.now().date()
    return (
        m_zvit_date_1_start_txt, m_zvit_date_1_finish_txt, m_zvit_date_2_start_txt, m_zvit_date_2_finish_txt,
        m_report_lang, m_zvit_date, m_zvit_date_txt)


def report_data(request, verbal=None, add_api=None):
    # print ("cab_report_data")
    # verbal - code report
    # RETURN = (return_list, return_args)
    # print ("verbal         = ", verbal)
    return_args = {}
    m_report_lang = translation.get_language()

    m_globalset = get_GlobalSettings()
    return_args.update(m_globalset)
    return_list = None
    m_zvit_date_start_txt = datetime.datetime.now()
    m_zvit_date_finish_txt = datetime.datetime.now()
    # m_find_type_game_list = get_game_verbal_list()

    m_zvit_date_2_start_txt = datetime.datetime.now()
    m_zvit_date_2_finish_txt = datetime.datetime.now()
    m_zvit_date = datetime.datetime.now().date()
    m_zvit_date_txt = m_zvit_date

    if add_api == None:
        if request.GET:
            m_zvit_date_start_txt, \
            m_zvit_date_finish_txt, \
            m_zvit_date_2_start_txt, \
            m_zvit_date_2_finish_txt, \
            m_report_lang, \
            m_zvit_date, \
            m_zvit_date_txt \
                = prep_date_iner(request)
    else:
        m_zvit_date_start_txt, \
        m_zvit_date_finish_txt, \
        m_zvit_date_2_start_txt, \
        m_zvit_date_2_finish_txt, \
        m_report_lang, \
        m_zvit_date, \
        m_zvit_date_txt \
            = prep_date_api(add_api)
    # сменить язык
    m_report_lang_old = translation.get_language()
    translation.activate(m_report_lang)

    # print("m_zvit_date_start_txt = ", m_zvit_date_start_txt)
    # print("m_zvit_date_finish_txt = ", m_zvit_date_finish_txt)
    # print("m_zvit_date_start_txt = ", m_zvit_date_2_start_txt)
    # print("m_zvit_date_start_txt = ", m_zvit_date_2_finish_txt)

    # print("m_find_type_game_list = ", m_find_type_game_list)
    m_zvit_date_start_db = m_zvit_date_start_txt + relativedelta(hour=0, minute=0, second=0, microsecond=0)
    m_zvit_date_finish_db = m_zvit_date_finish_txt + relativedelta(days=+1, hour=0, minute=0, second=0, microsecond=0)
    m_zvit_date_2_start_db = m_zvit_date_2_start_txt + relativedelta(hour=0, minute=0, second=0, microsecond=0)
    m_zvit_date_2_finish_db = m_zvit_date_2_finish_txt + relativedelta(days=+1, hour=0, minute=0, second=0,
                                                                       microsecond=0)
    m_zvit_date_start_txt = datetime.datetime.strftime(m_zvit_date_start_txt, "%d.%m.%Y")
    m_zvit_date_finish_txt = datetime.datetime.strftime(m_zvit_date_finish_txt, "%d.%m.%Y")
    return_args['date_start_txt'] = m_zvit_date_start_txt
    return_args['date_finish_txt'] = m_zvit_date_finish_txt
    return_args['date_range'] = '{} - {}'.format(m_zvit_date_start_txt, m_zvit_date_finish_txt)
    m_zvit_date_2_start_txt = datetime.datetime.strftime(m_zvit_date_2_start_txt, "%d.%m.%Y")
    m_zvit_date_2_finish_txt = datetime.datetime.strftime(m_zvit_date_2_finish_txt, "%d.%m.%Y")
    return_args['date_start_2_txt'] = m_zvit_date_2_start_txt
    return_args['date_finish_2_txt'] = m_zvit_date_2_finish_txt
    return_args['date_range_2'] = '{} - {}'.format(m_zvit_date_2_start_txt, m_zvit_date_2_finish_txt)
    return_args['date'] = m_zvit_date_txt
    if verbal == "Rep_01":
        m_zvit_date_finish_db = m_zvit_date_finish_db + relativedelta(days=-1, hour=0, minute=0, second=0,
                                                                      microsecond=0)
        tickets = Ticket_history.objects.filter(
            req_dt__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()])
        by_ptype_gtype = tickets.values('games_id__t_payment__verbal', 'game_type__caption').distinct().annotate(
            games_count=Count('games_id', distinct=True),
            tickets_count=Count('id'),
            amount_count=Sum('cost_2')
        )
        by_ptype = tickets.values('games_id__t_payment__verbal').distinct().annotate(
            game_type__caption=Value('Total', output_field=CharField()),
            games_count=Count('games_id', distinct=True),
            tickets_count=Count('id'),
            amount_count=Sum('cost_2')
        )
        total = by_ptype.aggregate(Sum('games_count'), Sum('tickets_count'),
                                   Sum('amount_count'))
        return_list = list(by_ptype_gtype.union(by_ptype).order_by('games_id__t_payment__verbal', 'game_type__caption'))
        return_list.append({'games_id__t_payment__verbal': 'Total', 'game_type__caption': 'Total',
                            'games_count': total['games_count__sum'],
                            'tickets_count': total['tickets_count__sum'],
                            'amount_count': total['amount_count__sum']})

    elif verbal == "Rep_02":
        bal_operations_list = BalanceOperation.objects.filter(
            created__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()])
        if "uPhone" in dict(request.GET).keys():
            phone = request.GET.get('uPhone')
            bal_operations_list = bal_operations_list.filter(user_id__profile__mobile__icontains=phone)
            return_args['m_uPhone'] = phone
        if "uEmail" in dict(request.GET).keys():
            email = request.GET.get('uEmail')
            bal_operations_list = bal_operations_list.filter(user_id__email__icontains=email)
            return_args['m_uEmail'] = email
        return_list = list(bal_operations_list.values(
            'created', 'user_id__email', 'user_id__profile__name', 'user_id__profile__mobile',
            'type_balanceoperation__caption', 'amount', 'status__caption', 'pay_response'
        ).order_by('-created'))

        # m_local_tz = 'Israel'
        # return_list = []
        # _return_list = BalanceOperation.objects.filter(
        #     created__range=[m_zvit_date_start_db, m_zvit_date_finish_db], ).order_by("-created")
        # rep_total = {}
        # rep_total["type_line"] = "total_report"
        # rep_total["type_group"] = gettext("TOTAL")
        # rep_total["g_c"] = 0
        # rep_total["w_c"] = 0
        # rep_total["w_a"] = 0
        # rep_total["b_c"] = 0
        # rep_total["b_a"] = 0
        # rep_total["r_c"] = 0
        # rep_total["r_a"] = 0
        # rep_total["s_c"] = 0
        # rep_total["s_a"] = 0
        #
        # for ItemStr in _return_list:
        #     rep_item = {}
        #     rep_item["type_line"] = "item_str"
        #     rep_item["date"] = datetime.datetime.strftime(ItemStr.created.astimezone(tz.gettz(m_local_tz)),
        #                                                   "%d.%m.%Y %H:%M:%S")
        #     rep_item["user_name"] = ItemStr.user_id.profile.name
        #     rep_item["user_phone"] = ItemStr.user_id.profile.mobile
        #     rep_item["user_email"] = ItemStr.user_id.email
        #     rep_item["type_operation"] = ItemStr.type_balanceoperation.caption
        #     rep_item["status"] = ItemStr.status.caption
        #     rep_item["amount"] = ItemStr.amount
        #     rep_item["pay_response"] = ItemStr.pay_response
        #     rep_item["tranzila_payment_method"] = ""
        #     rep_item["tranzila_response"] = ""
        #     rep_item["tranzila_index"] = ""
        #     if ItemStr.pay_response:
        #         try:
        #             m_response = f"{ItemStr.pay_response[12:-1]}"
        #             m_response = m_response.replace("\'", "\"")
        #             m_response = json.loads(m_response)
        #
        #             rep_item["tranzila_payment_method"] = m_response.get("payment_method",
        #                                                                  "")  # .replace("[", "").replace("]", "").replace("'", "")
        #             if len(rep_item["tranzila_payment_method"]) > 0:
        #                 rep_item["tranzila_payment_method"] = rep_item["tranzila_payment_method"][0]
        #
        #             rep_item["tranzila_response"] = m_response.get("Response",
        #                                                            "")  # .replace("[", "").replace("]", "").replace("'", "")
        #             if len(rep_item["tranzila_response"]) > 0:
        #                 rep_item["tranzila_response"] = rep_item["tranzila_response"][0]
        #
        #             rep_item["tranzila_index"] = m_response.get("index",
        #                                                         "")  # .replace("[", "").replace("]", "").replace("'", "")
        #             if len(rep_item["tranzila_index"]) > 0:
        #                 rep_item["tranzila_index"] = rep_item["tranzila_index"][0]
        #         except Exception as ex:
        #             # print("ex = ", ex)
        #             pass
        #     else:
        #         pass
        #     # print("10")
        #     # rep_item["tranzila_payment_method"] = ItemStr.
        #     # rep_item["tranzila_response"] = ItemStr.
        #     # rep_item["tranzila_index"] = ItemStr.
        #
        #     return_list.append(rep_item)
        # return_list.append(rep_total)

    elif verbal == "Rep_03":
        return_list = []
        _return_list = Profile.objects.all().exclude(balance=0).order_by("-balance")
        rep_total = {}
        rep_total["type_line"] = "total_report"
        rep_total["type_group"] = gettext("TOTAL")
        rep_total["id"] = gettext("TOTAL")
        rep_total["name"] = ""
        rep_total["mobile"] = ""
        rep_total["email"] = ""
        rep_total["date_joined"] = ""
        rep_total["i_doc"] = ""
        rep_total["balance"] = 0

        for ItemStr in _return_list:
            rep_item = {}
            rep_item["type_line"] = ""
            rep_item["type_group"] = ""
            rep_item["id"] = ItemStr.id
            rep_item["name"] = ItemStr.name
            rep_item["mobile"] = ItemStr.mobile
            rep_item["email"] = ItemStr.user.email
            rep_item["date_joined"] = datetime.datetime.strftime(ItemStr.date_joined, "%d.%m.%Y %H:%M:%S")
            rep_item["i_doc"] = ItemStr.i_doc
            rep_item["balance"] = ItemStr.balance
            return_list.append(rep_item)

            rep_total["balance"] += ItemStr.balance

        return_list.append(rep_total)

    elif verbal == "Rep_04":
        m_statuses = request.GET.get('status')
        return_queryset = Payout.objects.filter(created__range=[m_zvit_date_start_db, m_zvit_date_finish_db]
                                            ).order_by('-created')
        if m_statuses:
            m_statuses_list = [i for i in m_statuses.split('-') if i != '']
            return_args['payout_statuses'] = m_statuses_list
            return_queryset = return_queryset.filter(status__in=m_statuses_list)
        return_args['total_amount'] = 0
        return_args['total_amount_minus_percent'] = 0
        return_args['total_percent'] = 0
        if len(return_queryset) > 0:
            for item in return_queryset:
                return_args['total_amount'] += item.amount
                return_args['total_amount_minus_percent'] += item.amount_minus_percent
                return_args['total_percent'] += item.percent
        return_list = []
        for item in return_queryset:
            status = 'NEW'
            if item.status == '01':
                status = 'OK'
            elif item.status == '02':
                status = 'REJECT'
            return_list.append({
                'created': datetime.datetime.strftime(item.created, "%d.%m.%Y %H:%M:%S"),
                'user_name': item.user_id.profile.name, 'user_mobile': item.user_id.profile.mobile,
                'user_email': item.user_id.email, 'status': status, 'acc_name': item.acc_name,
                'name_bank': item.name_bank, 'acc_num': item.acc_num, 'id': item.id,
                'amount': float(item.amount), 'percent': float(item.percent), 'branch': item.branch,
                'amount_minus_percent': float(item.amount_minus_percent),
            })

    elif verbal in ["Rep_05", "Rep_50", "Rep_52"]:
        tickets = Ticket_history.objects.filter(req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db])
        if verbal == "Rep_52":
            tickets = Ticket_history.objects.filter(t_cabala_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db])
        if verbal in ["Rep_50", "Rep_52"]:
            tickets = tickets.filter(~Q(game_type__t_type__verbal='old'))
            return_args['rep_lotto'] = True
            return_args['rep_lotto_cabala'] = True
        all_tickets = tickets.values('game_type__caption', 'req_id', 'req_dt', 'answ_dt', 'answ_nom', 'status', 'img_06',
                                     'cost_1', 'cost_2', 'games_id__user_id__profile__name', 't_cabala_dt',
                                     'games_id__user_id__profile__mobile', 'games_id__user_id__email',
                                     'games_id__user_id__id', 'games_id__t_status__caption'
                                     ).annotate(profit=F('cost_2') - F('cost_1'),
                                                type=Value('simple', output_field=CharField()),
                                                win_as_int=Case(
                                                    When(answ_win_sum='', then=Value(0)),
                                                    When(answ_win_sum=None, then=Value(0)),
                                                    default=Cast('answ_win_sum', DecimalField(max_digits=15, decimal_places=2)),
                                                    output_field=DecimalField(max_digits=15, decimal_places=2))
                                                )
        by_gtype = tickets.values('game_type__caption').distinct().annotate(
            req_id=Cast(Count('req_id'), CharField()),
            req_dt=Value('2000-01-01', output_field=DateTimeField()),
            answ_dt=Value('2000-01-01', output_field=DateTimeField()),
            answ_nom=Value('', output_field=CharField()),
            status=Value('', output_field=CharField()),
            img_06=Value('', output_field=CharField()),
            cost_1=Sum('cost_1'), cost_2=Sum('cost_2'),
            games_id__user_id__profile__name=Value('', output_field=CharField()),
            t_cabala_dt=Value('2000-01-01', output_field=DateTimeField()),
            games_id__user_id__profile__mobile=Value('', output_field=CharField()),
            games_id__user_id__email=Value('', output_field=CharField()),
            games_id__user_id__id=Value(-1, output_field=BigIntegerField()),
            games_id__t_status__caption=Value('', output_field=CharField()),
            profit=F('cost_2') - F('cost_1'),
            type=Value('total', output_field=CharField()),
            win_as_int=Sum(Case(
                When(answ_win_sum='', then=Value(0)),
                When(answ_win_sum=None, then=Value(0)),
                default=Cast('answ_win_sum', DecimalField(max_digits=15, decimal_places=2)),
                output_field=DecimalField(max_digits=15, decimal_places=2)))
        )
        return_list = list(by_gtype.union(all_tickets, all=True).order_by('game_type__caption', '-req_dt'))
        total_values = by_gtype.aggregate(Sum('cost_1'), Sum('cost_2'), Sum('win_as_int'),
                                          Sum('profit'), req_id__sum=Sum(Cast('req_id', IntegerField())))
        return_list.append({
            'game_type__caption': 'Total', 'profit': total_values['profit__sum'],
            'cost_1': total_values['cost_1__sum'], 'cost_2': total_values['cost_2__sum'],
            'win_as_int': total_values['win_as_int__sum'], 'req_id': total_values['req_id__sum'],
            'type': 'general'
        })

    elif verbal == "Rep_06":
        print("Rep_06")
        print(request.POST)
        m_local_tz = 'Israel'
        ## полный период - текущий месяц
        return_list = []

        m_date_check = datetime.datetime.now()
        m_date_check = m_date_check + relativedelta(days=+1, hour=0, minute=0, second=0, microsecond=0)

        if m_zvit_date_finish_db > m_date_check:
            m_zvit_date_finish_db = m_date_check

        print("m_zvit_date_start_db 2 = ", m_zvit_date_start_db)
        print("m_zvit_date_finish_db 2= ", m_zvit_date_finish_db)

        m_zvit_date_start_txt = m_zvit_date_start_db
        m_zvit_date_finish_txt = m_zvit_date_finish_db + relativedelta(days=-1, hour=0, minute=0, second=0,
                                                                       microsecond=0)

        return_args['date_rep_start_txt'] = datetime.datetime.strftime(m_zvit_date_start_txt, "%d.%m.%Y")
        return_args['date_rep_finish_txt'] = datetime.datetime.strftime(m_zvit_date_finish_txt, "%d.%m.%Y")
        return_args['date_rep_range'] = '{} - {}'.format(return_args['date_rep_start_txt'],
                                                         return_args['date_rep_finish_txt'])

        print("dates in request = ", m_zvit_date_start_db, m_zvit_date_finish_db)
        _return_list = Ticket_history.objects.filter(
            req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db],
            # games_id__verbal__in=m_find_type_game_list
        ).order_by("game_type", "-req_dt")

        try:
            m_procent_udachi = return_args.get("GL_Udachi_Profit", 0)
            m_procent_udachi = int(m_procent_udachi)
        except:
            m_procent_udachi = 100

        print("len(_return_list) = ", len(_return_list))

        if len(_return_list) > 0:
            rep_total = {}
            rep_total["type_line"] = "total_report"
            rep_total["type_group"] = gettext("TOTAL")
            rep_total["type_group_code"] = ""
            rep_total["count_ticket"] = 0
            rep_total["cost_1"] = ""
            rep_total["cost_2"] = ""
            rep_total["sum_cost_1"] = 0
            rep_total["sum_cost_2"] = 0
            rep_total["profit_ticket"] = 0
            rep_total["profit_all"] = 0
            rep_total["profit_udachi"] = 0
            rep_total["profit_extcomp"] = 0
            rep_total["profit_average"] = 0
            rep_total["win_count"] = 0
            rep_total["win_sum"] = 0

            rep_group = {}
            rep_group["type_line"] = "total_group"
            rep_group["type_group"] = gettext(_return_list[0].game_type.caption)
            rep_group["type_group_code"] = _return_list[0].game_type.verbal
            rep_group["count_ticket"] = 0
            rep_group["cost_1"] = _return_list[0].cost_1
            rep_group["cost_2"] = _return_list[0].cost_2
            rep_group["sum_cost_1"] = 0
            rep_group["sum_cost_2"] = 0
            rep_group["profit_ticket"] = rep_group["cost_2"] - rep_group["cost_1"]
            rep_group["profit_all"] = 0
            rep_group["profit_udachi"] = 0
            rep_group["profit_extcomp"] = 0
            rep_group["profit_average"] = 0
            rep_group["win_count"] = 0
            rep_group["win_sum"] = 0

            for ItemStr in _return_list:
                if rep_group["type_group_code"] != ItemStr.game_type.verbal:
                    return_list.append(rep_group)
                    rep_group = {}
                    rep_group["type_line"] = "total_group"
                    rep_group["type_group"] = gettext(ItemStr.game_type.caption)
                    rep_group["type_group_code"] = gettext(ItemStr.game_type.verbal)
                    rep_group["count_ticket"] = 0
                    rep_group["cost_1"] = ItemStr.cost_1
                    rep_group["cost_2"] = ItemStr.cost_2
                    rep_group["sum_cost_1"] = 0
                    rep_group["sum_cost_2"] = 0
                    rep_group["profit_ticket"] = rep_group["cost_2"] - rep_group["cost_1"]
                    rep_group["profit_all"] = 0
                    rep_group["profit_udachi"] = 0
                    rep_group["profit_extcomp"] = 0
                    rep_group["profit_average"] = 0
                    rep_group["win_count"] = 0
                    rep_group["win_sum"] = 0

                rep_item = {}
                rep_item["type_line"] = "item_str"
                rep_item["type_group"] = gettext(ItemStr.game_type.caption)
                rep_item["type_group_code"] = ItemStr.game_type.verbal
                rep_item["n_req"] = ItemStr.req_id
                try:
                    rep_item["d_req"] = datetime.datetime.strftime(ItemStr.req_dt.astimezone(tz.gettz(m_local_tz)),
                                                                   "%d.%m.%Y %H:%M:%S")
                except:
                    rep_item["d_req"] = ""
                try:
                    rep_item["d_answ"] = datetime.datetime.strftime(ItemStr.answ_dt.astimezone(tz.gettz(m_local_tz)),
                                                                    "%d.%m.%Y %H:%M:%S")
                except:
                    rep_item["d_answ"] = ""

                rep_item["number"] = ItemStr.answ_nom
                rep_item["win"] = ItemStr.answ_win
                try:
                    rep_item["win_sum"] = decimal.Decimal(ItemStr.answ_win_sum)
                except:
                    rep_item["win_sum"] = 0

                rep_item["game_last"] = -1
                #
                rep_item["cost_1"] = ItemStr.cost_1
                rep_item["cost_2"] = ItemStr.cost_2
                rep_item["sum_cost_1"] = ItemStr.cost_1
                rep_item["sum_cost_2"] = ItemStr.cost_2
                rep_item["profit_ticket"] = ItemStr.cost_2 - ItemStr.cost_1
                rep_item["profit_all"] = ItemStr.cost_2 - ItemStr.cost_1
                rep_item["profit_udachi"] = round(rep_item["profit_all"] * m_procent_udachi / 100, 2)
                rep_item["profit_extcomp"] = round(rep_item["profit_all"] - rep_item["profit_udachi"], 2)
                rep_item["profit_average"] = m_procent_udachi
                rep_item["win_count"] = 1 if ItemStr.answ_win else 0
                try:
                    rep_item["win_sum"] = decimal.Decimal(ItemStr.answ_win_sum)
                except:
                    rep_item["win_sum"] = 0
                #

                rep_group["count_ticket"] += 1
                rep_group["sum_cost_1"] += rep_item["sum_cost_1"]
                rep_group["sum_cost_2"] += rep_item["sum_cost_2"]
                # rep_group["profit_ticket"] = 0
                rep_group["profit_all"] += rep_item["profit_all"]
                rep_group["profit_udachi"] += rep_item["profit_udachi"]
                rep_group["profit_extcomp"] += rep_item["profit_extcomp"]
                rep_group["profit_average"] = 0
                rep_group["win_count"] += rep_item["win_count"]
                rep_group["win_sum"] += rep_item["win_sum"]

                rep_total["count_ticket"] += 1
                rep_total["sum_cost_1"] += rep_item["sum_cost_1"]
                rep_total["sum_cost_2"] += rep_item["sum_cost_2"]
                # rep_total["profit_ticket"] = 0
                rep_total["profit_all"] += rep_item["profit_all"]
                rep_total["profit_udachi"] += rep_item["profit_udachi"]
                rep_total["profit_extcomp"] += rep_item["profit_extcomp"]
                rep_total["profit_average"] = 0
                rep_total["win_count"] += rep_item["win_count"]
                rep_total["win_sum"] += rep_item["win_sum"]

                # return_list.append(rep_item)

            return_list.append(rep_group)
            return_list.append(rep_total)

        return_args['total_client_sum1'] = -rep_total["sum_cost_1"]
        return_args['total_client_sum2'] = -rep_total["sum_cost_2"]
        return_args['total_win_sum'] = rep_total["win_sum"]
        return_args['total_profit'] = rep_total["profit_all"]
        return_args['total_deposit'] = return_args.get("GL_Udachi_Deposit", 0)
        return_args['total_creditcard'] = return_args.get("GL_Udachi_CreditCard", 0)
        return_args['total_invoce'] = return_args['total_client_sum1'] \
                                      + return_args['total_win_sum'] \
                                      + int(return_args['total_deposit']) \
                                      + int(return_args['total_creditcard'])

        print("len(return_list) = ", len(return_list))

        return_args['return_list_month'] = return_list
        ## последний день
        print("last day")
        return_list = []
        m_zvit_date_start_db = m_zvit_date_finish_db + relativedelta(days=-1, hour=0, minute=0, second=0, microsecond=0)

        print("m_zvit_date_start_db  = ", m_zvit_date_start_db)
        print("m_zvit_date_finish_db = ", m_zvit_date_finish_db)

        return_args['date_rep_last_day'] = datetime.datetime.strftime(m_zvit_date_start_db, "%d.%m.%Y")

        _return_list = Ticket_history.objects.filter(
            req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db],
            # games_id__verbal__in=m_find_type_game_list
        ).order_by("game_type", "-req_dt")

        print("22 len(_return_list) = ", len(_return_list))

        if len(_return_list) > 0:
            rep_total = {}
            rep_total["type_line"] = "total_report"
            rep_total["type_group"] = gettext("TOTAL")
            rep_total["type_group_code"] = ""
            rep_total["count_ticket"] = 0
            rep_total["cost_1"] = ""
            rep_total["cost_2"] = ""
            rep_total["sum_cost_1"] = 0
            rep_total["sum_cost_2"] = 0
            rep_total["profit_ticket"] = 0
            rep_total["profit_all"] = 0
            rep_total["profit_udachi"] = 0
            rep_total["profit_extcomp"] = 0
            rep_total["profit_average"] = 0
            rep_total["win_count"] = 0
            rep_total["win_sum"] = 0

            rep_group = {}
            rep_group["type_line"] = "total_group"
            rep_group["type_group"] = gettext(_return_list[0].game_type.caption)
            rep_group["type_group_code"] = gettext(_return_list[0].game_type.verbal)
            rep_group["count_ticket"] = 0
            rep_group["cost_1"] = _return_list[0].cost_1
            rep_group["cost_2"] = _return_list[0].cost_2
            rep_group["sum_cost_1"] = 0
            rep_group["sum_cost_2"] = 0
            rep_group["profit_ticket"] = rep_group["cost_2"] - rep_group["cost_1"]
            rep_group["profit_all"] = 0
            rep_group["profit_udachi"] = 0
            rep_group["profit_extcomp"] = 0
            rep_group["profit_average"] = 0
            rep_group["win_count"] = 0
            rep_group["win_sum"] = 0

            for ItemStr in _return_list:
                if rep_group["type_group_code"] != gettext(ItemStr.game_type.verbal):
                    return_list.append(rep_group)
                    rep_group = {}
                    rep_group["type_line"] = "total_group"
                    rep_group["type_group"] = gettext(ItemStr.game_type.caption)
                    rep_group["type_group_code"] = gettext(ItemStr.game_type.verbal)
                    rep_group["count_ticket"] = 0
                    rep_group["cost_1"] = ItemStr.cost_1
                    rep_group["cost_2"] = ItemStr.cost_2
                    rep_group["sum_cost_1"] = 0
                    rep_group["sum_cost_2"] = 0
                    rep_group["profit_ticket"] = rep_group["cost_2"] - rep_group["cost_1"]
                    rep_group["profit_all"] = 0
                    rep_group["profit_udachi"] = 0
                    rep_group["profit_extcomp"] = 0
                    rep_group["profit_average"] = 0
                    rep_group["win_count"] = 0
                    rep_group["win_sum"] = 0

                rep_item = {}
                rep_item["type_line"] = "item_str"
                rep_item["type_group"] = gettext(ItemStr.game_type.caption)
                rep_item["n_req"] = ItemStr.req_id
                try:
                    rep_item["d_req"] = datetime.datetime.strftime(ItemStr.req_dt.astimezone(tz.gettz(m_local_tz)),
                                                                   "%d.%m.%Y %H:%M:%S")
                except:
                    rep_item["d_req"] = ""
                try:
                    rep_item["d_answ"] = datetime.datetime.strftime(ItemStr.answ_dt.astimezone(tz.gettz(m_local_tz)),
                                                                    "%d.%m.%Y %H:%M:%S")
                except:
                    rep_item["d_answ"] = ""

                rep_item["number"] = ItemStr.answ_nom
                rep_item["win"] = ItemStr.answ_win
                try:
                    rep_item["win_sum"] = decimal.Decimal(ItemStr.answ_win_sum)
                except:
                    rep_item["win_sum"] = 0

                rep_item["game_last"] = -1
                #
                rep_item["cost_1"] = ItemStr.cost_1
                rep_item["cost_2"] = ItemStr.cost_2
                rep_item["sum_cost_1"] = ItemStr.cost_1
                rep_item["sum_cost_2"] = ItemStr.cost_2
                rep_item["profit_ticket"] = ItemStr.cost_2 - ItemStr.cost_1
                rep_item["profit_all"] = ItemStr.cost_2 - ItemStr.cost_1
                rep_item["profit_udachi"] = round(rep_item["profit_all"] * m_procent_udachi / 100, 2)
                rep_item["profit_extcomp"] = round(rep_item["profit_all"] - rep_item["profit_udachi"], 2)
                rep_item["profit_average"] = 0
                rep_item["win_count"] = 1 if ItemStr.answ_win else 0
                try:
                    rep_item["win_sum"] = decimal.Decimal(ItemStr.answ_win_sum)
                except:
                    rep_item["win_sum"] = 0
                #

                rep_group["count_ticket"] += 1
                rep_group["sum_cost_1"] += rep_item["sum_cost_1"]
                rep_group["sum_cost_2"] += rep_item["sum_cost_2"]
                # rep_group["profit_ticket"] = 0
                rep_group["profit_all"] += rep_item["profit_all"]
                rep_group["profit_udachi"] += rep_item["profit_udachi"]
                rep_group["profit_extcomp"] += rep_item["profit_extcomp"]
                rep_group["profit_average"] = 0
                rep_group["win_count"] += rep_item["win_count"]
                rep_group["win_sum"] += rep_item["win_sum"]

                rep_total["count_ticket"] += 1
                rep_total["sum_cost_1"] += rep_item["sum_cost_1"]
                rep_total["sum_cost_2"] += rep_item["sum_cost_2"]
                # rep_total["profit_ticket"] = 0
                rep_total["profit_all"] += rep_item["profit_all"]
                rep_total["profit_udachi"] += rep_item["profit_udachi"]
                rep_total["profit_extcomp"] += rep_item["profit_extcomp"]
                rep_total["profit_average"] = 0
                rep_total["win_count"] += rep_item["win_count"]
                rep_total["win_sum"] += rep_item["win_sum"]

                # return_list.append(rep_item)

            return_list.append(rep_group)
            return_list.append(rep_total)

    elif verbal == "Rep_07":
        # m_zvit_date_finish_db = m_zvit_date_finish_db + relativedelta(days=-1, hour=0, minute=0, second=0,
        #                                                               microsecond=0)
        players_list = Ticket_history.objects.filter(
            req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db]).values(
            'games_id__user_id__profile__name', 'games_id__user_id__profile__mobile', 'games_id__user_id__profile__date_joined',
            'games_id__user_id__email').annotate(
            games_count=Count('games_id', distinct=True),
            tickets_count=Count('id'),
            amount_sum=Sum('cost_2', output_field=DecimalField()),
            amount_sum_real=Coalesce(Sum('cost_2',
                                         filter=(~Q(games_id__t_payment__verbal='balance'))), 0, output_field=DecimalField()),
            subs_tickets_count=Count('id', filter=Q(games_id__t_subs__isnull=False),)
        ).order_by('-amount_sum')

        total_values = players_list.aggregate(Sum('games_count'), Sum('tickets_count'), Sum('subs_tickets_count'),
                                              Sum('amount_sum'), Count('games_id__user_id__profile__name'),
                                              Sum('amount_sum_real'))
        return_list = list(players_list)
        return_list.append({'games_count': total_values['games_count__sum'],
                            'tickets_count': total_values['tickets_count__sum'],
                            'amount_sum': total_values['amount_sum__sum'],
                            'amount_sum_real': total_values['amount_sum_real__sum'],
                            'subs_tickets_count': total_values['subs_tickets_count__sum'],
                            'games_id__user_id__profile__name': 'TOTAL', 'total': True,
                            'games_id__user_id__profile__mobile':
                                total_values['games_id__user_id__profile__name__count']})

    elif verbal == "Rep_08":
        m_local_tz = 'Israel'
        _return_list = Ticket_history.objects.filter(
            req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db],
            # games_id__verbal__in=m_find_type_game_list
        ).order_by("req_dt")

        for ItemStr in _return_list:
            m_rep_item_d_req = ItemStr.req_dt.astimezone(tz.gettz(m_local_tz))

        try:
            m_procent_udachi = return_args.get("GL_Udachi_Profit", 0)
            m_procent_udachi = int(m_procent_udachi)
        except:
            m_procent_udachi = 100

        m_data_labels = []
        m_data_user = []
        m_data_profit = []
        m_data_tickets = []

        return_list = []

        if len(_return_list) > 0:
            rep_total = {}
            # rep_total["type_line"] = "total_report"
            # rep_total["type_group"] = gettext("TOTAL")
            # rep_total["count_ticket"] = 0
            # rep_total["cost_1"] = ""
            # rep_total["cost_2"] = ""
            # rep_total["sum_cost_1"] = 0
            # rep_total["sum_cost_2"] = 0
            # rep_total["profit_ticket"] = 0
            # rep_total["profit_all"] = 0
            # rep_total["profit_udachi"] = 0
            # rep_total["profit_extcomp"] = 0
            # rep_total["profit_average"] = 0
            # rep_total["win_count"] = 0
            # rep_total["win_sum"] = 0
            user_list = []
            rep_group = {}
            rep_group["type_line"] = "total_group"
            m_date_group = datetime.datetime.strftime(_return_list[0].req_dt.astimezone(tz.gettz(m_local_tz)),
                                                      "%d.%m.%Y")
            # user_list.append(_return_list[0].games_id.user_id_id)
            rep_group["type_group"] = m_date_group
            rep_group["total_amount"] = 0
            rep_group["total_profit"] = 0
            rep_group["c4"] = 0
            rep_group["c5"] = 0
            rep_group["c6"] = 0
            rep_group["c7"] = 0
            rep_group["c8"] = 0
            rep_group["c9"] = 0  # ticket
            rep_group["l_total_amount"] = 0
            rep_group["l_total_profit"] = 0
            rep_group["l_c4"] = 0
            rep_group["l_c5"] = 0
            rep_group["l_c6"] = 0
            rep_group["l_c7"] = 0
            rep_group["l_c8"] = 0
            rep_group["l_c9"] = 0

            for ItemStr in _return_list:
                m_date_group = datetime.datetime.strftime(ItemStr.req_dt.astimezone(tz.gettz(m_local_tz)), "%d.%m.%Y")
                if rep_group["type_group"] != m_date_group:
                    m_data_labels.append(rep_group["type_group"])
                    m_data_user.append(rep_group["c6"])
                    m_data_profit.append(rep_group["total_profit"])
                    m_data_tickets.append(rep_group["c9"])

                    rep_group["c4"] = rep_group["total_profit"] - rep_group["l_total_profit"]
                    if rep_group["l_total_profit"] > 0:
                        rep_group["c5"] = round((rep_group["c4"] / rep_group["l_total_profit"]) * 100, 2)
                    rep_group["c7"] = rep_group["c6"] - rep_group["l_c6"]
                    if rep_group["l_c6"] > 0:
                        rep_group["c8"] = round((rep_group["c7"] / rep_group["l_c6"]) * 100, 2)

                    rep_group_last = rep_group.copy()
                    return_list.append(rep_group)
                    rep_group = {}
                    rep_group["type_line"] = "total_group"
                    rep_group["type_group"] = m_date_group
                    rep_group["total_amount"] = 0
                    rep_group["total_profit"] = 0
                    rep_group["c4"] = 0
                    rep_group["c5"] = 0
                    rep_group["c6"] = 0
                    rep_group["c7"] = 0
                    rep_group["c8"] = 0
                    rep_group["c9"] = 0
                    rep_group["l_total_amount"] = rep_group_last["total_amount"]
                    rep_group["l_total_profit"] = rep_group_last["total_profit"]
                    rep_group["l_c4"] = 0
                    rep_group["l_c5"] = 0
                    rep_group["l_c6"] = rep_group_last["c6"]
                    rep_group["l_c7"] = 0
                    rep_group["l_c8"] = 0
                    rep_group["l_c9"] = rep_group_last["c9"]
                    user_list = []

                rep_item = {}
                rep_item["type_line"] = "item_str"
                rep_item["type_group"] = m_date_group
                rep_item["n_req"] = ItemStr.req_id
                rep_item["number"] = ItemStr.answ_nom
                rep_item["win"] = ItemStr.answ_win
                try:
                    rep_item["win_sum"] = decimal.Decimal(ItemStr.answ_win_sum)
                except:
                    rep_item["win_sum"] = 0

                rep_item["game_last"] = -1

                rep_group["total_amount"] += ItemStr.cost_2
                rep_group["total_profit"] += ItemStr.cost_2 - ItemStr.cost_1
                rep_group["c4"] = 0
                rep_group["c5"] = 0
                if ItemStr.games_id.user_id_id in user_list:
                    pass
                else:
                    rep_group["c6"] += 1
                    user_list.append(ItemStr.games_id.user_id_id)
                rep_group["c7"] = 0
                rep_group["c8"] = 0
                rep_group["c9"] += 1

            rep_group["c4"] = rep_group["total_profit"] - rep_group["l_total_profit"]
            if rep_group["l_total_profit"] > 0:
                rep_group["c5"] = round((rep_group["c4"] / rep_group["l_total_profit"]) * 100, 2)
            rep_group["c7"] = rep_group["c6"] - rep_group["l_c6"]
            if rep_group["l_c6"] > 0:
                rep_group["c8"] = round((rep_group["c7"] / rep_group["l_c6"]) * 100, 2)
            m_data_labels.append(rep_group["type_group"])
            m_data_user.append(rep_group["c6"])
            m_data_profit.append(rep_group["total_profit"])
            m_data_tickets.append(rep_group["c9"])
            return_list.append(rep_group)
            # return_list.append(rep_total)

        return_args['data_labels'] = m_data_labels
        return_args['data_user'] = m_data_user
        return_args['data_profit'] = m_data_profit
        return_args['data_tickets'] = m_data_tickets

        return_args['total_deposit'] = return_args.get("GL_Udachi_Deposit", 0)
        return_args['total_creditcard'] = return_args.get("GL_Udachi_CreditCard", 0)
        # return_args['total_invoce'] = return_args['total_client_sum'] \
        #                               + return_args['total_win_sum'] \
        #                               + int(return_args['total_deposit']) \
        #                               + int(return_args['total_creditcard'])
        return_args['return_list_month'] = return_list

        all_amount = [i['total_amount'] for i in return_list]
        all_profit = [i['total_profit'] for i in return_list]
        all_users = [i['c6'] for i in return_list]
        all_tickets = [i['c9'] for i in return_list]
        averages = {'type': 'Avg',
                    'amount': round(sum(all_amount) / len(all_amount), 2),
                    'profit': round(sum(all_profit) / len(all_profit), 2),
                    'users': round(sum(all_users) / len(all_users), 2),
                    'tickets': round(sum(all_tickets) / len(all_tickets), 2),
                    }
        return_args['averages'] = averages

    elif verbal == "Rep_09":
        m_local_tz = 'Israel'
        return_list = []
        # _return_list = Ticket_history.objects.filter(
        #     req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db],
        #     # games_id__verbal__in=m_find_type_game_list
        # ).exclude(games_id__t_payment__verbal="balance").order_by("games_id__t_payment__order", "game_type")
        # #order_by("req_dt")
        # # ).order_by("games_id__t_payment__order", "game_type")

        _return_list = Game_history.objects.filter(
            t_status__verbal="start",
            dt_add__range=[m_zvit_date_start_db, m_zvit_date_finish_db],
        ).exclude(t_payment__verbal="balance").order_by("t_payment__order")

        if len(_return_list) > 0:
            rep_total = {}
            rep_total["type_line"] = "total_report"
            rep_total["type_group"] = gettext("TOTAL")
            rep_total["g_c"] = 0
            rep_total["w_c"] = 0
            rep_total["w_a"] = 0
            rep_total["b_c"] = 0
            rep_total["b_a"] = 0
            rep_total["r_c"] = 0
            rep_total["r_a"] = 0
            rep_total["s_c"] = 0
            rep_total["s_a"] = 0
            rep_total["tranzila_amount"] = 0

            rep_group = {}
            rep_group["type_line"] = "total_group"
            rep_group["type_group"] = gettext(_return_list[0].t_payment.caption)
            rep_group["g_c"] = 0
            rep_group["w_c"] = 0
            rep_group["w_a"] = 0
            rep_group["b_c"] = 0
            rep_group["b_a"] = 0
            rep_group["r_c"] = 0
            rep_group["r_a"] = 0
            rep_group["s_c"] = 0
            rep_group["s_a"] = 0
            rep_group["tranzila_amount"] = 0

            for ItemStr in _return_list:

                rep_item = {}
                rep_item["type_line"] = "item_str"
                rep_item["type_group"] = gettext(ItemStr.t_payment.caption)
                # rep_item["type_item"] = gettext(ItemStr.game_type.caption)
                rep_item["type_item"] = ItemStr.ticket_list["list_order"][0]["tic_caption"]
                rep_item["g_c"] = 0
                rep_item["w_c"] = 0
                rep_item["w_a"] = 0
                rep_item["b_c"] = 0
                rep_item["b_a"] = 0
                rep_item["r_c"] = 0
                rep_item["r_a"] = 0
                rep_item["s_c"] = 0
                rep_item["s_a"] = 0
                rep_item["game_last"] = -1
                rep_item["u_name"] = ItemStr.user_id.profile.name
                rep_item["u_email"] = ItemStr.user_id.email
                rep_item["u_phone"] = ItemStr.user_id.profile.mobile
                rep_item["tranzila_date"] = ""
                rep_item["tranzila_amount"] = ""
                rep_item["tranzila_response"] = ""
                rep_item["tranzila_index"] = ""
                rep_item["tranzila_myid"] = ""
                rep_item["tranzila_ccno"] = ""
                m_payment_status_verbal = "00"

                m_games_id = ItemStr.id
                m_BalanceOperation = BalanceOperation.objects.filter(games_id_id=m_games_id)

                if len(m_BalanceOperation) > 0:
                    m_payment_status_verbal = m_BalanceOperation[0].status.verbal
                    rep_item["tranzila_date"] = datetime.datetime.strftime(
                        m_BalanceOperation[0].created.astimezone(tz.gettz(m_local_tz)), "%d.%m.%Y %H:%M:%S")
                    rep_item["tranzila_amount"] = m_BalanceOperation[0].amount

                    m_pay_response = m_BalanceOperation[0].pay_response
                    if m_pay_response:
                        m_response = f"{m_pay_response[12:-1]}"
                        m_response = m_response.replace("\'", "\"")

                        m_response = m_response[min(m_response.find("["), m_response.find("{")):]

                        try:
                            m_response = json.loads(m_response)
                        except Exception as ex:
                            print("\n\n\nm_response = ", m_response, "\n\n\n")
                            break

                        rep_item["tranzila_response"] = m_response.get("Response", "")
                        if len(rep_item["tranzila_response"]) > 0:
                            rep_item["tranzila_response"] = rep_item["tranzila_response"][0]

                        rep_item["tranzila_index"] = m_response.get("index", "")
                        if len(rep_item["tranzila_index"]) > 0:
                            rep_item["tranzila_index"] = rep_item["tranzila_index"][0]

                        rep_item["tranzila_myid"] = m_response.get("myid", "")
                        if len(rep_item["tranzila_myid"]) > 0:
                            rep_item["tranzila_myid"] = rep_item["tranzila_myid"][0]

                        rep_item["tranzila_ccno"] = m_response.get("ccno", "")
                        if len(rep_item["tranzila_ccno"]) > 0:
                            rep_item["tranzila_ccno"] = rep_item["tranzila_ccno"][0]

                # print("12-5")
                # Response': ['000']
                # myid': ['319448767']
                # order_id': ['32035']
                # 'index': ['98875'],

                # if rep_group["type_group"] != gettext(ItemStr.games_id.t_payment.caption) or rep_item["type_item"] != gettext(ItemStr.game_type.caption):
                #     return_list.append(rep_item)
                #     rep_item = {}
                #     rep_item["type_line"] = "item_str"
                #     rep_item["type_group"] = gettext(ItemStr.games_id.t_payment.caption)
                #     rep_item["type_item"] = gettext(ItemStr.game_type.caption)
                #     rep_item["g_c"] = 0
                #     rep_item["w_c"] = 0
                #     rep_item["w_a"] = 0
                #     rep_item["b_c"] = 0
                #     rep_item["b_a"] = 0
                #     rep_item["r_c"] = 0
                #     rep_item["r_a"] = 0
                #     rep_item["s_c"] = 0
                #     rep_item["s_a"] = 0
                #     rep_item["game_last"] = -1

                if rep_group["type_group"] != gettext(ItemStr.t_payment.caption):
                    return_list.append(rep_group)
                    rep_group = {}
                    rep_group["type_line"] = "total_group"
                    rep_group["type_group"] = gettext(ItemStr.t_payment.caption)
                    rep_group["g_c"] = 0
                    rep_group["w_c"] = 0
                    rep_group["w_a"] = 0
                    rep_group["b_c"] = 0
                    rep_group["b_a"] = 0
                    rep_group["r_c"] = 0
                    rep_group["r_a"] = 0
                    rep_group["s_c"] = 0
                    rep_group["s_a"] = 0
                    rep_group["tranzila_amount"] = 0

                rep_group["tranzila_amount"] += int(rep_item["tranzila_amount"])
                rep_total["tranzila_amount"] += int(rep_item["tranzila_amount"])

                if m_payment_status_verbal == "01":
                    rep_item["w_c"] += 1
                    # rep_item["w_a"] += ItemStr.cost_2
                    rep_group["w_c"] += 1
                    # rep_group["w_a"] += ItemStr.cost_2
                    rep_total["w_c"] += 1
                    # rep_total["w_a"] += ItemStr.cost_2

                if m_payment_status_verbal == "02":
                    rep_item["b_c"] += 1
                    # rep_item["b_a"] += ItemStr.cost_2
                    rep_group["b_c"] += 1
                    # rep_group["b_a"] += ItemStr.cost_2
                    rep_total["b_c"] += 1
                    # rep_total["b_a"] += ItemStr.cost_2

                if m_payment_status_verbal == "03":
                    rep_item["r_c"] += 1
                    # rep_item["r_a"] += ItemStr.cost_2
                    rep_group["r_c"] += 1
                    # rep_group["r_a"] += ItemStr.cost_2
                    rep_total["r_c"] += 1
                    # rep_total["r_a"] += ItemStr.cost_2

                if m_payment_status_verbal == "04":
                    if rep_item["game_last"] != ItemStr.id:
                        rep_item["g_c"] += 1
                        rep_group["g_c"] += 1
                        rep_total["g_c"] += 1
                    rep_item["s_c"] = 1
                    # rep_item["s_a"] = ItemStr.cost_2
                    rep_group["s_c"] += 1
                    # rep_group["s_a"] += ItemStr.cost_2
                    rep_total["s_c"] += 1
                    # rep_total["s_a"] += ItemStr.cost_2

                rep_item["game_last"] = ItemStr.id

                # return_list.append(rep_item_0)
                return_list.append(rep_item)
            return_list.append(rep_group)
            return_list.append(rep_total)

    elif verbal == "Rep_10":
        profiles_registered = Profile.objects.filter(
            date_joined__range=[m_zvit_date_start_db, m_zvit_date_finish_db]
        ).values_list('user_id__id', flat=True)

        have_tickets = Ticket_history.objects.filter(
            games_id__user_id__id__in=profiles_registered).values(
            'games_id__user_id__profile__id', 'games_id__user_id__profile__date_joined').annotate(
            min_date=Min('req_dt'),
            delta=ExpressionWrapper(F('min_date') - F('games_id__user_id__profile__date_joined'),
                                    output_field=DurationField()),
            delta_days=Case(
                When(delta__lt=Value(timedelta(days=1)), then=1),
                When(Q(delta__gt=Value(timedelta(days=1))) & Q(delta__lte=Value(timedelta(days=7))), then=2),
                When(Q(delta__gt=Value(timedelta(days=7))) & Q(delta__lte=Value(timedelta(days=14))), then=3),
                When(Q(delta__gt=Value(timedelta(days=14))) & Q(delta__lte=Value(timedelta(days=30))), then=4),
                When(delta__gt=Value(timedelta(days=30)), then=5),
                output_field=IntegerField())
        )
        total_values = have_tickets.aggregate(
            count_users=Count('games_id__user_id__profile__id'),
            days_1=Count('delta_days', filter=Q(delta_days=1)),
            days_2=Count('delta_days', filter=Q(delta_days=2)),
            days_3=Count('delta_days', filter=Q(delta_days=3)),
            days_4=Count('delta_days', filter=Q(delta_days=4)),
            days_5=Count('delta_days', filter=Q(delta_days=5)),
        )
        no_play = len(profiles_registered) - total_values['count_users']

        return_args['data_labels'] = ['1', '2 - 7', '8 - 14', '15 - 30', '30+', 'no play']
        return_args['data_players'] = [total_values['days_1'], total_values['days_2'], total_values['days_3'],
                                       total_values['days_4'], total_values['days_5'], no_play]
        return_list = {i: j for (i, j) in zip(return_args['data_labels'], return_args['data_players'])}

    elif verbal == "Rep_11":
        m_local_tz = 'Israel'
        return_list = []

        m_data_labels = ["00:00 - 00:30",
                         "00:30 - 01:00",
                         "01:00 - 01:30",
                         "01:30 - 02:00",
                         "02:00 - 02:30",
                         "02:30 - 03:00",
                         "03:00 - 03:30",
                         "03:30 - 04:00",
                         "04:00 - 04:30",
                         "04:30 - 05:00",
                         "05:00 - 05:30",
                         "05:30 - 06:00",
                         "06:00 - 06:30",
                         "06:30 - 07:00",
                         "07:00 - 07:30",
                         "07:30 - 08:00",
                         "08:00 - 08:30",
                         "08:30 - 09:00",
                         "09:00 - 09:30",
                         "09:30 - 10:00",
                         "10:00 - 10:30",
                         "10:30 - 11:00",
                         "11:00 - 11:30",
                         "11:30 - 12:00",
                         "12:00 - 12:30",
                         "12:30 - 13:00",
                         "13:00 - 13:30",
                         "13:30 - 14:00",
                         "14:00 - 14:30",
                         "14:30 - 15:00",
                         "15:00 - 15:30",
                         "15:30 - 16:00",
                         "16:00 - 16:30",
                         "16:30 - 17:00",
                         "17:00 - 17:30",
                         "17:30 - 18:00",
                         "18:00 - 18:30",
                         "18:30 - 19:00",
                         "19:00 - 19:30",
                         "19:30 - 20:00",
                         "20:00 - 20:30",
                         "20:30 - 21:00",
                         "21:00 - 21:30",
                         "21:30 - 22:00",
                         "22:00 - 22:30",
                         "22:30 - 23:00",
                         "23:00 - 23:30",
                         "23:30 - 00:00",
                         ]
        # первый блок
        return_list_01 = []

        for numItem in range(48):
            rep_item = {}
            rep_item["type_line"] = ""
            rep_item["type_group"] = ""
            rep_item["name"] = m_data_labels[numItem]
            rep_item["c01"] = 0
            rep_item["c02"] = "0 %"
            rep_item["c03"] = 0
            rep_item["c03_list"] = []
            rep_item["c04"] = "0 %"
            return_list_01.append(rep_item)

        _return_list_01 = Ticket_history.objects.filter(
            req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db]
        )
        m_total_01_c01 = 0
        m_total_01_c03 = 0
        for Item_t in _return_list_01:
            m_data_tek_0 = Item_t.req_dt
            m_data_tek = m_data_tek_0.astimezone(tz.gettz(m_local_tz))
            m_data_h = m_data_tek.hour * 60
            m_data_m = m_data_tek.minute + m_data_h
            m_index = int(m_data_m / 30)
            # tickets
            return_list_01[m_index]["c01"] += 1
            m_total_01_c01 += 1
            # players
            m_tmp_user = Item_t.games_id.user_id_id
            ##
            if m_tmp_user in return_list_01[m_index]["c03_list"]:
                pass
            else:
                return_list_01[m_index]["c03"] += 1
                return_list_01[m_index]["c03_list"].append(m_tmp_user)
                m_total_01_c03 += 1

        data_chart01_01 = []
        data_chart01_02 = []
        for Item_list in return_list_01:
            data_chart01_01.append(Item_list["c01"])
            data_chart01_02.append(Item_list["c03"])
            if m_total_01_c01 > 0:
                Item_list["c02"] = f'{round(100 * (Item_list["c01"] / m_total_01_c01), 2)} %'
            else:
                Item_list["c02"] = f'0 %'
            if m_total_01_c03 > 0:
                Item_list["c04"] = f'{round(100 * (Item_list["c03"] / m_total_01_c03), 2)} %'
            else:
                Item_list["c04"] = f'0 %'

        return_args['data_labels_01'] = m_data_labels
        return_args['data_label_01_01'] = gettext("Tickets")
        return_args['data_label_01_02'] = gettext("Players")
        return_args['return_list_01'] = return_list_01

        return_args['data_chart_01_01'] = data_chart01_01
        return_args['data_chart_01_02'] = data_chart01_02

        m_total_01_c02 = '100 %'
        m_total_01_c04 = '100 %'

        return_args['total_01_c01'] = m_total_01_c01
        return_args['total_01_c02'] = m_total_01_c02
        return_args['total_01_c03'] = m_total_01_c03
        return_args['total_01_c04'] = m_total_01_c04

        # второй блок
        return_list_02 = []

        for numItem in range(48):
            rep_item = {}
            rep_item["type_line"] = ""
            rep_item["type_group"] = ""
            rep_item["name"] = m_data_labels[numItem]
            rep_item["c01"] = 0
            rep_item["c02"] = "0 %"
            rep_item["c03"] = 0
            rep_item["c03_list"] = []
            rep_item["c04"] = "0 %"
            return_list_02.append(rep_item)

        _return_list_02 = Ticket_history.objects.filter(
            req_dt__range=[m_zvit_date_2_start_db, m_zvit_date_2_finish_db]
        )
        m_total_02_c01 = 0
        m_total_02_c03 = 0
        for Item_t in _return_list_02:
            m_data_tek_0 = Item_t.req_dt
            m_data_tek = m_data_tek_0.astimezone(tz.gettz(m_local_tz))
            m_data_h = m_data_tek.hour * 60
            m_data_m = m_data_tek.minute + m_data_h
            m_index = int(m_data_m / 30)
            # tickets
            return_list_02[m_index]["c01"] += 1
            m_total_02_c01 += 1
            # players
            m_tmp_user = Item_t.games_id.user_id_id
            ##
            if m_tmp_user in return_list_02[m_index]["c03_list"]:
                pass
            else:
                return_list_02[m_index]["c03"] += 1
                return_list_02[m_index]["c03_list"].append(m_tmp_user)
                m_total_02_c03 += 1

        data_chart02_01 = []
        data_chart02_02 = []
        for Item_list in return_list_02:
            data_chart02_01.append(Item_list["c01"])
            data_chart02_02.append(Item_list["c03"])
            if m_total_02_c01 > 0:
                Item_list["c02"] = f'{round(100 * (Item_list["c01"] / m_total_02_c01), 2)} %'
            else:
                Item_list["c02"] = f'0 %'
            if m_total_02_c03 > 0:
                Item_list["c04"] = f'{round(100 * (Item_list["c03"] / m_total_02_c03), 2)} %'
            else:
                Item_list["c04"] = f'0 %'

        return_args['data_labels_02'] = m_data_labels
        return_args['data_label_02_01'] = gettext("Tickets")
        return_args['data_label_02_02'] = gettext("Players")
        return_args['return_list_02'] = return_list_02

        return_args['data_chart_02_01'] = data_chart02_01
        return_args['data_chart_02_02'] = data_chart02_02

        m_total_02_c02 = '100 %'
        m_total_02_c04 = '100 %'

        return_args['total_02_c01'] = m_total_02_c01
        return_args['total_02_c02'] = m_total_02_c02
        return_args['total_02_c03'] = m_total_02_c03
        return_args['total_02_c04'] = m_total_02_c04

    elif verbal == "Rep_12":
        m_local_tz = 'Israel'
        return_list = []

        m_data_labels = [gettext("Sunday"),
                         gettext("Monday"),
                         gettext("Tuesday"),
                         gettext("Wednesday"),
                         gettext("Thursday"),
                         gettext("Friday"),
                         gettext("Saturday"),
                         ]
        # первый блок
        return_list_01 = []

        for numItem in range(7):
            rep_item = {}
            rep_item["type_line"] = ""
            rep_item["type_group"] = ""
            rep_item["name"] = m_data_labels[numItem]
            rep_item["c01"] = 0
            rep_item["c02"] = "0 %"
            rep_item["c03"] = 0
            rep_item["c03_list"] = []
            rep_item["c04"] = "0 %"
            return_list_01.append(rep_item)

        _return_list_01 = Ticket_history.objects.filter(
            req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db]
        )

        m_total_01_c01 = 0
        m_total_01_c03 = 0
        for Item_t in _return_list_01:
            m_data_tek_0 = Item_t.req_dt
            m_data_tek = m_data_tek_0.astimezone(tz.gettz(m_local_tz))
            m_index = m_data_tek.isoweekday() - 1

            print("m_index = ", m_index, m_data_tek)
            # tickets
            return_list_01[m_index]["c01"] += 1
            m_total_01_c01 += 1
            # players
            m_tmp_user = Item_t.games_id.user_id_id
            ##
            if m_tmp_user in return_list_01[m_index]["c03_list"]:
                pass
            else:
                return_list_01[m_index]["c03"] += 1
                return_list_01[m_index]["c03_list"].append(m_tmp_user)
                m_total_01_c03 += 1

        print("002")
        data_chart01_01 = []
        data_chart01_02 = []
        for Item_list in return_list_01:
            data_chart01_01.append(Item_list["c01"])
            data_chart01_02.append(Item_list["c03"])
            if m_total_01_c01 > 0:
                Item_list["c02"] = f'{round(100 * (Item_list["c01"] / m_total_01_c01), 2)} %'
            else:
                Item_list["c02"] = f'0 %'
            if m_total_01_c03 > 0:
                Item_list["c04"] = f'{round(100 * (Item_list["c03"] / m_total_01_c03), 2)} %'
            else:
                Item_list["c04"] = f'0 %'

        print("003")
        return_args['data_labels_01'] = m_data_labels
        return_args['data_label_01_01'] = gettext("Tickets")
        return_args['data_label_01_02'] = gettext("Players")
        return_args['return_list_01'] = return_list_01
        print("004")

        return_args['data_chart_01_01'] = data_chart01_01
        return_args['data_chart_01_02'] = data_chart01_02
        print("005")

        m_total_01_c02 = '100 %'
        m_total_01_c04 = '100 %'
        print("006")

        return_args['total_01_c01'] = m_total_01_c01
        return_args['total_01_c02'] = m_total_01_c02
        return_args['total_01_c03'] = m_total_01_c03
        return_args['total_01_c04'] = m_total_01_c04

        # второй блок
        return_list_02 = []

        for numItem in range(7):
            rep_item = {}
            rep_item["type_line"] = ""
            rep_item["type_group"] = ""
            rep_item["name"] = m_data_labels[numItem]
            rep_item["c01"] = 0
            rep_item["c02"] = "0 %"
            rep_item["c03"] = 0
            rep_item["c03_list"] = []
            rep_item["c04"] = "0 %"
            return_list_02.append(rep_item)

        _return_list_02 = Ticket_history.objects.filter(
            req_dt__range=[m_zvit_date_2_start_db, m_zvit_date_2_finish_db]
        )
        m_total_02_c01 = 0
        m_total_02_c03 = 0
        for Item_t in _return_list_02:
            m_data_tek_0 = Item_t.req_dt
            m_data_tek = m_data_tek_0.astimezone(tz.gettz(m_local_tz))
            m_index = m_data_tek.isoweekday() - 1
            # tickets
            return_list_02[m_index]["c01"] += 1
            m_total_02_c01 += 1
            # players
            m_tmp_user = Item_t.games_id.user_id_id
            ##
            if m_tmp_user in return_list_02[m_index]["c03_list"]:
                pass
            else:
                return_list_02[m_index]["c03"] += 1
                return_list_02[m_index]["c03_list"].append(m_tmp_user)
                m_total_02_c03 += 1

        data_chart02_01 = []
        data_chart02_02 = []
        for Item_list in return_list_02:
            data_chart02_01.append(Item_list["c01"])
            data_chart02_02.append(Item_list["c03"])
            if m_total_02_c01 > 0:
                Item_list["c02"] = f'{round(100 * (Item_list["c01"] / m_total_02_c01), 2)} %'
            else:
                Item_list["c02"] = f'0 %'
            if m_total_02_c03 > 0:
                Item_list["c04"] = f'{round(100 * (Item_list["c03"] / m_total_02_c03), 2)} %'
            else:
                Item_list["c04"] = f'0 %'

        return_args['data_labels_02'] = m_data_labels
        return_args['data_label_02_01'] = gettext("Tickets")
        return_args['data_label_02_02'] = gettext("Players")
        return_args['return_list_02'] = return_list_02

        return_args['data_chart_02_01'] = data_chart02_01
        return_args['data_chart_02_02'] = data_chart02_02

        m_total_02_c02 = '100 %'
        m_total_02_c04 = '100 %'

        return_args['total_02_c01'] = m_total_02_c01
        return_args['total_02_c02'] = m_total_02_c02
        return_args['total_02_c03'] = m_total_02_c03
        return_args['total_02_c04'] = m_total_02_c04

    elif verbal == "Rep_13":
        m_local_tz = 'Israel'
        return_list = []
        _return_list = Profile.objects.all().order_by("date_joined")
        rep_total = {}
        rep_total["type_line"] = "total_report"
        rep_total["type_group"] = gettext("TOTAL")
        rep_total["id"] = gettext("TOTAL")
        rep_total["name"] = ""
        rep_total["mobile"] = ""
        rep_total["email"] = ""
        rep_total["date_joined"] = ""
        rep_total["i_doc"] = ""
        rep_total["balance"] = 0

        for ItemStr in _return_list:
            rep_item = {}
            rep_item["type_line"] = ""
            rep_item["type_group"] = ""
            rep_item["id"] = ItemStr.id
            rep_item["name"] = ItemStr.name
            rep_item["mobile"] = ItemStr.mobile
            rep_item["email"] = ItemStr.user.email
            rep_item["date_joined"] = datetime.datetime.strftime(ItemStr.date_joined, "%d.%m.%Y %H:%M:%S")
            rep_item["i_doc"] = ItemStr.i_doc
            rep_item["balance"] = ItemStr.balance
            return_list.append(rep_item)

            rep_total["balance"] += ItemStr.balance

        return_list.append(rep_total)

    elif verbal == "Rep_14":
        return_list = []
        verbal_types = ['credit_card', 'bit', 'applepay']
        _return_list = BalanceOperation.objects.filter(type_balanceoperation__verbal__in=verbal_types).filter(
            created__range=[m_zvit_date_start_db, m_zvit_date_finish_db],
        )
        for item in _return_list:
            return_list.append(item)
        p_answers_without_fk = PaymentAnswer.objects.filter(balance_operation_id__isnull=True)
        if p_answers_without_fk:
            return_args['without_fk'] = [i.json_data for i in p_answers_without_fk]

    elif verbal == "Rep_15":
        return_list = []
        users_with_tickets = list(Ticket_history.objects.values_list('games_id__user_id_id__profile', flat=True
                                                                     ).distinct())
        return_list = Profile.objects.exclude(id__in=users_with_tickets).order_by('id')
        return_args['users_count'] = return_list.count()

    elif verbal == "Rep_16":
        players_list = Ticket_history.objects.filter(
            req_dt__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()]
        ).values('games_id__user_id__profile__name', 'games_id__user_id__profile__mobile',
                 'games_id__user_id__email', 'games_id__user_id__profile__balance',
                 'games_id__user_id__profile__date_joined'
                 ).annotate(games_count=Count('games_id', distinct=True),
                            tickets_count=Count('id'),
                            amount_sum=Sum('cost_2')).filter(games_count__gt=5).order_by('-amount_sum')
        return_list = list(players_list)

    elif verbal == "Rep_17":
        m_local_tz = 'Israel'
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        total_months = {}
        for dt in rrule(MONTHLY, dtstart=m_zvit_date_start_db, until=m_zvit_date_finish_db):
            key = (dt.month, dt.year)
            total_months[key] = {'str_key': f'{months[key[0]-1]} {dt.year}', 'tickets_count': 0, 'amount_sum': 0}

        tickets = Ticket_history.objects.filter(req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db]).order_by('req_dt')
        for ticket in tickets:
            month = ticket.req_dt.astimezone(tz.gettz(m_local_tz)).month
            year = ticket.req_dt.astimezone(tz.gettz(m_local_tz)).year
            total_months[(month, year)]['tickets_count'] += 1
            total_months[(month, year)]['amount_sum'] += ticket.cost_2

        months_labels = [i['str_key'] for i in total_months.values()]
        ticket_sum_data = [i['amount_sum'] for i in total_months.values()]
        ticket_count_data = [i['tickets_count'] for i in total_months.values()]
        tickets_by_month = [[i['str_key'], i['amount_sum'], i['tickets_count']] for i in total_months.values()]
        return_list = [months_labels, ticket_sum_data, ticket_count_data, tickets_by_month]

        # tickets_by_month = Ticket_history.objects.filter(req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db]).values(
        #     'req_dt__month', 'req_dt__year').annotate(
        #     tickets_count=Count('id'), amount_sum=Sum('cost_2'))

        # lst = Game_history.objects.filter(t_status__verbal="start").order_by('dt_add')
        # lst = lst.filter(dt_add__range=[m_zvit_date_start_db, m_zvit_date_finish_db])

        # if lst.count() > 0:
        #     totalMonths = []
        #
        #     month_start = lst.first().dt_add.astimezone(tz.gettz(m_local_tz)).month
        #     year_start = lst.first().dt_add.astimezone(tz.gettz(m_local_tz)).year
        #
        #     month_end = lst.last().dt_add.astimezone(tz.gettz(m_local_tz)).month
        #     year_end = lst.last().dt_add.astimezone(tz.gettz(m_local_tz)).year
        #
        #     if not (year_end - year_start):
        #         totalMonths += months[month_start - 1: month_end]
        #     else:
        #         totalMonths += months[month_start - 1:]
        #         totalMonths += months * (year_end - year_start - 1)
        #         totalMonths += months[: month_end]
        #
        #     totalMonths[0] = totalMonths[0] + f" {year_start}"
        #
        #     year = year_start

            # while ("January" in totalMonths):
            #     # TODO ЭТО КОСТЫЛЬ УРОВНЯ 100
            #     idx_start = totalMonths.index(f"January {year}")
            #     idx_stop = totalMonths.index("January")
            #     for i, m in enumerate(totalMonths[idx_start:idx_stop]):
            #         if m != f"January {year}":
            #             totalMonths[i] = f'{m} {year}'
            #     year += 1
            #     totalMonths[totalMonths.index("January")] = f"January {year}"
            #     idx_start_2 = totalMonths.index(f"January {year}")
            #     for m in totalMonths[idx_start_2:]:
            #         if m != f"January {year}":
            #             totalMonths[totalMonths.index(m)] = f'{m} {year}'

            # totalTicketSum = [0] * len(totalMonths)
            # totalTicketCount = [0] * len(totalMonths)
            #
            # for Item in lst:
            #     index = Item.dt_add.astimezone(tz.gettz(m_local_tz)).month + (
            #             Item.dt_add.astimezone(tz.gettz(m_local_tz)).year - year_start) * 12 - month_start
            #     totalTicketSum[index] += Item.ticket_sum
            #     totalTicketCount[index] += Item.ticket_num
            #
            # return_list.append(totalMonths)
            # return_list.append(totalTicketSum)
            # return_list.append(totalTicketCount)
            #
            # return_list.append(list(zip(totalMonths, totalTicketSum, totalTicketCount)))
        # else:
        #     return_list.append([])
        #     return_list.append([0])
        #     return_list.append([0])
        #
        #     return_list.append(list(zip([], [0], [0])))

    elif verbal == "Rep_18":
        m_local_tz = 'Israel'

        return_list = []
        _return_list = [[i["t_check_user__username"], i["t_check_user__profile__name"]] for i in
                        list(Ticket_history.objects.values("t_check_user__username",
                                                           "t_check_user__profile__name").distinct())]

        max_ticket_count = -1
        min_ticket_count = -1

        for username in _return_list:
            if not username:
                continue

            values = Ticket_history.objects.filter(t_check_user__username=username[0],
                                                   t_check_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db])

            total_tickets = values.count()

            if total_tickets == 0:
                continue

            if total_tickets > max_ticket_count or max_ticket_count == -1:
                max_ticket_count = total_tickets

            if total_tickets < min_ticket_count or min_ticket_count == -1:
                min_ticket_count = total_tickets

            check_time_list = {}

            avg_time_sum = 0
            avg_time_count = 0

            for check_start, check_end, t_id in values.values_list("t_check_dt", "answ_dt", "id"):
                if check_start and check_end:
                    t = check_start.timestamp() - check_end.timestamp()
                    if t < 0:
                        continue

                    avg_time_sum += t
                    avg_time_count += 1

                    check_time_list[t] = t_id

            min_check_time = int(min(check_time_list))
            min_t_id = check_time_list[min(check_time_list)]

            max_check_time = int(max(check_time_list))
            max_t_id = check_time_list[max(check_time_list)]

            avg_time = int(avg_time_sum / avg_time_count)

            work_days = len(
                set(dt["t_check_dt"].astimezone(tz.gettz(m_local_tz)).date() for dt in values.values("t_check_dt")))

            return_list.append([(username[1], username[0]), total_tickets,
                                [timedelta(seconds=min_check_time), min_t_id],
                                [timedelta(seconds=max_check_time), max_t_id],
                                avg_time, work_days, [0, 0]])

        return_list.sort(key=lambda e: e[4])

        def delta(e):
            e[4] = timedelta(seconds=e[4])
            return e

        return_list = list(map(delta, return_list))

        # 0 - None
        # 1 - Success
        # 2 - Danger

        print(min_ticket_count, max_ticket_count)

        for Item in return_list:
            if Item[1] == min_ticket_count:
                Item[6][0] = 2

            if Item[1] == max_ticket_count:
                Item[6][0] = 1

        return_list_length = len(return_list)

        if return_list_length >= 1:
            return_list[0][6][1] = 1
        if return_list_length >= 2:
            return_list[1][6][1] = 1
        if return_list_length >= 3:
            return_list[-1][6][1] = 2
        if return_list_length >= 4:
            return_list[-2][6][1] = 2

    elif verbal in ["Rep_19", "Rep_20", "Rep_21", "Rep_22"]:

        if "daterange" not in dict(request.GET).keys():
            m_zvit_date_start_db = m_zvit_date_start_db.replace(day=1)
            return_args['date_range'] = '{} - {}'.format(m_zvit_date_start_db.strftime("%d.%m.%y"),
                                                         m_zvit_date_finish_db.strftime("%d.%m.%y"))

        result_list = Ticket_history.objects.filter(
            req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db]).values(
            'games_id__user_id__email', 'games_id__user_id__profile__name', 'games_id__user_id__profile__mobile'
        ).distinct().annotate(
            days=Count('req_dt__date', distinct=True),
            games=Count('games_id', distinct=True),
            tickets=Count('id'),
            money=Sum('cost_2'),
            win=Sum(Case(When(answ_win_sum='', then=Value(0)),
                         When(answ_win_sum=None, then=Value(0)),
                         default=Cast('answ_win_sum', DecimalField(max_digits=15, decimal_places=2)),
                         output_field= DecimalField(max_digits=15, decimal_places=2))),
            group=Case(
                When(money__gte=1000, then=Value('gold')),
                When(Q(money__lt=1000) & Q(money__gte=120), then=Value('silver')),
                When(money__lte=120, then=Value('bronze')),
                output_field=CharField()
            )).order_by('-money')
        if verbal == 'Rep_19':
            return_list = result_list.filter(group='gold')
        elif verbal == 'Rep_20':
            return_list = result_list.filter(group='silver')
        elif verbal == 'Rep_21':
            return_list = result_list.filter(group='bronze')
        elif verbal == 'Rep_22':
            return_list = result_list

    elif verbal == "Rep_23":
        # m_zvit_date_finish_db = m_zvit_date_finish_db + relativedelta(days=-1, hour=0, minute=0, second=0,
        #                                                               microsecond=0)
        # m_zvit_date_2_finish_db = m_zvit_date_2_finish_db + relativedelta(days=-1, hour=0, minute=0, second=0,
        #                                                                   microsecond=0)
        if "daterange" not in dict(request.GET).keys():
            m_zvit_date_start_db = m_zvit_date_start_db.replace(day=1)
            m_zvit_date_finish_txt = m_zvit_date_finish_db + relativedelta(days=-1, hour=0, minute=0, second=0,
                                                                           microsecond=0)
            return_args['date_range'] = '{} - {}'.format(m_zvit_date_start_db.strftime("%d.%m.%y"),
                                                         m_zvit_date_finish_txt.strftime("%d.%m.%y"))

        if "daterange_2" not in dict(request.GET).keys():
            m_zvit_date_2_start_db = m_zvit_date_2_start_db.replace(day=1)
            m_zvit_date_2_finish_txt = m_zvit_date_2_finish_db + relativedelta(days=-1, hour=0, minute=0, second=0,
                                                                           microsecond=0)
            return_args['date_range_2'] = '{} - {}'.format(m_zvit_date_2_start_db.strftime("%d.%m.%y"),
                                                           m_zvit_date_2_finish_txt.strftime("%d.%m.%y"))


        return_list = []

        def add(date_start, date_end):
            _return_list = Ticket_history.objects.filter(req_dt__range=[date_start, date_end])
            print(len(list(_return_list)), '==============================================================================')
            tickets_old = _return_list.filter(
                games_id__user_id__profile__date_joined__lt=date_start).count()
            tickets_new = _return_list.filter(
                games_id__user_id__profile__date_joined__gte=date_start).count()
            tickets_total = tickets_old + tickets_new

            if tickets_total > 0:
                tickets_new_percent = round((tickets_new / tickets_total) * 100, 2)
                tickets_old_percent = round((tickets_old / tickets_total) * 100, 2)
            else:
                tickets_new_percent = 0
                tickets_old_percent = 0

            users_old = _return_list.filter(
                games_id__user_id__profile__date_joined__lt=date_start).values_list("games_id__user_id",
                                                                                                 flat=True).distinct().count()
            users_new = _return_list.filter(
                games_id__user_id__profile__date_joined__range=[date_start, date_end]).values_list(
                "games_id__user_id", flat=True).distinct().count()
            users_total = users_new + users_old

            if users_total > 0:
                users_new_percent = round((users_new / users_total) * 100, 2)
                users_old_percent = round((users_new / users_total) * 100, 2)
            else:
                users_new_percent = 0
                users_old_percent = 0

            return_list.append([tickets_total,
                                users_total,
                                users_new,
                                users_new_percent,
                                tickets_new,
                                tickets_new_percent,
                                users_old,
                                users_old_percent,
                                tickets_old,
                                tickets_old_percent,
                                ])

        add(m_zvit_date_start_db, m_zvit_date_finish_db)
        add(m_zvit_date_2_start_db, m_zvit_date_2_finish_db)

    elif verbal == "Rep_24":
        if "daterange" not in dict(request.GET).keys():
            m_zvit_date_start_db = m_zvit_date_start_db.replace(day=1)
            return_args["date_range"] = "{} - {}".format(m_zvit_date_start_db.strftime("%d.%m.%y"),
                                                         m_zvit_date_finish_db.strftime("%d.%m.%y"))

        users_tickets_by_types = Ticket_history.objects.filter(
            req_dt__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()]).values(
            'games_id__user_id__email', 'games_id__user_id__profile__name', 'games_id__user_id__profile__mobile',
            'game_type__caption').distinct().annotate(
            games=Count('games_id', distinct=True),
            tickets=Count('id'),
            money=Coalesce(Sum('cost_2', output_field=IntegerField()), 0)
        ).order_by('games_id__user_id__email')

        distinct_users = list(users_tickets_by_types.values_list('games_id__user_id__email', flat=True))
        users_tickets_by_types = list(users_tickets_by_types)

        return_list = []
        for user in distinct_users:
            vals = [j for j in users_tickets_by_types if j['games_id__user_id__email'] == user]
            user_name = vals[0]['games_id__user_id__profile__name']
            user_email = vals[0]['games_id__user_id__email']
            user_phone = vals[0]['games_id__user_id__profile__mobile']
            if len(vals) == 1:
                sum_ticks = max_ticks = vals[0]['tickets']
                sum_games = max_games = vals[0]['games']
                sum_money = max_money = vals[0]['money']
                max_caption = vals[0]['game_type__caption']
                perc_ticks = perc_games = perc_money = 100
            else:
                sum_ticks = sum([val['tickets'] for val in vals])
                max_ticks = max([val['tickets'] for val in vals])
                sum_games = sum([val['games'] for val in vals])
                max_games = max([val['games'] for val in vals])
                max_caption = [val['game_type__caption'] for val in vals if val['tickets'] == max_ticks][0]
                perc_games = round((max_games / sum_games) * 100, 2)
                perc_ticks = round((max_ticks / sum_ticks) * 100, 2)
                sum_money = sum([val['money'] for val in vals])
                max_money = max([val['money'] for val in vals])
                perc_money = round((max_money / sum_money) * 100, 2)
            return_list.append({
                'user_name': user_name, 'user_email': user_email, 'user_phone': user_phone,
                'sum_games': sum_games, 'sum_ticks': sum_ticks, 'max_caption': max_caption,
                'max_games': max_games, 'max_ticks': max_ticks, 'perc_games': perc_games, 'perc_ticks': perc_ticks,
                'sum_money': sum_money, 'max_money': max_money, 'perc_money': perc_money
            })
            return_list = sorted(return_list, key=lambda d: (d['max_caption'], d['max_money']), reverse=True)

    elif verbal == "Rep_25":
        return_list = []
        _return_list = SubsSmsToSend.objects.filter(
            dt_plan__range=[m_zvit_date_start_db, m_zvit_date_finish_db]).order_by('-dt_plan')
        for ItemStr in _return_list:
            rep_item = {"id": ItemStr.id, "t_subs": ItemStr.t_subs,
                        "t_task": ItemStr.t_task, "t_game": ItemStr.t_game,
                        "t_status": ItemStr.t_status, "recipient": ItemStr.recipient,
                        "hash": ItemStr.hash, "html_message": ItemStr.html_message,
                        "request": ItemStr.request, "answer": ItemStr.answer,
                        "dt_add": ItemStr.dt_add,
                        "dt_plan": ItemStr.dt_plan}
            if ItemStr.dt_start is not None:
                rep_item["dt_start"] = ItemStr.dt_start
            if ItemStr.dt_stop is not None:
                rep_item["dt_stop"] = ItemStr.dt_stop
            if ItemStr.answer != '':
                if 'SUCCESS' not in ItemStr.answer:
                    rep_item['answer_wrong'] = True
            # print(type(rep_item["dt_add"]), rep_item["dt_add"])
            return_list.append(rep_item)

    elif verbal == "Rep_26":
        return_list = []
        _return_list = Subscription.objects.filter(
            (Q(dt_start__range=[m_zvit_date_start_db, m_zvit_date_finish_db]) | Q(dt_start__lt=m_zvit_date_start_db) &
             (Q(dt_stop__range=[m_zvit_date_start_db, m_zvit_date_finish_db]) | Q(dt_stop__gt=m_zvit_date_finish_db))
             ))
        now_date = datetime.datetime.now().date()
        _list_dates = []
        delta = m_zvit_date_finish_db - m_zvit_date_start_db
        if delta.days > 0:
            for i in range(delta.days):
                i_date = m_zvit_date_start_db + timedelta(i)
                week_day = i_date.isoweekday()
                israel_weekday = week_day + 1 if week_day in range(1, 7) else 1
                _list_dates.append((i_date.date(), f'day_{israel_weekday}'))

        for ItemStr in _return_list:
            rep_item = {"id": ItemStr.id, "user_id": ItemStr.user_id,
                        "day_1": ItemStr.day_1, "day_2": ItemStr.day_2,
                        "day_3": ItemStr.day_3, "day_4": ItemStr.day_4,
                        "day_5": ItemStr.day_5, "day_6": ItemStr.day_6,
                        "day_7": ItemStr.day_7,
                        "dt_start": ItemStr.dt_start.date(),
                        "dt_stop": ItemStr.dt_stop.date(),
                        "dates_sms": {}
                        }
            for dt in _list_dates:
                if rep_item['dt_start'] <= dt[0] <= rep_item['dt_stop']:
                    if rep_item[dt[1]]:
                        if dt[0] > now_date:
                            rep_item['dates_sms'][dt[0]] = ['Sms should be, but the date has not yet arrived']
                        else:
                            sms = SubsSmsToSend.objects.filter(t_subs_id=rep_item['id'], dt_plan__date=dt[0])
                            if sms.exists():
                                if 'SUCCESS' in sms[0].answer:
                                    rep_item['dates_sms'][dt[0]] = [sms[0], 'success']
                                else:
                                    if sms[0].answer == '' and not sms[0].dt_stop:
                                        rep_item['dates_sms'][dt[0]] = [sms[0], 'wait']
                                    else:
                                        rep_item['dates_sms'][dt[0]] = [sms[0], 'bad']
                            else:
                                rep_item['dates_sms'][dt[0]] = ['Sms should be, BUT ITS NOT!', 'bad']
                    else:
                        rep_item['dates_sms'][dt[0]] = ['Sms should not be']
                else:
                    rep_item['dates_sms'][dt[0]] = ['Sms should not be, subscription is not active']
            return_list.append(rep_item)

    elif verbal == "Rep_27":
        now_date = datetime.datetime.now().date()
        return_list = []
        _return_list = Subscription.objects.all().order_by('-id')
        tickets_list = Ticket_type.objects.values_list('caption', flat=True)
        tickets_counter = {caption: 0 for caption in tickets_list}
        for t_sub in _return_list:
            t_sub_info = subs_get_full_info(t_sub.id)
            if t_sub_info:
                if t_sub_info['dt_stop'].date() <= now_date and t_sub_info['deb_cred'] == 0:
                    t_sub_info["status"] = 'ok'
                if t_sub_info['dt_stop'].date() <= now_date and t_sub_info['deb_cred'] != 0:
                    t_sub_info["status"] = 'not_ok'
                # добавить в tickets_counter кол-во билeтов, которые нужно иметь в наличии
                if t_sub_info['all_ticket_left'] > 0:
                    tickets_counter[t_sub.ticket_list['caption']] += t_sub_info['all_ticket_left']
                return_list.append(t_sub_info)
        return_args['tickets_counter'] = tickets_counter

    elif verbal == 'Rep_28':
        return_list = []
        dates = []
        delta = m_zvit_date_finish_db - m_zvit_date_start_db
        if delta.days > 0:
            for i in range(delta.days):
                dates.append(m_zvit_date_start_db + timedelta(i))
            for date in dates:
                tickets_without_subs = 0
                tickets_without_subs_money = 0
                tickets_without_subs_profit = 0
                subs_money = 0
                subs_profit = 0
                users = list(Profile.objects.filter(date_joined__date=date.date()).values_list('user_id', flat=True))
                if len(users) > 0:
                    # tickets = Ticket_history.objects.filter(games_id__user_id__in=users, games_id__t_subs__isnull=True)
                    tickets = Ticket_history.objects.filter(games_id__user_id__in=users)
                    tickets_without_subs += tickets.count()
                    for ticket in tickets:
                        tickets_without_subs_money += ticket.cost_2
                        tickets_without_subs_profit += (ticket.cost_2 - ticket.cost_1)
                # subs = Subscription.objects.filter(user_id__in=users)
                # for sub in subs:
                #     subs_money += sub.paid_amount
                #     sub_ticket_type = sub.ticket_list.get('type')
                #     t_type = Ticket_type.objects.get(verbal=sub_ticket_type)
                #     ticket_profit = t_type.cost_2 - t_type.cost_1
                #     subs_profit += ticket_profit * int(sub.ticket_list.get('tickets_amount'))

                str_date = datetime.datetime.strftime(date, "%d.%m.%Y")
                rep_item = {
                    'date': str_date, 'users_count': len(users), 'tickets_without_subs': tickets_without_subs,
                    'tickets_without_subs_money': tickets_without_subs_money,
                    'tickets_without_subs_profit': tickets_without_subs_profit}
                # rep_item = {
                #     'date': str_date, 'users_count': len(users), 'tickets_without_subs': tickets_without_subs,
                #     'tickets_without_subs_money': tickets_without_subs_money,
                #     'tickets_without_subs_profit': tickets_without_subs_profit,
                #     'subs_money': subs_money, 'subs_profit': subs_profit, 'subs_count': len(subs)
                # }
                return_list.append(rep_item)

        return_args['total_users_count'] = sum([i['users_count'] for i in return_list])
        return_args['total_tickets_without_subs'] = sum([i['tickets_without_subs'] for i in return_list])
        return_args['total_tickets_without_subs_money'] = sum([i['tickets_without_subs_money'] for i in return_list])
        return_args['total_tickets_without_subs_profit'] = sum([i['tickets_without_subs_profit'] for i in return_list])

    elif verbal == 'Rep_29':
        return_list = []
        subs_list = Subscription.objects.filter(
            Q(dt_start__lte=m_zvit_date_finish_db) & Q(dt_stop__gte=m_zvit_date_start_db)
        ).values_list('user_id', flat=True)
        user_ids_with_subs = set(subs_list)
        for user in user_ids_with_subs:
            user_obj = User.objects.get(id=user)
            rep_item = {'email': user_obj.email, 'mobile': user_obj.profile.mobile, 'name': user_obj.profile.name}
            tickets_list = Ticket_history.objects.filter(games_id__user_id=user,
                                                         req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db])
            user_subs = []
            subs_tickets = 0
            money_subs = 0
            profit_subs = 0
            not_sub_tickets = 0
            money_without_sub = 0
            profit_without_sub = 0

            for ticket in tickets_list:
                if ticket.games_id.t_subs:
                    subs_tickets += 1
                    # user_subs.append(ticket.games_id.t_subs)
                    money_subs += ticket.cost_2
                    profit_subs += (ticket.cost_2 - ticket.cost_1)
                else:
                    not_sub_tickets += 1
                    money_without_sub += ticket.cost_2
                    profit_without_sub += (ticket.cost_2 - ticket.cost_1)

            unique_subs = set(user_subs)
            left_subs_tickets = 0
            # for sub in unique_subs:
            #     money_subs += sub.paid_amount
            #     count_tickets = sub.ticket_list.get('tickets_amount')
            #     left_subs_tickets += int(count_tickets)
            #     sub_ticket_type = sub.ticket_list.get('type')
            #     t_type = Ticket_type.objects.get(verbal=sub_ticket_type)
            #     ticket_profit = t_type.cost_2 - t_type.cost_1
            #     profit_subs += ticket_profit * int(sub.ticket_list.get('tickets_amount'))
            # left_subs_tickets -= subs_tickets

            rep_item['subs_tickets'] = subs_tickets
            if subs_tickets == 0:
                continue
            rep_item['left_subs_tickets'] = left_subs_tickets
            rep_item['subs_money'] = money_subs
            rep_item['subs_profit'] = profit_subs

            rep_item['not_sub_tickets'] = not_sub_tickets
            rep_item['money_without_sub'] = money_without_sub
            rep_item['profit_without_sub'] = profit_without_sub

            rep_item['all_tickets'] = not_sub_tickets + subs_tickets
            rep_item['all_money'] = money_without_sub + money_subs
            rep_item['all_profit'] = profit_without_sub + profit_subs
            return_list.append(rep_item)
        return_list = sorted(return_list, key=lambda d: d['email'])
        total = {'total': True, 'users_count': 0, 'subs_tickets': 0, 'left_subs_tickets': 0, 'subs_money': 0,
                 'subs_profit': 0, 'not_sub_tickets': 0, 'money_without_sub': 0, 'profit_without_sub': 0,
                 'all_tickets': 0, 'all_money': 0, 'all_profit': 0}
        for i in return_list:
            total['users_count'] += 1
            for key, value in i.items():
                if key not in ['email', 'mobile', 'name']:
                    total[key] += value
        return_list.append(total)

    elif verbal == 'Rep_30':
        m_zvit_date_2_finish_db = m_zvit_date_2_finish_db + relativedelta(days=-1, hour=0, minute=0, second=0,
                                                                          microsecond=0)
        return_list = []
        bloggers_list = Blogger.objects.all().order_by('-id')
        blogger_types = BloggerType.objects.values_list('verbal', flat=True)
        totals = {i: {'users': 0, 'tickets': 0, 'amount': 0} for i in blogger_types}
        print(totals, '\n')
        for blogger in bloggers_list:
            rep_item = {'id': blogger.id, 'name': blogger.name, 'phone': blogger.phone,
                        'accounts': blogger.accounts, 'ref_hash': blogger.ref_hash,
                        'ref_link': blogger.ref_link}
            blogger_users = Profile.objects.filter(settings__ref_blogger_id=blogger.id).filter(
                date_joined__range=[m_zvit_date_start_db, m_zvit_date_finish_db]).annotate(
                num_tickets=Count('user__game_user__games_id_history',
                                  filter=Q(user__game_user__games_id_history__req_dt__date__range=[
                                      m_zvit_date_2_start_db.date(), m_zvit_date_2_finish_db.date()])),
                sum_amount=Coalesce(Sum('user__game_user__games_id_history__cost_2',
                                        filter=Q(user__game_user__games_id_history__req_dt__date__range=[
                                            m_zvit_date_2_start_db.date(), m_zvit_date_2_finish_db.date()])),
                                    0, output_field=DecimalField()))
            count_users = blogger_users.count()
            count_tickets = sum([i.num_tickets for i in blogger_users])
            sum_amount = sum([i.sum_amount for i in blogger_users])
            rep_item['count_tickets'] = count_tickets
            rep_item['sum_amount'] = sum_amount
            rep_item['users'] = blogger_users
            rep_item['count_users'] = count_users
            blogger_type = blogger.b_type.verbal
            totals[blogger_type]['users'] += rep_item['count_users']
            totals[blogger_type]['tickets'] += rep_item['count_tickets']
            totals[blogger_type]['amount'] += rep_item['sum_amount']
            if count_users > 0:
                return_list.append(rep_item)

        return_args['totals'] = totals

    elif verbal == 'Rep_31':
        m_find_only_paid = request.GET.get('onlypaid', '0')
        return_args['only_paid'] = True if m_find_only_paid == '1' else False
        return_list = []
        profile__list = Profile.objects.filter(date_joined__range=[m_zvit_date_start_db, m_zvit_date_finish_db],
                                               i_confirmed=False).annotate(balance_opers=Count('user__balance_user')
                                                                           ).filter(balance_opers__gt=0
                                                                                    ).order_by('-date_joined')
        for user in profile__list:
            rep_item = {'user': user}
            bal_operations = BalanceOperation.objects.filter(user_id=user.user)
            if m_find_only_paid == '1':
                bal_operations = bal_operations.filter(status__caption='block')
            if len(bal_operations) > 0:
                rep_item['bal_opers'] = bal_operations
                id_confirm = IdConfirmation.objects.filter(user=user.user).exists()
                if id_confirm:
                    rep_item['id_confirmation'] = IdConfirmation.objects.filter(user=user.user)[0]
                return_list.append(rep_item)

    elif verbal == "Rep_32":
        return_list = []
        if (not request.GET and not add_api) or (
                add_api and (add_api.get('daterange_1') == '' or add_api.get('daterange_2') == '')):
            m_zvit_date_start_db = m_zvit_date_start_db + relativedelta(day=1, hour=0, minute=0, second=0,
                                                                        microsecond=0)
            m_zvit_date_finish_db = datetime.datetime.now() + relativedelta(hour=23, minute=59, second=59,
                                                                            microsecond=0)
            m_zvit_date_2_start_db = m_zvit_date_start_db - relativedelta(months=1)
            m_zvit_date_2_finish_db = m_zvit_date_finish_db - relativedelta(months=1)

            m_zvit_date_start_txt = datetime.datetime.strftime(m_zvit_date_start_db, "%d.%m.%Y")
            m_zvit_date_finish_txt = datetime.datetime.strftime(m_zvit_date_finish_db, "%d.%m.%Y")
            return_args['date_range'] = f'{m_zvit_date_start_txt} - {m_zvit_date_finish_txt}'

            m_zvit_date_2_start_txt = datetime.datetime.strftime(m_zvit_date_2_start_db, "%d.%m.%Y")
            m_zvit_date_2_finish_txt = datetime.datetime.strftime(m_zvit_date_2_finish_db, "%d.%m.%Y")
            return_args['date_range_2'] = f'{m_zvit_date_2_start_txt} - {m_zvit_date_2_finish_txt}'

            return_args['date_finish_txt'] = m_zvit_date_finish_txt
            return_args['date_finish_2_txt'] = m_zvit_date_2_finish_txt
        elif ('daterange' in request.GET and 'daterange_2' in request.GET) or \
                (add_api and ('daterange_1' in add_api and 'daterange_2' in add_api)):
            m_zvit_date_finish_db = m_zvit_date_finish_db + relativedelta(days=-1, hour=23, minute=59, second=59)
            m_zvit_date_2_finish_db = m_zvit_date_2_finish_db + relativedelta(days=-1, hour=23, minute=59, second=59)

        month_list_1 = Ticket_history.objects.filter(req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db]
                                                     ).aggregate(amount=Coalesce(Sum('cost_2'), 0, output_field=DecimalField()),
                                                                 users=Count('games_id__user_id', distinct=True))
        day_list_1 = Ticket_history.objects.filter(req_dt__date=m_zvit_date_finish_db.date()
                                                   ).aggregate(amount=Coalesce(Sum('cost_2'), 0, output_field=DecimalField()),
                                                               users=Count('games_id__user_id', distinct=True))

        month_list_2 = Ticket_history.objects.filter(req_dt__range=[m_zvit_date_2_start_db, m_zvit_date_2_finish_db]
                                                     ).aggregate(amount=Coalesce(Sum('cost_2'), 0, output_field=DecimalField()),
                                                                 users=Count('games_id__user_id', distinct=True))
        day_list_2 = Ticket_history.objects.filter(req_dt__date=m_zvit_date_2_finish_db.date()
                                                   ).aggregate(amount=Coalesce(Sum('cost_2'), 0, output_field=DecimalField()),
                                                               users=Count('games_id__user_id', distinct=True))

        if month_list_1['amount'] < month_list_2['amount']:
            month_list_1['amount_lower'] = True
        elif month_list_1['amount'] > month_list_2['amount']:
            month_list_2['amount_lower'] = True

        if month_list_1['users'] < month_list_2['users']:
            month_list_1['users_lower'] = True
        elif month_list_1['users'] > month_list_2['users']:
            month_list_2['users_lower'] = True

        if day_list_1['amount'] < day_list_2['amount']:
            day_list_1['amount_lower'] = True
        elif day_list_1['amount'] > day_list_2['amount']:
            day_list_2['amount_lower'] = True

        if day_list_1['users'] < day_list_2['users']:
            day_list_1['users_lower'] = True
        elif day_list_1['users'] > day_list_2['users']:
            day_list_2['users_lower'] = True

        return_list.append({
            'month_list_1': month_list_1, 'month_list_2': month_list_2,
            'day_list_1': day_list_1, 'day_list_2': day_list_2
        })

    elif verbal == "Rep_33":
        return_list = []
        unique_user_id = Subscription.objects.values('user_id').distinct().annotate(
            active=(Count('id', filter=Q(enabled=True))), non_active=(Count('id', filter=Q(enabled=False))))
        for user in unique_user_id:
            if user['active'] == 0:
                user_subs = Subscription.objects.filter(user_id__id=user['user_id']).order_by('id')
                rep_item = {
                    'user': user_subs[0].user_id, 'subs': user_subs
                }
                return_list.append(rep_item)

    elif verbal == "Rep_34":
        today = datetime.datetime.now()
        today_subt_ten = (today + relativedelta(days=-10)).date()
        today_add_five = (today + relativedelta(days=+5)).date()
        return_list = []
        subs_list = Subscription.objects.filter(dt_stop__date__range=[today_subt_ten, today_add_five])
        for sub in subs_list:
            rep_item = {
                'id': sub.id, 'user': sub.user_id,
                'dt_start': datetime.datetime.strftime(sub.dt_start + relativedelta(hours=+4), "%d.%m.%Y"),
                'dt_stop': datetime.datetime.strftime(sub.dt_stop + relativedelta(hours=+4), "%d.%m.%Y"),
                'ticket': sub.ticket_list, 'paid': sub.paid_amount, 'another_subs': []
            }
            user_all_subs = Subscription.objects.filter(user_id=sub.user_id)
            if user_all_subs.count() > 1:
                for sub2 in user_all_subs:
                    if sub2.id > sub.id and sub2 not in subs_list:
                        rep_item['another_subs'].append({
                            'id': sub2.id,
                            'dt_start': datetime.datetime.strftime(sub2.dt_start + relativedelta(hours=+4), "%d.%m.%Y"),
                            'dt_stop': datetime.datetime.strftime(sub2.dt_stop + relativedelta(hours=+4), "%d.%m.%Y"),
                            'ticket': sub2.ticket_list, 'paid': sub2.paid_amount
                        })
            sub_autopays = SubsAutoPay.objects.filter(p_subs=sub).order_by('-dt_start')
            if sub_autopays.count() > 0:
                last_autopay = sub_autopays[0]
                success = 'Error 'if not last_autopay.p_status else 'Success'
                rep_item['last_autopay'] = {'date': datetime.datetime.strftime(
                    last_autopay.dt_start + relativedelta(hours=+4), "%d.%m.%Y"),
                    'success': success}
            return_list.append(rep_item)
        return_list = sorted(return_list, key=lambda d: datetime.datetime.strptime(d['dt_stop'], "%d.%m.%Y"))

    elif verbal == "Rep_35":
        users_1_period = Ticket_history.objects.filter(
            req_dt__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()]
        ).values_list('games_id__user_id', flat=True).distinct()
        users_2_period = Ticket_history.objects.filter(
            req_dt__date__range=[m_zvit_date_2_start_db.date(), m_zvit_date_2_finish_db.date()]
        ).values_list('games_id__user_id', flat=True).distinct()
        intersection = set(users_1_period) & set(users_2_period)

        return_list = Ticket_history.objects.filter(games_id__user_id__in=intersection).values(
            'games_id__user_id_id__email',
            'games_id__user_id_id__profile__name',
            'games_id__user_id_id__profile__mobile').distinct().annotate(
            tickets_1=(
                Count('id', filter=Q(req_dt__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()]))),
            tickets_2=(Count('id', filter=Q(
                req_dt__date__range=[m_zvit_date_2_start_db.date(), m_zvit_date_2_finish_db.date()]))),
            amount_1=(Sum('cost_2',
                          filter=Q(req_dt__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()]))),
            amount_2=(Sum('cost_2', filter=Q(
                req_dt__date__range=[m_zvit_date_2_start_db.date(), m_zvit_date_2_finish_db.date()]))),
            games_1=(Count('games_id',
                           filter=Q(req_dt__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()]))),
            games_2=(Count('games_id', filter=Q(
                req_dt__date__range=[m_zvit_date_2_start_db.date(), m_zvit_date_2_finish_db.date()]))),
            tickets_perc=Case(
                When(tickets_1__gt=0, then=F('tickets_2') * 1.0 / F('tickets_1') * 100 - 100),
                default=None,
                output_field=FloatField()
            ),
            games_perc=Case(
                When(games_1__gt=0, then=F('games_2') * 1.0 / F('games_1') * 100 - 100),
                default=None,
                output_field=FloatField()
            ),
            amount_perc=Case(
                When(amount_1__gt=0, then=F('amount_2') * 1.0 / F('amount_1') * 100 - 100),
                default=None,
                output_field=FloatField()
            )
        ).order_by('-amount_2')

        total = return_list.aggregate(Count('games_id__user_id_id__email'), Sum('games_1'), Sum('games_2'),
                                      Sum('tickets_1'), Sum('tickets_2'),
                                      Sum('amount_1'), Sum('amount_2'))
        total.update({'tickets_perc': (total['tickets_2__sum'] / total['tickets_1__sum'] * 100 - 100),
                      'games_perc': (total['games_2__sum'] / total['games_1__sum'] * 100 - 100),
                      'amount_perc': (total['amount_2__sum'] / total['amount_1__sum'] * 100 - 100)})
        return_args['total_values'] = total

    elif verbal == "Rep_36":
        m_zvit_date_finish_db = m_zvit_date_finish_db + relativedelta(days=-1)
        delta = relativedelta(m_zvit_date_start_db, m_zvit_date_finish_db)
        delta_month = abs(delta.months + (delta.years * 12))
        return_list = Ticket_history.objects.filter(
            req_dt__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()]).values(
            'games_id__user_id_id__email', 'games_id__user_id_id__profile__name',
            'games_id__user_id_id__profile__mobile',
            'games_id__user_id_id__profile__date_joined__date').distinct().annotate(
            month_count=Count(Func(F('req_dt'), Value('MM.yyyy'), function='to_char', output_field=CharField()),
                              distinct=True),
            days_count=Count('req_dt__date', distinct=True),
            tickets_count=Count('id'),
            amount_sum=Sum('cost_2'),
            avg_days=Case(
                When(month_count__gt=0, then=F('days_count') * 1.0 / F('month_count')),
                default=None,
                output_field=FloatField()
            ),
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
        ).order_by('-month_count', '-days_count')
        for item in return_list:
            if item['games_id__user_id_id__profile__date_joined__date'] < m_zvit_date_start_db.date():
                delta = relativedelta(m_zvit_date_start_db, m_zvit_date_finish_db)
            elif item['games_id__user_id_id__profile__date_joined__date'] > m_zvit_date_start_db.date():
                delta = relativedelta(item['games_id__user_id_id__profile__date_joined__date'], m_zvit_date_finish_db)
            delta_month = abs(delta.months + (delta.years * 12))
            if abs(delta.days) > 0:
                delta_month += 1
            if delta_month == 0:
                delta_month = 1
            month_percent = (item['month_count'] / delta_month) * 100
            item['month_percent'] = month_percent

    elif verbal == "Rep_37":
        tasks = Task_history.objects.filter(
            dt_stop__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()], t_type__verbal='sms').values_list(
            'id', flat=True)
        users_list = SmsToSend.objects.filter(t_task__id__in=tasks).values(
            'user_id', 'user_id__email', 'user_id__profile__name', 'user_id__profile__mobile', 'dt_stop'
        ).annotate(
            dt_stop_add_6=ExpressionWrapper(F('dt_stop') + timedelta(hours=6), output_field=DateTimeField()),
            games_count=Count('user_id__game_user__games_id_history__games_id', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')]),
                              distinct=True),
            tickets_count=Count('user_id__game_user__games_id_history', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')])),
            amount_cost_2=Coalesce(Sum('user_id__game_user__games_id_history__cost_2', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')])), 0, output_field=DecimalField()),
            amount_cost_1=Coalesce(Sum('user_id__game_user__games_id_history__cost_1', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')])), 0, output_field=DecimalField()),
            profit=F('amount_cost_2') - F('amount_cost_1')
        ).order_by('id')

        total_dict = {}
        for item in users_list:
            key = item['user_id__email']
            if key not in total_dict:
                total_dict[key] = {
                    'name': item['user_id__profile__name'],
                    'mobile': item['user_id__profile__mobile'],
                    'sms': 1,
                    'games': item['games_count'],
                    'tickets': item['tickets_count'],
                    'amount': item['amount_cost_2'],
                    'profit': item['profit'],
                }
            else:
                total_dict[key]['sms'] += 1
                total_dict[key]['games'] += item['games_count']
                total_dict[key]['tickets'] += item['tickets_count']
                total_dict[key]['amount'] += item['amount_cost_2']
                total_dict[key]['profit'] += item['profit']

        return_list = dict(sorted(total_dict.items(), key=lambda x: x[1]['games'], reverse=True))

    elif verbal == "Rep_38":
        tasks = Task_history.objects.filter(
            dt_stop__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()]).values_list(
            'id', flat=True)
        users_list = SmsToSend.objects.filter(t_task__id__in=tasks).values(
            't_task__id', 'user_id', 'user_id__email', 'user_id__profile__name', 'user_id__profile__mobile', 'dt_stop'
        ).annotate(
            dt_stop_add_6=ExpressionWrapper(F('dt_stop') + timedelta(hours=6), output_field=DateTimeField()),
            games_count=Count('user_id__game_user__games_id_history__games_id', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')]),
                              distinct=True),
            tickets_count=Count('user_id__game_user__games_id_history', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')])),
            amount_cost_2=Coalesce(Sum('user_id__game_user__games_id_history__cost_2', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')])), 0, output_field=DecimalField()),
            amount_cost_1=Coalesce(Sum('user_id__game_user__games_id_history__cost_1', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')])), 0, output_field=DecimalField()),
            profit=F('amount_cost_2') - F('amount_cost_1')
        ).exclude(games_count=0).order_by('-t_task__id')

        total_dict = {}
        for item in users_list:
            key = item['t_task__id']
            if key not in total_dict:
                total_dict[key] = {
                    'games': item['games_count'],
                    'tickets': item['tickets_count'],
                    'amount': item['amount_cost_2'],
                    'profit': item['profit'],
                }
            else:
                total_dict[key]['games'] += item['games_count']
                total_dict[key]['tickets'] += item['tickets_count']
                total_dict[key]['amount'] += item['amount_cost_2']
                total_dict[key]['profit'] += item['profit']
        for task in total_dict:
            task_info = Task_history.objects.filter(id=task).values(
                'task_num_ok', 'dt_start', 'dt_stop', 'task_text', 't_type__caption')[
                0]
            total_dict[task]['sms'] = task_info['task_num_ok']
            total_dict[task]['task_text'] = task_info['task_text']
            total_dict[task]['dt_start'] = task_info['dt_start']
            total_dict[task]['dt_stop'] = task_info['dt_stop']
            total_dict[task]['t_type'] = task_info['t_type__caption']
        return_list = total_dict

    elif verbal == "Rep_39":
        return_list = []
        totals = {'manager': 'TOTAL', 'total': True, 'total_subs': 0, 'total_bonus': 0, 'total_money': 0}
        manager_list = SubsManager.objects.filter(enabled=True)
        for manager in manager_list:
            manager_dict = {'manager': manager.name}
            manager_subs_list = list(Subscription.objects.filter(
                manager=manager,
                dt_add__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()]).values(
                'user_id__email', 'user_id__profile__name', 'user_id__profile__mobile',
                'ticket_list__caption', 'ticket_list__tickets_amount', 'paid_amount', 'type_payment__caption',
                'dt_start', 'dt_stop', 'bonus'
            ))
            manager_dict['subs_list'] = manager_subs_list
            if len(manager_subs_list) > 0:
                return_list.append(manager_dict)
            manager_total_subs = len(manager_subs_list)
            manager_total_bonus = sum([i['bonus'] for i in manager_subs_list if i['bonus']])
            manager_total_money = sum([i['paid_amount'] for i in manager_subs_list if i['paid_amount']])
            return_list.append({'manager': f'{manager.name} total', 'total': True,
                                'total_subs': manager_total_subs, 'total_bonus': manager_total_bonus,
                                'total_money': manager_total_money
                                })
            totals['total_subs'] += manager_total_subs
            totals['total_bonus'] += manager_total_bonus
            totals['total_money'] += manager_total_money
        return_list.append(totals)
    elif verbal == "Rep_40":
        gifts = Ticket_history.objects.filter(
            games_id__dt_add__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()],
            games_id__ticket_list__gift=True).values(
            'games_id_id', 'games_id__user_id__email', 'games_id__user_id__profile__name',
            'games_id__user_id__profile__mobile', 'games_id__dt_add', 'games_id__ticket_list',
            'game_type__caption', 'games_id__t_payment__caption', 'games_id__user_recipient__email',
            'games_id__user_recipient__profile__name', 'games_id__user_recipient__profile__mobile').annotate(
            tickets_count=Count('id'),
            money=Coalesce(Sum('cost_2'), 0, output_field=DecimalField()),
            tickets_played=Count('id', filter=Q(status="33")),
            tickets_not_played=Count('id', filter=~Q(status="33")),
        ).order_by('-games_id__dt_add')
        return_list = gifts
    elif verbal == "Rep_41":
        gifts = list(Ticket_history.objects.filter(
            games_id__dt_add__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()],
            games_id__ticket_list__gift=True).values(
            'games_id_id', 'games_id__user_id__email', 'games_id__user_id__profile__name',
            'games_id__user_id__profile__mobile', 'games_id__dt_add', 'games_id__ticket_list',
            'game_type__caption', 'games_id__t_payment__caption', 'games_id__user_recipient__email',
            'games_id__user_recipient__profile__name', 'games_id__user_recipient__profile__mobile').annotate(
            tickets_count=Count('id'),
            money=Coalesce(Sum('cost_2'), 0, output_field=DecimalField()),
            tickets_played=Count('id', filter=Q(status="33")),
            tickets_not_played=Count('id', filter=~Q(status="33")),
        ).order_by('-games_id__dt_add'))

        unique_senders = set([(i['games_id__user_id__email'], i['games_id__user_id__profile__name'],
                               i['games_id__user_id__profile__mobile']) for i in gifts])
        for sender in unique_senders:
            sender_amount = sum([i['money'] for i in gifts if i['games_id__user_id__email'] == sender[0]])
            sender_tickets_count = sum(
                [i['tickets_count'] for i in gifts if i['games_id__user_id__email'] == sender[0]])
            sender_games_count = len([i['games_id_id'] for i in gifts if i['games_id__user_id__email'] == sender[0]])
            gifts.append({'games_id__user_id__email': sender[0], 'games_id__user_id__profile__name': sender[1],
                          'games_id__user_id__profile__mobile': sender[2],
                          'total': True, 'sender_amount': sender_amount, 'sender_tickets_count': sender_tickets_count,
                          'sender_games_count': sender_games_count})

        gifts = sorted(gifts, key=lambda d: (d['games_id__user_id__email']), reverse=True)
        return_list = gifts
    elif verbal == "Rep_42":
        percent_udachi = return_args.get("GL_Udachi_Profit", 0)
        if type(percent_udachi) == int or percent_udachi.isdigit():
            percent_udachi = int(percent_udachi)
        else:
            percent_udachi = 0
        percent_scratch = 100 - percent_udachi
        return_list = []
        x = []
        delta = m_zvit_date_finish_db - m_zvit_date_start_db
        if delta.days > 0:
            for i in range(delta.days):
                x.append((m_zvit_date_start_db + timedelta(i)).date())
            for date in x:
                str_date = datetime.datetime.strftime(date, "%d.%m.%Y")
                total_user_registered = Profile.objects.filter(date_joined__date=date).count()
                total_money_info = Ticket_history.objects.filter(req_dt__date=date).aggregate(
                    money_cost2=Coalesce(Sum('cost_2'), 0, output_field=DecimalField()),
                    money_cost1=Coalesce(Sum('cost_1'), 0, output_field=DecimalField()),
                )
                total_registered = Ticket_history.objects.filter(
                    req_dt__date=date, games_id__user_id_id__profile__date_joined__date=date).aggregate(
                        money_cost2=Coalesce(Sum('cost_2'), 0, output_field=DecimalField()),
                        users_count=Count('games_id__user_id_id', distinct=True)
                )
                total_users_money_old = Ticket_history.objects.filter(
                    req_dt__date=date, games_id__user_id_id__profile__date_joined__date__lt=date).aggregate(
                        money_cost2=Coalesce(Sum('cost_2'), 0, output_field=DecimalField())
                )
                total_users_money_not_blogger = Ticket_history.objects.filter(
                    req_dt__date=date,
                    games_id__user_id_id__profile__settings__ref_blogger_id__isnull=True
                    ).aggregate(
                        money_cost2=Coalesce(Sum('cost_2'), 0, output_field=DecimalField())
                )
                fb_bloggers = list(Blogger.objects.filter(b_type__verbal='facebook').values_list('id', flat=True))
                total_users_money_fb = Ticket_history.objects.filter(
                    req_dt__date=date, games_id__user_id_id__profile__settings__ref_blogger_id__in=fb_bloggers,
                    ).aggregate(
                        money_cost2=Coalesce(Sum('cost_2'), 0, output_field=DecimalField())
                )
                outbrain_bloggers = list(Blogger.objects.filter(b_type__verbal='outbrain').values_list('id', flat=True))
                total_users_money_outbrain = Ticket_history.objects.filter(
                    req_dt__date=date,
                    games_id__user_id_id__profile__settings__ref_blogger_id__in=outbrain_bloggers,
                ).aggregate(
                    money_cost2=Coalesce(Sum('cost_2'), 0, output_field=DecimalField())
                )
                total_profit = round((total_money_info['money_cost2'] - total_money_info['money_cost1']) / 100 * percent_scratch, 1)
                rep_item = {'date': str_date, 'total_money': total_money_info['money_cost2'],
                            'total_profit': total_profit,
                            'total_user_registered': total_user_registered,
                            'total_users_play_registered': total_registered['users_count'],
                            'total_users_money_registered': total_registered['money_cost2'],
                            'total_users_money_old': total_users_money_old['money_cost2'],
                            'total_users_money_fb': total_users_money_fb['money_cost2'],
                            'total_users_money_outbrain': total_users_money_outbrain['money_cost2'],
                            'total_users_money_not_blogger': total_users_money_not_blogger['money_cost2']}
                return_list.append(rep_item)
        totals = {'date': 'TOTAL', 'total': True,
                  'total_money': sum([i['total_money'] for i in return_list]),
                  'total_profit': round(sum([i['total_profit'] for i in return_list]), 1),
                  'total_user_registered': sum([i['total_user_registered'] for i in return_list]),
                  'total_users_play_registered': sum([i['total_users_play_registered'] for i in return_list]),
                  'total_users_money_registered': sum([i['total_users_money_registered'] for i in return_list]),
                  'total_users_money_old': sum([i['total_users_money_old'] for i in return_list]),
                  'total_users_money_fb': sum([i['total_users_money_fb'] for i in return_list]),
                  'total_users_money_outbrain': sum([i['total_users_money_outbrain'] for i in return_list]),
                  'total_users_money_not_blogger': sum([i['total_users_money_not_blogger'] for i in return_list]),
                  }
        return_list.append(totals)
    elif verbal == 'Rep_43':
        subs_list = Subscription.objects.filter(
            enabled=True, u_paycard__isnull=True).order_by('user_id')
        return_list = subs_list
    elif verbal == 'Rep_44':
        one_day_before = (m_zvit_date_start_db + relativedelta(days=-1)).date()
        return_list = []
        subs_list = Subscription.objects.filter(dt_stop__date=one_day_before)
        for sub in subs_list:
            t_sub_info = subs_get_full_info(sub.id)
            if t_sub_info and t_sub_info['deb_cred'] != 0:
                continue
            else:
                user_all_subs = Subscription.objects.filter(user_id=sub.user_id, enabled=True)
                if user_all_subs.count() > 1:
                    for sub2 in user_all_subs:
                        t_sub_info2 = subs_get_full_info(sub2.id)
                        if t_sub_info2 and t_sub_info2['deb_cred'] != 0:
                            continue
                        else:
                            return_list.append(sub)
                else:
                    return_list.append(sub)
    elif verbal == "Rep_45":
        total_dict_sms = {}
        sms_tasks = Task_history.objects.filter(
            dt_stop__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()], t_type__verbal='sms').values_list(
            'id', flat=True)
        sms_users_list = SmsToSend.objects.filter(t_task__id__in=sms_tasks).values(
            'user_id', 'user_id__email', 'user_id__profile__name', 'user_id__profile__mobile', 'dt_stop'
        ).annotate(
            dt_stop_add_6=ExpressionWrapper(F('dt_stop') + timedelta(hours=6), output_field=DateTimeField()),
            games_count=Count('user_id__game_user__games_id_history__games_id', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')]),
                              distinct=True),
            tickets_count=Count('user_id__game_user__games_id_history', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')])),
            amount_cost_2=Coalesce(Sum('user_id__game_user__games_id_history__cost_2', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')])), 0, output_field=DecimalField()),
            amount_cost_1=Coalesce(Sum('user_id__game_user__games_id_history__cost_1', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')])), 0, output_field=DecimalField()),
            profit=F('amount_cost_2') - F('amount_cost_1')
        ).order_by('id')

        for item in sms_users_list:
            key = item['user_id__email']
            if key not in total_dict_sms:
                total_dict_sms[key] = {
                    'name': item['user_id__profile__name'],
                    'mobile': item['user_id__profile__mobile'],
                    'sms': 1,
                    'games': item['games_count'],
                    'tickets': item['tickets_count'],
                    'amount': item['amount_cost_2'],
                    'profit': item['profit'],
                    'sms_wa': 0,
                    'games_wa': 0,
                    'tickets_wa': 0,
                    'amount_wa': 0,
                    'profit_wa': 0,

                }
            else:
                total_dict_sms[key]['sms'] += 1
                total_dict_sms[key]['games'] += item['games_count']
                total_dict_sms[key]['tickets'] += item['tickets_count']
                total_dict_sms[key]['amount'] += item['amount_cost_2']
                total_dict_sms[key]['profit'] += item['profit']

        total_dict_whatsapp = {}
        whatsapp_tasks = Task_history.objects.filter(
            dt_stop__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()],
            t_type__verbal='whatsapp').values_list(
            'id', flat=True)
        whatsapp_users_list = SmsToSend.objects.filter(t_task__id__in=whatsapp_tasks).values(
            'user_id', 'user_id__email', 'user_id__profile__name', 'user_id__profile__mobile', 'dt_stop'
        ).annotate(
            dt_stop_add_6=ExpressionWrapper(F('dt_stop') + timedelta(hours=6), output_field=DateTimeField()),
            games_count=Count('user_id__game_user__games_id_history__games_id', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')]),
                              distinct=True),
            tickets_count=Count('user_id__game_user__games_id_history', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')])),
            amount_cost_2=Coalesce(Sum('user_id__game_user__games_id_history__cost_2', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')])), 0, output_field=DecimalField()),
            amount_cost_1=Coalesce(Sum('user_id__game_user__games_id_history__cost_1', filter=Q(
                user_id__game_user__games_id_history__req_dt__range=[F('dt_stop'), F('dt_stop_add_6')])), 0, output_field=DecimalField()),
            profit=F('amount_cost_2') - F('amount_cost_1')
        ).order_by('id')

        for item in whatsapp_users_list:
            key = item['user_id__email']
            if key not in total_dict_whatsapp:
                total_dict_whatsapp[key] = {
                    'name': item['user_id__profile__name'],
                    'mobile': item['user_id__profile__mobile'],
                    'sms_wa': 1,
                    'games_wa': item['games_count'],
                    'tickets_wa': item['tickets_count'],
                    'amount_wa': item['amount_cost_2'],
                    'profit_wa': item['profit'],
                    'sms': 0,
                    'games': 0,
                    'tickets': 0,
                    'amount': 0,
                    'profit': 0,
                }
            else:
                total_dict_whatsapp[key]['sms_wa'] += 1
                total_dict_whatsapp[key]['games_wa'] += item['games_count']
                total_dict_whatsapp[key]['tickets_wa'] += item['tickets_count']
                total_dict_whatsapp[key]['amount_wa'] += item['amount_cost_2']
                total_dict_whatsapp[key]['profit_wa'] += item['profit']
        for key, val in total_dict_whatsapp.items():
            if key in total_dict_sms:
                total_dict_sms[key]['sms_wa'] = val['sms_wa']
                total_dict_sms[key]['games_wa'] = val['games_wa']
                total_dict_sms[key]['tickets_wa'] = val['tickets_wa']
                total_dict_sms[key]['amount_wa'] = val['amount_wa']
                total_dict_sms[key]['profit_wa'] = val['profit_wa']
            else:
                total_dict_sms.update({key: val})
        return_list = dict(sorted(total_dict_sms.items(), key=lambda x: (x[1]['games'], x[1]['games_wa']), reverse=True))
    elif verbal == "Rep_46":
        users_list = BalanceOperation.objects.filter(
            confirm__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()],
            type_balanceoperation__verbal='credit_card', status__verbal='04').values_list('user_id', flat=True)
        return_list = []
        for user in set(users_list):
            user_ccno = set()  # Уникальные номера карт
            user_list = []
            user_balops = BalanceOperation.objects.filter(
                confirm__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()],
                type_balanceoperation__verbal='credit_card', status__verbal='04', user_id_id=user).order_by('confirm')
            user_profile = Profile.objects.get(user_id=user)
            for balop in user_balops:
                balop_dict = {'id': balop.id, 'date': balop.confirm, 'amount': balop.amount}
                pay_response = balop.pay_response
                try:
                    ccno_start = pay_response.find("'ccno")
                    ccno_json = json.loads('{' + pay_response[ccno_start: ccno_start+16].replace("'", '"') + '}')
                    if ccno_json.get('ccno'):
                        user_ccno.add(ccno_json['ccno'][0])
                        balop_dict['ccno'] = ccno_json['ccno'][0]
                except Exception:
                    continue
                user_list.append(balop_dict)
            if len(user_ccno) > 1:
                return_list.append({'user': user_profile, 'balops': user_list})
    elif verbal == "Rep_47":
        winning_tickets_list = Ticket_history.objects.filter(
            req_dt__date__range=[m_zvit_date_start_db.date(), m_zvit_date_finish_db.date()],
            answ_win=True
        ).values('games_id__user_id__email', 'games_id__user_id__profile__name', 'games_id__user_id__profile__mobile',
                 'id', 'answ_nom', 'game_type__caption', 'answ_win_sum', 'req_dt'
                 ).order_by('games_id__user_id__email', '-req_dt')
        return_list = {}
        for ticket in winning_tickets_list:
            email = ticket['games_id__user_id__email']
            name = ticket['games_id__user_id__profile__name']
            mobile = ticket['games_id__user_id__profile__mobile']
            ticket_dict = {'ticket_id': ticket['id'], 'ticket_number': ticket['answ_nom'], 'date': ticket['req_dt'],
                           'game_type': ticket['game_type__caption'], 'win_sum': ticket['answ_win_sum']}
            if email not in return_list:
                return_list[email] = {'name': name, 'mobile': mobile, 'tickets': [ticket_dict]}
            else:
                return_list[email]['tickets'].append(ticket_dict)
        for key, value in return_list.items():
            if len(value['tickets']) > 1:
                return_list[key]['tickets'].append({
                    'ticket_id': 'Total', 'ticket_number': len(value['tickets']),
                    'win_sum': sum([decimal.Decimal(t['win_sum']) for t in value['tickets']])})
    elif verbal == "Rep_48":
        return_list = []
        dates = []
        delta = m_zvit_date_finish_db - m_zvit_date_start_db
        if delta.days > 0:
            for i in range(delta.days):
                dates.append(m_zvit_date_start_db + timedelta(i))
            for date in dates:
                profiles = Profile.objects.filter(date_birthday__day=date.day, date_birthday__month=date.month)
                for profile in profiles:
                    rep_item = {'date': datetime.datetime.strftime(date, "%d.%m"),
                                'date_birthday': datetime.datetime.strftime(profile.date_birthday, "%d.%m.%Y"),
                                'email': profile.user.email, 'name': profile.name, 'mobile': profile.mobile}
                    return_list.append(rep_item)
    elif verbal == "Rep_49":
        print("Rep_49")
        print(request.POST)
        m_local_tz = 'Israel'
        ## полный период - текущий месяц
        return_list = []

        m_date_check = datetime.datetime.now()
        m_date_check = m_date_check + relativedelta(days=+1, hour=0, minute=0, second=0, microsecond=0)

        if m_zvit_date_finish_db > m_date_check:
            m_zvit_date_finish_db = m_date_check

        m_zvit_date_start_txt = m_zvit_date_start_db
        m_zvit_date_finish_txt = m_zvit_date_finish_db + relativedelta(days=-1, hour=0, minute=0, second=0,
                                                                       microsecond=0)

        return_args['date_rep_start_txt'] = datetime.datetime.strftime(m_zvit_date_start_txt, "%d.%m.%Y")
        return_args['date_rep_finish_txt'] = datetime.datetime.strftime(m_zvit_date_finish_txt, "%d.%m.%Y")
        return_args['date_rep_range'] = '{} - {}'.format(return_args['date_rep_start_txt'],
                                                         return_args['date_rep_finish_txt'])

        print("dates in request = ", m_zvit_date_start_db, m_zvit_date_finish_db)
        _return_list = Ticket_history.objects.filter(
            req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db],
            games_id__game_type__verbal__in=['game_lotto', 'game_lotto_gift']
        ).order_by("game_type", "-req_dt")

        try:
            m_procent_udachi = return_args.get("GL_Udachi_Profit", 0)
            m_procent_udachi = decimal.Decimal(m_procent_udachi)
        except:
            m_procent_udachi = 100

        print("len(_return_list) = ", len(_return_list))
        print(_return_list)
        if len(_return_list) > 0:
            rep_total = {}
            rep_total["type_line"] = "total_report"
            rep_total["type_group"] = gettext("TOTAL")
            rep_total["type_group_code"] = ""
            rep_total["count_ticket"] = 0
            rep_total["count_ticket_goverment"] = 0
            rep_total["count_ticket_cancelled"] = 0
            rep_total["count_ticket_test"] = 0
            rep_total["cost_1"] = ""
            rep_total["cost_2"] = ""
            rep_total["sum_cost_1"] = 0
            rep_total["sum_cost_2"] = 0
            rep_total["profit_ticket"] = 0
            rep_total["profit_all"] = 0
            rep_total["profit_udachi"] = 0
            rep_total["profit_extcomp"] = 0
            rep_total["profit_average"] = 0
            rep_total["win_count"] = 0
            rep_total["win_sum"] = 0

            rep_group = {}
            rep_group["type_line"] = "total_group"
            rep_group["type_group"] = gettext(_return_list[0].game_type.caption)
            rep_group["type_group_code"] = _return_list[0].game_type.verbal
            rep_group["count_ticket"] = 0
            rep_group["count_ticket_goverment"] = 0
            rep_group["count_ticket_cancelled"] = 0
            rep_group["count_ticket_test"] = 0
            rep_group["cost_1"] = _return_list[0].cost_1
            rep_group["cost_2"] = _return_list[0].cost_2
            rep_group["sum_cost_1"] = 0
            rep_group["sum_cost_2"] = 0
            rep_group["profit_ticket"] = rep_group["cost_2"] - rep_group["cost_1"]
            rep_group["profit_all"] = 0
            rep_group["profit_udachi"] = 0
            rep_group["profit_extcomp"] = 0
            rep_group["profit_average"] = 0
            rep_group["win_count"] = 0
            rep_group["win_sum"] = 0

            for ItemStr in _return_list:
                if rep_group["type_group_code"] != ItemStr.game_type.verbal:
                    return_list.append(rep_group)
                    rep_group = {}
                    rep_group["type_line"] = "total_group"
                    rep_group["type_group"] = gettext(ItemStr.game_type.caption)
                    rep_group["type_group_code"] = gettext(ItemStr.game_type.verbal)
                    rep_group["count_ticket"] = 0
                    rep_group["count_ticket_goverment"] = 0
                    rep_group["count_ticket_cancelled"] = 0
                    rep_group["count_ticket_test"] = 0
                    rep_group["cost_1"] = ItemStr.cost_1
                    rep_group["cost_2"] = ItemStr.cost_2
                    rep_group["sum_cost_1"] = 0
                    rep_group["sum_cost_2"] = 0
                    rep_group["profit_ticket"] = rep_group["cost_2"] - rep_group["cost_1"]
                    rep_group["profit_all"] = 0
                    rep_group["profit_udachi"] = 0
                    rep_group["profit_extcomp"] = 0
                    rep_group["profit_average"] = 0
                    rep_group["win_count"] = 0
                    rep_group["win_sum"] = 0

                rep_item = {}
                rep_item["type_line"] = "item_str"
                rep_item["type_group"] = gettext(ItemStr.game_type.caption)
                rep_item["type_group_code"] = ItemStr.game_type.verbal
                rep_item["n_req"] = ItemStr.req_id
                try:
                    rep_item["d_req"] = datetime.datetime.strftime(ItemStr.req_dt.astimezone(tz.gettz(m_local_tz)),
                                                                   "%d.%m.%Y %H:%M:%S")
                except:
                    rep_item["d_req"] = ""
                try:
                    rep_item["d_answ"] = datetime.datetime.strftime(ItemStr.answ_dt.astimezone(tz.gettz(m_local_tz)),
                                                                    "%d.%m.%Y %H:%M:%S")
                except:
                    rep_item["d_answ"] = ""

                rep_item["number"] = ItemStr.answ_nom
                rep_item["win"] = ItemStr.answ_win
                try:
                    rep_item["win_sum"] = decimal.Decimal(ItemStr.answ_win_sum)
                except:
                    rep_item["win_sum"] = 0

                rep_item["game_last"] = -1
                #
                rep_item["cost_1"] = ItemStr.cost_1
                rep_item["cost_2"] = ItemStr.cost_2
                rep_item["sum_cost_1"] = ItemStr.cost_1
                rep_item["sum_cost_2"] = ItemStr.cost_2
                rep_item["profit_ticket"] = ItemStr.cost_2 - ItemStr.cost_1
                rep_item["profit_all"] = ItemStr.cost_2 - ItemStr.cost_1
                rep_item["profit_udachi"] = round(rep_item["profit_all"] * m_procent_udachi / 100, 2)
                rep_item["profit_extcomp"] = round(rep_item["profit_all"] - rep_item["profit_udachi"], 2)
                rep_item["profit_average"] = m_procent_udachi
                rep_item["win_count"] = 1 if ItemStr.answ_win else 0
                try:
                    rep_item["win_sum"] = decimal.Decimal(ItemStr.answ_win_sum)
                except:
                    rep_item["win_sum"] = 0
                #
                rep_group["count_ticket"] += 1
                rep_total["count_ticket"] += 1
                if ItemStr.games_id.t_status.verbal == 'test_game':
                    rep_group['count_ticket_test'] += 1
                    rep_total['count_ticket_test'] += 1
                elif ItemStr.games_id.t_status.verbal == 'lotto_cancelled':
                    rep_group['count_ticket_cancelled'] += 1
                    rep_total['count_ticket_cancelled'] += 1
                else:
                    rep_group['count_ticket_goverment'] += 1
                    rep_total['count_ticket_goverment'] += 1
                    rep_group["sum_cost_1"] += rep_item["sum_cost_1"]
                    rep_group["sum_cost_2"] += rep_item["sum_cost_2"]
                    rep_group["profit_all"] += rep_item["profit_all"]
                    rep_group["profit_udachi"] += rep_item["profit_udachi"]
                    rep_group["profit_extcomp"] += rep_item["profit_extcomp"]
                    rep_group["profit_average"] = 0
                    rep_group["win_count"] += rep_item["win_count"]
                    rep_group["win_sum"] += rep_item["win_sum"]

                    # rep_group["sum_cost_1"] += rep_item["sum_cost_1"]
                    # rep_group["sum_cost_2"] += rep_item["sum_cost_2"]
                    # rep_group["profit_ticket"] = 0



                    rep_total["sum_cost_1"] += rep_item["sum_cost_1"]
                    rep_total["sum_cost_2"] += rep_item["sum_cost_2"]
                    # rep_total["profit_ticket"] = 0
                    rep_total["profit_all"] += rep_item["profit_all"]
                    rep_total["profit_udachi"] += rep_item["profit_udachi"]
                    rep_total["profit_extcomp"] += rep_item["profit_extcomp"]
                    rep_total["profit_average"] = 0
                    rep_total["win_count"] += rep_item["win_count"]
                    rep_total["win_sum"] += rep_item["win_sum"]

                # return_list.append(rep_item)

            return_list.append(rep_group)
            return_list.append(rep_total)
        print('RETURN LIST', return_list)
        return_args['total_client_sum1'] = -rep_total["sum_cost_1"]
        return_args['total_client_sum2'] = -rep_total["sum_cost_2"]
        return_args['total_win_sum'] = rep_total["win_sum"]
        return_args['total_profit'] = rep_total["profit_all"]
        return_args['total_deposit'] = return_args.get("GL_Udachi_Deposit", 0)
        return_args['total_creditcard'] = return_args.get("GL_Udachi_CreditCard", 0)
        return_args['total_invoce'] = return_args['total_client_sum1'] \
                                      + return_args['total_win_sum'] \
                                      + int(return_args['total_deposit']) \
                                      + int(return_args['total_creditcard'])

        print("len(return_list) = ", len(return_list))

        return_args['return_list_month'] = return_list
        ## последний день
        print("last day")
        return_list = []
        m_zvit_date_start_db = m_zvit_date_finish_db + relativedelta(days=-1, hour=0, minute=0, second=0, microsecond=0)

        print("m_zvit_date_start_db  = ", m_zvit_date_start_db)
        print("m_zvit_date_finish_db = ", m_zvit_date_finish_db)

        return_args['date_rep_last_day'] = datetime.datetime.strftime(m_zvit_date_start_db, "%d.%m.%Y")

        _return_list = Ticket_history.objects.filter(
            req_dt__range=[m_zvit_date_start_db, m_zvit_date_finish_db],
            games_id__game_type__verbal__in=['game_lotto', 'game_lotto_gift']
        ).order_by("game_type", "-req_dt")

        print("22 len(_return_list) = ", len(_return_list))

        if len(_return_list) > 0:
            rep_total = {}
            rep_total["type_line"] = "total_report"
            rep_total["type_group"] = gettext("TOTAL")
            rep_total["type_group_code"] = ""
            rep_total["count_ticket"] = 0
            rep_total["count_ticket_goverment"] = 0
            rep_total["count_ticket_cancelled"] = 0
            rep_total["count_ticket_test"] = 0
            rep_total["cost_1"] = ""
            rep_total["cost_2"] = ""
            rep_total["sum_cost_1"] = 0
            rep_total["sum_cost_2"] = 0
            rep_total["profit_ticket"] = 0
            rep_total["profit_all"] = 0
            rep_total["profit_udachi"] = 0
            rep_total["profit_extcomp"] = 0
            rep_total["profit_average"] = 0
            rep_total["win_count"] = 0
            rep_total["win_sum"] = 0

            rep_group = {}
            rep_group["type_line"] = "total_group"
            rep_group["type_group"] = gettext(_return_list[0].game_type.caption)
            rep_group["type_group_code"] = gettext(_return_list[0].game_type.verbal)
            rep_group["count_ticket"] = 0
            rep_group["count_ticket_goverment"] = 0
            rep_group["count_ticket_cancelled"] = 0
            rep_group["count_ticket_test"] = 0
            rep_group["cost_1"] = _return_list[0].cost_1
            rep_group["cost_2"] = _return_list[0].cost_2
            rep_group["sum_cost_1"] = 0
            rep_group["sum_cost_2"] = 0
            rep_group["profit_ticket"] = rep_group["cost_2"] - rep_group["cost_1"]
            rep_group["profit_all"] = 0
            rep_group["profit_udachi"] = 0
            rep_group["profit_extcomp"] = 0
            rep_group["profit_average"] = 0
            rep_group["win_count"] = 0
            rep_group["win_sum"] = 0

            for ItemStr in _return_list:
                if rep_group["type_group_code"] != gettext(ItemStr.game_type.verbal):
                    return_list.append(rep_group)
                    rep_group = {}
                    rep_group["type_line"] = "total_group"
                    rep_group["type_group"] = gettext(ItemStr.game_type.caption)
                    rep_group["type_group_code"] = gettext(ItemStr.game_type.verbal)
                    rep_group["count_ticket"] = 0
                    rep_group["count_ticket_goverment"] = 0
                    rep_group["count_ticket_cancelled"] = 0
                    rep_group["count_ticket_test"] = 0
                    rep_group["cost_1"] = ItemStr.cost_1
                    rep_group["cost_2"] = ItemStr.cost_2
                    rep_group["sum_cost_1"] = 0
                    rep_group["sum_cost_2"] = 0
                    rep_group["profit_ticket"] = rep_group["cost_2"] - rep_group["cost_1"]
                    rep_group["profit_all"] = 0
                    rep_group["profit_udachi"] = 0
                    rep_group["profit_extcomp"] = 0
                    rep_group["profit_average"] = 0
                    rep_group["win_count"] = 0
                    rep_group["win_sum"] = 0

                rep_item = {}
                rep_item["type_line"] = "item_str"
                rep_item["type_group"] = gettext(ItemStr.game_type.caption)
                rep_item["n_req"] = ItemStr.req_id
                try:
                    rep_item["d_req"] = datetime.datetime.strftime(ItemStr.req_dt.astimezone(tz.gettz(m_local_tz)),
                                                                   "%d.%m.%Y %H:%M:%S")
                except:
                    rep_item["d_req"] = ""
                try:
                    rep_item["d_answ"] = datetime.datetime.strftime(ItemStr.answ_dt.astimezone(tz.gettz(m_local_tz)),
                                                                    "%d.%m.%Y %H:%M:%S")
                except:
                    rep_item["d_answ"] = ""

                rep_item["number"] = ItemStr.answ_nom
                rep_item["win"] = ItemStr.answ_win
                try:
                    rep_item["win_sum"] = decimal.Decimal(ItemStr.answ_win_sum)
                except:
                    rep_item["win_sum"] = 0

                rep_item["game_last"] = -1
                #
                rep_item["cost_1"] = ItemStr.cost_1
                rep_item["cost_2"] = ItemStr.cost_2
                rep_item["sum_cost_1"] = ItemStr.cost_1
                rep_item["sum_cost_2"] = ItemStr.cost_2
                rep_item["profit_ticket"] = ItemStr.cost_2 - ItemStr.cost_1
                rep_item["profit_all"] = ItemStr.cost_2 - ItemStr.cost_1
                rep_item["profit_udachi"] = round(rep_item["profit_all"] * m_procent_udachi / 100, 2)
                rep_item["profit_extcomp"] = round(rep_item["profit_all"] - rep_item["profit_udachi"], 2)
                rep_item["profit_average"] = 0
                rep_item["win_count"] = 1 if ItemStr.answ_win else 0
                try:
                    rep_item["win_sum"] = decimal.Decimal(ItemStr.answ_win_sum)
                except:
                    rep_item["win_sum"] = 0
                #
                rep_group["count_ticket"] += 1
                rep_total["count_ticket"] += 1
                if ItemStr.games_id.t_status.verbal == 'test_game':
                    rep_group['count_ticket_test'] += 1
                    rep_total['count_ticket_test'] += 1
                elif ItemStr.games_id.t_status.verbal == 'lotto_cancelled':
                    rep_group['count_ticket_cancelled'] += 1
                    rep_total['count_ticket_cancelled'] += 1
                else:
                    rep_group['count_ticket_goverment'] += 1
                    rep_total['count_ticket_goverment'] += 1

                    rep_group["sum_cost_1"] += rep_item["sum_cost_1"]
                    rep_group["sum_cost_2"] += rep_item["sum_cost_2"]
                    # rep_group["profit_ticket"] = 0
                    rep_group["profit_all"] += rep_item["profit_all"]
                    rep_group["profit_udachi"] += rep_item["profit_udachi"]
                    rep_group["profit_extcomp"] += rep_item["profit_extcomp"]
                    rep_group["profit_average"] = 0
                    rep_group["win_count"] += rep_item["win_count"]
                    rep_group["win_sum"] += rep_item["win_sum"]


                    rep_total["sum_cost_1"] += rep_item["sum_cost_1"]
                    rep_total["sum_cost_2"] += rep_item["sum_cost_2"]
                    # rep_total["profit_ticket"] = 0
                    rep_total["profit_all"] += rep_item["profit_all"]
                    rep_total["profit_udachi"] += rep_item["profit_udachi"]
                    rep_total["profit_extcomp"] += rep_item["profit_extcomp"]
                    rep_total["profit_average"] = 0
                    rep_total["win_count"] += rep_item["win_count"]
                    rep_total["win_sum"] += rep_item["win_sum"]

                return_list.append(rep_item)

            return_list.append(rep_group)
            return_list.append(rep_total)
        return_args['return_list_day'] = return_list
    elif verbal == "Rep_51":
        profile_list = Profile.objects.filter(date_joined__range=[m_zvit_date_start_db, m_zvit_date_finish_db]
                                              ).values('city').annotate(count=Count('id')).order_by('-count')
        total = {'city': 'Total', 'type': 'total', 'percent': 100,
                 'count': profile_list.aggregate(Sum('count'))['count__sum']}
        profile_list = list(profile_list)
        for item in profile_list:
            item['percent'] = round((item['count'] / total['count'] * 100), 2)
        profile_list.append(total)
        return_list = profile_list
    elif verbal == 'Rep_53':
        return_list = []
        now = timezone.now().date()
        day_ago = now - timedelta(days=1)
        lotto_types = TypeTicketType.objects.filter(verbal__in=['chance', '123', '777', 'lotto'])
        for lotto_type in lotto_types:
            results = GameLottoResults.objects.filter(lotto_type=lotto_type, draw_date__date=day_ago)
            tickets = Ticket_history.objects.filter(lotto_result__in=results, answ_win=True).values('id').annotate(
                win_as_int=Case(When(answ_win_sum='', then=Value(0)),
                                When(answ_win_sum=None, then=Value(0)),
                                default=Cast('answ_win_sum', DecimalField(max_digits=15, decimal_places=2)),
                                output_field=DecimalField(max_digits=15, decimal_places=2)))
            if tickets.count() > 0:
                total_win_sum = tickets.aggregate(Sum('win_as_int'))['win_as_int__sum']
            else:
                total_win_sum = 0
            return_list.append({"type_ticket_type": lotto_type.caption, "tickets_count": tickets.count(), "win_sum": total_win_sum})
    elif verbal == 'Rep_54':
        print('here we are')
        print(m_zvit_date)
        return_list = []
        ticket_list = Ticket_history.objects.filter(t_cabala_dt__date=m_zvit_date)
        for ticket in ticket_list:
            lotto_result = ticket.lotto_result
            if lotto_result:
                lottery_date = ticket.lotto_result.draw_date
                lottery_date = datetime.datetime.strftime(lottery_date, "%d.%m.%Y %H:%M")
            else:
                lottery_date = ''
            status = ticket.status
            if status != '33':
                win_sum = 'unknown'
            else:
                if ticket.answ_win_sum and ticket.answ_win_sum != '' :
                    win_sum = float(ticket.answ_win_sum)
                else:
                    win_sum = 0
            return_list.append({
                'ticket_type': ticket.game_type.caption,
                'lottomatic_number': ticket.answ_nom,
                'lottery_number': ticket.answ_lottery_number,
                'lottery_date': lottery_date,
                'ticket_cost': float(ticket.cost_1),
                'win_sum': win_sum,
                'ticket_id': ticket.id
            })
        print(return_list)
    elif verbal == 'Rep_55':
        return_list = []
        subs_list = Subscription.objects.filter(dt_stop__range=[m_zvit_date_start_db, m_zvit_date_finish_db])
        for sub in subs_list:
            str_start = datetime.datetime.strftime(sub.dt_start, "%d.%m.%Y")
            str_stop = datetime.datetime.strftime(sub.dt_stop, "%d.%m.%Y")
            total_period = f'{str_start} - {str_stop}'
            sub_tickets = Ticket_history.objects.filter(games_id__t_subs__id=sub.id)
            sub_tickets_count = sub_tickets.count()
            sub_tickets_win = sub_tickets.annotate(win_as_int=Case(
                When(answ_win_sum='', then=Value(0)),
                When(answ_win_sum=None, then=Value(0)),
                default=Cast('answ_win_sum', DecimalField(max_digits=15, decimal_places=2)),
                output_field=DecimalField(max_digits=15, decimal_places=2))).aggregate(Sum('win_as_int'))['win_as_int__sum']

            duration = int(sub.ticket_list.get("days_sub_works", 0))

            last_period_start = sub.dt_stop - relativedelta(days=duration)
            str_last_period_start = datetime.datetime.strftime(last_period_start, "%d.%m.%Y")
            last_period = f'{str_last_period_start} - {str_stop}'

            total_packages = 0
            if duration != 0:
                total_packages = round(sub_tickets_count / duration, 1)

            return_list.append(
                {'email': sub.user_id.email, 'name': sub.user_id.profile.name, 'mobile': sub.user_id.profile.mobile,
                 'finish_date': str_stop, 'last_period': last_period, 'total_period': total_period,
                 'total_packages': total_packages, 'total_money_sub': sub.paid_amount, 'duration': duration,
                 'total_win_sub': sub_tickets_win, 'id': sub.id, 'ticket_type': sub.ticket_list.get('caption'),
                 'type_payment': "" if sub.type_payment is None else sub.type_payment.caption
                 }
            )
    elif verbal == 'Rep_56':
        return_list = []


    return return_list, return_args
