#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys, codecs, os

from el_t01.settings import BASE_DIR
from el_t01_app.models import Type_balanceoperation, Type_balanceoperation_status, Type_payment, \
    Type_currency, Type_program, SiteLang, Ticket_type, Devices_list, \
    Documentation_list, List_external_company, List_jellyfish, Report_list, \
    SiteSkin, EmailToSend, PayResponse, Faqtabl

t_Type_balanceoperation = Type_balanceoperation.objects.all()
t_Type_balanceoperation_status = Type_balanceoperation_status.objects.all()
t_Type_payment = Type_payment.objects.all()
t_Type_currency = Type_currency.objects.all()
t_Type_program = Type_program.objects.all()
t_SiteLang = SiteLang.objects.all()
t_Ticket_type = Ticket_type.objects.all()
t_Devices_list = Devices_list.objects.all()
t_Documentation_list = Documentation_list.objects.all()
t_List_external_company = List_external_company.objects.all()
t_List_jellyfish = List_jellyfish.objects.all()
t_Report_list = Report_list.objects.all()
t_SiteSkin = SiteSkin.objects.all()
t_EmailToSend = EmailToSend.objects.all()
t_PayResponse = PayResponse.objects.all()
t_Faqtabl = Faqtabl.objects.all()


text_1 = '{% trans "'
text_2 = '" %}\n'

t_dir = os.path.join(BASE_DIR, 'templates', 'transl')
print ('t_dir = ', t_dir)
t_file = os.path.join(BASE_DIR, 'templates', 'transl', 'trans_filled.html')
print ('t_file = ', t_file)

f_out = codecs.open(t_file, "w", encoding="utf-8")

f_out.write(u"---t_Type_balanceoperation ---\n")
for item_t in t_Type_balanceoperation :
    f_out.write("%s%s%s" % (text_1, item_t.caption, text_2 ) )

f_out.write(u"---t_Type_balanceoperation_status---\n")
for item_t in t_Type_balanceoperation_status:
    f_out.write("%s%s%s" % (text_1, item_t.caption, text_2 ) )

f_out.write(u"---t_Type_payment---\n")
for item_t in t_Type_payment:
    f_out.write("%s%s%s" % (text_1, item_t.caption, text_2 ) )
    if item_t.description_01:
        f_out.write("%s%s%s" % (text_1, item_t.description_01, text_2))
    if item_t.description_02:
        f_out.write("%s%s%s" % (text_1, item_t.description_02, text_2))
    if item_t.txt_warning:
        f_out.write("%s%s%s" % (text_1, item_t.txt_warning, text_2))

f_out.write(u"---t_Type_currency---\n")
for item_t in t_Type_currency:
    f_out.write("%s%s%s" % (text_1, item_t.code, text_2 ) )
    f_out.write("%s%s%s" % (text_1, item_t.caption, text_2 ) )
    if item_t.description:
        f_out.write("%s%s%s" % (text_1, item_t.description, text_2))

f_out.write(u"---t_Type_program---\n")
for item_t in t_Type_program:
    f_out.write("%s%s%s" % (text_1, item_t.caption, text_2 ) )
    f_out.write("%s%s%s" % (text_1, item_t.description, text_2 ) )

f_out.write(u"---t_SiteLang---\n")
for item_t in t_SiteLang:
    f_out.write("%s%s%s" % (text_1, item_t.lang_name, text_2 ) )
    f_out.write("%s%s%s" % (text_1, item_t.lang_code, text_2 ) )

f_out.write(u"---t_Ticket_type---\n")
for item_t in t_Ticket_type:
    f_out.write("%s%s%s" % (text_1, item_t.caption, text_2 ) )
    if item_t.description_01:
        f_out.write("%s%s%s" % (text_1, item_t.description_01, text_2))
    if item_t.description_02:
        f_out.write("%s%s%s" % (text_1, item_t.description_02, text_2))
    if item_t.description_03:
        f_out.write("%s%s%s" % (text_1, item_t.description_03, text_2))
    if item_t.description_04:
        f_out.write("%s%s%s" % (text_1, item_t.description_04, text_2))
    if item_t.description_05:
        f_out.write("%s%s%s" % (text_1, item_t.description_05, text_2))

f_out.write(u"---t_Devices_list---\n")
for item_t in t_Devices_list:
    f_out.write("%s%s%s" % (text_1, item_t.caption, text_2 ) )

f_out.write(u"---t_Documentation_list---\n")
for item_t in t_Documentation_list:
    f_out.write("%s%s%s" % (text_1, item_t.caption, text_2 ) )
    f_out.write("%s%s%s" % (text_1, item_t.description, text_2 ) )

f_out.write(u"---t_List_external_company---\n")
for item_t in t_List_external_company:
    f_out.write("%s%s%s" % (text_1, item_t.caption, text_2 ) )

f_out.write(u"---t_List_jellyfish---\n")
for item_t in t_List_jellyfish:
    f_out.write("%s%s%s" % (text_1, item_t.caption, text_2 ) )

f_out.write(u"---t_Report_list---\n")
for item_t in t_Report_list:
    f_out.write("%s%s%s" % (text_1, item_t.caption, text_2 ) )

f_out.write(u"---t_SiteSkin---\n")
for item_t in t_SiteSkin:
    f_out.write("%s%s%s" % (text_1, item_t.name, text_2 ) )


f_out.write(u"---t_Faqtabl---\n")
for item_t in t_Faqtabl:
    f_out.write("%s%s%s" % (text_1, item_t.faq_title, text_2 ) )
    if item_t.faq_info:
        f_out.write("%s%s%s" % (text_1, item_t.faq_info , text_2))


# f_out.write(u"---t_EmailToSend---\n")
# for item_t in t_EmailToSend:
#     pass
#     # f_out.write("%s%s%s" % (text_1, item_t.code, text_2 ) )
#
# f_out.write(u"---t_PayResponse---\n")
# for item_t in t_PayResponse:
#     pass
#     # f_out.write("%s%s%s" % (text_1, item_t.code, text_2 ) )
#
f_out.write(u"------\n")

f_out.close()
