from django.shortcuts import render

def gympage(request):
    return render(request, '003/gym.html')

def ticketview(request):
    return render(request, '003/ticket_game.html')