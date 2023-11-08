# ! /usr/bin/env python
# -*- coding: utf-8 -*-

from whatsapp_api_client_python import API as API

ID_INSTANCE = '1101799936'
API_TOKEN_INSTANCE = '5a09de27f2af4af8810a43feaa7f3d3251239252fc424aad81'

greenAPI = API.GreenApi(ID_INSTANCE, API_TOKEN_INSTANCE)

def main():
    # result = greenAPI.sending.sendMessage('79316003342@c.us', 'Вова Вовочка ')
    # result = greenAPI.sending.sendMessage('38503810452@c.us', 'Super VIKA ')
    # result = greenAPI.sending.sendMessage('79316003342@c.us', 'Super VIKA ')
    # result = greenAPI.sending.sendMessage('972549962510@c.us', 'Привет от СУПЕР Вики https://scratch-il.com/')
    result = greenAPI.sending.sendMessage('972549219455@c.us', 'Привет от СУПЕР Вики https://scratch-il.com/')
    # result = greenAPI.sending.sendMessage('380685334270@c.us', 'Привіт ми з України')

    # 380 68 533 4270 972 54-996-2510

    print(result.data)

if __name__ == "__main__":
    main()