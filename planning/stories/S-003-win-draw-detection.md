# S-003: Win/Draw Detection Logic

**Story Type**: User Story
**Priority**: High
**Estimate**: 0.5 days
**Sprint**: Sprint 1
**Status**: 📋 PENDING

---

## User Story

**As a** player
**I want** automatic win/draw detection
**So that** the game knows when it's over and declares the winner

---

## Acceptance Criteria

- [ ] When a player gets 3 in a row horizontally, they win
- [ ] When a player gets 3 in a column vertically, they win
- [ ] When a player gets 3 diagonally, they win
- [ ] When all 9 squares are filled with no winner, the game is a draw
- [ ] When the game ends, the status is automatically updated
- [ ] When the game ends, no more moves are allowed

---

## Definition of Done

- [ ] `check_winner()` method on Game model
- [ ] `is_draw()` method on Game model
- [ ] Status automatically updated after each move
- [ ] Tests for all 8 winning combinations:
  - Row 0 (positions 0, 1, 2)
  - Row 1 (positions 3, 4, 5)
  - Row 2 (positions 6, 7, 8)
  - Column 0 (positions 0, 3, 6)
  - Column 1 (positions 1, 4, 7)
  - Column 2 (positions 2, 5, 8)
  - Diagonal \ (positions 0, 4, 8)
  - Diagonal / (positions 2, 4, 6)
- [ ] Tests for draw scenarios
- [ ] Tests for game-in-progress scenarios
- [ ] Test coverage >95%

---

## Winning Patterns

Board positions:
```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

Winning combinations (8 total):
```python
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
```

---

## Game Status Values

```python
class GameStatus:
    IN_PROGRESS = 'in_progress'
    X_WINS = 'x_wins'
    O_WINS = 'o_wins'
    DRAW = 'draw'
```

---

## Logic Flow

After each move:
1. Check if current player won (check all 8 patterns)
2. If winner found, update status to '{player}_wins'
3. If no winner and board is full, update status to 'draw'
4. If no winner and board not full, status remains 'in_progress'
5. Switch current_player if game still in progress

---

## Test Cases

**Win Detection Tests**:
1. Test X wins - top row (0, 1, 2)
2. Test O wins - top row (0, 1, 2)
3. Test X wins - middle row (3, 4, 5)
4. Test X wins - bottom row (6, 7, 8)
5. Test X wins - left column (0, 3, 6)
6. Test X wins - middle column (1, 4, 7)
7. Test X wins - right column (2, 5, 8)
8. Test X wins - diagonal \ (0, 4, 8)
9. Test X wins - diagonal / (2, 4, 6)
10. Test O wins - each pattern

**Draw Detection Tests**:
1. Full board with no winner
2. Near-full board, game in progress

**Edge Cases**:
1. Empty board (no winner, not draw)
2. Single move (no winner, not draw)
3. One square remaining, about to draw

---

## Technical Implementation

**Method: `check_winner()`**
```python
def check_winner(self):
    """
    Check if there's a winner.
    Returns: 'X', 'O', or None
    """
    for combo in WINNING_COMBINATIONS:
        if (self.board[combo[0]] == self.board[combo[1]] ==
            self.board[combo[2]] and self.board[combo[0]] is not None):
            return self.board[combo[0]]
    return None
```

**Method: `is_draw()`**
```python
def is_draw(self):
    """
    Check if game is a draw (board full, no winner).
    Returns: bool
    """
    return None not in self.board and self.check_winner() is None
```

**Method: `update_status()`**
```python
def update_status(self):
    """
    Update game status after a move.
    """
    winner = self.check_winner()
    if winner == 'X':
        self.status = GameStatus.X_WINS
    elif winner == 'O':
        self.status = GameStatus.O_WINS
    elif self.is_draw():
        self.status = GameStatus.DRAW
    else:
        self.status = GameStatus.IN_PROGRESS
```

---

## Tasks

This story is implemented through:
- T-002: Game Model & Migrations (model methods)
- T-003: REST API Implementation (integration with move endpoint)

---

## Notes

- Win detection runs after every move
- Performance is not a concern (only 8 combinations to check)
- Logic should be in the model, not the view/serializer (business logic belongs in model layer)
