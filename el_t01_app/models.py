#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField


class Type_payment(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    caption = models.CharField(max_length=100, default='')
    verbal = models.CharField(max_length=30, default='')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    is_active = models.BooleanField(default=True, verbose_name=u'Active')
    subs_enabled = models.BooleanField(default=False, verbose_name=u'Enabled for subscription')
    max_win = models.IntegerField(default=0, verbose_name=u'Max win')
    foto_1 = models.ImageField(upload_to='ticket/payment/', default='', blank=True, null=True, verbose_name=u'Logo')
    description_01 = models.TextField(default='', blank=True)
    description_02 = models.TextField(default='', blank=True)

    popup = models.BooleanField(default=False, verbose_name=u'Popup')
    txt_warning = models.CharField(max_length=1000, default='', blank=True, verbose_name=u'Popup message')
    link_redirect = models.CharField(max_length=100, default='', blank=True, verbose_name=u'Link action')

    def __str__(self):
        return self.caption


class UserPayCard(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE,
                                related_name="user_paycard",
                                verbose_name=u'User')
    dt_lastpay = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date last')
    tranzila_tk = models.CharField(max_length=100, null=False, blank=False)
    ccno = models.CharField(max_length=10, default='', blank=True)
    mask_card  = models.CharField(max_length=20, default='', blank=True)
    myid = models.CharField(max_length=20, default='', blank=True)
    expmonth = models.CharField(max_length=2, default='', blank=True)
    expyear = models.CharField(max_length=4, default='', blank=True)
    description = models.CharField(max_length=250, null=True, blank='True', verbose_name='Description')


class SubsManager(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name='Enabled')
    name = models.CharField(max_length=150, verbose_name='Name')
    description = models.TextField(default='', blank=True, verbose_name='Description')

    def __str__(self):
        return self.name


dict_subscription_creator = (
    ('00', 'Manager'),
    ('01', 'User')
)


class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE,
                                related_name="subs_user",
                                verbose_name=u'User subs')
    user_id_creator = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name="subs_user_creator",
                                        verbose_name=u'User subs creator')
    u_paycard = models.ForeignKey(UserPayCard, null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name="subs_paycard", verbose_name=u'Pay Card')

    creator = models.CharField(max_length=2, default='00', blank=True, null=True, choices=dict_subscription_creator,
                               verbose_name='Creator')
    dt_add = models.DateTimeField(auto_now_add=False, null=False, blank=False, verbose_name=u'Date ADD')
    dt_modified = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date modified')
    dt_start = models.DateTimeField(auto_now_add=False, null=False, blank=False, verbose_name=u'Date START')
    dt_stop = models.DateTimeField(auto_now_add=False, null=False, blank=False, verbose_name=u'Date STOP')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')

    ticket_list = JSONField(default=dict, null=True, blank=True, verbose_name=u'Ticket List')
    day_1 = models.BooleanField(default=False, verbose_name=u'San')
    day_2 = models.BooleanField(default=False, verbose_name=u'Mon')
    day_3 = models.BooleanField(default=False, verbose_name=u'Tue')
    day_4 = models.BooleanField(default=False, verbose_name=u'Wed')
    day_5 = models.BooleanField(default=False, verbose_name=u'Thu')
    day_6 = models.BooleanField(default=False, verbose_name=u'Fri')
    day_7 = models.BooleanField(default=False, verbose_name=u'Sat')

    time_1 = models.CharField(max_length=5, default='00.00', verbose_name=u'Time San')
    time_2 = models.CharField(max_length=5, default='00.00', verbose_name=u'Time Mon')
    time_3 = models.CharField(max_length=5, default='00.00', verbose_name=u'Time Tue')
    time_4 = models.CharField(max_length=5, default='00.00', verbose_name=u'Time Wed')
    time_5 = models.CharField(max_length=5, default='00.00', verbose_name=u'Time Thu')
    time_6 = models.CharField(max_length=5, default='00.00', verbose_name=u'Time Fri')
    time_7 = models.CharField(max_length=5, default='00.00', verbose_name=u'Time Sat')

    amount_subs = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Amount_subs')
    amount_add = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Amount_add')
    amount_total = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Amount_total')

    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Paid amount')
    paid_date = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Paid Date')
    auto_pay = models.BooleanField(default=False, verbose_name=u'Auto Payment')
    last_pay = models.BooleanField(default=True, verbose_name=u'Last Pay OK')
    auto_pay_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Auto Pay Amount')
    auto_pay_day = models.IntegerField(default=0, verbose_name=u'Auto Pay Day')

    total_tickets_amount = models.IntegerField(default=0, verbose_name=u'Total tickets amount')
    total_days_amount = models.IntegerField(default=0, verbose_name=u'Total days amount')
    description = models.TextField(default='', blank=True)

    manager = models.ForeignKey(SubsManager, null=True, blank=True, on_delete=models.PROTECT,
                                related_name="subs_manager", verbose_name=u'Manager')
    type_payment = models.ForeignKey(Type_payment, null=True, blank=True, on_delete=models.PROTECT,
                                     related_name="subs_type_payment", verbose_name=u'Payment type')
    bonus = models.FloatField(default=0, null=True, blank=True, verbose_name=u'Bonus')
    history = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return f"{self.id}-{self.user_id.email}"


