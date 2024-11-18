from django.urls import path
from .views import home, command

urlpatterns = [
    path('home/', home.home_view, name='home'),
    path('commands/', command.command_view, name='command'),
]