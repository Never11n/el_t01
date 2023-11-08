from django.shortcuts import render

def indexpage(request):
    return render(request, '002/index.html')


def lotery(request):
    return render(request, '002/lotery.html')