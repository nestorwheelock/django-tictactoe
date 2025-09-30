# T-004: Frontend Templates

**Related Story**: S-004 (Optional Frontend Templates)
**Estimate**: 3 hours
**Priority**: Medium
**Status**: 📋 PENDING
**Depends On**: T-003

---

## AI Coding Brief

**Role**: Frontend Developer (Vanilla JS/CSS)
**Objective**: Create optional frontend templates and JavaScript for playing tic-tac-toe games using the REST API
**User Request**: "Create simple frontend interface for the game"

---

## Constraints

**Allowed File Paths**:
- `tictactoe/templates/tictactoe/`
- `tictactoe/static/tictactoe/`
- `tictactoe/views.py` (template views already added in T-003)
- `tictactoe/tests/test_views.py`

**Forbidden Paths**:
- API files (already done)
- Model files (already done)

**Technical Constraints**:
- No JavaScript frameworks (vanilla JS only)
- No CSS frameworks (pure CSS)
- No build process required
- Must work without JavaScript (graceful degradation)
- Support modern browsers only (ES6+)

---

## Deliverables

### 1. Base Template (tictactoe/templates/tictactoe/base.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Tic-Tac-Toe{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'tictactoe/game.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <div class="container">
        <header>
            <h1>Tic-Tac-Toe</h1>
        </header>

        <main>
            {% block content %}{% endblock %}
        </main>

        <footer>
            <p>Django Tic-Tac-Toe Module v1.0.0</p>
        </footer>
    </div>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 2. Game List Template (tictactoe/templates/tictactoe/game_list.html)

```html
{% extends "tictactoe/base.html" %}

{% block title %}Games | Tic-Tac-Toe{% endblock %}

{% block content %}
<div class="game-list">
    <div class="list-header">
        <h2>All Games</h2>
        <button id="new-game-btn" class="btn btn-primary">New Game</button>
    </div>

    {% if games %}
    <table class="games-table">
        <thead>
            <tr>
                <th>Game ID</th>
                <th>Status</th>
                <th>Current Player</th>
                <th>Created</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for game in games %}
            <tr>
                <td>#{{ game.id }}</td>
                <td>
                    <span class="status status-{{ game.status }}">
                        {{ game.get_status_display }}
                    </span>
                </td>
                <td>{{ game.current_player }}</td>
                <td>{{ game.created_at|date:"Y-m-d H:i" }}</td>
                <td>
                    <a href="{% url 'tictactoe:game-detail' game.id %}" class="btn btn-small">
                        Play
                    </a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p class="no-games">No games yet. Create your first game!</p>
    {% endif %}
</div>
{% endblock %}

{% block extra_js %}
{% load static %}
<script src="{% static 'tictactoe/game.js' %}"></script>
<script>
    document.getElementById('new-game-btn').addEventListener('click', async () => {
        const gameId = await TicTacToe.createGame();
        if (gameId) {
            window.location.href = `/tictactoe/game/${gameId}/`;
        }
    });
</script>
{% endblock %}
```

### 3. Game Detail Template (tictactoe/templates/tictactoe/game_detail.html)

```html
{% extends "tictactoe/base.html" %}
{% load static %}

{% block title %}Game #{{ game.id }} | Tic-Tac-Toe{% endblock %}

{% block content %}
<div class="game-container">
    <div class="game-header">
        <a href="{% url 'tictactoe:game-list' %}" class="btn btn-secondary">← Back to Games</a>
        <h2>Game #{{ game.id }}</h2>
    </div>

    <div class="game-info">
        <div class="info-item">
            <span class="label">Current Player:</span>
            <span id="current-player" class="value player-{{ game.current_player }}">
                {{ game.current_player }}
            </span>
        </div>
        <div class="info-item">
            <span class="label">Status:</span>
            <span id="game-status" class="value status-{{ game.status }}">
                {{ game.get_status_display }}
            </span>
        </div>
    </div>

    <div id="game-board" class="board" data-game-id="{{ game.id }}">
        {% for cell in game.board %}
        <div class="cell" data-position="{{ forloop.counter0 }}">
            {% if cell %}
            <span class="mark mark-{{ cell }}">{{ cell }}</span>
            {% endif %}
        </div>
        {% endfor %}
    </div>

    <div class="game-actions">
        <button id="new-game-btn" class="btn btn-primary">New Game</button>
        <button id="refresh-btn" class="btn btn-secondary">Refresh</button>
    </div>

    <div id="message" class="message"></div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'tictactoe/game.js' %}"></script>
<script>
    const gameId = {{ game.id }};
    TicTacToe.initGame(gameId);
</script>
{% endblock %}
```

