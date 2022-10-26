from django.urls import path
from .views import *
# from . import views

urlpatterns = [
    #path('register/', registerForm, name='register'),
    path('register/', registerForm, name='register'),
    path('login/', loginForm, name='login'),
    path('logout/', logoutUser, name="logout"),
    path('dashboard/', index, name="dashboard"),
    path('surface/', surface, name="surface"),
    path('railroad/', railroad, name="railroad"),
    path("predict/", predict, name="predict"),

]
