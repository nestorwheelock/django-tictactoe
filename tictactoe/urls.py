from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'tictactoe'

router = DefaultRouter()
router.register(r'games', views.GameViewSet, basename='game')

urlpatterns = [
    path('api/', include(router.urls)),
]