### 4. JavaScript (tictactoe/static/tictactoe/game.js)

```javascript
const TicTacToe = {
    apiBaseUrl: '/tictactoe/api',
    currentGameId: null,

    async createGame() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/games/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                return data.id;
            } else {
                this.showError('Failed to create game');
                return null;
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
            return null;
        }
    },

    async loadGame(gameId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/games/${gameId}/`);

            if (response.ok) {
                const data = await response.json();
                this.updateBoard(data);
                return data;
            } else {
                this.showError('Failed to load game');
                return null;
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
            return null;
        }
    },

    async makeMove(gameId, position) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/games/${gameId}/move/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ position }),
            });

            const data = await response.json();

            if (response.ok) {
                this.updateBoard(data);
                this.showMessage(data.message || 'Move successful', 'success');
                return data;
            } else {
                this.showError(data.error || 'Invalid move');
                return null;
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
            return null;
        }
    },

    updateBoard(gameData) {
        // Update board cells
        const cells = document.querySelectorAll('.cell');
        cells.forEach((cell, index) => {
            const mark = gameData.board[index];
            cell.innerHTML = mark ? `<span class="mark mark-${mark}">${mark}</span>` : '';

            // Enable/disable cells based on game state
            if (gameData.status === 'in_progress' && !mark) {
                cell.classList.add('clickable');
            } else {
                cell.classList.remove('clickable');
            }
        });

        // Update game info
        const currentPlayerEl = document.getElementById('current-player');
        if (currentPlayerEl) {
            currentPlayerEl.textContent = gameData.current_player;
            currentPlayerEl.className = `value player-${gameData.current_player}`;
        }

        const statusEl = document.getElementById('game-status');
        if (statusEl) {
            const statusText = {
                'in_progress': 'In Progress',
                'x_wins': 'X Wins!',
                'o_wins': 'O Wins!',
                'draw': 'Draw'
            }[gameData.status];
            statusEl.textContent = statusText;
            statusEl.className = `value status-${gameData.status}`;
        }

        // Show game over message
        if (gameData.status !== 'in_progress') {
            const messages = {
                'x_wins': '🎉 Player X wins!',
                'o_wins': '🎉 Player O wins!',
                'draw': '🤝 It\'s a draw!'
            };
            this.showMessage(messages[gameData.status], 'success');
        }
    },

    showMessage(text, type = 'info') {
        const messageEl = document.getElementById('message');
        if (messageEl) {
            messageEl.textContent = text;
            messageEl.className = `message message-${type}`;
            setTimeout(() => {
                messageEl.textContent = '';
                messageEl.className = 'message';
            }, 3000);
        }
    },

    showError(text) {
        this.showMessage(text, 'error');
    },

    initGame(gameId) {
        this.currentGameId = gameId;

        // Load initial game state
        this.loadGame(gameId);

        // Setup cell click handlers
        const board = document.getElementById('game-board');
        if (board) {
            board.addEventListener('click', async (e) => {
                const cell = e.target.closest('.cell');
                if (cell && cell.classList.contains('clickable')) {
                    const position = parseInt(cell.dataset.position);
                    await this.makeMove(gameId, position);
                }
            });
        }

        // Setup new game button
        const newGameBtn = document.getElementById('new-game-btn');
        if (newGameBtn) {
            newGameBtn.addEventListener('click', async () => {
                const newGameId = await this.createGame();
                if (newGameId) {
                    window.location.href = `/tictactoe/game/${newGameId}/`;
                }
            });
        }

        // Setup refresh button
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.loadGame(gameId);
            });
        }
    }
};
```

### 5. CSS (tictactoe/static/tictactoe/game.css)

```css
/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    border-radius: 10px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    padding: 30px;
}

header h1 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
}

/* Game board */
.game-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.game-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-bottom: 20px;
}

.game-info {
    display: flex;
    gap: 30px;
    margin-bottom: 30px;
    font-size: 18px;
}

.info-item {
    display: flex;
    gap: 10px;
}

.info-item .label {
    font-weight: bold;
    color: #666;
}

.info-item .value {
    color: #333;
}

