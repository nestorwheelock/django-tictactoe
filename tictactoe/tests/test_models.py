import pytest
from django.core.exceptions import ValidationError
from tictactoe.models import Game


@pytest.mark.django_db
class TestGameModel:

    def test_game_creation_defaults(self):
        """Test game is created with correct defaults."""
        game = Game.objects.create()
        assert game.board == [None] * 9
        assert game.current_player == 'X'
        assert game.status == 'in_progress'
        assert game.created_at is not None
        assert game.updated_at is not None

    def test_board_initialization(self):
        """Test board initializes as 9 nulls."""
        game = Game.objects.create()
        assert len(game.board) == 9
        assert all(cell is None for cell in game.board)

    def test_valid_move(self):
        """Test making a valid move."""
        game = Game.objects.create()
        result = game.make_move(0)
        assert result['success'] is True
        assert game.board[0] == 'X'
        assert game.current_player == 'O'

    def test_occupied_position_raises_error(self):
        """Test moving to occupied position raises ValidationError."""
        game = Game.objects.create()
        game.make_move(0)
        with pytest.raises(ValidationError, match="Position already occupied"):
            game.make_move(0)

    def test_invalid_position_negative_raises_error(self):
        """Test negative position raises ValidationError."""
        game = Game.objects.create()
        with pytest.raises(ValidationError, match="Position must be between 0 and 8"):
            game.make_move(-1)

    def test_invalid_position_too_high_raises_error(self):
        """Test position > 8 raises ValidationError."""
        game = Game.objects.create()
        with pytest.raises(ValidationError, match="Position must be between 0 and 8"):
            game.make_move(9)

    def test_move_after_game_over_raises_error(self):
        """Test move after game ends raises ValidationError."""
        game = Game.objects.create()
        game.status = Game.STATUS_X_WINS
        game.save()
        with pytest.raises(ValidationError, match="Game is already finished"):
            game.make_move(0)

    def test_player_switching(self):
        """Test current player switches after valid move."""
        game = Game.objects.create()
        assert game.current_player == 'X'
        game.make_move(0)
        assert game.current_player == 'O'
        game.make_move(1)
        assert game.current_player == 'X'

    def test_x_wins_top_row(self):
        """Test X wins with top row (0,1,2)."""
        game = Game.objects.create()
        game.make_move(0)  # X
        game.make_move(3)  # O
        game.make_move(1)  # X
        game.make_move(4)  # O
        game.make_move(2)  # X wins
        assert game.status == Game.STATUS_X_WINS

    def test_x_wins_middle_row(self):
        """Test X wins with middle row (3,4,5)."""
        game = Game.objects.create()
        game.make_move(3)  # X
        game.make_move(0)  # O
        game.make_move(4)  # X
        game.make_move(1)  # O
        game.make_move(5)  # X wins
        assert game.status == Game.STATUS_X_WINS

    def test_x_wins_bottom_row(self):
        """Test X wins with bottom row (6,7,8)."""
        game = Game.objects.create()
        game.make_move(6)  # X
        game.make_move(0)  # O
        game.make_move(7)  # X
        game.make_move(1)  # O
        game.make_move(8)  # X wins
        assert game.status == Game.STATUS_X_WINS

    def test_x_wins_left_column(self):
        """Test X wins with left column (0,3,6)."""
        game = Game.objects.create()
        game.make_move(0)  # X
        game.make_move(1)  # O
        game.make_move(3)  # X
        game.make_move(2)  # O
        game.make_move(6)  # X wins
        assert game.status == Game.STATUS_X_WINS

    def test_x_wins_middle_column(self):
        """Test X wins with middle column (1,4,7)."""
        game = Game.objects.create()
        game.make_move(1)  # X
        game.make_move(0)  # O
        game.make_move(4)  # X
        game.make_move(2)  # O
        game.make_move(7)  # X wins
        assert game.status == Game.STATUS_X_WINS

    def test_x_wins_right_column(self):
        """Test X wins with right column (2,5,8)."""
        game = Game.objects.create()
        game.make_move(2)  # X
        game.make_move(0)  # O
        game.make_move(5)  # X
        game.make_move(1)  # O
        game.make_move(8)  # X wins
        assert game.status == Game.STATUS_X_WINS

    def test_x_wins_diagonal_descending(self):
        """Test X wins with diagonal \\ (0,4,8)."""
        game = Game.objects.create()
        game.make_move(0)  # X
        game.make_move(1)  # O
        game.make_move(4)  # X
        game.make_move(2)  # O
        game.make_move(8)  # X wins
        assert game.status == Game.STATUS_X_WINS

    def test_x_wins_diagonal_ascending(self):
        """Test X wins with diagonal / (2,4,6)."""
        game = Game.objects.create()
        game.make_move(2)  # X
        game.make_move(0)  # O
        game.make_move(4)  # X
        game.make_move(1)  # O
        game.make_move(6)  # X wins
        assert game.status == Game.STATUS_X_WINS

    def test_o_wins_top_row(self):
        """Test O wins with top row (0,1,2)."""
        game = Game.objects.create()
        game.make_move(3)  # X
        game.make_move(0)  # O
        game.make_move(4)  # X
        game.make_move(1)  # O
        game.make_move(6)  # X
        game.make_move(2)  # O wins
        assert game.status == Game.STATUS_O_WINS

    def test_draw_detection(self):
        """Test draw when board is full with no winner."""
        game = Game.objects.create()
        moves = [0, 1, 2, 4, 3, 5, 7, 6, 8]  # Results in draw
        for move in moves:
            game.make_move(move)
        assert game.status == Game.STATUS_DRAW

    def test_game_in_progress(self):
        """Test game remains in progress with partial board."""
        game = Game.objects.create()
        game.make_move(0)
        game.make_move(1)
        assert game.status == Game.STATUS_IN_PROGRESS

    def test_str_representation(self):
        """Test __str__ method."""
        game = Game.objects.create()
        assert f"Game {game.id}" in str(game)
        assert "In Progress" in str(game)

    def test_board_display(self):
        """Test get_board_display method."""
        game = Game.objects.create()
        game.make_move(0)  # X at position 0
        display = game.get_board_display()
        assert 'X' in display
        assert '|' in display

    def test_check_winner_returns_none_empty_board(self):
        """Test check_winner returns None for empty board."""
        game = Game.objects.create()
        assert game.check_winner() is None

    def test_check_winner_returns_x_when_x_wins(self):
        """Test check_winner returns 'X' when X has won."""
        game = Game.objects.create()
        game.board = ['X', 'X', 'X', None, None, None, None, None, None]
        assert game.check_winner() == 'X'

    def test_is_draw_returns_false_for_partial_board(self):
        """Test is_draw returns False for partial board."""
        game = Game.objects.create()
        game.make_move(0)
        assert game.is_draw() is False

    def test_is_draw_returns_true_for_full_board_no_winner(self):
        """Test is_draw returns True when board full with no winner."""
        game = Game.objects.create()
        game.board = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']
        assert game.is_draw() is True
