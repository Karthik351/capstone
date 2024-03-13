# myapp/urls.py
from django.urls import path
from . import views
from .views import create_candlestick_chart


urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name='home'),
    path('markets/', create_candlestick_chart, name='markets'),
    path('portfolio/', views.portfolio, name='portfolio'),

]
