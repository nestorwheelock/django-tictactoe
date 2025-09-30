from django.db import models
from django.core.exceptions import ValidationError


class Game(models.Model):
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

    PLAYER_X = 'X'
    PLAYER_O = 'O'

    PLAYER_CHOICES = [
        (PLAYER_X, 'Player X'),
        (PLAYER_O, 'Player O'),
    ]

    WINNING_COMBINATIONS = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    board = models.JSONField(default=list, help_text="Game board state (9 elements)")
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

    def __str__(self) -> str:
        return f"Game {self.id} - {self.get_status_display()}"

    def save(self, *args, **kwargs) -> None:
        if not self.board:
            self.board = [None] * 9
        super().save(*args, **kwargs)

    def make_move(self, position: int) -> dict:
        if self.status != self.STATUS_IN_PROGRESS:
            raise ValidationError("Game is already finished")

        if not isinstance(position, int) or position < 0 or position > 8:
            raise ValidationError("Position must be between 0 and 8")

        if self.board[position] is not None:
            raise ValidationError("Position already occupied")

        self.board[position] = self.current_player
        self.update_status()

        if self.status == self.STATUS_IN_PROGRESS:
            self.current_player = self.PLAYER_O if self.current_player == self.PLAYER_X else self.PLAYER_X

        self.save()

        return {
            'success': True,
            'message': 'Move successful'
        }

    def check_winner(self) -> str | None:
        for combo in self.WINNING_COMBINATIONS:
            if (self.board[combo[0]] == self.board[combo[1]] ==
                self.board[combo[2]] and self.board[combo[0]] is not None):
                return self.board[combo[0]]
        return None

    def is_draw(self) -> bool:
        return None not in self.board and self.check_winner() is None

    def update_status(self) -> None:
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
        def cell(val):
            return val if val else ' '

        return f"""
 {cell(self.board[0])} | {cell(self.board[1])} | {cell(self.board[2])}
-----------
 {cell(self.board[3])} | {cell(self.board[4])} | {cell(self.board[5])}
-----------
 {cell(self.board[6])} | {cell(self.board[7])} | {cell(self.board[8])}
"""
