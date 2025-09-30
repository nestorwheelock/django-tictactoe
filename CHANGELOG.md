# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-09-30

### Added

**Core Game Logic:**
- Game model with JSONField board storage (9 positions)
- Automatic win detection for all 8 winning combinations (3 rows, 3 columns, 2 diagonals)
- Draw detection when board is full with no winner
- Move validation (position bounds checking, occupation detection, game-over prevention)
- Player switching after valid moves
- Game status tracking (in_progress, x_wins, o_wins, draw)
- Visual board display method for debugging and admin

**REST API:**
- Complete CRUD operations using Django REST Framework
- POST /tictactoe/api/games/ - Create new game
- GET /tictactoe/api/games/ - List all games
- GET /tictactoe/api/games/{id}/ - Retrieve game with detailed board display
- POST /tictactoe/api/games/{id}/move/ - Make a move with position validation
- DELETE /tictactoe/api/games/{id}/ - Delete game
- Proper HTTP status codes (201, 200, 400, 404, 204)
- Comprehensive error messages for all validation failures
- GameSerializer with read-only field protection
- MoveSerializer with position validation (0-8 range)
- GameDetailSerializer with board visualization

**Frontend Interface:**
- Responsive web templates with vanilla JavaScript and CSS
- Game list view showing all games with status badges
- Interactive game board with click-to-move functionality
- Real-time status updates and win/draw notifications
- Create new game button on both list and detail views
- Refresh button to reload current game state
- Success/error message system with auto-dismiss
- Color-coded player marks (X = purple, O = violet)
- Status badges with color coding for game states
- Mobile-responsive design (320px+)
- Gradient background with card-based layout
- Hover effects and animations

**Django Admin Integration:**
- Admin interface for Game model
- List display showing ID, status, current player, timestamps
- Filtering by status, current player, and creation date
- Readonly board visualization in collapsed fieldset
- Proper field organization in fieldsets

**Testing:**
- Comprehensive test suite with 63 tests
- 98% overall test coverage
- Unit tests for all model methods (25 tests)
- Integration tests for all API endpoints (20 tests)
- Template view tests (7 tests)
- Package setup tests (11 tests)
- pytest-django configuration
- Coverage reporting with HTML output

**Documentation:**
- Complete README with installation instructions
- API endpoint documentation with request/response examples
- Quick start guide with code examples
- Customization guide (templates, CSS, views)
- Development setup instructions
- Contributing guidelines (CONTRIBUTING.md)
- Changelog following Keep a Changelog format
- Example usage with Python requests and Django shell
- MIT License

**Package Configuration:**
- Pip-installable package structure
- setup.py with proper metadata and classifiers
- Support for Python 3.8-3.12
- Support for Django 4.0-5.x
- Django REST Framework 3.14+ integration
- Package includes static files and templates
- MANIFEST.in for proper file inclusion

### Features

- **Reusable Django App**: Self-contained module installable in any Django project
- **RESTful API**: Full game management through well-documented API endpoints
- **Web Interface**: Optional pre-built playable interface
- **Type Hints**: Full type annotation throughout codebase
- **Customizable**: Override templates, CSS, and views in host project
- **Admin Ready**: Manage games through Django admin interface
- **Well-Tested**: >95% test coverage with comprehensive test suite
- **Production Ready**: Follows Django and DRF best practices

### Technical Details

**Dependencies:**
- Python ≥3.8
- Django ≥4.0, <6.0
- Django REST Framework ≥3.14, <4.0

**Development Dependencies:**
- pytest ≥7.0
- pytest-django ≥4.5
- pytest-cov ≥4.0
- black ≥23.0
- flake8 ≥6.0

**Architecture:**
- Models: Game model with business logic methods
- Serializers: GameSerializer, MoveSerializer, GameDetailSerializer
- Views: GameViewSet (API) + template views (game_list, game_detail)
- URLs: Router-based API + template view routing
- Templates: base.html, game_list.html, game_detail.html
- Static: game.css (254 lines), game.js (169 lines)
- Tests: test_models.py, test_api.py, test_views.py, test_setup.py

**Code Quality:**
- PEP 8 compliant
- Type hints on all functions
- Comprehensive docstrings
- Black formatted
- Flake8 validated

[Unreleased]: https://github.com/nestorwheelock/django-tictactoe/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/nestorwheelock/django-tictactoe/releases/tag/v1.0.0
