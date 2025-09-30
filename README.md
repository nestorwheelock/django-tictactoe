# Django Tic-Tac-Toe

A reusable Django app module providing a complete tic-tac-toe game with REST API and optional web interface.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-4.0%2B-green)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features

- **Complete Game Logic**: Board management, win/draw detection, move validation
- **REST API**: Full CRUD operations with Django REST Framework
- **Web Interface**: Optional responsive frontend templates
- **Django Admin Integration**: Manage games through Django admin
- **Pip-Installable**: Easy integration into existing Django projects
- **Comprehensive Tests**: >95% test coverage with pytest
- **Type Hints**: Full type annotation throughout codebase
- **Customizable**: Override templates, CSS, and views

## Requirements

- Python 3.8+
- Django 4.0+ or 5.x
- Django REST Framework 3.14+

## Installation

### Development Installation

```bash
git clone https://github.com/nestorwheelock/django-tictactoe.git
cd django-tictactoe
pip install -e .
```

### Future: Via pip

```bash
pip install django-tictactoe
```

## Quick Start

### 1. Add to INSTALLED_APPS

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'tictactoe',
]
```

### 2. Include URLs

```python
# urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tictactoe/', include('tictactoe.urls')),
]
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Start Server

```bash
python manage.py runserver
```

### 5. Access the App

- **Web Interface**: http://localhost:8000/tictactoe/
- **API Root**: http://localhost:8000/tictactoe/api/games/
- **Admin Interface**: http://localhost:8000/admin/

## API Endpoints

### Create Game

**Endpoint**: `POST /tictactoe/api/games/`

**Description**: Create a new tic-tac-toe game.

**Request**: No body required

**Response** (201 Created):
```json
{
  "id": 1,
  "board": [null, null, null, null, null, null, null, null, null],
  "current_player": "X",
  "status": "in_progress",
  "created_at": "2025-09-30T12:00:00Z",
  "updated_at": "2025-09-30T12:00:00Z"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/tictactoe/api/games/
```

### List Games

**Endpoint**: `GET /tictactoe/api/games/`

**Description**: Retrieve all games.

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "board": ["X", "O", "X", null, "X", "O", null, null, null],
    "current_player": "O",
    "status": "in_progress",
    "created_at": "2025-09-30T12:00:00Z",
    "updated_at": "2025-09-30T12:05:00Z"
  }
]
```

### Get Game

**Endpoint**: `GET /tictactoe/api/games/{id}/`

**Description**: Retrieve a specific game with detailed information.

**Response** (200 OK):
```json
{
  "id": 1,
  "board": ["X", "O", "X", null, "X", "O", null, null, null],
  "current_player": "O",
  "status": "in_progress",
  "created_at": "2025-09-30T12:00:00Z",
  "updated_at": "2025-09-30T12:05:00Z",
  "board_display": "\n X | O | X \n-----------\n   | X | O \n-----------\n   |   |   \n"
}
```

### Make Move

**Endpoint**: `POST /tictactoe/api/games/{id}/move/`

**Description**: Make a move in the game.

**Request Body**:
```json
{
  "position": 3
}
```

**Position Values**: 0-8 (board positions left-to-right, top-to-bottom)

```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

**Response** (200 OK):
```json
{
  "id": 1,
  "board": ["X", "O", "X", "O", "X", "O", null, null, null],
  "current_player": "X",
  "status": "in_progress",
  "created_at": "2025-09-30T12:00:00Z",
  "updated_at": "2025-09-30T12:06:00Z",
  "message": "Move successful"
}
```

**Error Responses**:

```json
// 400 Bad Request - Position occupied
{
  "error": "['Position already occupied']"
}

// 400 Bad Request - Game over
{
  "error": "['Game is already finished']"
}

// 400 Bad Request - Invalid position
{
  "error": {"position": ["Ensure this value is less than or equal to 8."]}
}
```

### Delete Game

**Endpoint**: `DELETE /tictactoe/api/games/{id}/`

**Description**: Delete a game.

**Response** (204 No Content): Empty response body

## Frontend Usage

The package includes optional responsive templates for playing games through a web interface.

### Game List

Navigate to `/tictactoe/` to see all games:

- View game status (in progress, X wins, O wins, draw)
- See current player
- Create new games
- Access individual games to play

### Game Play

Navigate to `/tictactoe/game/{id}/` to play a game:

