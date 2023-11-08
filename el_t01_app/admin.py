from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import (Blogger, BloggerRef, BloggerType,
                     Profile, Ticket_type, Devices_list, TypeTicketType, GameLottoResults, GameLottoProfit,
                     Documentation_list, SiteLang, List_external_company,
                     Report_list, Type_program, SiteSkin, Type_currency, Type_payment,
                     Game_history, Ticket_history, BalanceOperation, Type_balanceoperation, GameType,
                     PayResponse, Type_balanceoperation_status, List_jellyfish,
                     Type_game_status, Feedback, EmailToSend, Globalset, Payout, Payadd,
                     Cashadd, Partner, Faqtabl, Task_status, Task_type, Task_history, SmsToSend,
                     Type_blacklist, Blacklist, PaymentAnswer, BalRecalculate, Subscription,
                     Task_subs_status, Task_subs, SubsSmsToSend, GiftSmsToSend, IdConfirmation,
                     IdConfirmationStatus, BotMessageManagers, APIExtPage, APIExtHash, LayoutScript,
                     SubsTranzillaAnswer, UserPayCard, SubsAutoPay, SubsManager, SubsBonus,
                     DiscountOwner, Discount, DiscountHistory, DiscountList, DiscountSet,
                     NotificationSystem,
                     MessWhatsapp,
                     EmailSettings,
                     CommentCallcenter,
                     LottoSubscription)



from django.contrib.auth.models import User
admin.site.unregister(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username']
    ordering = ['-id']
    search_fields = ('name', 'email', 'username')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'mobile', 'user', 'balance', 'i_confirmed']
    search_fields = ('name', 'user__email')
    raw_id_fields = ('user',)
    actions = ['change_i_confirmed']

    @admin.action(description='Сhange i_confirmed status to True')
    def change_i_confirmed(self, request, queryset):
        updated = queryset.update(i_confirmed=True)
        self.message_user(request, ngettext(
            '%d profile i_confirmed status was successfully updated.',
            '%d profiles i_confirmed status were successfully updated.',
            updated,
        ) % updated, messages.SUCCESS)


@admin.register(Ticket_type)
class Ticket_typeAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption', 'verbal', 'order', 'in_play', 'enabled', 'cost_1', 'cost_2',
                    'verbal_jellyfish', 'verbal_government', 'setting']
    ordering = ['order']


@admin.register(Devices_list)
class Devices_listAdmin(admin.ModelAdmin):
    list_display = ['caption', 't_type', 'id', 'order', 'verbal', 'enabled', 'scratch', 'dmove']
    ordering = ['order']


@admin.register(Ticket_history)
class Ticket_historyAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'game_type', 'answ_nom', 'answ_lottery_number', 'lotto_result', 'games_id',
                    'game_type', 'req_dt', 'cost_2', 'req_id', 'answ_dt', 'answ_nom',
                    'answ_win', 'answ_win_sum', 'balance_01', 'balance_02', 'hash']
    ordering = ['-req_dt']
    search_fields = ['games_id__id']
    list_filter = ['game_type', 'answ_win', 'answ_win_sum']
    raw_id_fields = ('games_id', 'lotto_result')


@admin.register(SiteLang)
class SiteLangAdmin(admin.ModelAdmin):
    list_display = ['lang_name', 'lang_code', 'order', 'enabled']
    ordering = ['order']


@admin.register(Documentation_list)
class Documentation_listAdmin(admin.ModelAdmin):
    list_display = ['caption', 'order', 'enabled']
    ordering = ['order']


@admin.register(List_external_company)
class List_external_companyAdmin(admin.ModelAdmin):
    list_display = ['caption', 'order', 'enabled', 'verbal', 'status', 'api_token', 'type_mode']
    ordering = ['order']


@admin.register(Game_history)
class Game_historyAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_type', 'user_id', 'user_recipient', 't_status', 'ticket_num', 'ticket_sum', 't_company',
                    'dt_add', 'dt_start', 'dt_stop', 't_subs']
    search_fields = ['id', 'user_id__email']
    list_filter = ['t_status', 't_payment']
    raw_id_fields = ('user_id', 't_subs', 't_discount', 'user_recipient')


@admin.register(Report_list)
class Report_listAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'verbal', 'caption', 'template', 'export_template',
                    'add_param', 'status', 'order', 'description']
    ordering = ['order']


@admin.register(Type_program)
class Type_programAdmin(admin.ModelAdmin):
    list_display = ['caption', 'verbal']


@admin.register(SiteSkin)
class SiteSkinAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'order', 'enabled', 'code']
    ordering = ['order']


@admin.register(Type_currency)
class Type_currencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'verbal', 'caption']
    ordering = ['order']


@admin.register(Type_payment)
class Type_paymentAdmin(admin.ModelAdmin):
    list_display = ['caption', 'id', 'order', 'enabled', 'is_active', 'subs_enabled', 'verbal', 'caption']
    ordering = ['order']


