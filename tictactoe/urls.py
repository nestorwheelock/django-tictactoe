from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'tictactoe'

router = DefaultRouter()
router.register(r'games', views.GameViewSet, basename='game')

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),

    # Frontend URLs
    path('', views.game_list, name='game-list'),
    path('game/<int:pk>/', views.game_detail, name='game-detail'),
]
