from django.contrib import admin
from django.urls import path
from menu.views import menu_view, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', menu_view),
    path('', home)
]