class Task_subs_status(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    caption = models.CharField(max_length=100, default='')
    verbal = models.CharField(max_length=30, default='')
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.caption


class Task_subs(models.Model):
    id = models.AutoField(primary_key=True)
    t_status = models.ForeignKey(Task_subs_status, on_delete=models.PROTECT,
                                 related_name="t_task_subs_status", verbose_name=u'Status')
    dt_start = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date START')
    dt_stop = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date STOP')
    task_ok = models.TextField(default='', blank=True, verbose_name=u'Subs OK')
    task_error = models.TextField(default='', blank=True, verbose_name=u'Subs ERROR')
    task_ok_num = models.IntegerField(default=0, verbose_name=u'Count OK')
    task_error_num = models.IntegerField(default=0, verbose_name=u'Count ERROR')


class Type_balanceoperation(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    caption = models.CharField(max_length=100, default='')
    verbal = models.CharField(max_length=30, default='')
    verbal_payment = models.CharField(max_length=30, default='', blank=True)
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    max_win = models.IntegerField(default=0, verbose_name=u'Max win')
    for_balance = models.CharField(max_length=30, blank=True, default='') ## minus plus

    def __str__(self):
        return self.caption


class Type_balanceoperation_status(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    caption = models.CharField(max_length=100, default='', verbose_name=u'Caption')
    verbal = models.CharField(max_length=30, default='', verbose_name=u'Varbal')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')

    def __str__(self):
        return self.caption


class Type_game_status(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    caption = models.CharField(max_length=100, default='', verbose_name=u'Caption')
    verbal = models.CharField(max_length=30, default='', verbose_name=u'Varbal')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')

    def __str__(self):
        return self.caption


class Type_currency(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, blank=True, null=True, verbose_name=u'Очередность')
    code = models.CharField(max_length=10, default='')
    caption = models.CharField(max_length=100, default='')
    verbal = models.CharField(max_length=10, default='')
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.caption


dict_device_status = (
    ('00', 'READY'),
    ('01', 'BUSY'),
)


class Type_program(models.Model):
    id = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=100, default='')
    verbal = models.CharField(max_length=30, default='')
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.caption


class SiteLang(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, blank=True, null=True, verbose_name=u'Очередность')
    lang_name = models.CharField(max_length=100, default='', blank=True, null=True, verbose_name=u'Названия языка')
    lang_code = models.CharField(max_length=100, default='', blank=True, null=True, verbose_name=u'Код языка')
    enabled = models.BooleanField(default=True, verbose_name=u'Использовать')

    def __str__(self):
        return self.lang_name

    class Meta:
        ordering = ('order',)


class MessWhatsapp(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name='Enabled')
    verbal = models.CharField(max_length=50, unique=True, verbose_name='Verbal code')
    caption = models.CharField(max_length=100, blank=True, null=True, verbose_name='Caption')
    id_instance = models.CharField(max_length=150, verbose_name='ID Instance')
    api_token = models.TextField(verbose_name='API Token')
    api_url = models.CharField(max_length=250, verbose_name='API Url')
    max_users = models.IntegerField(default=0)


dict_user_confirmed = (
    ('00', 'Новый'),
    ('01', 'Подтвержден'),
    ('02', 'Заблокирован'),
)

dict_user_level = (
    ('00', 'Admin'),
    ('01', 'user'),
    ('02', 'user 2'),
    ('03', 'user 3'),
)


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, unique=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, default='')
    date_joined = models.DateTimeField(null=True)
    date_birthday = models.DateField(null=True, verbose_name=u'Birthday')
    user_confirmed = models.CharField(max_length=2, default='00', blank=True, null=True, choices=dict_user_confirmed,
                                      verbose_name=u'Статус пользователя')
    user_level = models.CharField(max_length=2, default='00', blank=True, null=True, choices=dict_user_level,
                                  verbose_name=u'Уровень пользователя')
    hash = models.CharField(max_length=128, default='', blank=True, null=True)
    mail_confirmed = models.BooleanField(default=False)

    mobile_code = models.CharField(max_length=10, default='', blank=True, null=True)
    mobile = models.CharField(max_length=500, default='', blank=True, null=True)
    mobile_confirmed = models.BooleanField(default=False)
    mail_subs = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    notifications = models.IntegerField(default=0)
    is_boss = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    first_login = models.BooleanField(default=True)
    i_doc = models.CharField(max_length=20, default='', blank=True, null=True, verbose_name=u'ID')
    i_foto = models.ImageField(upload_to='profile/img/', default='', blank=True, null=True, verbose_name=u'ID foto')
    i_photo_face = models.ImageField(upload_to='profile/img/', default='', blank=True, null=True,
                                     verbose_name='Photo face')
    i_confirmed = models.BooleanField(default=False, blank=True, null=True, verbose_name=u'ID confirmed')
    # adress
    city = models.CharField(max_length=150, default='', blank=True, null=True, verbose_name=u'City')
    street = models.CharField(max_length=150, default='', blank=True, null=True, verbose_name=u'Street')
    building = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name=u'Building')
    apartments = models.CharField(max_length=20, default='', blank=True, null=True, verbose_name=u'Apartments')
    #
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance_pre = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    language = models.CharField(max_length=50, default='', blank=True, null=True)
    #
    max_ticket_d = models.IntegerField(default=0)
    max_ticket_m = models.IntegerField(default=0)
    max_sum_d = models.IntegerField(default=0)
    max_sum_m = models.IntegerField(default=0)
    #
    tranzila_token = models.CharField(max_length=50, default='', blank=True, null=True)
    reklama = models.BooleanField(default=False, verbose_name=u'Reklama')
    # avatar = models.ImageField(upload_to='profile/img/', default='', blank=True, null=True,
    #                            verbose_name=u'Logo(Avatar)')
    # foto = models.ImageField(upload_to='profile/img/', default='', blank=True, null=True, verbose_name=u'Фото')
    # settings
    settings = JSONField(default=dict, null=True, blank=True)
    mess_whatsapp = models.ForeignKey(MessWhatsapp, null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name="mess_whatsapp_users", verbose_name='Mess whatsapp instance')
    phone_code = models.CharField(max_length=10, default='', blank=True, null=True)

    def __str__(self):
        return self.name


class TypeTicketType(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name='Enabled')
    in_play = models.BooleanField(default=True, verbose_name=u'in_play')
    verbal = models.CharField(max_length=30, default='', verbose_name='Verbal code')
    caption = models.CharField(max_length=100, default='', verbose_name='Caption')
    foto_1 = models.ImageField(upload_to='ticket/type_img/', default='', blank=True, null=True, verbose_name=u'Foto 1')
    foto_2 = models.ImageField(upload_to='ticket/type_img/', default='', blank=True, null=True, verbose_name=u'Foto 2')
    order = models.IntegerField(default=0, blank=True, null=True, verbose_name=u'Ordering')

    def __str__(self):
        return self.caption


def ticket_type_subs_settings_default():
    return {"subs_duration": [{"days": 15, "price": 0}, {"days": 30, "price": 0}]}


class Ticket_type(models.Model):
    id = models.AutoField(primary_key=True)
    t_type = models.ForeignKey(TypeTicketType, null=True, blank=True, on_delete=models.CASCADE,
                               related_name="type_ticket_type", verbose_name=u'Type')
    caption = models.CharField(max_length=100, default='')
    verbal = models.CharField(max_length=30, default='')
    verbal_jellyfish = models.CharField(max_length=30, default='')
    verbal_government = models.CharField(max_length=30, default='')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    in_play = models.BooleanField(default=True, verbose_name=u'in_play')
    order = models.IntegerField(default=0, verbose_name=u'Order')
    type_program = models.ForeignKey(Type_program, null=True, blank=True, on_delete=models.CASCADE,
                                 related_name="ticket_type_program", verbose_name=u'Version program')
    type_currency = models.ForeignKey(Type_currency, null=True, blank=True, on_delete=models.CASCADE,
                                 related_name="ticket_type_currency", verbose_name=u'currency')
    max_win = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Max win')
    foto_1 = models.ImageField(upload_to='ticket/img/', default='', blank=True, null=True, verbose_name=u'Foto 1')
    foto_2 = models.ImageField(upload_to='ticket/img/', default='', blank=True, null=True, verbose_name=u'Foto 2')
    cost_1 = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Cost 1')
    cost_2 = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Cost 2')
    approx_time = models.IntegerField(default=0, verbose_name=u'Approx time')
    description_01 = models.TextField(default='', blank=True)
    description_02 = models.TextField(default='', blank=True)
    description_03 = models.TextField(default='', blank=True)
    description_04 = models.TextField(default='', blank=True)
    description_05 = models.TextField(default='', blank=True)
    min_t = models.IntegerField(default=0, verbose_name=u'Min ticket')
    max_t = models.IntegerField(default=0, verbose_name=u'Max ticket')

    subs_enabled = models.BooleanField(default=True, verbose_name='Enabled for subscription')
    subs_order = models.IntegerField(default=0, verbose_name='Order in subscription list')
    subs_description = models.TextField(default='', blank=True, verbose_name='Description for subscription list')
    subs_setting = JSONField(default=ticket_type_subs_settings_default, verbose_name="Settings for subscription")
    setting = JSONField(default=dict, blank=True, null=True, verbose_name="Settings")

    def __str__(self):
        return self.caption


dict_profit_type = (
    ('00', 'Amount'),
    ('01', 'Percent'),
)


dict_profit_rounding = (
    ('00', 'Round off mathematically'),
    ('01', 'To the biggest integer'),
)


class GameLottoProfit(models.Model):
    id = models.AutoField(primary_key=True)
    ticket_type = models.ForeignKey(Ticket_type, null=True, blank=True, on_delete=models.CASCADE,
                                    related_name="ticket_type_profits", verbose_name=u'Type ticket')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    profit_type = models.CharField(max_length=2, default='', null=True, blank=True, verbose_name=u'Profit type',
                                   choices=dict_profit_type)
    profit_rounding = models.CharField(max_length=2, default='', null=True, blank=True, verbose_name=u'Profit rounding',
                                       choices=dict_profit_rounding)
    sum_from = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=u'From sum')
    sum_to = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=u'To sum')
    amount_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                        verbose_name=u'Amount profit')
    percent_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                         verbose_name=u'Percent profit')

    def __str__(self):
        return f'{self.ticket_type}: {self.sum_from}-{self.sum_to}'


