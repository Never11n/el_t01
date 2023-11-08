from django.shortcuts import render

def mainpage(request):
    return render(request, '001/main.html')

def choisepage(request):
    img_id = [
        1,2,3,4,5,6,7
    ]
    return render(request, '001/choise.html', {'img_id':img_id})

def gamepage(request, img_id):
    return render(request, '001/game.html')