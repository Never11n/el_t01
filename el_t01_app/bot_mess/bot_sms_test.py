#! /usr/bin/env python
# -*- coding: utf-8 -*-


import bot_config_telegram as telegram_config
import telebot

# 269227574 i
# 691868702 ivam
# 780668678
# 663389884 Настя
# Vika 1039901510

bot = telebot.TeleBot(telegram_config.token)
# m_adress = Item_t_UserModerator.telegram_id
# m_adress =  691868702
# m_text = "GOD LiKE ISRAEL"
# print ("bot.send_message", m_adress, m_text)
# bot.send_message(m_adress, m_text, parse_mode='html')
#
# m_adress =  780668678
# m_text = "GOD LiKE ISRAEL ticket = 354646354 , URGENT 10000"
# print ("bot.send_message", m_adress, m_text)
# bot.send_message(m_adress, m_text, parse_mode='html')
#


m_adress =  269227574
m_text = "VIKA VREDINA"
print ("bot.send_message", m_adress, m_text)
bot.send_message(m_adress, m_text, parse_mode='html')


m_adress =  1039901510
m_text = "VIKA VREDINA"
print ("bot.send_message", m_adress, m_text)
bot.send_message(m_adress, m_text, parse_mode='html')


#
#
# def create_ad_notification_subscr(ad_id, type_verbal):
#     ## для тендеров t_UserSubscription = UserPaidSubscription.objects.filter(user_id=args['me'].id, type_category='00').exclude(status_code=0)
#     if type_verbal == "new_ad_subscr_notification":
#         try:
#             ad = Ad.objects.get(id=int(ad_id))
#             # если все украинское то не берем регион
#             # выбрать список клиентов которые подписались и по списку сформировать извещения
#             #user_id -- для какого пользователя
#             #new -- новое сообщение или старое
#             #type_verbal -- тип сообщения
#             #created -- дата создания
#             #tender = models.ForeignKey(Tender -- ссылка на тендер
#             #ad = models.ForeignKey(Ad -- ссылка на обявление
#             #applicants_count -- ???
#             t_UserSubscription = []
#             if ad.for_all_city :
#                 _t_UserSubscription = UserPaidSubscription.objects.filter(parent_category_id=ad.parent_category_id, category_id=ad.category_id, subcategory_id=ad.subcategory_id, type_category='01').exclude(status_code=0)
#                 for Item_t_UserSubscription in _t_UserSubscription:
#                     t_UserSubscription.append({"s_id": Item_t_UserSubscription.id, "user_id":Item_t_UserSubscription.user_id, "caption":Item_t_UserSubscription.caption })
#             else:
#                 #_t_UserSubscription = UserPaidSubscription.objects.filter(parent_category_id=ad.parent_category_id, category_id=ad.category_id, subcategory_id=ad.subcategory_id, region_id=ad.region_id, city_id=ad.city_id, type_category='01').exclude(status_code=0)
#                 _t_UserSubscription = UserPaidSubscription.objects.filter(parent_category_id=ad.parent_category_id, category_id=ad.category_id, subcategory_id=ad.subcategory_id, region_id=ad.region_id, type_category='01').exclude(status_code=0)
#                 print ("3")
#                 for Item_t_UserSubscription in _t_UserSubscription:
#                     print ("4")
#                     if Item_t_UserSubscription.city_id is None:
#                         t_UserSubscription.append({"s_id": Item_t_UserSubscription.id, "user_id": Item_t_UserSubscription.user_id, "caption": Item_t_UserSubscription.caption})
#                     else:
#                         if Item_t_UserSubscription.city_id == ad.city_id:
#                             t_UserSubscription.append({"s_id": Item_t_UserSubscription.id, "user_id": Item_t_UserSubscription.user_id, "caption": Item_t_UserSubscription.caption})
#                     print ("5")
#                     # , city_id=ad.city_id
#             print ("6", len(t_UserSubscription))
#             if len(t_UserSubscription) > 0:
#                 print ("7")
#                 n = Notification()
#                 for ItemSubscr in t_UserSubscription:
#                     print ("1 = ", ItemSubscr )
#                     owner_subscr = Profile.objects.get(user=ItemSubscr["user_id"])
#                     m_list_messenger = owner_subscr.list_messenger
#                     try:
#                         m_list_messenger = json.loads(m_list_messenger)
#                         m_notification_on_email = m_list_messenger.get('reg_check_3_1', False)
#                     except:
#                         m_list_messenger = {}
#                         m_notification_on_email = False
#
#                     s_ad = SubscriptionAd()
#                     s_ad.subscription_id = ItemSubscr["s_id"]
#                     s_ad.ad_id = ad_id
#                     s_ad.save()
#
#                     create_notification_on_mesenger(ItemSubscr["user_id"], "new_ad_subscr_notification", ItemSubscr["caption"])
#
# #                    if m_notification_on_email:
# #                        send_mail_new_ad_subscr_notification(ItemSubscr["user_id"], ItemSubscr["caption"] )
#
#                     n.user_id = ItemSubscr["user_id"]
#                     n.ad_id = ad.id
#                     n.type_verbal = str(type_verbal)
#                     n.save()
#
#         except Exception as e:
#             report_exception('create_ad_notification', e.message)
#     elif type_verbal == "new_tender_subscr_notification":
#         pass
#     else:
#         try:
#             ad = Ad.objects.get(id=int(ad_id))
#             n = Notification()
#             n.user_id = ad.creator.id
#             n.ad_id = ad.id
#             n.type_verbal = str(type_verbal)
#             n.save()
#         except Exception as e:
#             report_exception('create_ad_notification', e.message)
#
#
# def create_tender_notification_subscr(tender_id, type_verbal):
#     print ("create_tender_notification_subscr")
#     ## для тендеров t_UserSubscription = UserPaidSubscription.objects.filter(user_id=args['me'].id, type_category='00').exclude(status_code=0)
#     if type_verbal == "new_tender_subscr_notification":
#         print ("create_tender_notification_subscr -- 11")
#         try:
#             tender = Tender.objects.get(id=int(tender_id))
#             # если все украинское то не берем регион
#             # выбрать список клиентов которые подписались и по списку сформировать извещения
#             #user_id -- для какого пользователя
#             #new -- новое сообщение или старое
#             #type_verbal -- тип сообщения
#             #created -- дата создания
#             #tender = models.ForeignKey(Tender -- ссылка на тендер
#             #ad = models.ForeignKey(Ad -- ссылка на обявление
#             #applicants_count -- ???
#             t_UserSubscription = []
#             if tender.for_all_city :
#                 _t_UserSubscription = UserPaidSubscription.objects.filter(parent_category_id=tender.parent_category_id, category_id=tender.category_id, subcategory_id=tender.subcategory_id, type_category='00').exclude(status_code=0)
#                 for Item_t_UserSubscription in _t_UserSubscription:
#                     t_UserSubscription.append({"s_id": Item_t_UserSubscription.id, "user_id":Item_t_UserSubscription.user_id, "caption":Item_t_UserSubscription.caption })
#             else:
#                 #_t_UserSubscription = UserPaidSubscription.objects.filter(parent_category_id=ad.parent_category_id, category_id=ad.category_id, subcategory_id=ad.subcategory_id, region_id=ad.region_id, city_id=ad.city_id, type_category='01').exclude(status_code=0)
#                 _t_UserSubscription = UserPaidSubscription.objects.filter(parent_category_id=tender.parent_category_id,
#                                                                           category_id=tender.category_id,
#                                                                           subcategory_id=tender.subcategory_id,
#                                                                           type_category='00').exclude(status_code=0)
#                 print ("3")
#                 for Item_t_UserSubscription in _t_UserSubscription:
#                     print ("4")
#                     if Item_t_UserSubscription.city_id is None:
#                         t_UserSubscription.append({"s_id": Item_t_UserSubscription.id, "user_id": Item_t_UserSubscription.user_id, "caption": Item_t_UserSubscription.caption})
#                     else:
#                         if Item_t_UserSubscription.city_id == tender.city_id:
#                             t_UserSubscription.append({"s_id": Item_t_UserSubscription.id, "user_id": Item_t_UserSubscription.user_id, "caption": Item_t_UserSubscription.caption})
#                     print ("5")
#                     # , city_id=ad.city_id
#             print ("6", len(t_UserSubscription))
#             if len(t_UserSubscription) > 0:
#                 print ("7")
#                 n = Notification()
#                 for ItemSubscr in t_UserSubscription:
#                     print ("1 = ", ItemSubscr )
#                     owner_subscr = Profile.objects.get(user=ItemSubscr["user_id"])
#                     m_list_messenger = owner_subscr.list_messenger
#                     try:
#                         m_list_messenger = json.loads(m_list_messenger)
#                         m_notification_on_email = m_list_messenger.get('reg_check_3_1', False)
#                     except:
#                         m_list_messenger = {}
#                         m_notification_on_email = False
#
#                     s_tender = SubscriptionTender()
#                     s_tender.subscription_id = ItemSubscr["s_id"]
#                     s_tender.tender_id = tender_id
#                     s_tender.save()
#
#                     create_notification_on_mesenger(ItemSubscr["user_id"], "new_tender_subscr_notification", ItemSubscr["caption"])
#
# #                    if m_notification_on_email:
# #                        send_mail_new_ad_subscr_notification(ItemSubscr["user_id"], ItemSubscr["caption"] )
#
#                     n.user_id = ItemSubscr["user_id"]
#                     n.tender_id = tender.id
#                     n.type_verbal = str(type_verbal)
#                     n.save()
#
#         except Exception as e:
#             report_exception('create_ad_notification', e.message)
#     else:
#         try:
#             ad = Ad.objects.get(id=int(ad_id))
#             n = Notification()
#             n.user_id = ad.creator.id
#             n.ad_id = ad.id
#             n.type_verbal = str(type_verbal)
#             n.save()
#         except Exception as e:
#             report_exception('create_ad_notification', e.message)
#
#
# def create_ad_notification(ad_id, type_verbal):
#     # отсылка сообщения ( на входе ID объявления и тип сообщения )
#     # запускаем функцию отправки на мессенджер ( ID пользователя и тип сообщения )
#     print ("create_ad_notification = ", ad_id, type_verbal)
#     try:
#         t_ad = Ad.objects.get(id=int(ad_id))
#         m_caption = ""
#         m_lang = t_ad.language
#
#         try:
#             m_caption_cat_par = t_ad.parent_category.caption
#             m_caption = m_caption_cat_par
#         except:
#             m_caption_cat_par = ""
#         print ("11")
#         try:
#             m_caption_cat = t_ad.category.caption
#             m_caption = m_caption + " - " + m_caption_cat
#         except:
#             m_caption_cat = ""
#         print ("22")
#         try:
#             m_caption_cat_sub = t_ad.subcategory.caption
#             m_caption = m_caption + " - " + m_caption_cat_sub
#         except:
#             m_caption_cat_sub = ""
#         print ("33")
#
#         if m_caption != "":
#             m_caption = '"' + m_caption + '"'
#
#         print ("44-1 ", m_caption)
#         print ("44-2 ", t_ad.created.strftime("%d.%m.%Y"), type(t_ad.created.strftime("%d.%m.%Y")) )
#
#         loc_lang = m_lang
#         if loc_lang == 'ru' or loc_lang == 'ua':
#             pass
#         else:
#             loc_lang = 'ua'
#
#         m_old_lang = translation.get_language()
#         translation.activate(loc_lang)
#
#         m_caption = m_caption + ' ' + gettext(u'от') + ' ' + t_ad.created.strftime("%d.%m.%Y")
#         print ("44")
#         translation.activate(m_old_lang)
#
#         '''
#         user_id = models.IntegerField(default=0)
#         new = models.BooleanField(default=True)
#         type_verbal = models.CharField(default='', blank=True, null=True, max_length=100)
#         created = models.DateTimeField(auto_now_add=True, null=False)
#         tender = models.ForeignKey(Tender, related_name='notification_tender_relation', null=True)
#         ad = models.ForeignKey(Ad, related_name='notification_ad_relation', null=True)
#         applicants_count = models.IntegerField(default=0)
#         view = models.BooleanField(default=False)
#         '''
#         n = Notification()
#         n.user_id = t_ad.creator.id
#         n.ad_id = t_ad.id
#         n.type_verbal = str(type_verbal)
#         n.save()
#         create_notification_on_mesenger(t_ad.creator.id, type_verbal, m_caption, m_lang )
#         print ("8=")
#     except Exception as e:
#         report_exception('create_ad_notification', e.message)
#
#
# def create_tender_notification(tender_id, type_verbal, loc_last_oferta_user=0 ):
#     # отсылка сообщения ( на входе ID тендера и тип сообщения )
#     # запускаем функцию отправки на мессенджер ( ID пользователя и тип сообщения )
#     print ("create_tender_notification = ", tender_id, type_verbal)
#     try:
#         tender = Tender.objects.get(id=int(tender_id))
#         m_lang = tender.language
#         if loc_last_oferta_user == 0:
#             m_tender_creator_id = tender.creator.id
#         else:
#             m_tender_creator_id = loc_last_oferta_user
#
#         n = Notification()
#         n.user_id = m_tender_creator_id
#         n.tender_id = tender.id
#         n.type_verbal = str(type_verbal)
#         n.save()
#
#         create_notification_on_mesenger(m_tender_creator_id, type_verbal, tender.caption, m_lang, tender.price)
#         print ("8=")
#     except Exception as e:
#         report_exception('create_tender_notification', e.message)
#
# def create_notification_feedback(user_id, type_verbal, loc_lang='ua'):
#     # отсылка сообщения ( на входе ID пользователя и тип сообщения )
#     # запускаем функцию отправки на мессенджер ( ID пользователя и тип сообщения )
#     print ("create_notification_feedback = ", user_id, type_verbal, loc_lang)
#     try:
#         n = Notification()
#         n.user_id = user_id
#         n.type_verbal = str(type_verbal)
#         n.save()
#         create_notification_on_mesenger(user_id, type_verbal, '', loc_lang)
#     except Exception as e:
#         report_exception('create_tender_notification', e.message)
#
#
# def create_simple_notification(user_id, type_verbal):
#     try:
#         n = Notification()
#         n.user_id = user_id
#         n.type_verbal = str(type_verbal)
#         n.save()
#     except Exception as e:
#         report_exception('create_tender_notification', e.message)
#
#
# def notifications(request):
#     args = fetch_user_data(request)
#     if not args['logged_in']:
#         return redirect('/login')
#     p = 1
#     if 'p' in request.GET:
#         p = int(request.GET['p'])
#
#     print ("args['me'].id = ", args['me'].id)
# #    all_notifications = Notification.objects.filter(user_id=args['me'].id)
# #    for n in all_notifications :
# #        if n.new == True and n.view == True:
# #            n.new = False
# #       n.view = True
# #       n.save()
#
#     Notification.objects.filter(user_id=args['me'].id, new=True, view=True, enabled=True).update(new=False)
#     Notification.objects.filter(user_id=args['me'].id, view=False, enabled=True).update(view=True)
#
#     old_notifications = Notification.objects.filter(user_id=args['me'].id, new=False, enabled=True).order_by("-created")
#     args['old_notifications'] = old_notifications
#     print ("old_notifications", old_notifications.count() )
#
#     new_notifications = Notification.objects.filter(user_id=args['me'].id, new=True, enabled=True).order_by("-created")
#     args['new_notifications'] = new_notifications
#     print ("new_notifications", new_notifications.count() )
#
#     # items = Notification.objects.filter(user_id=args['me'].id, new=True)
#
#     # args['notifications'] = items
#     # if items.count() > 0:
#     #     args['notifications'] = paginate(items, p, 10)
#     #     try:
#     #         for i in args['notifications'].object_list:
#     #             n = Notification.objects.get(id=i.id)
#     #             n.new = False
#     #             n.save()
#     #         update_user_counters(args['me'].id)
#     #     except Exception as ex:
#     #         print 'error while set notifications to old'
#     return render_to_response('notifications/notifications.html', args)
#
# def create_notification_on_mesenger(loc_user_id, loc_type_verbal, loc_caption='', loc_lang='ua', loc_price='' ):
#     # запускаем функцию отправки на мессенджер ( ID пользователя и тип сообщения )
#     # проверить у пользователя если стоит отсылать на мессенджер почту запускаем
#     print ("create_notification_on_mesenger")
#     # у пользователя берем спсиок мессенджеров
#     # проверить у пользователя если стоит отсылать сообщение на мессенджер запускаем
#     # ПОEMAIL VIBER TELEGRAM
#     # переключаем на указаный язык loc_lang , в конце вернутся на старый язык
#
#     # список глобальных настроек мессенджеров
#     '''
#     id order enabled name      logo              control_enabled  mess_func
#     1  0     1       e-mail    ico_email.png     0                func_mail
#     2  2     1       Viber     ico_viber.png     1                func_viber
#     3  3     1       Telegram  ico_telegram.png  1                func_telegram
#     4  4     0       WhatsApp  ico_whatsapp.png  1                func_whatsapp
#     '''
#     if loc_lang == 'ru' or loc_lang == 'ua':
#         pass
#     else:
#         loc_lang = 'ua'
#
#     m_old_lang = translation.get_language()
#     print ("loc_lang   =", loc_lang )
#     print ("m_old_lang =", m_old_lang )
#     translation.activate(loc_lang)
#
#     print ("001")
#
#     try:
#         m_messglob_bool_email = TablMessenger.objects.get(name="e-mail").enabled
#         m_messglob_code_email = TablMessenger.objects.get(name="e-mail").id
#     except:
#         m_messglob_bool_email = False
#         m_messglob_code_email = 0
#
#     print ("002")
#
#     try:
#         m_messglob_bool_viber = TablMessenger.objects.get(name="Viber").enabled
#         m_messglob_code_viber = TablMessenger.objects.get(name="Viber").id
#     except:
#         m_messglob_bool_viber = False
#         m_messglob_code_viber = 0
#
#     print ("003")
#
#     try:
#         m_messglob_bool_teleg = TablMessenger.objects.get(name="Telegram").enabled
#         m_messglob_code_teleg = TablMessenger.objects.get(name="Telegram").id
#     except:
#         m_messglob_bool_teleg = False
#         m_messglob_code_teleg = 0
#
#     print ("004")
#
#     try:
#         m_messglob_bool_watsapp = TablMessenger.objects.get(name="WhatsApp").enabled
#         m_messglob_code_watsapp = TablMessenger.objects.get(name="WhatsApp").id
#     except:
#         m_messglob_bool_watsapp = False
#         m_messglob_code_watsapp = 0
#
#     print ("cnm 1")
#
#     # для разных типов сообщений выбераем настройку
#     m_typemes_email = 0
#     m_typemes_viber = 0
#     m_typemes_teleg = 0
#     m_typemes_watsapp = 0
#     m_templ_mail = ""
#     m_Subscr_caption = ""
#     m_Subscr_price = 0
#     m_subject = ""
#     m_text_add_telegram = ''
#     if loc_type_verbal == "new_ad_subscr_notification":
#         m_typemes_email = 3
#         m_typemes_viber = 3
#         m_typemes_teleg = 3
#         m_typemes_watsapp = 3
#         m_templ_mail = 'mail/your_new_ad_subscr_notification.html'
#         m_Subscr_caption = loc_caption
#         m_subject = gettext(u'СтройБук - Новое объявление по подписке')
#         m_text_add_telegram = gettext(u'По Вашей подписке есть новое объявление.')
#     elif loc_type_verbal == "tender_will_be_closed":
#         m_typemes_email = 1
#         m_typemes_viber = 1
#         m_typemes_teleg = 1
#         m_typemes_watsapp = 1
#         m_templ_mail = 'mail/tender_will_be_closed.html'
#         m_Subscr_caption = loc_caption
#         m_subject = gettext(u'СтройБук - Окончание торгов')
#         m_text_add_telegram = gettext(u'Торги по Вашему тендеру') +' "'+ m_Subscr_caption +'" '+ gettext(u'закрываются через 1 день.')
#     elif loc_type_verbal == "ad_will_be_closed":
#         m_typemes_email = 1
#         m_typemes_viber = 1
#         m_typemes_teleg = 1
#         m_typemes_watsapp = 1
#         m_templ_mail = 'mail/ad_will_be_closed.html'
#         m_Subscr_caption = loc_caption
#         m_subject = gettext(u'СтройБук - Окончание срока публикации')
#         m_text_add_telegram = gettext(u'Публикация Вашего объявления') +' '+ m_Subscr_caption +' '+ gettext(u'заканчивается через 1 день.')
#     elif loc_type_verbal == "tender_finished":
#         m_typemes_email = 1
#         m_typemes_viber = 1
#         m_typemes_teleg = 1
#         m_typemes_watsapp = 1
#         m_templ_mail = 'mail/tender_finished.html'
#         m_Subscr_caption = loc_caption
#         m_subject = gettext(u'СтройБук - Тендер завершен')
#         m_text_add_telegram = gettext(u'Торги по Вашему тендеру') + ' "' + m_Subscr_caption + '" ' + gettext(
#             u'завершены.')
#     elif loc_type_verbal == "tender_finished_2":
#         m_typemes_email = 1
#         m_typemes_viber = 1
#         m_typemes_teleg = 1
#         m_typemes_watsapp = 1
#         m_templ_mail = 'mail/tender_finished.html'
#         m_Subscr_caption = loc_caption
#         m_subject = gettext(u'СтройБук - Тендер завершен')
#         m_text_add_telegram = gettext(u'Торги по Вашему тендеру') + ' "' + m_Subscr_caption + '" ' + gettext(
#             u'завершены.')
#     elif loc_type_verbal == "ad_finished":
#         m_typemes_email = 1
#         m_typemes_viber = 1
#         m_typemes_teleg = 1
#         m_typemes_watsapp = 1
#         m_templ_mail = 'mail/ad_finished.html'
#         m_Subscr_caption = loc_caption
#         m_subject = gettext(u'СтройБук - Срок публикации завершён')
#         m_text_add_telegram = gettext(u'Срок публикации Вашего объявления') +' '+ m_Subscr_caption +' '+ gettext(u'завершён.')
#
#     elif loc_type_verbal == "tender_published":
#         m_typemes_email = 1
#         m_typemes_viber = 1
#         m_typemes_teleg = 1
#         m_typemes_watsapp = 1
#         m_templ_mail = 'mail/tender_published.html'
#         m_Subscr_caption = loc_caption
#         m_subject = gettext(u'СтройБук - Публикация тендера')
#         m_text_add_telegram = gettext(u'Ваше Тендерное задание') +' "'+ m_Subscr_caption +'" '+ gettext(u'успешно опубликовано.')
#
#     elif loc_type_verbal == "tender_not_published":
#         m_typemes_email = 1
#         m_typemes_viber = 1
#         m_typemes_teleg = 1
#         m_typemes_watsapp = 1
#         m_templ_mail = 'mail/tender_not_published.html'
#         m_Subscr_caption = loc_caption
#         m_subject = gettext(u'СтройБук - Публикация тендера')
#         m_text_add_telegram = gettext(u'Ваш тендер') +' "'+ m_Subscr_caption +'" '+ gettext(u'был отклонен. Необходимо ознакомиться с правилами публикации тендеров.')
#
#     elif loc_type_verbal == "new_tender_application":
#         m_typemes_email = 1
#         m_typemes_viber = 1
#         m_typemes_teleg = 1
#         m_typemes_watsapp = 1
#         m_templ_mail = 'mail/tender_applicant.html'
#         m_Subscr_caption = loc_caption
#         m_Subscr_price = str(loc_price)
#         m_subject = gettext(u'СтройБук - Новая оферта')
#         #m_text_add_telegram = gettext(u'По Вашему тендеру') +' "'+ m_Subscr_caption +'" '+ gettext(u'есть новое предложение - ') + ' tender.price ' + ' грн.'
#         m_text_add_telegram = gettext(u'По Вашему тендеру') + ' "' + m_Subscr_caption + '" ' + gettext(u'есть новая оферта - ') + m_Subscr_price + ' ' + CURRENT_SITE_CURRENCY
#
#     elif loc_type_verbal == "tender_perebit":
#         m_typemes_email = 1
#         m_typemes_viber = 1
#         m_typemes_teleg = 1
#         m_typemes_watsapp = 1
#         m_templ_mail = 'mail/tender_perebit.html'
#         m_Subscr_caption = loc_caption
#         m_Subscr_price = str(loc_price)
#         m_subject = gettext(u'СтройБук - Оферта перебита')
#         #m_text_add_telegram = gettext(u'По Вашему тендеру') +' "'+ m_Subscr_caption +'" '+ gettext(u'есть новое предложение - ') + ' tender.price ' + ' грн.'
#         m_text_add_telegram = gettext(u'Ваша оферта по тендеру') +' "'+ m_Subscr_caption +'" '+ gettext(u'перебита')
#
#     elif loc_type_verbal == "new_tender_subscr_notification":
#         m_typemes_email = 3
#         m_typemes_viber = 3
#         m_typemes_teleg = 3
#         m_typemes_watsapp = 3
#         m_templ_mail = 'mail/your_new_tender_subscr_notification.html'
#         m_Subscr_caption = loc_caption
#         m_subject = gettext(u'СтройБук - Новый тендер по подписке')
#         m_text_add_telegram = gettext(u'По Вашей подписке есть новый тендер.') +' "'+ m_Subscr_caption +'" '
#
#     elif loc_type_verbal == "feedback_replay":
#         print ("feedback_replay feedback_replay 0001")
#         m_typemes_email = 0
#         m_typemes_viber = 3
#         m_typemes_teleg = 3
#         m_typemes_watsapp = 3
#         m_templ_mail = ''
#         m_Subscr_caption = loc_caption
#         m_subject = ''
#         m_text_add_telegram = gettext(u'По Вашему обращению Вам отправлен ответ на почту.')
#
#     else:
#         m_typemes_email = 0
#         m_typemes_viber = 0
#         m_typemes_teleg = 0
#         m_typemes_watsapp = 0
#         m_templ_mail = ""
#         m_Subscr_caption = ""
#         m_subject = ""
#         m_text_add_telegram = ''
#
#     print ("cnm 2")
#     # список настроек мессенджеров для пользователя
#     owner_notification = Profile.objects.get(user=loc_user_id)
#     m_list_messenger = owner_notification.list_messenger
#     try:
#         m_list_messenger = json.loads(m_list_messenger)
#     except:
#         m_list_messenger = {}
#
#     print ("cnm 3", "m_list_messenger = ", m_list_messenger)
#
#     m_messuser_bool_email = m_list_messenger.get('reg_check_%s_%s' % ( m_typemes_email, m_messglob_code_email ), False)
#     m_messuser_bool_viber = m_list_messenger.get('reg_check_%s_%s' % ( m_typemes_viber, m_messglob_code_viber ), False)
#     m_messuser_bool_teleg = m_list_messenger.get('reg_check_%s_%s' % ( m_typemes_teleg, m_messglob_code_teleg ), False)
#     m_messuser_bool_watsapp = m_list_messenger.get('reg_check_%s_%s' % ( m_typemes_watsapp, m_messglob_code_watsapp ), False)
#
#     print ("cnm 4")
#     print ("loc_user_id             = ", loc_user_id)
#     print ("m_typemes_teleg         = ", m_typemes_teleg)
#     print ("m_messglob_code_teleg   = ", m_messglob_code_teleg)
#     print ("m_messuser_bool_email   = ", m_messuser_bool_email )
#     print ("m_messuser_bool_viber   = ", m_messuser_bool_viber )
#     print ("m_messuser_bool_teleg   = ", m_messuser_bool_teleg )
#     print ("m_messuser_bool_watsapp = ", m_messuser_bool_watsapp )
#
#     if m_messglob_bool_email and m_messuser_bool_email :
#         print ("77-1")
#         user = User.objects.get(id=loc_user_id)
#         print ("77-71", user.email)
#         print ("77-72", m_subject)
#         print ("77-73", m_templ_mail)
#         print ("77-74", {'user': user, 'm_Subscr_caption': m_Subscr_caption})
#
#         save_and_send_email(user.email, m_subject ,
#                                 m_templ_mail,
#                                 {'user': user,
#                                  'm_Subscr_caption': m_Subscr_caption,
#                                  'm_Subscr_price': m_Subscr_price
#                                  }
#                             )
#         print ("77-2")
#
#     if m_messglob_bool_viber and m_messuser_bool_viber :
#         #send_viber(ItemSubscr["user_id"], ItemSubscr["caption"] )
#         pass
#     print ("m_messglob_bool_teleg and m_messuser_bool_teleg = ",  m_messglob_bool_teleg, m_messuser_bool_teleg)
#     if m_messglob_bool_teleg and m_messuser_bool_teleg :
#         print ("TELEGRAM ", owner_notification.telegram_id)
#         print ("loc_user_id = ", loc_user_id)
#         print ("telegram_id = " , owner_notification.telegram_id )
#
#         if owner_notification.telegram_id > 0:
#             bot = telebot.TeleBot(telegram_config.token)
#             m_text = m_text_add_telegram  + '\n' + gettext(u'<b>С уважением, Администрация СтройБук</b>.')
#             m_adress = owner_notification.telegram_id
#             bot.send_message(m_adress, m_text, parse_mode='html')
#     if m_messglob_bool_watsapp and m_messuser_bool_watsapp :
#         pass
#
#     translation.activate(m_old_lang)
#     return
#
# def delete_notif(request):
#     print ("tender_favorite_delete")
#     args = fetch_user_data ( request )
#     try:
#         t_note = Notification.objects.get( id=int(request.GET['notif']), user_id=args['me'].id)
#         t_note.enabled = False
#         t_note.save()
#         data = {"result": 'ok'}
#         return HttpResponse('ok')
#     except:
#         data = {"result": 'error'}
#         #return JsonResponse(data)
#         return HttpResponse('ok')
#
# def send_telegram_moderator(loc_typemes='', loc_textmes='' ):
#     print ("send_telegram_moderator", loc_typemes)
#     t_UserModerator = []
#     if loc_typemes == "new_tender":
#         t_UserModerator = Profile.objects.filter(mod_mes_tender=True)
#         m_text_add_telegram = u'Есть новый тендер на модерации'
#         m_text = m_text_add_telegram
#     if loc_typemes == "new_feedback":
#         t_UserModerator = Profile.objects.filter(mod_mes_feedback=True)
#         m_text_add_telegram = u'Есть новое сообщение FEEDBACK'
#         m_text = m_text_add_telegram
#     if loc_typemes == "new_block_ad":
#         t_UserModerator = Profile.objects.filter(mod_mes_feedback=True)
#         m_text_add_telegram = u'Есть заблокированное объявление'
#         m_text = m_text_add_telegram
#
#     for Item_t_UserModerator in t_UserModerator:
#         if Item_t_UserModerator.telegram_id > 0:
#         #if Item_t_UserModerator.telegram_id != "":
#             bot = telebot.TeleBot(telegram_config.token)
#             m_adress = Item_t_UserModerator.telegram_id
#             print ("bot.send_message", m_adress, m_text )
#             try:
#                 bot.send_message(m_adress, m_text, parse_mode='html')
#             except:
#                 pass
#
#
#
