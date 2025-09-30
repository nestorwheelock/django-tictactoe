# T-002: Game Model & Migrations

**Related Story**: S-002 (Game Board Management API), S-003 (Win/Draw Detection)
**Estimate**: 3 hours
**Priority**: High
**Status**: 📋 PENDING
**Depends On**: T-001

---

## AI Coding Brief

**Role**: Django Backend Developer
**Objective**: Implement the Game model with board state management, game logic methods, and Django admin integration
**User Request**: "Create game model with win/draw detection logic"

---

## Constraints

**Allowed File Paths**:
- `tictactoe/models.py`
- `tictactoe/admin.py`
- `tictactoe/migrations/`
- `tictactoe/tests/test_models.py`

**Forbidden Paths**:
- Other app files (views, serializers) - those come in T-003

**Technical Constraints**:
- Use JSONField for board storage (Django 3.1+)
- All game logic must be in model methods
- >95% test coverage required
- Must work with PostgreSQL, MySQL, SQLite

---

## Deliverables

### 1. Game Model (tictactoe/models.py)

```python
from django.db import models
from django.core.exceptions import ValidationError

class Game(models.Model):
    """
    Tic-tac-toe game model.

    Board is stored as JSON array of 9 elements (positions 0-8):
    [0, 1, 2]  -> Top row
    [3, 4, 5]  -> Middle row
    [6, 7, 8]  -> Bottom row

    Values: null (empty), "X", or "O"
    """

    # Game status choices
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_X_WINS = 'x_wins'
    STATUS_O_WINS = 'o_wins'
    STATUS_DRAW = 'draw'

    STATUS_CHOICES = [
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_X_WINS, 'X Wins'),
        (STATUS_O_WINS, 'O Wins'),
        (STATUS_DRAW, 'Draw'),
    ]

    # Player choices
    PLAYER_X = 'X'
    PLAYER_O = 'O'

    PLAYER_CHOICES = [
        (PLAYER_X, 'Player X'),
        (PLAYER_O, 'Player O'),
    ]

    # Winning combinations
    WINNING_COMBINATIONS = [
        [0, 1, 2],  # Top row
        [3, 4, 5],  # Middle row
        [6, 7, 8],  # Bottom row
        [0, 3, 6],  # Left column
        [1, 4, 7],  # Middle column
        [2, 5, 8],  # Right column
        [0, 4, 8],  # Diagonal \
        [2, 4, 6],  # Diagonal /
    ]

    # Fields
    board = models.JSONField(
        default=list,
        help_text="Game board state (9 elements)"
    )
    current_player = models.CharField(
        max_length=1,
        choices=PLAYER_CHOICES,
        default=PLAYER_X,
        help_text="Current player's turn"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_IN_PROGRESS,
        help_text="Current game status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Tic-Tac-Toe Game'
        verbose_name_plural = 'Tic-Tac-Toe Games'

    def __str__(self):
        return f"Game {self.id} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        """Initialize empty board on creation."""
        if not self.board:
            self.board = [None] * 9
        super().save(*args, **kwargs)

    def make_move(self, position: int) -> dict:
        """
        Make a move at the given position.

        Args:
            position: Board position (0-8)

        Returns:
            dict with 'success' bool and 'message' str

        Raises:
            ValidationError: If move is invalid
        """
        # Validation checks
        if self.status != self.STATUS_IN_PROGRESS:
            raise ValidationError("Game is already finished")

        if not isinstance(position, int) or position < 0 or position > 8:
            raise ValidationError("Position must be between 0 and 8")

        if self.board[position] is not None:
            raise ValidationError("Position already occupied")

        # Make the move
        self.board[position] = self.current_player

        # Update game status
        self.update_status()

        # Switch player if game still in progress
        if self.status == self.STATUS_IN_PROGRESS:
            self.current_player = self.PLAYER_O if self.current_player == self.PLAYER_X else self.PLAYER_X

        self.save()

        return {
            'success': True,
            'message': 'Move successful'
        }

    def check_winner(self) -> str | None:
        """
        Check if there's a winner.

        Returns:
            'X', 'O', or None
        """
        for combo in self.WINNING_COMBINATIONS:
            if (self.board[combo[0]] == self.board[combo[1]] ==
                self.board[combo[2]] and self.board[combo[0]] is not None):
                return self.board[combo[0]]
        return None

    def is_draw(self) -> bool:
        """
        Check if game is a draw (board full, no winner).

        Returns:
            bool
        """
        return None not in self.board and self.check_winner() is None

    def update_status(self) -> None:
        """Update game status based on current board state."""
        winner = self.check_winner()
        if winner == self.PLAYER_X:
            self.status = self.STATUS_X_WINS
        elif winner == self.PLAYER_O:
            self.status = self.STATUS_O_WINS
        elif self.is_draw():
            self.status = self.STATUS_DRAW
        else:
            self.status = self.STATUS_IN_PROGRESS

    def get_board_display(self) -> str:
        """Get human-readable board representation."""
        def cell(val):
            return val if val else ' '

        return f"""
        {cell(self.board[0])} | {cell(self.board[1])} | {cell(self.board[2])}
        ---------
        {cell(self.board[3])} | {cell(self.board[4])} | {cell(self.board[5])}
        ---------
        {cell(self.board[6])} | {cell(self.board[7])} | {cell(self.board[8])}
        """
```

