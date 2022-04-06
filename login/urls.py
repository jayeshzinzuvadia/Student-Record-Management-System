from django.urls import path
from . import views

app_name='login'
urlpatterns = [
    path('', views.manageLogin, name='login'),
    path('logout/', views.manageLogout, name='logout'),
]