from django.contrib import admin
from django.urls import path, include
from stat_pgs_tmpl import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
    path('', include('accounts.urls')),
]