### 2. Django Admin Integration (tictactoe/admin.py)

```python
from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'current_player', 'created_at', 'updated_at']
    list_filter = ['status', 'current_player', 'created_at']
    search_fields = ['id']
    readonly_fields = ['created_at', 'updated_at', 'board_display']

    fieldsets = (
        ('Game State', {
            'fields': ('board_display', 'current_player', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def board_display(self, obj):
        """Display board in admin."""
        return obj.get_board_display()
    board_display.short_description = 'Board'

    def has_add_permission(self, request):
        """Disable manual game creation in admin."""
        return False
```

### 3. Database Migration

Run `python manage.py makemigrations` to create initial migration

### 4. Comprehensive Model Tests (tictactoe/tests/test_models.py)

**Test Coverage Required**:
- Game creation with default values
- Board initialization
- Valid move making
- Invalid moves (occupied, out of bounds, game over)
- All 8 winning patterns for X
- All 8 winning patterns for O
- Draw detection
- Player switching
- Status updates
- String representation
- Board display

**Minimum 20 test cases** to achieve >95% coverage

Example test structure:
```python
import pytest
from django.core.exceptions import ValidationError
from tictactoe.models import Game

@pytest.mark.django_db
class TestGameModel:
    def test_game_creation_defaults(self):
        """Test game is created with correct defaults."""

    def test_board_initialization(self):
        """Test board initializes as 9 nulls."""

    def test_valid_move(self):
        """Test making a valid move."""

    def test_occupied_position_raises_error(self):
        """Test moving to occupied position raises ValidationError."""

    def test_invalid_position_raises_error(self):
        """Test invalid position raises ValidationError."""

    def test_move_after_game_over_raises_error(self):
        """Test move after game ends raises ValidationError."""

    def test_player_switching(self):
        """Test current player switches after valid move."""

    def test_x_wins_top_row(self):
        """Test X wins with top row (0,1,2)."""

    def test_x_wins_middle_row(self):
        """Test X wins with middle row (3,4,5)."""

    def test_x_wins_bottom_row(self):
        """Test X wins with bottom row (6,7,8)."""

    def test_x_wins_left_column(self):
        """Test X wins with left column (0,3,6)."""

    def test_x_wins_middle_column(self):
        """Test X wins with middle column (1,4,7)."""

    def test_x_wins_right_column(self):
        """Test X wins with right column (2,5,8)."""

    def test_x_wins_diagonal_descending(self):
        """Test X wins with diagonal \ (0,4,8)."""

    def test_x_wins_diagonal_ascending(self):
        """Test X wins with diagonal / (2,4,6)."""

    def test_o_wins_top_row(self):
        """Test O wins with top row (0,1,2)."""

    def test_draw_detection(self):
        """Test draw when board is full with no winner."""

    def test_game_in_progress(self):
        """Test game remains in progress with partial board."""

    def test_str_representation(self):
        """Test __str__ method."""

    def test_board_display(self):
        """Test get_board_display method."""
```

---

## Definition of Done

- [ ] Game model implemented with all fields and methods
- [ ] Model uses JSONField for board storage
- [ ] All 8 winning combinations correctly detected
- [ ] Draw detection working correctly
- [ ] Player switching logic correct
- [ ] Move validation comprehensive (occupied, bounds, game over)
- [ ] Django admin configured and working
- [ ] Database migration created and tested
- [ ] All model tests passing (minimum 20 tests)
- [ ] Test coverage >95% for models.py
- [ ] Type hints used throughout
- [ ] Docstrings for all methods
- [ ] PEP 8 compliant

---

## Validation Steps

1. Run `python manage.py makemigrations` - should create migration
2. Run `python manage.py migrate` - should apply successfully
3. Run `pytest tictactoe/tests/test_models.py -v` - all tests pass
4. Run `pytest tictactoe/tests/test_models.py --cov=tictactoe.models` - >95% coverage
5. Create game in Django shell - verify defaults
6. Make moves in Django shell - verify logic
7. Check Django admin - verify game appears and is readable

---

## Dependencies

**Blocking**: T-001 (App Module Setup)
**Blocked By**: T-003 (REST API depends on this model)

---

## Notes

- Focus on business logic correctness
- Comprehensive test coverage is critical
- Model methods should be pure logic (no HTTP concerns)
- Use Django's ValidationError for all validation failures
- Keep admin interface read-only (games created via API)
