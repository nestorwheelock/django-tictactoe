import pytest
from django.urls import reverse
from tictactoe.models import Game


@pytest.mark.django_db
class TestTemplateViews:
    """Test suite for template-based views."""

    def test_game_list_view_renders(self, client):
        """Test game list view renders correctly."""
        Game.objects.create()
        Game.objects.create()

        response = client.get(reverse('tictactoe:game-list'))
        assert response.status_code == 200
        assert 'games' in response.context
        assert len(response.context['games']) == 2

    def test_game_list_view_empty(self, client):
        """Test game list view with no games."""
        response = client.get(reverse('tictactoe:game-list'))
        assert response.status_code == 200
        assert 'games' in response.context
        assert len(response.context['games']) == 0

    def test_game_detail_view_renders(self, client):
        """Test game detail view renders correctly."""
        game = Game.objects.create()

        response = client.get(reverse('tictactoe:game-detail', args=[game.id]))
        assert response.status_code == 200
        assert response.context['game'].id == game.id

    def test_game_detail_view_404(self, client):
        """Test game detail view returns 404 for non-existent game."""
        response = client.get(reverse('tictactoe:game-detail', args=[999]))
        assert response.status_code == 404

    def test_game_list_template_used(self, client):
        """Test correct template is used for game list."""
        response = client.get(reverse('tictactoe:game-list'))
        assert response.status_code == 200
        assert 'tictactoe/game_list.html' in [t.name for t in response.templates]

    def test_game_detail_template_used(self, client):
        """Test correct template is used for game detail."""
        game = Game.objects.create()
        response = client.get(reverse('tictactoe:game-detail', args=[game.id]))
        assert response.status_code == 200
        assert 'tictactoe/game_detail.html' in [t.name for t in response.templates]

    def test_game_list_orders_by_created_desc(self, client):
        """Test game list is ordered by creation date descending."""
        game1 = Game.objects.create()
        game2 = Game.objects.create()

        response = client.get(reverse('tictactoe:game-list'))
        games = response.context['games']

        # Newer games should appear first
        assert games[0].id == game2.id
        assert games[1].id == game1.id
