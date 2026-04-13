from django.shortcuts import render
from .models import Dish
from django.http import HttpResponse

def menu_view(request):
    # Fetching all items from the "Pantry"
    all_dishes = Dish.objects.all()
    
    # Handing the data to the "Plating Station"
    return render(request, 'menu.html', {'menu_items': all_dishes})


def home(request):
    bistro = "<h1>My Cool Bistro</h1>"
    return HttpResponse(bistro)