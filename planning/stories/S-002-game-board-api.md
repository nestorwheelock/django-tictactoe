# S-002: Game Board Management API

**Story Type**: User Story
**Priority**: High
**Estimate**: 1 day
**Sprint**: Sprint 1
**Status**: 📋 PENDING

---

## User Story

**As a** developer using the module
**I want** REST API endpoints for game management
**So that** I can integrate tic-tac-toe into my frontend or application

---

## Acceptance Criteria

- [ ] When I POST to `/api/games/`, a new game is created and I receive a game ID
- [ ] When I GET `/api/games/{id}/`, I see the current board state and game status
- [ ] When I POST to `/api/games/{id}/move/` with valid position, the board updates
- [ ] When I POST an invalid move (occupied square), I receive a 400 error with clear message
- [ ] When I POST a move out of turn, I receive a 400 error
- [ ] When I POST a move after game is over, I receive a 400 error
- [ ] API responses follow REST conventions and include proper HTTP status codes

---

## Definition of Done

- [ ] Game model created with fields:
  - `board`: JSONField storing 9-cell array
  - `current_player`: CharField ('X' or 'O')
  - `status`: CharField ('in_progress', 'x_wins', 'o_wins', 'draw')
  - `created_at`, `updated_at`: DateTimeField
- [ ] GameSerializer with proper field validation
- [ ] GameViewSet with actions: create, retrieve, list, move
- [ ] URL routing configured with namespace 'tictactoe'
- [ ] Comprehensive API tests (>95% coverage):
  - Create game
  - Retrieve game
  - Valid moves
  - Invalid moves (occupied, wrong turn, game over)
  - Edge cases
- [ ] API documentation in README

---

## API Specification

### Endpoints

**Create Game**
```
POST /tictactoe/api/games/

Response 201:
{
  "id": 1,
  "board": [null, null, null, null, null, null, null, null, null],
  "current_player": "X",
  "status": "in_progress",
  "created_at": "2025-09-30T12:00:00Z",
  "updated_at": "2025-09-30T12:00:00Z"
}
```

**Get Game State**
```
GET /tictactoe/api/games/{id}/

Response 200:
{
  "id": 1,
  "board": ["X", null, "O", null, "X", null, null, null, null],
  "current_player": "O",
  "status": "in_progress",
  "created_at": "2025-09-30T12:00:00Z",
  "updated_at": "2025-09-30T12:05:00Z"
}
```

**Make Move**
```
POST /tictactoe/api/games/{id}/move/
{
  "position": 4
}

Response 200:
{
  "id": 1,
  "board": ["X", null, "O", null, "X", null, null, null, null],
  "current_player": "O",
  "status": "in_progress",
  "message": "Move successful"
}

Response 400 (invalid move):
{
  "error": "Position already occupied"
}

Response 400 (wrong turn):
{
  "error": "Not your turn"
}

Response 400 (game over):
{
  "error": "Game is already finished"
}
```

**List Games**
```
GET /tictactoe/api/games/

Response 200:
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "board": [...],
      "status": "x_wins",
      ...
    },
    {
      "id": 2,
      "board": [...],
      "status": "in_progress",
      ...
    }
  ]
}
```

**Delete Game**
```
DELETE /tictactoe/api/games/{id}/

Response 204 No Content
```

---

## Board Representation

Board is stored as JSON array with 9 elements (0-8):
```
[0, 1, 2]     Top row
[3, 4, 5]     Middle row
[6, 7, 8]     Bottom row

Values: null (empty), "X", or "O"
```

---

## Technical Notes

**Model Design**:
- Use JSONField for board (portable across DB backends)
- Status choices as constants
- Add model methods: `make_move()`, `check_winner()`, `is_draw()`

**Validation**:
- Position must be 0-8
- Position must be empty (null)
- Must be current player's turn
- Game must be in_progress status

**DRF Configuration**:
- Use ModelViewSet for standard CRUD
- Add custom action `@action(methods=['post'])` for move endpoint
- Use serializer validation for move logic

---

## Tasks

This story is implemented through:
- T-002: Game Model & Migrations
- T-003: REST API Implementation

---

## Test Scenarios

1. Create multiple games
2. Make alternating valid moves
3. Attempt occupied square
4. Attempt out-of-turn move
5. Attempt move after game ends
6. Invalid position (negative, >8, non-integer)
7. List all games
8. Retrieve non-existent game (404)
9. Delete game