class GameLottoResults(models.Model):
    id = models.AutoField(primary_key=True)
    lotto_type = models.ForeignKey(TypeTicketType, on_delete=models.CASCADE,
                                   related_name="type_ticket_type_results", verbose_name=u'Lotto Type')
    ticket_type = models.ForeignKey(Ticket_type, null=True, blank=True, on_delete=models.CASCADE,
                                    related_name="ticket_type_results", verbose_name=u'Type ticket')
    lottery_number = models.IntegerField(verbose_name='Lottery number')
    draw_date = models.DateTimeField(auto_now_add=False, verbose_name='Datetime of draw')
    result = JSONField(default=dict, verbose_name='Result')
    win_money = models.CharField(max_length=100, default='', verbose_name='Prize fund')

    def __str__(self):
        return f'{self.lotto_type} {self.draw_date}'


dict_type_run = (
    ('00', 'PRODUCT'),
    ('01', 'DEBUG'),
)


class Devices_list(models.Model):
    id = models.AutoField(primary_key=True)
    t_type = models.ForeignKey(Ticket_type, null=True, blank=True, on_delete=models.CASCADE, related_name="ticket_type",
                               verbose_name=u'Type ticket')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    verbal = models.CharField(max_length=20, default='', null=True, blank=True, unique=True, verbose_name=u'Code')
    caption = models.CharField(max_length=100, default='', null=True, blank=True, verbose_name=u'Caption')
    status = models.CharField(max_length=2, default='', null=True, blank=True, verbose_name=u'Status',
                              choices=dict_device_status)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    settings = JSONField(default=dict, null=True, blank=True)
    ipadres = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'Ip адрес')
    config_data = JSONField(default=dict, null=True, blank=True)
    api_token = models.CharField(max_length=100, default='', null=True, blank=True, verbose_name=u'Api Token')
    type_run = models.CharField(max_length=2, default='', null=True, blank=True, verbose_name=u'Режим работы',
                                choices=dict_type_run)
    step_knife = models.IntegerField(default=0, verbose_name=u'Шаг ножа')
    scratch = models.BooleanField(default=False, verbose_name=u'Scratch ticket')
    dmove = models.BooleanField(default=False, verbose_name=u'Move ticket')
    dmove_type = models.CharField(max_length=2, default='', null=True, blank=True, verbose_name=u'Move type')

    description = models.TextField(default='', blank=True)

    def __str__(self):
        return str(self.caption) if self.caption else ''

# 'Перечень документации '
class Documentation_list(models.Model):
    id = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=100, default='')
    verbal = models.CharField(max_length=20, default='')
    order = models.IntegerField(default=0)
    enabled = models.BooleanField(default=True, verbose_name=u'Использовать')
    file = models.FileField ( upload_to='doc/', default='', max_length=256, blank=True, null=True, verbose_name='Документ')
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.caption


# 'List external fish company'
dict_company_status = (
    ('00', 'Comp1'),
    ('01', 'Comp2'),
)
# 'List external mode'
dict_company_mode = (
    ('00', 'Test'),
    ('77', 'Prod'),
)

class List_external_company(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    verbal = models.CharField(max_length=40, default='', null=True, blank=True, verbose_name=u'Code')
    caption = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Caption')
    status = models.CharField(max_length=2, default='', null=True, blank=True, verbose_name=u'Status', choices=dict_company_status)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    api_token = models.CharField(max_length=100, default='', unique=True, verbose_name=u'Api Token')
    type_mode = models.CharField(max_length=2, default='00', null=True, blank=True, verbose_name=u'Type Mode', choices=dict_company_mode)
    game_start = models.BooleanField(default=False, verbose_name=u'Game Start')
    settings = JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return str(self.caption) if self.caption else ''


class List_jellyfish(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    verbal = models.CharField(max_length=40, default='', null=True, blank=True, unique=True, verbose_name=u'Code')
    caption = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Caption')
    order = models.IntegerField(default=0, verbose_name=u'Order')
    ipadres = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'Ip adres')
    api_token = models.CharField(max_length=100, default='', unique=True, verbose_name=u'Api Token')

    def __str__(self):
        return str(self.caption) if self.caption else ''

# Общий список СКИДОК
class Discount(models.Model):
    id = models.AutoField(primary_key=True)
    verbal = models.CharField(max_length=50, verbose_name='Verbal code')
    enabled = models.BooleanField(default=True, verbose_name='Enabled')
    caption = models.CharField(default="", max_length=100, verbose_name='Caption')
    caption_user = models.CharField(default="", max_length=100, verbose_name='Caption for user')
    start_date = models.DateTimeField(auto_now_add=False, verbose_name='Valid from')
    stop_date = models.DateTimeField(auto_now_add=False, verbose_name='Valid to')
    description = models.TextField(default='',null=True, blank=True, verbose_name='Description')

    def __str__(self):
        return f'{self.caption}'


# Настройка скидки - по какому билету какая величина скидки для каждой скидки
class DiscountSet(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name='Enabled')
    disc = models.ForeignKey(Discount, on_delete=models.PROTECT, null=True, blank=True,
                                    related_name='discount_set_discounts', verbose_name='Discount')
    ticket_type = models.ForeignKey(Ticket_type, on_delete=models.PROTECT, null=True, blank=True,
                                    related_name='discount_set_ticket_type', verbose_name='Ticket')
    discount_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Fixed discount')
    discount_percent = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Percentage discount')
    description = models.TextField(default='', null=True, blank=True, verbose_name='Description')


# Список от кого скидка - Менеджер , блогер , система-руководство
class DiscountOwner(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    caption = models.CharField(max_length=100, default='')
    verbal = models.CharField(max_length=30, default='')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')

    def __str__(self):
        return self.caption


# Список какая скидка для какого блогера или менеджера доступна
class DiscountList(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name='Enabled')
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT,
                                 related_name='discount_list', verbose_name='Discount type')
    owner = models.ForeignKey(DiscountOwner, null=False, blank=False, on_delete=models.PROTECT,
                                related_name="discount_owner",
                                verbose_name=u'Owner')
    id_owner = models.IntegerField(default=0, verbose_name='Id Owner')
    duration_hours = models.IntegerField(default=0, verbose_name='Duration in hours')

    def __str__(self):
        return f'{self.owner} {self.owner_id} - {self.discount}'

# Список пользователей кому назначена скидка
class DiscountHistory(models.Model):
    id = models.AutoField(primary_key=True)
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT,
                                 related_name='discount_history', verbose_name='Discount type')
    enabled = models.BooleanField(default=True, verbose_name='Enabled')
    all_users = models.BooleanField(default=True, verbose_name='Discount fo all users')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                             related_name="discount_user", verbose_name='Specific user')
    start_date = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name='Valid from')
    stop_date = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name='Valid to')
    description = models.TextField(default='', null=True, blank=True, verbose_name='Description')


