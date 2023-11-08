# ! /usr/bin/env python
# -*- coding: utf-8 -*-
# import bot_config_whatsapp as bot_config

from whatsapp_api_client_python import API

# greenAPI = API.GreenApi(bot_config.ID_INSTANCE, bot_config.API_TOKEN_INSTANCE)

def send_sms_whatsapp_01(loc_tel_code, loc_tel, loc_txt):
    print ("send_sms_whatsapp_01")
    greenAPI = API.GreenApi(ID_INSTANCE, API_TOKEN_INSTANCE)
    loc_tel = f"{loc_tel_code}{loc_tel}@c.us"
    result = greenAPI.sending.sendMessage(loc_tel, loc_txt)

    print(result.data)
    return (loc_txt, result.data)