@admin.register(BalanceOperation)
class BalanceOperationAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'user_id', 'type_balanceoperation', 'amount', 'status', 'games_id']
    search_fields = ('user_id__profile__name', 'user_id__email')
    raw_id_fields = ('user_id', 'games_id', 'subscription', 't_create_user')


@admin.register(PayResponse)
class PayResponseAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(Type_balanceoperation)
class Type_balanceoperationAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'caption', 'verbal', 'verbal_payment', 'enabled', 'max_win', 'for_balance']
    ordering = ['order']


@admin.register(Type_balanceoperation_status)
class Type_balanceoperation_statusAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'caption', 'verbal', 'enabled']
    ordering = ['order']


@admin.register(List_jellyfish)
class List_jellyfishAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption']
    ordering = ['order']


@admin.register(Type_game_status)
class Type_game_statusAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'caption', 'verbal', 'enabled']
    ordering = ['order']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'user_id', 'u_name', 'u_email', 'text', 'status',
                    'reply_text', 'reply_date', 'reply_lang', 't_check', 't_check_user', 't_check_dt']
    search_fields = ('user_id__profile__name', 'user_id__email')
    list_filter = ['status', 't_check']
    raw_id_fields = ('user_id', 't_check_user')



@admin.register(EmailToSend)
class EmailToSendAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'recipient']
    search_fields = ('recipient',)
    ordering = ['-id']
    list_filter = ['sent']


@admin.register(Globalset)
class GlobalsetAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'type', 'value', 'description']
    ordering = ['code']
    search_fields = ('code',)


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'created', 'acc_name', 'amount']
    search_fields = ('user_id__email',)
    raw_id_fields = ('user_id', 'bal_oper', 't_check_user')


@admin.register(Payadd)
class PayaddAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'created', 'acc_name', 'amount']
    raw_id_fields = ('user_id', 't_check_user', 'bal_oper')


@admin.register(Cashadd)
class CashaddAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'created', 'city', 'street', 'building', 'amount']
    ordering = ['-id']
    raw_id_fields = ('user_id', 'bal_oper', 't_check_user')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'enabled', 'url', 'company']
    ordering = ['order']


@admin.register(Faqtabl)
class FaqtablAdmin(admin.ModelAdmin):
    list_display = ['id', 'faq_enable', 'faq_order', 'faq_title', 'faq_info']
    ordering = ['faq_order']


@admin.register(Task_status)
class Task_statusAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption', 'verbal', 'enabled']


@admin.register(Task_type)
class Task_typeAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption', 'verbal', 'enabled']
    ordering = ['id']


@admin.register(Task_history)
class Task_historyAdmin(admin.ModelAdmin):
    list_display = ['id', 't_status', 't_type', 'task_name', 'task_num', 'task_text', 'task_add_conf1', 'dt_plan',
                    'dt_add', 'dt_start', 'dt_stop']
    list_filter = ('t_status',)


@admin.register(SmsToSend)
class SmsToSendAdmin(admin.ModelAdmin):
    list_display = ['id', 't_task_id', 'user_id', 'html_message', 'dt_add', 'dt_start', 'dt_stop']
    raw_id_fields = ('t_task', 'user_id')
    search_fields = ('user_id__email',)



@admin.register(Type_blacklist)
class Type_blacklistAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'caption', 'verbal', 'enabled']
    ordering = ['order']


@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'create_user', 'type_blacklist', 'text', 'enabled', ]
    ordering = ['-created']
    raw_id_fields = ('create_user',)



@admin.register(PaymentAnswer)
class PaymentAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment_index', 'created_date', 'balance_operation_id', 'status']
    raw_id_fields = ('balance_operation_id',)
    search_fields = ('payment_index',)


@admin.register(BalRecalculate)
class BalRecalculateAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'user_id_creator', 'creator', 'dt_start', 'dt_stop', 'enabled', 'auto_pay',
                    'total_tickets_amount', 'total_days_amount', 'manager', 'bonus', 'type_payment']
    search_fields = ('user_id__email',)
    list_filter = ('enabled', 'day_1', 'day_2', 'day_3', 'day_4', 'day_5', 'day_6', 'day_7')
    raw_id_fields = ('user_id', 'user_id_creator', 'u_paycard')


@admin.register(Task_subs_status)
class Task_subs_statusAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'enabled', 'caption', 'verbal', 'description']


@admin.register(Task_subs)
class Task_subsAdmin(admin.ModelAdmin):
    list_display = ['id', 't_status', 'dt_start', 'dt_stop', 'task_ok_num', 'task_error_num']
    list_filter = ('t_status',)


@admin.register(SubsSmsToSend)
class SubsSmsToSendAdmin(admin.ModelAdmin):
    list_display = ['id', 't_subs_id', 't_game_id', 'recipient', 'html_message', 't_status',
                    'dt_add', 'dt_plan', 'dt_start', 'dt_stop']
    search_fields = ('recipient',)
    list_filter = ('t_status',)
    raw_id_fields = ('t_game', 't_subs', 't_task')


