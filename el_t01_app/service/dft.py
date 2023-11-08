#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import random
from django.db.models import Q
from el_t01_app.models import Documentation_list
from el_t01_app.models import Ticket_type
from el_t01_app.models import SiteLang
from el_t01_app.models import Report_list
from el_t01_app.models import Devices_list
from el_t01_app.models import List_external_company
from el_t01_app.models import SiteSkin
from el_t01_app.models import Game_history
from el_t01_app.models import Type_game_status
from el_t01_app.models import Type_payment
from el_t01_app.models import Globalset
from el_t01_app.models import Feedback
from el_t01_app.models import Payout
from el_t01_app.models import Payadd
from el_t01_app.models import Cashadd
from el_t01_app.models import Partner
from el_t01_app.models import Task_type
from el_t01_app.models import Type_balanceoperation
from el_t01_app.models import Type_blacklist
from el_t01_app.models import LayoutScript
from el_t01_app.models import NotificationSystem
from el_t01_app.models import TypeTicketType


def get_dict_payment_type():
    return Type_payment.objects.filter(enabled=True).order_by("order")


def get_dict_tickets_type():
    return Ticket_type.objects.filter(enabled=True, t_type__verbal='old').order_by("order")


def get_dict_tickets_type_lotto():
    return Ticket_type.objects.filter(enabled=True).exclude(t_type__verbal='old').order_by("order")


def get_dict_tickets_type_subs():
    return Ticket_type.objects.filter(enabled=True).order_by("subs_order")


def get_list_lotto_types():
    return TypeTicketType.objects.filter(enabled=True).exclude(verbal='old').order_by('order')


def get_dict_tickets_type_random():
    m_list_ticket = Ticket_type.objects.filter(enabled=True, t_type__verbal='old').order_by("order")
    m_list_random = list(m_list_ticket)
    m_list_random = random.sample(m_list_random, len(m_list_random))
    return m_list_random


def get_dict_documentation_list():
    return Documentation_list.objects.filter(enabled=True).order_by("order")


def get_site_lang():
    tabl_site_lang = SiteLang.objects.filter(enabled=True).order_by("order")
    return tabl_site_lang


def get_report_list():
    tabl_report_list = Report_list.objects.filter(enabled=True).order_by("order")
    return tabl_report_list


def get_devices_list():
    # tabl_devices_list = Devices_list.objects.filter(enabled=True).order_by("order")
    tabl_devices_list = Devices_list.objects.all().order_by("order")
    return tabl_devices_list


def get_game_verbal_list():
    t_ticket_type = Ticket_type.objects.filter(enabled=True).order_by("order")
    m_return = []
    for item in t_ticket_type:
        m_return.append(item.verbal)
    return m_return


def get_external_company_list():
    tabl_external_company_list = List_external_company.objects.filter(enabled=True).order_by("order")
    return tabl_external_company_list


def get_site_skin():
    t_skin = SiteSkin.objects.filter(enabled=True).order_by("order")
    if t_skin.count() > 0:
        m_skin = t_skin[0].code
    else:
        m_skin = "001"
    return m_skin


def get_dict_cart_games(l_user_id):
    tabl_game = Game_history.objects.filter(user_id_id=l_user_id).filter(Q(t_status=1) | Q(t_status=2)).order_by("-dt_add")
    return tabl_game


def get_dict_game_status():
    t_Type_game_status = Type_game_status.objects.filter(enabled=True).order_by("order")
    d_return = {}
    for ItemStatus in t_Type_game_status:
        d_return[ItemStatus.verbal] = ItemStatus.id
    return d_return


def get_dict_ticket_status():
    pass
#     class Type_payment(models.Model):
#         id = models.AutoField(primary_key=True)
#         order = models.IntegerField(default=0, verbose_name=u'Order')
#         caption = models.CharField(max_length=100, default='')
#         verbal = models.CharField(max_length=30, default='')
#         enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
#         is_active = models.BooleanField(default=True, verbose_name=u'Active')
#         max_win = models.IntegerField(default=0, verbose_name=u'Max win')
#         foto_1 = models.ImageField(upload_to='ticket/payment/', verbose_name=u'Logo')
#         description_01 = models.TextField(default='', blank=True)
#         description_02 = models.TextField(default='', blank=True)


def get_GlobalSettings_old():
    ReturnData = {}
    t_Globalset = Globalset.objects.all()
    for Item in t_Globalset:
        ReturnData[Item.code] = Item.value.strip()
    return ReturnData


def get_GlobalSettings():
    ReturnData = {}
    t_Globalset = Globalset.objects.all()
    for Item in t_Globalset:
        m_tmp_val = Item.value.strip()
        m_tmp_name = f"GL_{Item.code}"
        if Item.type == "int":
            try:
                m_tmp_val = int(m_tmp_val)
            except:
                m_tmp_val = 0
        elif Item.type == "bool":
            if m_tmp_val == "True":
                m_tmp_val = True
            else:
                m_tmp_val = False
        ReturnData[m_tmp_name] = m_tmp_val
    return ReturnData


def get_count_feed_new():
    m_return = Feedback.objects.filter(status="00").count()
    return m_return


def get_count_payout_new():
    m_return = Payout.objects.filter(status="00").count()
    return m_return


def get_count_payadd_new():
    m_return = Payadd.objects.filter(status="00").count()
    return m_return


def get_count_cashadd_new():
    m_return = Cashadd.objects.filter(status="00").count()
    return m_return


def get_dict_partner():
    m_return = Partner.objects.filter(enabled=True).order_by("order")
    return m_return


def get_dict_tasktype():
    m_return = Task_type.objects.filter(enabled=True).order_by("order")
    return m_return


def get_dict_type_balanceoperation():
    m_return = Type_balanceoperation.objects.filter(enabled=True).order_by("order")
    return m_return


def get_dict_blacklist_type():
    m_return = Type_blacklist.objects.filter(enabled=True).order_by("order")
    return m_return


def get_layout_scripts(file_loc, script_loc):
    m_return = LayoutScript.objects.filter(file_location=file_loc, script_location=script_loc,
                                           enabled=True).order_by("ordering")
    return m_return


def get_dict_notification_system():
    return NotificationSystem.objects.filter(enabled=True).order_by("order")