.board {
    display: grid;
    grid-template-columns: repeat(3, 100px);
    grid-template-rows: repeat(3, 100px);
    gap: 10px;
    margin-bottom: 30px;
}

.cell {
    background: #f0f0f0;
    border: 2px solid #ddd;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 48px;
    font-weight: bold;
    cursor: default;
    transition: all 0.2s;
}

.cell.clickable {
    cursor: pointer;
    background: white;
}

.cell.clickable:hover {
    background: #e8f4f8;
    border-color: #667eea;
    transform: scale(1.05);
}

.mark-X {
    color: #667eea;
}

.mark-O {
    color: #764ba2;
}

/* Buttons */
.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
    display: inline-block;
}

.btn-primary {
    background: #667eea;
    color: white;
}

.btn-primary:hover {
    background: #5568d3;
}

.btn-secondary {
    background: #6c757d;
    color: white;
}

.btn-secondary:hover {
    background: #5a6268;
}

.btn-small {
    padding: 5px 15px;
    font-size: 14px;
}

.game-actions {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

/* Messages */
.message {
    padding: 10px 20px;
    border-radius: 5px;
    text-align: center;
    min-height: 20px;
}

.message-success {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.message-error {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

/* Status badges */
.status {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
}

.status-in_progress {
    background: #fff3cd;
    color: #856404;
}

.status-x_wins {
    background: #d4edda;
    color: #155724;
}

.status-o_wins {
    background: #d4edda;
    color: #155724;
}

.status-draw {
    background: #d1ecf1;
    color: #0c5460;
}

/* Game list */
.game-list {
    width: 100%;
}

.list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.games-table {
    width: 100%;
    border-collapse: collapse;
}

.games-table th,
.games-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.games-table th {
    background: #f8f9fa;
    font-weight: bold;
}

.games-table tr:hover {
    background: #f8f9fa;
}

.no-games {
    text-align: center;
    color: #666;
    padding: 40px;
}

footer {
    text-align: center;
    color: #666;
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #ddd;
}

/* Responsive */
@media (max-width: 480px) {
    .board {
        grid-template-columns: repeat(3, 80px);
        grid-template-rows: repeat(3, 80px);
        gap: 8px;
    }

    .cell {
        font-size: 36px;
    }
}
```

### 6. Template View Tests (tictactoe/tests/test_views.py)

```python
import pytest
from django.urls import reverse
from tictactoe.models import Game

@pytest.mark.django_db
class TestTemplateViews:
    def test_game_list_view(self, client):
        """Test game list view renders correctly."""
        Game.objects.create()
        Game.objects.create()

        response = client.get(reverse('tictactoe:game-list'))
        assert response.status_code == 200
        assert 'games' in response.context
        assert len(response.context['games']) == 2

    def test_game_detail_view(self, client):
        """Test game detail view renders correctly."""
        game = Game.objects.create()

        response = client.get(reverse('tictactoe:game-detail', args=[game.id]))
        assert response.status_code == 200
        assert response.context['game'].id == game.id

    def test_game_detail_view_404(self, client):
        """Test game detail view returns 404 for non-existent game."""
        response = client.get(reverse('tictactoe:game-detail', args=[999]))
        assert response.status_code == 404
```

---

## Definition of Done

- [ ] Base template created with proper structure
- [ ] Game list template showing all games
- [ ] Game detail template with playable board
- [ ] JavaScript handles all game interactions
- [ ] CSS provides clean, responsive design
- [ ] Error handling for API failures
- [ ] Success messages for actions
- [ ] Templates are overridable by host project
- [ ] Works on modern browsers (Chrome, Firefox, Safari, Edge)
- [ ] Template view tests written and passing
- [ ] No console errors
- [ ] Accessible keyboard navigation

---

## Validation Steps

1. Run development server
2. Navigate to `/tictactoe/` - see game list
3. Click "New Game" - creates and navigates to new game
4. Play complete game - verify moves work
5. Test invalid moves - verify error messages
6. Check responsive design on different screen sizes
7. Test in multiple browsers
8. Verify templates can be overridden
9. Check browser console for errors

---

## Dependencies

**Blocking**: T-003 (REST API Implementation)
**Blocked By**: None

---

## Notes

- Keep JavaScript simple and readable
- CSS should be easily customizable
- Templates should serve as examples
- No build process required (keep it simple)
- Focus on functionality over fancy animations