dict_game_status = (
    ('00', 'add to cart'),
    ('01', 'wait payment'),
    ('02', 'start'),
    # ('03', 'step 3'),
    # ('04', 'step 4'),
    # ('05', 'step 5'),
    ('30', 'error'),
    ('33', 'finish'),
    ('99', 'deleted'),
)


class GameType(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    caption = models.CharField(max_length=100)
    verbal = models.CharField(max_length=30)

    def __str__(self):
        return self.caption


class LottoSubscription(models.Model):
    id = models.AutoField(primary_key=True)
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lotto_subscription_user',
                                   verbose_name='User owner')
    ticket_type = models.ForeignKey(Ticket_type,  on_delete=models.CASCADE,
                                    related_name='lotto_subscription_ticket_type', verbose_name='Ticket type')
    date_created = models.DateTimeField(auto_now_add=False, null=False, blank=False, verbose_name=u'Date created')
    date_paid = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date paid')
    enabled = models.BooleanField(default=False)
    games_count = models.IntegerField(default=0)
    infinity = models.BooleanField(default=False)
    automatic = models.BooleanField(default=False)
    ticket_info = models.JSONField(default=dict, blank=True, null=True)
    ticket_cost_1 = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u' Ticket Cost 1')
    ticket_cost_2 = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Ticket Cost 2')
    subscription_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Subscription cost')
    u_paycard = models.ForeignKey(UserPayCard, null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name="lotto_subs_paycard", verbose_name=u'Pay Card')

    def __str__(self):
        return f"{self.id}-{self.user_owner.email}"


class Game_history(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                related_name="game_user",
                                verbose_name=u'User')
    user_recipient = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name="game_user_recipient",
                                       verbose_name='User-recipient if gift')
    game_type = models.ForeignKey(GameType, null=True, blank=True, on_delete=models.PROTECT,
                                  related_name="game_game_type", verbose_name='Game type')
    t_status = models.ForeignKey(Type_game_status, default=1, on_delete=models.CASCADE,
                                 related_name="t_status", verbose_name=u'Status')
    t_company = models.ForeignKey(List_external_company, null=True, blank=True, on_delete=models.CASCADE,
                                  related_name="t_company", verbose_name=u'Company')
    t_payment = models.ForeignKey(Type_payment, null=True, blank=True, on_delete=models.CASCADE,
                                  related_name="t_payment", verbose_name=u'Payment')
    t_discount = models.ForeignKey(DiscountHistory, null=True, blank=True, on_delete=models.PROTECT,
                                   related_name="game_h_discount", verbose_name=u'Discount')
    ticket_ext = models.TextField(default='', blank=True, verbose_name=u'Ticket List ext')
    ticket_list = JSONField(default=dict, null=True, blank=True, verbose_name=u'Ticket List')
    ticket_num = models.IntegerField(default=0, verbose_name=u'Ticket number')
    ticket_sum = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Ticket sum')
    user_ip = models.CharField(max_length=20, default='', null=True, blank=True, verbose_name=u'Start Game Ip')
    dt_add = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date ADD')
    dt_start = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date START')
    dt_stop = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date STOP')
    t_subs = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.CASCADE,
                               related_name="t_subs", verbose_name=u'Subscription')
    history = models.TextField(default='', blank=True, verbose_name=u'History')
    t_lotto_subs = models.ForeignKey(LottoSubscription, null=True, blank=True, on_delete=models.CASCADE,
                                     related_name="t_lotto_subs", verbose_name=u'Lotto Subscription')
    shop_code = models.CharField(max_length=100, default='', null=True, blank=True, verbose_name=u'Code of shop')


dict_history_status = (
    ('00', 'start'),
    ('01', 'ready'),
    ('02', 'wait confirm'),
    ('03', 'error SOD'),
    # ('04', 'step 4'),
    # ('05', 'step 5'),
    ('30', 'error'),
    ('33', 'finish game'),
)

# class Ticket_history_status(models.Model):
#     id = models.AutoField(primary_key=True)
#     order = models.IntegerField(default=0, verbose_name=u'Order')
#     caption = models.CharField(max_length=100, default='', verbose_name=u'Caption')
#     verbal = models.CharField(max_length=30, default='', verbose_name=u'Varbal')
#     enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
#
#     def __str__(self):
#         return self.caption
#
#
class Ticket_history(models.Model):
    id = models.AutoField(primary_key=True)
    # status = models.ForeignKey(Ticket_type, null=True, blank=True, on_delete=models.CASCADE,
    #                              related_name="game_type_history", verbose_name=u'Type GAME')
    #
    status = models.CharField(max_length=2, default='00', null=True, blank=True, verbose_name=u'Status', choices=dict_history_status)
    game_type = models.ForeignKey(Ticket_type, null=True, blank=True, on_delete=models.CASCADE,
                                 related_name="game_type_history", verbose_name=u'Type GAME')
    games_id = models.ForeignKey(Game_history, null=True, blank=True, on_delete=models.CASCADE,
                                 related_name="games_id_history",
                                 verbose_name=u'Game Id')
    req_id = models.CharField(unique=True, max_length=50, default='', null=True, blank=True, verbose_name=u'Код запроса')
    req_dt = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Дата запроса')
    answ_dt = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Дата ответа')
    answ_nom = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name=u'Номер билета')
    answ_nom_00 = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name=u'Номер билета 00')
    answ_lottery_number = models.IntegerField(null=True, blank=True, verbose_name=u'Номер лотереи')
    lotto_result = models.ForeignKey(GameLottoResults, null=True, blank=True, on_delete=models.SET_NULL,
                                     verbose_name=u'Номер результата')
    answ_tabl = JSONField(default=dict, null=True, blank=True, verbose_name=u'Таблица билета')
    answ_option = models.CharField(max_length=20, default='', null=True, blank=True, verbose_name=u'Option билета')
    answ_option_00 = models.CharField(max_length=20, default='', null=True, blank=True, verbose_name=u'Option билета 00')
    answ_win = models.BooleanField(default=False, verbose_name=u'Выигрыш')
    answ_win_00 = models.BooleanField(default=False, verbose_name=u'Выигрыш 00')
    answ_win_sum = models.CharField(max_length=20, default='', null=True, blank=True, verbose_name=u'Сумма выигрыша')
    answ_win_sum_00 = models.CharField(max_length=20, default='', null=True, blank=True, verbose_name=u'Сумма выигрыша 00')
    error_job = models.TextField(default='', blank=True, verbose_name=u'Error JOB')
    step_job = models.TextField(default='', blank=True, verbose_name=u'Step JOB')
    step_ticket = models.CharField(max_length=20, default='', null=True, blank=True, verbose_name=u'Step билета')
    t_dev = models.ForeignKey(Devices_list, null=True, blank=True, on_delete=models.CASCADE, related_name="dev_id",
                               verbose_name=u'Dev Id')
    img_01 = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Img 01 с камеры 01')
    img_02 = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Img 02 с камеры 02')
    img_03 = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Img 03 обрезаный 01')
    img_04 = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Img 04 обрезаный 02')
    img_05 = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Img 05 бланк 01')
    img_06 = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Img 06 бланк 02')
    img_07 = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Img 07 бланк 01 мал')
    img_08 = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Img 08 бланк 02 мал')
    # donor
    balance_01 = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Balance befor')
    cost_1 = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Cost Tiket 1')
    cost_02 = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Cost Tiket 2')
    cost_discount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Discount')
    cost_2 = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Cost Tiket 2 with Discount')
    balance_02 = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Balance after')
    # recipient
    recipient_balance_01 = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Balance befor')
    # cost_1 = models.IntegerField(default=0, verbose_name=u'Cost Tiket 1')
    # cost_02 = models.IntegerField(default=0, verbose_name=u'Cost Tiket 2')
    # cost_discount = models.IntegerField(default=0, verbose_name=u'Discount')
    # cost_2 = models.IntegerField(default=0, verbose_name=u'Cost Tiket 2 with Discount')
    recipient_balance_02 = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                               verbose_name=u'Recipient Balance after')

    hash = models.CharField(max_length=128, default='', blank=True, null=True)
    # check
    t_check = models.BooleanField(default=False, verbose_name=u'Check')
    t_check_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                related_name="check_user",
                                verbose_name=u'User check')
    t_check_dt = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date check')
    t_cabala_dt = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date cabala')

