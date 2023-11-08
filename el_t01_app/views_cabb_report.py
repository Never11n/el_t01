# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import io
import importlib

from openpyxl import Workbook
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from el_t01_app.service.service import get_main_args, check_template_exists
from el_t01_app.models import Profile, Report_list, BalanceOperation, Ticket_history, Payout


def cab_report_data(request, verbal=None):
    # # print ("cab_report_data")
    # # verbal - code report
    # # RETURN = (return_list, return_args)
    # print ("verbal         = ", verbal)
    return_args = {}
    return_list = None
    try:
        ReportDef_name = f"el_t01_app.service.report.report_data"
        ReportDef_module = importlib.import_module(ReportDef_name)
        ReportDef_module = importlib.reload(ReportDef_module)
        d_report_data = getattr(ReportDef_module, 'report_data')
        return_list, return_args = d_report_data(request, verbal)
        # print ("return_list, return_args =" , return_list, return_args)
    except Exception as ex:
        print("1. except cab_report = ", ex)
        return_args = {}
        return_list = None
    return (return_list, return_args)


def cabb_report(request, verbal=None):
    # print ("cab_report")
    # print ("verbal         = ", verbal)
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        args['get_param'] = ""
        if request.GET :
            args['get_param'] = request.GET.urlencode()
        try:
            args['l_head_list'] = []
            args['l_header_list'] = []
            args['l_footer_list'] = []
            args['l_script_list'] = []
            args['l_modal_list'] = []
            args['l_body_list'] = []
            args['l_layout_file'] = check_template_exists("cab_boss/layout.html")
            args['l_head_list'].append(check_template_exists("cab_boss/l_head_01.html"))
            args['l_header_list'].append(check_template_exists("cab_boss/l_header.html"))
            args['l_script_list'].append(check_template_exists("cab_boss/l_script_01.html"))
            args['menu_item'] = 'nav-link_cabb_reports'
            # args['l_modal_list'].append('cab_boss/cabb_modal_editbalance.html')
            t_report_item = Report_list.objects.get(verbal=verbal)
            args['report_item'] = t_report_item
            args['report_list'], args_add = cab_report_data(request, verbal=verbal)
            args.update(args_add)

            args['menu_reports_item'] = verbal

            find_options = t_report_item.add_param['filters']
            if len(find_options) > 0:
                args['l_find_form'] = check_template_exists("cab_boss/_cab_find_multi.html")
                for find_option in find_options:
                    args[find_option] = True

            args['l_btn_export'] = check_template_exists("cab_boss/_cab_btn_export.html")
            args['l_body_list'].append(check_template_exists(f"report/{t_report_item.template}"))
            args['main_tab'] = check_template_exists("cab_boss/cabinet.html")

            return render(request, args['main_tab'], args)
        except Exception as ex:
            ##### для ловли ошибочек с отчетами
            print(f" === {__file__} exception ===")
            print("item -> ", t_report_item.template)
            print(f" === {__file__} exception ===")
            ##### для ловли ошибочек с отчетами

            # raise ex

            print("except cab_report = ", ex)
            return redirect('/')


def cabb_report_exp(request, verbal=None, r_type=None):
    print("cabb_report_exp")
    args = get_main_args(request, section="main")
    if not args['logged_in']:
        return redirect('/')
    else:
        args['get_param'] = ""
        if request.GET:
            args['get_param'] = request.GET.urlencode()
        try:
            t_report_item = Report_list.objects.get(verbal=verbal)
            t_report_list, args_add = cab_report_data(request, verbal=verbal)
            export_file = t_report_item.export_template
            ReportDef_name = f"el_t01_app.service.report.{export_file}"
            ReportDef_module = importlib.import_module(ReportDef_name)
            ReportDef_module = importlib.reload(ReportDef_module)
            d_report_export = getattr(ReportDef_module, 'report_export')
            m_return_response = d_report_export(t_report_list, args_add)
            return m_return_response


        except Exception as ex:
            print("except === ", ex)
            f_response = io.BytesIO()
            wb = Workbook()
            m_title = "ERROR Report"
            ws = wb.active
            row_item = 1
            ws[f'A{row_item}'] = m_title
            wb.save(f_response)
            f_response.seek(0)
            m_return_response = HttpResponse(f_response.read(), content_type="application/vnd.ms-excel")
            m_return_response['Content-Disposition'] = f'filename="report.xlsx"'
            f_response.close()
            return m_return_response
