"""
Test URL configuration that mounts tictactoe app at /tictactoe/
"""
from django.urls import path, include

urlpatterns = [
    path('tictactoe/', include('tictactoe.urls')),
]