#    def __str__(self):  # __unicode__
#        return str(self.market.caption) if self.market.caption else ''


class Report_list(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    verbal = models.CharField(max_length=20, default='', null=True, blank=True, unique=True, verbose_name=u'Code')
    caption = models.CharField(max_length=100, default='', null=True, blank=True, verbose_name=u'Caption')
    status = models.CharField(max_length=2, default='', null=True, blank=True, verbose_name=u'Status', choices=dict_device_status)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    settings = JSONField(default=dict, null=True, blank=True)
    config_data = JSONField(default=dict, null=True, blank=True)
    export = models.BooleanField(default=True, verbose_name=u'Export')
    export_template = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Template excel')
    template = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Template')
    add_param = models.JSONField(default=dict, null=True, blank=True)
    export_add = models.BooleanField(default=True, verbose_name=u'Export add')
    export_add_temp = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Template add ')
    export_add_name = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name=u'Template add name')
    description = models.TextField(default='', max_length=250, blank=True)

    def __str__(self):
        return str(self.caption) if self.caption else ''


class SiteSkin(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, blank=True, null=True, verbose_name=u'Очередность')
    name = models.CharField(max_length=100, default='', blank=True, null=True, verbose_name=u'Названия')
    code = models.CharField(max_length=100, default='', blank=True, null=True, verbose_name=u'Код')
    enabled = models.BooleanField(default=True, verbose_name=u'Использовать')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order',)


class EmailToSend(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                related_name="email_user",
                                verbose_name=u'User')
    dt_add = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date ADD')
    dt_start = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date START')
    dt_stop = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date STOP')
    type = models.TextField(default='', max_length=50, null=True, blank=True)

    subject = models.TextField(default='', max_length=200, blank=True)
    recipient = models.TextField(default='', max_length=200, blank=True)
    html_message = models.TextField(default='', blank=True)
    sent = models.BooleanField(default=False, blank=True)
    hash = models.CharField(default='', max_length=100)

    def __str__(self):
        return self.subject


dict_status_op = (
    ('00', 'draft'),
    ('01', 'wait'),
    ('02', 'not pay'),
    ('10', 'ready'),
)


class BalanceOperation(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    confirm = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="balance_user",
                                verbose_name=u'User')
    type_balanceoperation = models.ForeignKey(Type_balanceoperation, null=True, blank=True,
                                              on_delete=models.CASCADE,
                                              related_name="type_balanceoperation",
                                              verbose_name=u'Type operation')
    games_id = models.ForeignKey(Game_history, null=True, blank=True, on_delete=models.CASCADE,
                                 related_name="balance_games_id",
                                 verbose_name=u'Game Id')
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Amount')
    status = models.ForeignKey(Type_balanceoperation_status, null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name="type_balanceoperation_status",
                               verbose_name=u'Status')
    description = models.TextField(default='', null=True, blank=True)
    pay_response = models.TextField(default='', null=True, blank=True)
    # check
    t_create = models.BooleanField(default=False, verbose_name=u'Manager')
    t_create_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                      related_name="balance_user_create",
                                      verbose_name=u'Manager create')
    t_create_dt = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date Manager create')
    subscription = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.CASCADE,
                                     related_name="balance_subscriptions",
                                     verbose_name=u'Subscription Id')
    lotto_subscription = models.ForeignKey(LottoSubscription, null=True, blank=True, on_delete=models.CASCADE,
                                           related_name="balance_lotto_subscriptions",
                                           verbose_name=u'Lotto Subscription')

    class Meta:
        ordering = ('-created',)


class PayResponse(models.Model):
    id = models.AutoField(primary_key=True)
    merchantAccount = models.CharField(default='', max_length=256, blank=True, null=True)
    orderReference = models.CharField(default='', max_length=256, blank=True, null=True)
    merchantSignature = models.CharField(default='', max_length=256, blank=True, null=True)
    amount = models.CharField(default='', max_length=256, blank=True, null=True)
    currency = models.CharField(default='', max_length=256, blank=True, null=True)
    authCode = models.CharField(default='', max_length=256, blank=True, null=True)
    email = models.CharField(default='', max_length=256, blank=True, null=True)
    phone = models.CharField(default='', max_length=256, blank=True, null=True)
    createdDate = models.CharField(default='', max_length=256, blank=True, null=True)
    processingDate = models.CharField(default='', max_length=256, blank=True, null=True)
    cardPan = models.CharField(default='', max_length=256, blank=True, null=True)
    cardType = models.CharField(default='', max_length=256, blank=True, null=True)
    issuerBankCountry = models.CharField(default='', max_length=256, blank=True, null=True)
    issuerBankName = models.CharField(default='', max_length=256, blank=True, null=True)
    recToken = models.CharField(default='', max_length=256, blank=True, null=True)
    transactionStatus = models.CharField(default='', max_length=256, blank=True, null=True)
    reason = models.CharField(default='', max_length=256, blank=True, null=True)
    reasonCode = models.CharField(default='', max_length=256, blank=True, null=True)
    fee = models.CharField(default='', max_length=256, blank=True, null=True)
    paymentSystem = models.CharField(default='', max_length=256, blank=True, null=True)


class FeedbackStatus(models.Model):
    id = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.caption


