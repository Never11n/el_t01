from .models import List_external_company
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .service.service import get_main_args


def shop_main(request, company_code):
    # "tab_list": [
    #     {"tab_id": "tab01", "tab_templ": "t0005/tab01.html", "tab_class": "d-block" },
    #     {"tab_id": "tab02", "tab_templ": "t0005/tab02.html", "tab_class": "d-none" },
    #     {"tab_id": "tab03", "tab_templ": "t0005/tab03.html", "tab_class": "d-none" },
    #     {"tab_id": "tab04", "tab_templ": "t0005/tab04.html", "tab_class": "d-none" },
    #     {"tab_id": "tab05", "tab_templ": "t0005/tab05.html", "tab_class": "d-none" },
    #     {"tab_id": "tab06", "tab_templ": "t0005/tab06.html", "tab_class": "d-none" },
    #     {"tab_id": "tab07", "tab_templ": "t0005/tab07.html", "tab_class": "d-none" },
    #     {"tab_id": "tab08", "tab_templ": "t0005/tab08.html", "tab_class": "d-none" },
    #     {"tab_id": "tab09", "tab_templ": "t0005/tab09.html", "tab_class": "d-none" }
    # ]

    if List_external_company.objects.filter(verbal=company_code).exists():
        m_external_company = List_external_company.objects.filter(verbal=company_code).order_by("order").first()
        m_template_name = f"{m_external_company.verbal}/main.html"
        print ("m_template_name = ", m_template_name)
        args = get_main_args(request, section="main")
        args["company_code"] = m_external_company.verbal
        args["tab_list"] = m_external_company.settings.get("tab_list", [])
        print ("tab_list = ", args["tab_list"])
        return render(request, m_template_name, args)
    else:
        print("permission no")
        return False
    