from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'tictactoe'

router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
]