dict_feedback_status = (
    ('00', 'NEW'),
    ('01', 'READY'),
    ('02', 'BLOCK'),
)

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name=u'Data create')
    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                related_name="feedback_user",
                                verbose_name=u'User in')
    u_name = models.CharField(max_length=100, default='', blank=True, null=True, verbose_name=u'User')
    u_email = models.EmailField(default='', blank=True, null=True, verbose_name=u'email')
    text = models.TextField(max_length=500, default='', blank=True, null=True, verbose_name=u'Text req')
    status = models.CharField(default="00", max_length=2, choices=dict_feedback_status, verbose_name=u'Status')
    reply_text = models.TextField(max_length=2000, default='', blank=True, null=True, verbose_name=u'Text ansver')
    reply_date = models.DateTimeField(blank=True, null=True, verbose_name=u'Date ansver')
    reply_lang = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name=u'Lang answer')
    # check
    t_check = models.BooleanField(default=False, verbose_name=u'OK')
    t_check_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                related_name="feedback_check_user",
                                verbose_name=u'User check')
    t_check_dt = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date check')

    def __str__(self):
        return self.text

    # class Meta:
    #     ordering = ('status', 'created')
    #


dict_payout_status = (
    ('00', 'NEW'),
    ('01', 'OK'),
    ('02', 'REJECT'),
    ('04', 'IN PROCESS'),
)


class Payout(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                related_name="payout_user",
                                verbose_name=u'User')
    created = models.DateTimeField(auto_now_add=False, verbose_name=u'Data create')
    status = models.CharField(default="00", max_length=2, choices=dict_payout_status, verbose_name=u'Status')
    bal_oper = models.OneToOneField(BalanceOperation, null=True, unique=True, on_delete=models.CASCADE, verbose_name=u'Operation')
    acc_name = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name=u'Account Name')
    name_bank = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name=u'Name Bank')
    branch = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name=u'Branch number')
    acc_num = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name=u'Account number')
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Amount')
    percent = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Percent')
    amount_minus_percent = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Amount minus percent')
    description = models.TextField(default='', blank=True, null=True, verbose_name='Description')
    reject_reason = models.TextField(default='', blank=True, null=True, verbose_name='Rejection reason')
    photo = models.ImageField(upload_to='payouts/', blank=True, null=True, verbose_name='Photo')
    # check
    t_check = models.BooleanField(default=False, verbose_name=u'OK')
    t_check_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                related_name="payout_check_user",
                                verbose_name=u'User check')
    t_check_dt = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date check')


    def __str__(self):
        return self.acc_name

    # class Meta:
    #     ordering = ('status', 'created')
    #


dict_payadd_status = (
    ('00', 'NEW'),
    ('01', 'OK'),
    ('02', 'BLOCK'),
)

class Payadd(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                related_name="payadd_user",
                                verbose_name=u'User')
    created = models.DateTimeField(auto_now_add=False, verbose_name=u'Data create')
    status = models.CharField(default="00", max_length=2, choices=dict_payadd_status, verbose_name=u'Status')
    bal_oper = models.OneToOneField(BalanceOperation, null=True, unique=True, on_delete=models.CASCADE, verbose_name=u'Operation')
    acc_name = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name=u'Account Name')
    name_bank = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name=u'Name Bank')
    branch = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name=u'Branch number')
    acc_num = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name=u'Account number')
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Amount')
    upload_doc = models.FileField(upload_to='users/doc_add/', default='', blank=True, null=True, verbose_name='Doc')
    # check
    t_check = models.BooleanField(default=False, verbose_name=u'OK')
    t_check_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                related_name="payadd_check_user",
                                verbose_name=u'User check')
    t_check_dt = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date check')


    # def __str__(self):
    #     return self.acc_name

    # class Meta:
    #     ordering = ('status', 'created')
    #


dict_cashadd_status = (
    ('00', 'NEW'),
    ('01', 'OK'),
    ('02', 'BLOCK'),
)

class Cashadd(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                related_name="cashadd_user",
                                verbose_name=u'User')
    created = models.DateTimeField(auto_now_add=False, verbose_name=u'Data create')
    status = models.CharField(default="00", max_length=2, choices=dict_cashadd_status, verbose_name=u'Status')
    bal_oper = models.OneToOneField(BalanceOperation, null=True, unique=True, on_delete=models.CASCADE, verbose_name=u'Operation')
    city = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name=u'City')
    street = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name=u'Street')
    building = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name=u'Building')
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Amount')
    # check
    t_check = models.BooleanField(default=False, verbose_name=u'OK')
    t_check_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                     related_name="cashadd_check_user",
                                     verbose_name=u'User check')
    t_check_dt = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date check')


    def __str__(self):
        return self.city + self.street + self.building


# глобальные настройки
dict_glob_type = (
    ('txt', 'txt'),
    ('int', 'int'),
    ('bool', 'bool'),
    # ('10', 'ready'),
)

class Globalset(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50) # код
    type = models.CharField(max_length=20, default='txt', blank=True, null=True, choices=dict_glob_type,
                                      verbose_name=u'Type') # type
    # value = models.CharField(max_length=500) # значение
    value = models.TextField() # значение
    description = models.CharField(max_length=500) # описание


class Partner(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0)
    enabled = models.BooleanField(default=True, verbose_name=u'Использовать')
    url = models.CharField(max_length=128, default='', blank=True, null=True)
    company = models.CharField(max_length=128, default='', blank=True, null=True)
    text = models.TextField(default='', max_length=380)
    image = models.ImageField(upload_to='partner_opinion/', default='', blank=True, null=True )

    def __str__(self):
        return self.company


class Faqtabl(models.Model):
    id = models.AutoField(primary_key=True)
    faq_enable = models.BooleanField(default=True)
    faq_order = models.IntegerField(default=0)
    faq_title = models.CharField(max_length=200, default='')
    faq_info = models.CharField(max_length=1000, default='')


