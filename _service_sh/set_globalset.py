#! /usr/bin/env python
# -*- coding: utf-8 -*-
from el_t01_app.models import Globalset
print ('------ Start Globalset ------')

m_list_globalparam = []

if True:
    # Main Param
    m_list_globalparam.append({"name":"Name_Company", "type":"txt", "val":"--Scratch--"})
    # SKIN
    m_list_globalparam.append({"name":"MainSkin", "type":"txt", "val":"003"})
    # TITLE
    m_list_globalparam.append({"name":"PageMain", "type":"txt", "val":"lending"})
    m_list_globalparam.append({"name":"PageMain_Title", "type":"txt", "val":"SOD|Machine control"})
    m_list_globalparam.append({"name":"PageMain_DESCRIPTION", "type":"txt", "val":"SOD|Machine control"})
    m_list_globalparam.append({"name":"PageCabinet_Title", "type":"txt", "val":"SOD|Machine control"})
    m_list_globalparam.append({"name":"PageCabinet_DESCRIPTION", "type":"txt", "val":"SOD|Machine control"})
    # Aboutus
    m_list_globalparam.append({"name":"Aboutus_Company", "type":"txt", "val":"New Sports and Marketing Ltd."})
    m_list_globalparam.append({"name":"Aboutus_Contact_Phone", "type":"txt", "val":"026364666"})
    m_list_globalparam.append({"name":"Aboutus_Cont"
                                      "ъact_Fax", "type":"txt", "val":"026364665"})
    m_list_globalparam.append({"name":"Aboutus_E-mail", "type":"txt", "val":"shmulik222@gmail.com"})
    m_list_globalparam.append({"name":"Aboutus_Adress", "type":"txt", "val":"haoman 24 Jerusalem"})

    m_list_globalparam.append({"name":"Movie_prepare", "type":"txt", "val":"scretch_01.mp4"})
    m_list_globalparam.append({"name":"Movie_list", "type":"txt", "val":"scretch_01.mp4"})
    # Whatsapp
    m_list_globalparam.append({"name":"Whatsapp_call_centr_phone", "type":"txt", "val":"+9720534751616"})
    m_list_globalparam.append({"name":"Whatsapp_apilist", "type":"txt", "val":"[{'':'', '':''}]"})
    # Sms Group
    m_list_globalparam.append({"name":"SMS_domen", "type":"txt", "val":"https://winwin-hishgad.co.il/"})
    m_list_globalparam.append({"name":"SMS_from", "type":"txt", "val":"WinWin"})
    m_list_globalparam.append({"name":"SMS_footer_name", "type":"txt", "val":"Israel"})
    m_list_globalparam.append({"name":"SMS_footer_phone", "type":"txt", "val":"0543139995"})
    m_list_globalparam.append({"name":"SMS_tuser", "type":"txt", "val":"scrach445"})
    m_list_globalparam.append({"name":"SMS_tpass", "type":"txt", "val":"scrach854"})
    # Tranzila
    m_list_globalparam.append({"name":"UrlTranzilaTerminalDirect", "type":"txt", "val":"https://direct.tranzila.com/scratch/iframenew.php"})
    m_list_globalparam.append({"name":"UrlTranzilaTerminalBit", "type":"txt", "val":"https://direct.tranzila.com/shmulik3355ch/iframenew.php"})
    m_list_globalparam.append({"name":"UrlTranzilaTerminalCCIFrame", "type":"txt", "val":"https://direct.tranzila.com/shmulik3355ch/iframenew.php"})
    m_list_globalparam.append({"name":"UrlTranzilaTerminalAplePay", "type":"txt", "val":"https://direct.tranzila.com/shmulik3355ch/iframenew.php"})
    m_list_globalparam.append({"name":"Tranzila_AplePay_type", "type":"txt", "val":"iframenew"})
    m_list_globalparam.append({"name":"TranzilaSupplier", "type":"txt", "val":"udaci2"})
    m_list_globalparam.append({"name":"Tranzila_CreditCard_type", "type":"txt", "val":"direct"})
    # Tranzila SUBS
    m_list_globalparam.append({"name":"Tranzila_subs_Url_CC", "type":"txt", "val":"https://direct.tranzila.com/udachi10tok/iframenew.php"})
    m_list_globalparam.append({"name":"Tranzila_subs_Url_Bit", "type":"txt", "val":"https://direct.tranzila.com/udachi10tok/iframenew.php"})
    m_list_globalparam.append({"name":"Tranzila_subs_Url_AP", "type":"txt", "val":"https://direct.tranzila.com/udachi10tok/iframenew.php"})
    m_list_globalparam.append({"name":"Tranzila_subs_Supplier", "type":"txt", "val":"udaci2"})
    m_list_globalparam.append({"name":"Tranzila_subs_CC_type", "type":"txt", "val":"iframe"})
    m_list_globalparam.append({"name":"Tranzila_subs_autopay_url", "type":"txt", "val":"https://api.tranzila.com/v1/transaction/credit_card/create"})
    m_list_globalparam.append({"name":"Tranzila_subs_terminal_name", "type":"txt", "val":"udachi6"})
    # CheckPAYMENT
    m_list_globalparam.append({"name":"CheckStartGame_day", "type":"int", "val":"3"})
    m_list_globalparam.append({"name":"CheckStartGame_maxamount", "type":"int", "val":"2000"})
    # Gift system
    m_list_globalparam.append({"name":"GIFT_SYSTEM", "type":"bool", "val":"False"})
    m_list_globalparam.append({"name":"GIFT_SYSTEM_need_registration", "type":"bool", "val":"False"})
    # сheck_id
    m_list_globalparam.append({"name":"Payment_check_id", "type":"bool", "val":"False"})
    m_list_globalparam.append({"name":"Payment_check_blacklist", "type":"bool", "val":"False"})
    # сheck_tickets
    m_list_globalparam.append({"name":"Check_ticket_win_wait", "type":"bool", "val":"True"})
    m_list_globalparam.append({"name":"Check_ticket_notwin_wait", "type":"bool", "val":"False"})
    m_list_globalparam.append({"name":"Check_ticket_win_timeout", "type":"int", "val":"30"})
    m_list_globalparam.append({"name":"Check_ticket_notwin_timeout", "type":"int", "val":"30"})
    # all permissions
    m_list_globalparam.append(dict(name="Permission_list", type="txt", val="tasks, add_money, user_edit, "
                                                                           "user_block, user_limit,"
                                                                           "user_reclama, user_edit_profile, "
                                                                           "user_edit_limits, user_edit_photo, "
                                                                           "user_edit_set_blogger, user_add_permissions"))
    # Massage text Group
    m_list_globalparam.append({"name": "MES_u_idconfirm_01", "type": "txt", "val": "bla bla"})
    m_list_globalparam.append({"name": "MES_u_idconfirm_02", "type": "txt", "val": "bla bla"})
    m_list_globalparam.append({"name": "MES_u_idconfirm_03", "type": "txt", "val": "bla bla"})
    m_list_globalparam.append({"name": "MES_u_idconfirm_for_all", "type": "bool", "val": "False"})
    m_list_globalparam.append({"name": "MES_u_birthday", "type": "txt", "val": "bla bla"})
    m_list_globalparam.append({"name": "MES_u_birthday_subject", "type": "txt", "val": "bla bla"})
    m_list_globalparam.append({"name": "MES_u_payout", "type": "bool", "val": "False"})
    m_list_globalparam.append({"name": "MES_u_payout_text", "type": "txt", "val": "bla bla"})
    m_list_globalparam.append({"name": "MES_u_payout_subject", "type": "txt", "val": "bla bla"})
    m_list_globalparam.append({"name": "Payout_percent_minus", "type": "txt", "val": "3.9"})
    # Check suspicious users
    m_list_globalparam.append({"name": "Checking_tickets_count", "type": "int", "val": "50"})
    m_list_globalparam.append({"name": "Checking_amount_sum", "type": "int", "val": "2000"})
    # reCAPTCHA token
    m_list_globalparam.append({"name": "reCAPTCHA_token", "type": "txt", "val": ""})
    m_list_globalparam.append({"name": "check_reCAPTCHA_on_feedback", "type": "bool", "val": "True"})

for index_item, item_t in enumerate(m_list_globalparam ):
    print("name = ", item_t["name"])
    try:
        t_item_param = Globalset.objects.get(code=item_t["name"])
        print("OK")
    except:
        print("ADD")
        t_item_param = Globalset()
        t_item_param.code = item_t["name"]
        t_item_param.type = item_t["type"]
        t_item_param.value = item_t["val"]
        t_item_param.description = item_t["name"]
        t_item_param.save()

print ('------ Finish Globalset ------')
