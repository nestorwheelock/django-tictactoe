import pytest
from rest_framework.test import APIClient
from rest_framework import status
from tictactoe.models import Game


@pytest.mark.django_db
class TestGameAPI:
    """Test suite for Game API endpoints."""

    def setup_method(self):
        """Setup test client before each test."""
        self.client = APIClient()
        self.base_url = '/tictactoe/api/games/'

    def test_create_game(self):
        """Test creating a new game."""
        response = self.client.post(self.base_url)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert response.data['board'] == [None] * 9
        assert response.data['current_player'] == 'X'
        assert response.data['status'] == 'in_progress'
        assert 'created_at' in response.data
        assert 'updated_at' in response.data

    def test_list_games(self):
        """Test listing all games."""
        Game.objects.create()
        Game.objects.create()
        response = self.client.get(self.base_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_list_games_empty(self):
        """Test listing games when none exist."""
        response = self.client.get(self.base_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_retrieve_game(self):
        """Test retrieving a single game."""
        game = Game.objects.create()
        response = self.client.get(f'{self.base_url}{game.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == game.id
        assert 'board_display' in response.data  # Detailed serializer

    def test_retrieve_nonexistent_game(self):
        """Test retrieving non-existent game returns 404."""
        response = self.client.get(f'{self.base_url}999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_game(self):
        """Test deleting a game."""
        game = Game.objects.create()
        response = self.client.delete(f'{self.base_url}{game.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Game.objects.filter(id=game.id).exists()

    def test_make_valid_move(self):
        """Test making a valid move."""
        game = Game.objects.create()
        response = self.client.post(
            f'{self.base_url}{game.id}/move/',
            {'position': 0},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['board'][0] == 'X'
        assert response.data['current_player'] == 'O'
        assert 'message' in response.data

    def test_make_move_occupied_position(self):
        """Test moving to occupied position returns error."""
        game = Game.objects.create()
        game.make_move(0)
        response = self.client.post(
            f'{self.base_url}{game.id}/move/',
            {'position': 0},
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert 'occupied' in str(response.data['error']).lower()

    def test_make_move_invalid_position_too_high(self):
        """Test invalid position (>8) returns error."""
        game = Game.objects.create()
        response = self.client.post(
            f'{self.base_url}{game.id}/move/',
            {'position': 10},
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_make_move_invalid_position_negative(self):
        """Test invalid position (<0) returns error."""
        game = Game.objects.create()
        response = self.client.post(
            f'{self.base_url}{game.id}/move/',
            {'position': -1},
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_make_move_missing_position(self):
        """Test missing position parameter returns error."""
        game = Game.objects.create()
        response = self.client.post(
            f'{self.base_url}{game.id}/move/',
            {},
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_make_move_game_over(self):
        """Test move after game over returns error."""
        game = Game.objects.create()
        # Set up winning position for X
        game.board = ['X', 'X', 'X', 'O', 'O', None, None, None, None]
        game.status = Game.STATUS_X_WINS
        game.save()

        response = self.client.post(
            f'{self.base_url}{game.id}/move/',
            {'position': 5},
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert 'finished' in str(response.data['error']).lower()

    def test_make_move_nonexistent_game(self):
        """Test move on non-existent game returns 404."""
        response = self.client.post(
            f'{self.base_url}999/move/',
            {'position': 0},
            format='json'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_complete_game_flow_x_wins(self):
        """Test complete game from creation to X winning."""
        # Create game
        response = self.client.post(self.base_url)
        game_id = response.data['id']

        # Play game: X wins top row
        moves = [
            (0, 'X', 'O'),  # X at 0
            (3, 'O', 'X'),  # O at 3
            (1, 'X', 'O'),  # X at 1
            (4, 'O', 'X'),  # O at 4
            (2, 'X', None)  # X at 2 (wins)
        ]

        for position, player, next_player in moves:
            response = self.client.post(
                f'{self.base_url}{game_id}/move/',
                {'position': position},
                format='json'
            )
            assert response.status_code == status.HTTP_200_OK
            assert response.data['board'][position] == player
            if next_player:
                assert response.data['current_player'] == next_player
                assert response.data['status'] == 'in_progress'

        # Check final state
        response = self.client.get(f'{self.base_url}{game_id}/')
        assert response.data['status'] == 'x_wins'

    def test_complete_game_flow_draw(self):
        """Test complete game resulting in draw."""
        # Create game
        response = self.client.post(self.base_url)
        game_id = response.data['id']

        # Play game to draw
        moves = [0, 1, 2, 4, 3, 5, 7, 6, 8]  # Results in draw
        for move in moves:
            response = self.client.post(
                f'{self.base_url}{game_id}/move/',
                {'position': move},
                format='json'
            )
            assert response.status_code == status.HTTP_200_OK

        # Check final state
        response = self.client.get(f'{self.base_url}{game_id}/')
        assert response.data['status'] == 'draw'

    def test_serializer_read_only_fields(self):
        """Test that read-only fields cannot be modified."""
        game = Game.objects.create()
        original_id = game.id

        response = self.client.patch(
            f'{self.base_url}{game.id}/',
            {
                'id': 999,
                'current_player': 'O',
                'status': 'x_wins'
            },
            format='json'
        )

        # Refresh from DB
        game.refresh_from_db()
        assert game.id == original_id
        assert game.current_player == 'X'  # Should not change
        assert game.status == 'in_progress'  # Should not change

    def test_board_display_in_detail_view(self):
        """Test that board_display is included in detail view."""
        game = Game.objects.create()
        game.make_move(0)
        game.make_move(4)

        response = self.client.get(f'{self.base_url}{game.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert 'board_display' in response.data
        assert 'X' in response.data['board_display']
        assert 'O' in response.data['board_display']


@pytest.mark.django_db
class TestGameSerializer:
    """Test suite for Game serializers."""

    def test_game_serializer_fields(self):
        """Test GameSerializer includes correct fields."""
        from tictactoe.serializers import GameSerializer
        game = Game.objects.create()
        serializer = GameSerializer(game)

        expected_fields = ['id', 'board', 'current_player', 'status', 'created_at', 'updated_at']
        assert all(field in serializer.data for field in expected_fields)

    def test_game_detail_serializer_includes_board_display(self):
        """Test GameDetailSerializer includes board_display."""
        from tictactoe.serializers import GameDetailSerializer
        game = Game.objects.create()
        serializer = GameDetailSerializer(game)

        assert 'board_display' in serializer.data
        assert isinstance(serializer.data['board_display'], str)

    def test_move_serializer_validation(self):
        """Test MoveSerializer validates position."""
        from tictactoe.serializers import MoveSerializer

        # Valid position
        serializer = MoveSerializer(data={'position': 5})
        assert serializer.is_valid()

        # Invalid - too high
        serializer = MoveSerializer(data={'position': 9})
        assert not serializer.is_valid()

        # Invalid - negative
        serializer = MoveSerializer(data={'position': -1})
        assert not serializer.is_valid()

        # Invalid - missing
        serializer = MoveSerializer(data={})
        assert not serializer.is_valid()
