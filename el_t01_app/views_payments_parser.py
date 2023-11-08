# !/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import csv
from datetime import datetime

from django.shortcuts import render, redirect

from .service.service import get_main_args, check_template_exists
from .models import PaymentAnswer, BalanceOperation



def dump_payments_data_to_database(file):
    # f = open(BASE_DIR + "/tranzila_transactions_list.csv", "r", encoding='utf-8')
    # f = open(file, "r", encoding='utf-8')
    f = file.read().decode('utf-8')
    reader = csv.reader(io.StringIO(f))
    column_keys = PaymentAnswer.get_columns_name()
    headers = next(reader)  # skip headers
    for row in reader:
        text_data = ','.join(row)
        json_data = {column_keys[i]: row[i] for i in range(len(column_keys))}
        index = json_data.get('payment_index')
        bal_oper_number = json_data.get('number_bal_op')
        if bal_oper_number != '' and BalanceOperation.objects.filter(id=bal_oper_number).exists():
            t_balance_operation = BalanceOperation.objects.get(id=bal_oper_number)
        else:
            t_balance_operation = None
        if PaymentAnswer.objects.filter(payment_index=index).exists():
            m_payment_answer = PaymentAnswer.objects.get(payment_index=index)
        else:
            m_payment_answer = PaymentAnswer()
            m_payment_answer.payment_index = index
        m_payment_answer.created_date = datetime.strptime(json_data.get('created_date'), "%Y-%m-%d %H:%M:%S")
        m_payment_answer.balance_operation_id = t_balance_operation
        m_payment_answer.status = json_data.get('status', '')
        m_payment_answer.json_data = json_data
        m_payment_answer.text_data = text_data
        m_payment_answer.save()


def upload_payment_answers_data(request):
    args = get_main_args(request, section="main")
    if not args['logged_in'] or not args['me'].profile.is_boss:
        return redirect('/')
    else:
        args['l_head_list'] = [check_template_exists("cab_boss/l_head_01.html")]
        args['l_header_list'] = [check_template_exists("cab_boss/l_header.html")]
        args['l_footer_list'] = []
        args['l_script_list'] = [check_template_exists("cab_boss/l_script_01.html")]
        args['l_layout_file'] = check_template_exists("cab_boss/layout.html")
        args['main_tab'] = f"{args['GL_MainSkin']}/cabinet/cabinet.html"
        args['l_body_list'] = [check_template_exists('cab_boss/upload_tranzilla_csv.html')]
        args['menu_item'] = 'nav-link_cabb_payout'
        if request.POST:
            if 'f_file_01' in request.FILES:
                file = request.FILES['f_file_01']
                try:
                    dump_payments_data_to_database(file)
                    return redirect('/payment_answers/')
                except Exception:
                    args['problem'] = 'Something was wrong. Please, make sure you send the csv file and try again.'
                    return render(request, args['main_tab'], args)
            else:
                args['problem'] = 'File is not found. Please, make sure you send the csv file.'
                return render(request, args['main_tab'], args)

        return render(request, args['main_tab'], args)
