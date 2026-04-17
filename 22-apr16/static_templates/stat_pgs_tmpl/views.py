from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    ctx = {
        'name': "Tony",
        'age': 25,
        'gains': 2344.322211
    }
    return render(request, 'home.html', ctx)

@login_required
def contact(request):
    return render(request, 'contact.html')
