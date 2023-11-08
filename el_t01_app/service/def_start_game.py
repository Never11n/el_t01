#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import time
import locale
import os
import json
import time
import requests
import logging
import logging.config
from django.utils import timezone
from fractions import Fraction
from dateutil.relativedelta import relativedelta
from dateutil.relativedelta import MO
from django.utils.translation import gettext
from el_t01_app.models import Profile, Ticket_history, Game_history, Ticket_type, Report_list
from el_t01_app.models import BalanceOperation, List_jellyfish, Profile, Ticket_history, Type_payment
from el_t01_app.service.dft import get_GlobalSettings

locale.setlocale(locale.LC_ALL, 'C')


class StartGame(object):
    def __init__(self, l_user=None, l_pay_ticket_type="", l_pay_ticket_col="", l_pay_method="", l_pay_game_id="", l_discount_user={}):
        print ("__init__")
        self.item_user = l_user
        self.item_ticket_type = l_pay_ticket_type
        self.item_ticket_col = l_pay_ticket_col
        self.item_pay_method_verbal = l_pay_method
        self.item_game_id = l_pay_game_id
        self.discount_user = l_discount_user
        self.set_log()
        logging.info(f'***** START GAME (user = {self.item_user}) ******')
        logging.info(f'  ticket_type = {self.item_ticket_type}')
        logging.info(f'  ticket_col  = {self.item_ticket_col}')
        logging.info(f'  pay_method  = {self.item_pay_method_verbal}')

        self.set_game_create = False
        self.set_game_start = False
        self.set_check_game = False
        self.ReturnBool = True
        self.ReturnText = ""

        self.globalset = get_GlobalSettings()
        t_dict_ticket_type = Ticket_type.objects.all()
        self.dict_ticket_type = {}
        for ItemTicketType in t_dict_ticket_type:
            print ("ItemTicketType.id = ", ItemTicketType.id)
            # self.dict_ticket_type[ItemTicketType.id] = ItemTicketType.verbal_jellyfish
            self.dict_ticket_type[ItemTicketType.id] = {
                "verbal_jellyfish": ItemTicketType.verbal_jellyfish,
                "caption": ItemTicketType.caption
            }

        self.item_pay_method = Type_payment.objects.get(verbal=self.item_pay_method_verbal)
        self.item_game_order = Game_history.objects.get(id=self.item_game_id)

        # self.item_game_order.t_payment_id = self.item_pay_method.id
        # self.item_game_order.save()

        # self.game_order_list = self.item_game_order.ticket_list["list_order"]
        # self.item_game_sum = 0
        # self.item_game_quantity = 0
        #
        # for ItemOrder in self.game_order_list:
        #     m_itemGame_type = ItemOrder["tic_type"]
        #     t_itemGameType = Ticket_type.objects.get(id=m_itemGame_type)
        #     m_ItemGame_num = ItemOrder["tic_num"]
        #     m_ItemGame_cost_1 = t_itemGameType.cost_1
        #     m_ItemGame_cost_2 = t_itemGameType.cost_2
        #     try:
        #         self.item_game_quantity += int(m_ItemGame_num)
        #     except:
        #         self.item_game_quantity += 0
        #     try:
        #         self.item_game_sum += int(m_ItemGame_num) * m_ItemGame_cost_2
        #     except:
        #         self.item_game_sum += 0
        #
        # self.item_game_order.ticket_sum = self.item_game_sum
        # self.item_game_order.save()
        # logging.info(f'  game_sum      = {self.item_game_sum}')
        # logging.info(f'  game_quantity = {self.item_game_quantity}')


    def set_log(self):
        m_dirlog_short = '../log/start_game'
        if not os.path.exists(m_dirlog_short):
            os.makedirs(m_dirlog_short)
        m_log_file = os.path.join(m_dirlog_short, 'start_game.log')

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

    # check
    def check_ticket_col(self):
        try:
            self.item_ticket_col = int(self.item_ticket_col)
            if self.item_ticket_col > 0:
                self.ReturnBool = True
                self.ReturnText = ""
            else:
                logging.info(f"Invalid number of tickets ({self.item_ticket_col})")
                self.ReturnBool = False
                self.ReturnText = (gettext("Invalid number of tickets."))
        except:
            self.t_Ticket_type = None
            self.item_game_sum = None
            logging.info(f"Invalid number of tickets")
            self.ReturnBool = False
            self.ReturnText = (gettext("Invalid number of tickets."))
        logging.info(f"Check ticket type = {self.ReturnBool}, {self.ReturnText}")


    def check_ticket_type(self):
        try:
            self.t_Ticket_type = Ticket_type.objects.get(verbal=self.item_ticket_type)
            self.item_game_sum = self.item_ticket_col * self.t_Ticket_type.cost_2
            self.ReturnBool = True
            self.ReturnText = ""
        except:
            self.t_Ticket_type = None
            self.item_game_sum = None
            logging.info(f"Ticket_type not found")
            self.ReturnBool = False
            self.ReturnText = (gettext("The game is not available. Try later."))
        logging.info(f"Check ticket type = {self.ReturnBool}, {self.ReturnText}")

    def check_pay(self):
        if self.item_game_order.t_status.verbal == "add_to_cart":

            self.item_game_order.t_payment_id = self.item_pay_method.id
            self.item_game_order.save()
            self.game_order_list = self.item_game_order.ticket_list["list_order"]
            self.item_game_sum = 0
            self.item_game_quantity = 0

            for ItemOrder in self.game_order_list:
                m_itemGame_type = ItemOrder["tic_type"]
                t_itemGameType = Ticket_type.objects.get(id=m_itemGame_type)
                m_ItemGame_num = ItemOrder["tic_num"]
                m_ItemGame_cost_1 = t_itemGameType.cost_1
                m_ItemGame_cost_2 = t_itemGameType.cost_2
                try:
                    self.item_game_quantity += int(m_ItemGame_num)
                except:
                    self.item_game_quantity += 0

                if self.discount_user.get("discount") == True:
                    self.discount_user_num = self.discount_user["discount_product_list"].get(t_itemGameType.id, 0)
                else:
                    self.discount_user_num = 0

                try:
                    self.item_game_sum += int(m_ItemGame_num) * (m_ItemGame_cost_2 - self.discount_user_num )
                except:
                    self.item_game_sum += 0

            self.item_game_order.ticket_list["discount"] = self.discount_user_num
            self.item_game_order.ticket_sum = self.item_game_sum
            self.item_game_order.save()
            logging.info(f'  game_sum      = {self.item_game_sum}')
            logging.info(f'  game_quantity = {self.item_game_quantity}')

            self.ReturnBool = True
            self.ReturnText = ""
        else:
            logging.info(f"Ticket already paid")
            self.ReturnBool = False
            self.ReturnText = (gettext("This game has already been paid for."))
        logging.info(f"Check ticket type = {self.ReturnBool}, {self.ReturnText}")

    def check_jellyfish_game(self):
        try:
            # list order = self.game_order_list
            print("=======================")
            # print("self.game_order_list = ", self.game_order_list)
            # [{'ip': '194.183.171.117 True', 'date': '20211217125738', 'tic_num': '1', 'tic_type': 3, 'tic_caption': 'BlackjacK 21'}]
            # print ("self.dict_ticket_type = ", self.dict_ticket_type)
            # проверить доступна машина или нет
            t_jellyfish = List_jellyfish.objects.filter(enabled=True).order_by("order")
            if t_jellyfish.count() > 0:
                item_jellyfish = t_jellyfish[0]
                # id enabled verbal caption order ipadres api_token
                m_url_1 = item_jellyfish.ipadres
                m_url_2 = "" if m_url_1.strip()[-1] == "/" else "/"
                m_url_3 = "api/v07/external/game_check"
                url = f"{m_url_1}{m_url_2}{m_url_3}"
                m_check_jellyfish_bool = True
                m_check_jellyfish_list = []

                for ItemOrderTicket in self.game_order_list:
                    m_tic_type = ItemOrderTicket["tic_type"]
                    # m_tic_name = ItemOrderTicket["tic_caption"]
                    m_tic_name = self.dict_ticket_type[m_tic_type]["caption"]
                    print ("m_tic_type = ", m_tic_type)
                    print ("tic_caption = ", m_tic_name)
                    m_game_id = self.dict_ticket_type[m_tic_type]["verbal_jellyfish"]
                    m_payload = {
                        "game_id": m_game_id,
                    }
                    payload = json.dumps(m_payload)
                    headers = {
                        'Token': item_jellyfish.api_token,
                        'Content-Type': 'application/json'
                    }
                    print("**********")
                    print("url     = ", url)
                    print("headers = ", headers)
                    print("payload = ", payload)

                    response = requests.request("POST", url, headers=headers, data=payload)
                    print("response.text =", response.text, response.status_code)
                    if response.status_code == 200:
                        try:
                            mj_response = json.loads(response.text)
                            if mj_response["status"] == "OK":
                                logging.info(f"check_jellyfish_game status OK")
                                self.ReturnBool = True
                                self.ReturnText = ""
                            else:
                                logging.info(f"Error check_jellyfish_game status NOT OK")
                                self.ReturnBool = False
                                m_check_jellyfish_bool = False
                                m_check_jellyfish_list.append(m_tic_name)
                        except:
                            logging.info(f"Error check_jellyfish_game status except")
                            self.ReturnBool = False
                            m_check_jellyfish_bool = False
                            m_check_jellyfish_list.append(m_tic_name)
                    else:
                        logging.info(f"Error check_jellyfish_game status {response.status_code}")
                        self.ReturnBool = False
                        m_check_jellyfish_bool = False
                        m_check_jellyfish_list.append(m_tic_name)
                # end for
                if m_check_jellyfish_bool == False:
                    self.ReturnText = gettext("Unable to start the game (")
                    for itemError in m_check_jellyfish_list:
                        self.ReturnText += gettext(itemError) + ", "
                    self.ReturnText = self.ReturnText[:-1]
                    self.ReturnText += gettext("). Try later.")
            else:
                logging.info("Error check_jellyfish_game not available")
                self.ReturnBool = False
                self.ReturnText = (gettext("The game is not available. Try later."))
            logging.info(f"check_jellyfish_game = {self.ReturnBool}, {self.ReturnText}")
        except:
            self.t_Ticket_type = None
            logging.info(f"Error check_jellyfish_game")
            self.ReturnBool = False
            self.ReturnText = (gettext("The game is not available. Try later."))
        logging.info(f"Check jellyfish_game = {self.ReturnBool}, {self.ReturnText}")

    def check_maxticday(self):
        # print("check_maxticday")
        # print ("=======================")
        # print ("self.globalset = ", self.globalset)

        m_date_now = datetime.datetime.now()
        m_date_start = m_date_now + relativedelta(hour=0, minute=0, second=0, microsecond=0)
        m_date_finish = m_date_now + relativedelta(days=+1, hour=0, minute=0, second=0, microsecond=0)

        # print ("self.item_user = ", self.item_user)
        # print ("m_date_start   = ", m_date_start )
        # print ("m_date_finish  = ", m_date_finish )
        # print ("self.item_user = ", self.item_user, self.item_user.id)

        t_ticketuserday = Ticket_history.objects.filter(games_id__user_id_id=self.item_user.id,
                                                        req_dt__range=[m_date_start, m_date_finish]
                                                          )

        t_ticketuserday = t_ticketuserday.count()
        # print("t_ticketuserday = ", t_ticketuserday)
        m_maxticday = self.globalset.get("MaxTicDay", "1000")
        try:
            m_maxticday = int(m_maxticday)
        except Exception as ex:
            m_maxticday = 1000

        if m_maxticday  >= t_ticketuserday :
            self.ReturnBool = True
            self.ReturnText = ""
        else:
            self.ReturnBool = False
            self.ReturnText = (gettext("According to the rules of the site, you can buy no more than"))
            self.ReturnText += f" {m_maxticday} "
            self.ReturnText += (gettext("tickets"))
        logging.info(f"check_maxticday = {self.ReturnBool}, {self.ReturnText}, {t_ticketuserday}")


    def check_balance(self):
        print("check_balance")
        print("balance = ",
              self.item_user.profile.balance,
              type(self.item_user.profile.balance),
              self.item_game_sum,
              type(self.item_game_sum)
              )
        if self.item_user.profile.balance >= self.item_game_sum:
            # self.item_user.profile.balance = self.item_user.profile.balance - self.item_game_sum
            # self.item_user.profile.save()
            self.ReturnBool = True
            self.ReturnText = ""
        else:
            self.ReturnBool = False
            self.ReturnText = (gettext("You don't have enough money. Try another payment option."))
        logging.info(f"check_balance = {self.ReturnBool}, {self.ReturnText}")

    def create_game_ticket(self):
        print("create_game_ticket")
        mReturnBool = True
        # mReturnBool = False
        if mReturnBool:
            mReturnBool = True
            mReturnText = "OK"
        else:
            mReturnBool = False
            mReturnText = gettext("Unable to start the game. Try later.")
        logging.info(f"Create game ticket = {self.ReturnBool}, {self.ReturnText}")

    def step_start(self):
        self.StepTimeStart = datetime.datetime.now()
        self.StepNum += 1
        logging.info("  " + "*" * 60)

    def step_stop(self, l_name_step=""):
        TimeTask = str((datetime.datetime.now() - self.TaskTimeStart))
        TimeTest = str((datetime.datetime.now() - self.StepTimeStart))
        str_log = "  {} = {} = {} = {} = {}".format(
            str(self.StepNum).zfill(2), TimeTask, TimeTest, l_name_step, self.StepStatus
        )
        self.StepLog += str_log + "\n"
        self.StepStatus = None
        logging.info(str_log)

    def save_db(self, l_type):
        return
        try:
            if l_type == "start":
                self.item_ticket_job.dt_start = timezone.now()
                self.item_ticket_job.status = "01"
                self.item_ticket_job.save()
            if l_type == "rezult":
                m_answ_win = self.answ_win
                m_answ_win_sum = self.answ_win_sum
                if m_answ_win_sum >= 1000:
                    m_answ_win = False
                    m_answ_win_sum = 0

                self.item_ticket_job.dt_stop = timezone.now()
                self.item_ticket_job.answ_dt = timezone.now()
                self.item_ticket_job.answ_nom = self.answ_nom
                self.item_ticket_job.answ_tabl = self.answ_tabl
                self.item_ticket_job.answ_option = self.answ_option
                self.item_ticket_job.answ_win = m_answ_win  ## 'Выигрыш'
                self.item_ticket_job.answ_win_sum = m_answ_win_sum  ## 'Сумма выигрыша'
                self.item_ticket_job.step_job = self.StepLog
                self.item_ticket_job.status = "33"
                self.item_ticket_job.his_job = self.history_job
                self.item_ticket_job.save()
            self.StepStatus = "OK"
        except Exception as ex:
            self.StepStatus = ex


    def game_return(self):
        logging.info(f'----- GAME RETURN (user = {self.item_user.id} {self.item_user}) -----')
        logging.info("*" * 60)
        print("game_return")
        self.ReturnDict = {}
        if self.ReturnBool:
            self.ReturnDict["AnswerCod"] = "01"
            self.ReturnDict["AnswerText"] = self.ReturnText
            self.ReturnDict["AnswerHref"] = f"/cab-game-payment/{self.item_game_id}/"
        else:
            self.ReturnDict["AnswerCod"] = "00"
            self.ReturnDict["AnswerText"] = self.ReturnText

        return (self.ReturnDict)


    def run_job(self):
        print ("run_job run_job run_job")
        # +++ проверка количества билетов
        # self.check_ticket_col()
        # if self.ReturnBool == False:
        #     logging.info(f"Ticket_type not found")
        #     return (self.game_return())
        # +++ проверка лимитов суммы в день

        # проверка оплачен или нет
        self.check_pay()
        if self.ReturnBool == False:
            logging.info(f"check_pay")
            return (self.game_return())

        # +++ проверка лимитов количества билетов в день
        self.check_maxticday()
        if self.ReturnBool == False:
            logging.info(f"check_max_tic_day")
            return (self.game_return())

        # +++ проверка типа игры
        # self.check_ticket_type()
        # if self.ReturnBool == False:
        #     logging.info(f"Ticket_type not found")
        #     return (self.game_return())

        # +++ проверка balance
        if self.item_pay_method_verbal == "balance":
            self.check_balance()
            if self.ReturnBool == False:
                logging.info(f"check_balance error")
                return (self.game_return())
        # +++ проверка доступности машины
        self.check_jellyfish_game()
        if self.ReturnBool == False:
            logging.info(f"Jellyfish not aviable")
            return (self.game_return())

        # self.create_game_ticket()  # self.item_game_id

        # self.save_db("rezult")

        logging.info("*" * 60)
        logging.info('----- STOP  job {} -----')
        print ("self.ReturnBool, self.ReturnText = ", self.ReturnBool, self.ReturnText )
        logging.info('----- STOP  job {} -----')
        return (self.game_return())
