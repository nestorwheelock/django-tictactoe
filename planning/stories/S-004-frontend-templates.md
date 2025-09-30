# S-004: Optional Frontend Templates

**Story Type**: User Story
**Priority**: Medium
**Estimate**: 0.5 days
**Sprint**: Sprint 1
**Status**: 📋 PENDING

---

## User Story

**As a** Django developer
**I want** optional pre-built templates
**So that** I can use the game immediately without building a UI

---

## Acceptance Criteria

- [ ] When I visit `/tictactoe/`, I see a list of games
- [ ] When I visit `/tictactoe/game/{id}/`, I see a playable game board
- [ ] When I click an empty square on my turn, my move is made
- [ ] When the game ends, I see the result (winner or draw)
- [ ] When I click "New Game", a new game is created
- [ ] Templates are customizable/overridable via Django's template system
- [ ] Works with any Django template engine
- [ ] No CSS framework dependencies (pure CSS)
- [ ] Responsive design works on desktop and tablet

---

## Definition of Done

- [ ] Base template: `tictactoe/base.html`
- [ ] Game list template: `tictactoe/game_list.html`
- [ ] Game play template: `tictactoe/game_detail.html`
- [ ] JavaScript file: `tictactoe/static/tictactoe/game.js`
- [ ] CSS file: `tictactoe/static/tictactoe/game.css`
- [ ] Django views for template rendering
- [ ] URL configuration for frontend views
- [ ] Template documentation in README
- [ ] JavaScript uses Fetch API for all game operations
- [ ] Error handling for API failures

---

## Template Structure

```
tictactoe/templates/tictactoe/
├── base.html           # Base template with common structure
├── game_list.html      # List all games
└── game_detail.html    # Play game

tictactoe/static/tictactoe/
├── game.js             # Game interaction logic
└── game.css            # Styling
```

---

## UI Design

**Game Board Layout**:
```
┌─────────────────────────┐
│   Tic-Tac-Toe Game      │
│                         │
│  ┌───┬───┬───┐          │
│  │   │   │   │          │
│  ├───┼───┼───┤          │
│  │   │   │   │          │
│  ├───┼───┼───┤          │
│  │   │   │   │          │
│  └───┴───┴───┘          │
│                         │
│  Current Player: X      │
│  Status: In Progress    │
│                         │
│  [New Game]             │
└─────────────────────────┘
```

---

## Frontend Features

**Game List Page** (`/tictactoe/`):
- Display all games in a table
- Show game ID, status, created date
- Link to play each game
- "Create New Game" button

**Game Play Page** (`/tictactoe/game/{id}/`):
- 3x3 grid of clickable squares
- Display current player's turn
- Display game status
- Show winner/draw message when game ends
- "New Game" button
- "Back to Games" link

**JavaScript Functionality**:
- Load game state on page load
- Handle square clicks
- Make API calls to move endpoint
- Update board display after moves
- Disable clicks when game is over
- Show error messages for invalid moves

---

## Technical Implementation

**Views** (in `views.py`):
```python
def game_list(request):
    """Display list of all games."""

def game_detail(request, pk):
    """Display single game for playing."""
```

**URLs** (in `urls.py`):
```python
urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),

    # Frontend URLs
    path('', views.game_list, name='game-list'),
    path('game/<int:pk>/', views.game_detail, name='game-detail'),
]
```

**JavaScript** (game.js):
- Fetch game state
- Handle click events
- POST moves to API
- Update DOM with new state
- Handle errors gracefully

**CSS** (game.css):
- Grid layout for board
- Hover effects on squares
- Different colors for X and O
- Responsive sizing
- Game status styling

---

## Customization Support

Developers can override templates by creating their own:
```
# In host Django project
templates/
└── tictactoe/
    ├── base.html           # Override base
    └── game_detail.html    # Override game page
```

CSS can be customized by:
1. Overriding the entire CSS file
2. Adding additional CSS that overrides specific rules
3. Using CSS variables (if we define them)

---

## Browser Support

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)

Uses modern JavaScript (ES6+):
- Fetch API
- Arrow functions
- Template literals
- Const/let

---

## Tasks

This story is implemented through:
- T-004: Frontend Templates

---

## Test Scenarios

1. Load game list page
2. Create new game from UI
3. Load game detail page
4. Make valid move by clicking square
5. Attempt invalid move (occupied square)
6. Complete full game to win
7. Complete full game to draw
8. View finished game (no moves allowed)
9. Navigate between pages
10. Handle API errors gracefully

---

## Notes

- Templates are optional - API can be used standalone
- Keep JavaScript simple - no build process required
- Pure CSS - no preprocessors needed
- Follow Django template best practices
- Use Django's static file system