class Task_status(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    caption = models.CharField(max_length=100, default='')
    verbal = models.CharField(max_length=30, default='')
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.caption

class Task_type(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    caption = models.CharField(max_length=100, default='')
    verbal = models.CharField(max_length=30, default='')
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.caption


class Task_history(models.Model):
    id = models.AutoField(primary_key=True)
    t_status = models.ForeignKey(Task_status, default=1, on_delete=models.CASCADE,
                                 related_name="t_task_status", verbose_name=u'Status')
    t_type = models.ForeignKey(Task_type, null=True, blank=True, on_delete=models.CASCADE,
                               related_name="t_task_type", verbose_name=u'Type')
    task_name = models.TextField(default='', blank=True, verbose_name=u'Task name')
    task_user = models.TextField(default='', blank=True, verbose_name=u'Task user')
    task_user_ok = models.TextField(default='', blank=True, verbose_name=u'Task user OK')
    task_num = models.IntegerField(default=0, verbose_name=u'Count users')
    task_num_ok = models.IntegerField(default=0, verbose_name=u'Count users')
    task_text = models.TextField(default='', blank=True, verbose_name=u'Task text')
    subject = models.TextField(default='', null=True, blank=True, verbose_name=u'Subject')
    task_add_conf1 = models.BooleanField(default=False, blank=True)
    # ticket_sum = models.IntegerField(default=0, verbose_name=u'Ticket sum')
    # user_ip = models.CharField(max_length=20, default='', null=True, blank=True, verbose_name=u'Start Game Ip')
    dt_plan = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date Plan')
    dt_add = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date ADD')
    dt_start = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date START')
    dt_stop = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date STOP')
    image = models.ImageField(upload_to='tasks/', default='', blank=True, null=True, verbose_name='Image')


class SmsToSend(models.Model):
    id = models.AutoField(primary_key=True)
    t_task = models.ForeignKey(Task_history, default=1, on_delete=models.CASCADE,
                               related_name="t_task_history",
                               verbose_name=u'Task')
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                related_name="sms_user",
                                verbose_name=u'User')
    subject = models.TextField(default='', max_length=200, blank=True)
    recipient = models.TextField(default='', max_length=200, blank=True)
    html_message = models.TextField(default='', blank=True)
    sent = models.TextField(default='', blank=True)
    hash = models.CharField(unique=True, max_length=100)
    request = models.TextField(default='', blank=True)
    answer = models.TextField(default='', blank=True)
    dt_add = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date ADD')
    dt_start = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date START')
    dt_stop = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date STOP')

    def __str__(self):
        return self.subject


class SubsSmsToSend(models.Model):
    id = models.AutoField(primary_key=True)
    t_subs = models.ForeignKey(Subscription, null=False, blank=False, on_delete=models.CASCADE,
                                 related_name="t_subs_sms", verbose_name=u'Subscription')
    t_game = models.ForeignKey(Game_history, null=False, blank=False, on_delete=models.CASCADE,
                                 related_name="t_subs_sms_game",
                                 verbose_name=u'Game Id')
    t_task = models.ForeignKey(Task_subs, null=True, blank=True, on_delete=models.PROTECT,
                                 related_name="t_sms_task_subs", verbose_name=u'Task sms')
    t_status = models.ForeignKey(Task_subs_status, null=True, blank=True, on_delete=models.PROTECT,
                                 related_name="t_sms_subs_status", verbose_name=u'Status')
    hash = models.CharField(default='', max_length=100)
    recipient = models.CharField(default='', max_length=100, verbose_name=u'Phone number')
    html_message = models.TextField(default='', blank=True)
    request = models.TextField(default='', blank=True)
    answer = models.TextField(default='', blank=True)
    dt_add = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date ADD')
    dt_plan = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date PLAN')
    dt_start = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date START')
    dt_stop = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date STOP')

    def __str__(self):
        return self.recipient


class Cabala_history(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=False)
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    cab_id = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name=u'Code')
    cab_dt = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date')
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=u'Amount')
    description = models.TextField(default='', blank=True)

#    def __str__(self):  # __unicode__
#        return str(self.market.caption) if self.market.caption else ''


class Type_blacklist(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    caption = models.CharField(max_length=100, default='')
    verbal = models.CharField(max_length=30, default='')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')

    def __str__(self):
        return self.caption


class Blacklist(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=False)
    create_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                related_name="Blacklist_user_create",
                                verbose_name=u'Manager')
    type_blacklist = models.ForeignKey(Type_blacklist, null=True, blank=True,
                                              on_delete=models.CASCADE,
                                              related_name="type_balanceoperation",
                                              verbose_name=u'Type operation')
    text = models.CharField(max_length=100, default='')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    description = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.text


class PaymentAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    payment_index = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    balance_operation_id = models.ForeignKey(BalanceOperation, null=True, blank=True,
                                             on_delete=models.CASCADE,
                                             related_name='payment_answers',
                                             verbose_name=u'BalanceOperation number')
    status = models.CharField(max_length=3, default='', null=True, blank=True,
                              verbose_name=u'Status payment from payment system')
    json_data = models.JSONField(default=dict, null=True, blank=True)
    text_data = models.TextField(default='', null=True, blank=True)

    @staticmethod
    def get_columns_name():
        return [
            "terminal", "payment_index", "created_date", "transaction_type",
            "security", "amount", "currency", "paid_with", "card_last_4_digits",
            "card_expiring_at", "of_payments", "fisrt_payment_amount", "asy_other_payment",
            "owner_social_id", "issuer_payer_card", "card_type", "card_brand",
            "bank_code", "branch_number", "account_number", "status",
            "error_message", "shva_transmit", "payment_type", "shva_authorization",
            "customer1", "cvv_check_status", "id_check_status", "shva_voucher",
            "finance_document_id", "cancelled_document_id", "token",
            "company_name", "contact", "payer_email", "payer_address", "payer_phone", "payer_city",
            "description", "notes", "number_bal_op", "dc_disable", "child_terminal_name"
        ]


class BalRecalculate(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                related_name="BalRecalculate_user",
                                verbose_name=u'User')
    text = models.TextField(default='', max_length=200, blank=True)
    job = models.TextField(default='', blank=True)

    def __str__(self):
        return self.text


class GiftSmsToSend(models.Model):
    id = models.AutoField(primary_key=True)
    t_game = models.ForeignKey(Game_history, null=False, blank=False, on_delete=models.CASCADE,
                               related_name="t_gift_sms_game",
                               verbose_name=u'Game Id')
    t_status = models.ForeignKey(Task_subs_status, null=True, blank=True, on_delete=models.PROTECT,
                                 related_name="t_sms_gift_status", verbose_name=u'Status')
    hash = models.CharField(default='', max_length=100)
    recipient = models.CharField(default='', max_length=100, verbose_name=u'Phone number')
    html_message = models.TextField(default='', blank=True)
    request = models.TextField(default='', blank=True)
    answer = models.TextField(default='', blank=True)
    dt_add = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date ADD')
    dt_plan = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date PLAN')
    dt_start = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date START')
    dt_stop = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date STOP')
    add_param = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f'{self.id} {self.recipient}'


class BloggerType(models.Model):
    id = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=100, default='')
    verbal = models.CharField(max_length=50, default='')
    description = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.caption


class Blogger(models.Model):
    id = models.AutoField(primary_key=True)
    b_type = models.ForeignKey(BloggerType, on_delete=models.PROTECT, null=True, blank=True,
                               related_name='type_bloggers',
                               verbose_name='Type')
    name = models.CharField(default='', max_length=100, verbose_name='Full name')
    phone = models.CharField(default='', max_length=100, null=True, blank=True, verbose_name='Phone')
    accounts = models.JSONField(default=dict, null=True, blank=True, verbose_name='Social media accounts')
    notes = models.TextField(null=True, blank=True, verbose_name='Notes')
    ref_hash = models.CharField(unique=True, default='', max_length=100)
    ref_link = models.CharField(default='', max_length=250)
    add_params = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return self.name


class BloggerRef(models.Model):
    id = models.AutoField(primary_key=True)
    dt_add = models.DateTimeField(auto_now_add=False, null=False, blank=False, verbose_name=u'Date ADD')
    utm_code = models.CharField(default='', max_length=20)
    blogger = models.ForeignKey(Blogger, null=True, blank=True, on_delete=models.PROTECT,
                                 related_name="t_blogger_refs", verbose_name=u'Blogger')
    u_ip = models.CharField(max_length=20, default='', null=True, blank=True, verbose_name=u'User Ip')
    http_referer = models.CharField(default='', max_length=150, verbose_name='http_referer')

    def __str__(self):
        return self.utm_code


class IdConfirmationStatus(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, verbose_name='Order')
    caption = models.CharField(max_length=50, default='', verbose_name='Name')
    verbal = models.CharField(max_length=10, default='', verbose_name='Code')
    enabled = models.BooleanField(default=True, verbose_name='Enabled')

    def __str__(self):
        return self.caption