- Interactive 3x3 board
- Click cells to make moves
- Real-time status updates
- Win/draw detection
- Create new games
- Refresh current game state

## Customization

### Override Templates

Create your own templates in your project to override the default ones:

```
your_project/
└── templates/
    └── tictactoe/
        ├── base.html           # Override base layout
        ├── game_list.html      # Override game list
        └── game_detail.html    # Override game board
```

### Override CSS

Customize the appearance by overriding the CSS file:

```
your_project/
└── static/
    └── tictactoe/
        └── game.css
```

### Custom Views

Use the Game model and API in your own views:

```python
from django.views.generic import ListView
from tictactoe.models import Game

class MyActiveGames(ListView):
    model = Game
    template_name = 'my_template.html'

    def get_queryset(self):
        return Game.objects.filter(status=Game.STATUS_IN_PROGRESS)
```

### JavaScript Integration

Use the TicTacToe JavaScript object in your own templates:

```javascript
// Create a game
const gameId = await TicTacToe.createGame();

// Make a move
await TicTacToe.makeMove(gameId, 4);  // Center position

// Load game state
const gameData = await TicTacToe.loadGame(gameId);
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/nestorwheelock/django-tictactoe.git
cd django-tictactoe

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tictactoe --cov-report=html

# Run specific test file
pytest tictactoe/tests/test_models.py -v
```

### Code Quality

```bash
# Format code
black tictactoe/

# Check code style
flake8 tictactoe/

# Type checking (if using mypy)
mypy tictactoe/
```

## Testing

The package includes comprehensive tests with >95% coverage:

- **63 tests** covering all functionality
- Unit tests for models, serializers, views
- Integration tests for API endpoints
- Template view tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=tictactoe --cov-report=term-missing

# Run specific test class
pytest tictactoe/tests/test_api.py::TestGameAPI -v
```

## Architecture

```
tictactoe/
├── models.py           # Game model with business logic
├── serializers.py      # DRF serializers
├── views.py            # API viewsets and template views
├── urls.py             # URL configuration
├── admin.py            # Django admin configuration
├── templates/          # HTML templates
│   └── tictactoe/
│       ├── base.html
│       ├── game_list.html
│       └── game_detail.html
├── static/             # Static files
│   └── tictactoe/
│       ├── game.css
│       └── game.js
└── tests/              # Test suite
    ├── test_models.py
    ├── test_api.py
    ├── test_views.py
    └── test_setup.py
```

## Game Logic

### Board Representation

The board is stored as a 9-element array:

```python
[0, 1, 2,  # Top row
 3, 4, 5,  # Middle row
 6, 7, 8]  # Bottom row
```

Values: `None` (empty), `"X"`, or `"O"`

### Win Conditions

8 winning combinations are checked:
- 3 rows (horizontal)
- 3 columns (vertical)
- 2 diagonals

### Game States

- `in_progress`: Game is active
- `x_wins`: Player X has won
- `o_wins`: Player O has won
- `draw`: Board is full with no winner

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Created by Nestor Wheelock

Built with:
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [pytest](https://pytest.org/)

## Support

- GitHub Issues: https://github.com/nestorwheelock/django-tictactoe/issues
- Documentation: This README
- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/

## Example Usage

### Python Requests

```python
import requests

BASE_URL = 'http://localhost:8000/tictactoe/api'

# Create a new game
response = requests.post(f'{BASE_URL}/games/')
game = response.json()
game_id = game['id']
print(f"Created game {game_id}")

# Make moves (X wins top row)
moves = [0, 3, 1, 4, 2]
for i, position in enumerate(moves):
    response = requests.post(
        f'{BASE_URL}/games/{game_id}/move/',
        json={'position': position}
    )
    game = response.json()
    print(f"Move {i+1}: {game['current_player']} at position {position}")
    print(f"Status: {game['status']}")

# Game result
final_game = requests.get(f'{BASE_URL}/games/{game_id}/').json()
print(f"\nFinal status: {final_game['status']}")
print(final_game['board_display'])
```

### Django Shell

```python
from tictactoe.models import Game

# Create game
game = Game.objects.create()

# Make moves
game.make_move(0)  # X at position 0
game.make_move(3)  # O at position 3
game.make_move(1)  # X at position 1
game.make_move(4)  # O at position 4
game.make_move(2)  # X at position 2 (wins!)

# Check result
print(game.status)  # 'x_wins'
print(game.get_board_display())
```