@admin.register(GiftSmsToSend)
class GiftSmsToSendAdmin(admin.ModelAdmin):
    list_display = ['id', 't_game_id', 'recipient', 'html_message', 't_status', 'dt_add',
                    'dt_plan', 'add_param']
    search_fields = ('recipient', 't_game_id')
    list_filter = ('t_status',)
    raw_id_fields = ('t_game', )


@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'b_type', 'accounts', 'ref_hash', 'ref_link']
    search_fields = ('name',)


@admin.register(BloggerRef)
class BloggerRefAdmin(admin.ModelAdmin):
    list_display = ['id', 'utm_code', 'blogger', 'http_referer', 'u_ip', 'dt_add']
    search_fields = ('utm_code',)


@admin.register(IdConfirmationStatus)
class IdConfirmationStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'caption', 'verbal', 'enabled']


@admin.register(IdConfirmation)
class IdConfirmationAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'dt_add', 'user', 'check', 'check_dt', 'check_user', 'reject_reason']
    raw_id_fields = ('user', 'check_user')
    search_fields = ('user__email',)


@admin.register(BotMessageManagers)
class BotMessageManagersAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'name', 'add_param', 'description']
    search_fields = ('name',)


@admin.register(APIExtPage)
class APIExtPageAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'caption', 'template', 'allowed_companies', 'add_param']


@admin.register(APIExtHash)
class APIExtHashAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'api_hash', 'api_link', 'page', 'dt_add']


@admin.register(LayoutScript)
class LayoutScriptAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'ordering', 'js_script', 'file_location', 'script_location', 'description']
    ordering = ['file_location']


@admin.register(SubsTranzillaAnswer)
class SubsTranzillaAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer_type', 'answer']


@admin.register(UserPayCard)
class UserPayCardAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'tranzila_tk', 'ccno', 'mask_card', 'myid', 'expmonth', 'expyear', 'dt_lastpay']
    raw_id_fields = ('user_id',)


@admin.register(SubsAutoPay)
class SubsAutoPayAdmin(admin.ModelAdmin):
    list_display = ['id', 'p_subs', 'p_status', 'dt_start', 'dt_stop']
    raw_id_fields = ('p_subs', )
    search_fields = ('name', 'user__email')


@admin.register(SubsBonus)
class SubsBonusAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'type_payment', 'for_all', 'manager', 'ticket_type',
                    'min_days', 'max_days', 'bonus_amount', 'bonus_percent']
    raw_id_fields = ('manager',)


@admin.register(SubsManager)
class SubsManagerAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'name', 'description']


@admin.register(BloggerType)
class BloggerTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'verbal', 'caption', 'description']


@admin.register(DiscountOwner)
class DiscountOwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'caption', 'verbal', 'enabled']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'caption', 'verbal', 'start_date',
                    'stop_date']


@admin.register(DiscountSet)
class DiscountSetAdmin(admin.ModelAdmin):
    list_display = ['disc', 'ticket_type', 'id', 'enabled', 'discount_amount', 'discount_percent']
    ordering = ['disc', 'ticket_type']


@admin.register(DiscountList)
class DiscountListAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'owner', 'id_owner', 'duration_hours']


@admin.register(DiscountHistory)
class DiscountHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'discount', 'all_users', 'user', 'enabled', 'start_date', 'stop_date']
    raw_id_fields = ('user', 'discount')


@admin.register(NotificationSystem)
class NotificationSystemAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'created', 'dt_start', 'dt_stop', 'text', 'description', 'new', 'verbal']


@admin.register(GameType)
class GameTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'verbal', 'caption', 'enabled']


@admin.register(MessWhatsapp)
class MessWhatsappAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'verbal', 'caption', 'id_instance', 'api_token', 'api_url', 'max_users']


@admin.register(TypeTicketType)
class TypeTicketTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'in_play', 'verbal', 'caption', 'order']


@admin.register(GameLottoResults)
class GameLottoResultsAdmin(admin.ModelAdmin):
    list_display = ['id', 'lotto_type', 'ticket_type', 'lottery_number', 'draw_date', 'result', 'win_money']


@admin.register(GameLottoProfit)
class GameLottoProfitAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'ticket_type', 'profit_type', 'profit_rounding', 'sum_from', 'sum_to',
                    'amount_profit', 'percent_profit']


@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'verbal', 'subject', 'text', 'layout_template', 'mail_template', 'parameters']


@admin.register(CommentCallcenter)
class CommentCallcenterAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_profile', 'creator', 'text', 'date_return', 'date_created']
    raw_id_fields = ('user_profile', 'creator')


@admin.register(LottoSubscription)
class LottoSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_owner', 'ticket_type', 'date_created', 'date_paid', 'enabled', 'games_count',
                    'infinity', 'automatic', 'ticket_info', 'ticket_cost_1', 'ticket_cost_2', 'subscription_cost']
    raw_id_fields = ('user_owner',)