class IdConfirmation(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.ForeignKey(IdConfirmationStatus, null=True, blank=True, on_delete=models.PROTECT,
                               related_name="id_conf_status", verbose_name='Status')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT,
                             related_name="user_id_conf", verbose_name='User')
    dt_add = models.DateTimeField(auto_now_add=False, null=False, blank=False, verbose_name='Date ADD')

    photo_id = models.ImageField(upload_to='id_confirms/', default='', blank=True, null=True,
                                 verbose_name='Photo id')
    photo_face = models.ImageField(upload_to='id_confirms/', default='', blank=True, null=True,
                                   verbose_name='Photo face')
    photo_id_preview = models.URLField(default='', blank=True, null=True, verbose_name='Url Photo id thumb')
    photo_face_preview = models.URLField(default='', blank=True, null=True, verbose_name='Url Photo face thumb')
    check = models.BooleanField(default=False, verbose_name='Check')
    check_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT,
                                   related_name="check_id_conf_user", verbose_name='User check')
    check_dt = models.DateTimeField(auto_now_add=False, null=True, blank=True,
                                    verbose_name='Date admin review')
    description = models.TextField(default='', blank=True, verbose_name='Description')
    reject_reason = models.TextField(default='', blank=True, verbose_name='Rejection reason')
    add_param = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.user}'


class IdRejectReason(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, verbose_name='Order')
    caption = models.CharField(max_length=250, default='', verbose_name='Name')
    verbal = models.CharField(max_length=10, default='', verbose_name='Code')
    enabled = models.BooleanField(default=True, verbose_name='Enabled')

    def __str__(self):
        return self.caption


class BotMessageManagers(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name='Enabled')
    name = models.CharField(max_length=150, verbose_name='Name')
    description = models.TextField(default='', blank=True, verbose_name='Description')
    add_param = models.JSONField(default=dict, blank=True)


class APIExtPage(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name='Enabled')
    caption = models.CharField(max_length=100, verbose_name='Page name')
    allowed_companies = models.TextField(default='', blank=True,
                                         verbose_name='List of allowed companies')
    template = models.CharField(max_length=250, verbose_name=u'Template')
    add_param = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.caption


class APIExtHash(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name='Enabled')
    api_hash = models.CharField(max_length=10, unique=True, verbose_name='Hash')
    api_link = models.CharField(max_length=250, verbose_name='Link')
    page = models.ForeignKey(APIExtPage, on_delete=models.CASCADE,
                             related_name="page_hash", verbose_name='Page to show')
    dt_add = models.DateTimeField(auto_now_add=False, null=False, blank=False, verbose_name='Date ADD')

    def __str__(self):
        return self.api_hash


script_location = (
    ('ht', 'head top'),
    ('hb', 'head bottom'),
    ('bt', 'body top'),
    ('bb', 'body bottom'),
)


file_location = (
    ('main', 'main'),
    ('cab', 'cabinet')
)


class LayoutScript(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name='Enabled')
    ordering = models.IntegerField(default=0, verbose_name='Ordering')
    js_script = models.TextField(verbose_name='JS Script')
    file_location = models.CharField(max_length=5, choices=file_location, verbose_name='File')
    script_location = models.CharField(max_length=2, choices=script_location, verbose_name='Script location')
    description = models.CharField(max_length=250, null=True, blank='True', verbose_name='Description')


class SubsTranzillaAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    answer_type = models.CharField(max_length=20, default='', blank=True)
    answer = models.TextField(default='', blank=True)
    created_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    balance_operation_id = models.ForeignKey(BalanceOperation, null=True, blank=True,
                                             on_delete=models.CASCADE,
                                             related_name='subs_payment_answers',
                                             verbose_name='BalanceOperation number')


class SubsBonus(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name='Enabled')
    type_payment = models.ForeignKey(Type_payment, null=True, blank=True, on_delete=models.PROTECT,
                                     related_name="subs_bonus_type_payment", verbose_name=u'Payment type')
    for_all = models.BooleanField(default=True, verbose_name='For all managers')
    manager = models.ForeignKey(SubsManager, on_delete=models.PROTECT, null=True, blank=True,
                                related_name='subs_managers',
                                verbose_name='For a specific manager')
    ticket_type = models.ForeignKey(Ticket_type, on_delete=models.PROTECT,
                                    related_name='ticket_type_subs_managers',
                                    verbose_name='Ticket type')
    min_days = models.IntegerField(default=0, verbose_name='Minimum number of days')
    max_days = models.IntegerField(default=0, verbose_name='Maximum number of days')
    bonus_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Fixed bonus')
    bonus_percent = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Percentage bonus')

    def __str__(self):
        return f'{self.ticket_type} {self.min_days}-{self.max_days}'


class NotificationSystem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    new = models.BooleanField(default=True)
    verbal = models.CharField(max_length=20, default='', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=False, null=False)
    dt_start = models.DateTimeField(auto_now_add=False, null=False, blank=False, verbose_name=u'Date START')
    dt_stop = models.DateTimeField(auto_now_add=False, null=False, blank=False, verbose_name=u'Date STOP')
    text = models.TextField(default='', blank=True, verbose_name='Text')
    description = models.CharField(max_length=250, null=True, blank='True', verbose_name='Description')


class NotificationUser(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0, verbose_name=u'Order')
    enabled = models.BooleanField(default=True, verbose_name=u'Enabled')
    user_id = models.IntegerField(default=0)
    new = models.BooleanField(default=True)
    verbal = models.CharField(max_length=20, default='', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=False, null=False)
    dt_start = models.DateTimeField(auto_now_add=False, null=False, blank=False, verbose_name=u'Date START')
    dt_stop = models.DateTimeField(auto_now_add=False, null=False, blank=False, verbose_name=u'Date STOP')
    text = models.TextField(default='', blank=True, verbose_name='Text')
    description = models.CharField(max_length=250, null=True, blank='True', verbose_name='Description')


class EmailSettings(models.Model):
    id = models.AutoField(primary_key=True)
    verbal = models.CharField(max_length=100, verbose_name='Verbal')
    subject = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name='Subject')
    text = models.TextField(default='', blank=True, null=True, verbose_name='Text')
    layout_template = models.CharField(max_length=250, default='', blank=True, null=True,
                                       verbose_name='Layout template')
    mail_template = models.CharField(max_length=250, default='', verbose_name='Mail template')
    parameters = models.JSONField(default=dict, blank=True, null=True)


class CommentCallcenter(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment_callcenter_user',
                                     verbose_name='User profile')
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment_callcenter_admin_creator',
                                verbose_name='Admin profile')
    text = models.TextField(default='', blank=True, null=True, verbose_name='Text comment')
    date_return = models.DateField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date return')
    date_created = models.DateTimeField(auto_now_add=False, null=False, blank=False, verbose_name=u'Date created')


class SubsAutoPay(models.Model):
    id = models.AutoField(primary_key=True)
    p_subs = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.PROTECT,
                               related_name="p_subs", verbose_name=u'Subscription')
    p_lotto_subs = models.ForeignKey(LottoSubscription, null=True, blank=True, on_delete=models.PROTECT,
                                     related_name="p_lotto_subs", verbose_name=u'Lotto Subscription')
    p_status = models.BooleanField(default=False, verbose_name=u'Success')
    request = models.TextField(default='', blank=True)
    answer = models.TextField(default='', blank=True)
    dt_start = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date request')
    dt_stop = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=u'Date answer')

