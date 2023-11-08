#!/bin/bash
source ../../venv/bin/activate
#python ../manage.py shell < vsaka_periodic_tasks.py
#python ../manage.py shell < vsaka_periodic_tasks_birthday.py
#python ../manage.py shell < fix_game_histories.py
python ../manage.py shell < vsaka_test_email.py
#python ../manage.py shell < vsaka_lotto_tickets.py
#python ../manage.py shell < vsaka_test_decimal.py

#python ../manage.py shell < email_validation.py
