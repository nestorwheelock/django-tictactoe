# T-003: REST API Implementation

**Related Story**: S-002 (Game Board Management API)
**Estimate**: 3 hours
**Priority**: High
**Status**: 📋 PENDING
**Depends On**: T-002

---

## AI Coding Brief

**Role**: Django REST Framework Developer
**Objective**: Implement REST API endpoints for game management using Django REST Framework with comprehensive validation and error handling
**User Request**: "Create REST API for tic-tac-toe game operations"

---

## Constraints

**Allowed File Paths**:
- `tictactoe/serializers.py`
- `tictactoe/views.py`
- `tictactoe/urls.py`
- `tictactoe/tests/test_api.py`

**Forbidden Paths**:
- Model files (already done in T-002)
- Template files (come in T-004)

**Technical Constraints**:
- Use Django REST Framework ViewSets
- Follow REST conventions (proper HTTP methods and status codes)
- Comprehensive input validation
- >95% test coverage
- API versioning via URL namespace

---

## Deliverables

### 1. Serializers (tictactoe/serializers.py)

```python
from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    """Serializer for Game model."""

    class Meta:
        model = Game
        fields = ['id', 'board', 'current_player', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'current_player', 'status', 'created_at', 'updated_at']

    def validate_board(self, value):
        """Validate board structure."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Board must be a list")

        if len(value) != 9:
            raise serializers.ValidationError("Board must have exactly 9 elements")

        for cell in value:
            if cell not in [None, 'X', 'O']:
                raise serializers.ValidationError("Board cells must be null, 'X', or 'O'")

        return value


class MoveSerializer(serializers.Serializer):
    """Serializer for making a move."""

    position = serializers.IntegerField(min_value=0, max_value=8)

    def validate_position(self, value):
        """Validate position is within bounds."""
        if value < 0 or value > 8:
            raise serializers.ValidationError("Position must be between 0 and 8")
        return value


class GameDetailSerializer(GameSerializer):
    """Extended serializer with board display."""

    board_display = serializers.SerializerMethodField()

    class Meta(GameSerializer.Meta):
        fields = GameSerializer.Meta.fields + ['board_display']

    def get_board_display(self, obj):
        """Get formatted board display."""
        return obj.get_board_display()
```

### 2. ViewSets (tictactoe/views.py)

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Game
from .serializers import GameSerializer, MoveSerializer, GameDetailSerializer

class GameViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Game model.

    Provides CRUD operations plus custom 'move' action.
    """

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action."""
        if self.action == 'retrieve':
            return GameDetailSerializer
        return GameSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new game.

        POST /api/games/
        """
        game = Game.objects.create()
        serializer = self.get_serializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        """
        Make a move in the game.

        POST /api/games/{id}/move/
        Body: {"position": 0-8}

        Returns:
            200: Move successful, returns updated game state
            400: Invalid move (occupied, out of turn, game over)
            404: Game not found
        """
        game = self.get_object()
        serializer = MoveSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        position = serializer.validated_data['position']

        try:
            result = game.make_move(position)
            game_serializer = self.get_serializer(game)
            return Response({
                **game_serializer.data,
                'message': result['message']
            }, status=status.HTTP_200_OK)

        except DjangoValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
```

### 3. Template Views (for frontend - basic)

```python
from django.shortcuts import render, get_object_or_404

def game_list(request):
    """Display list of all games."""
    games = Game.objects.all()
    return render(request, 'tictactoe/game_list.html', {'games': games})

def game_detail(request, pk):
    """Display single game for playing."""
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'tictactoe/game_detail.html', {'game': game})
```

### 4. URL Configuration (tictactoe/urls.py)

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'tictactoe'

router = DefaultRouter()
router.register(r'games', views.GameViewSet, basename='game')

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),

    # Frontend URLs (implemented in T-004)
    path('', views.game_list, name='game-list'),
    path('game/<int:pk>/', views.game_detail, name='game-detail'),
]
```

### 5. Comprehensive API Tests (tictactoe/tests/test_api.py)

**Test Coverage Required**:
- Create game endpoint
- List games endpoint
- Retrieve game endpoint
- Delete game endpoint
- Make valid move
- Make invalid moves (all error cases)
- API response formats
- HTTP status codes
- Error message clarity

**Minimum 15 test cases**

Example test structure:
```python
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from tictactoe.models import Game

@pytest.mark.django_db
class TestGameAPI:
    def setup_method(self):
        """Setup test client."""
        self.client = APIClient()

    def test_create_game(self):
        """Test creating a new game."""
        response = self.client.post('/tictactoe/api/games/')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert response.data['board'] == [None] * 9
        assert response.data['current_player'] == 'X'
        assert response.data['status'] == 'in_progress'

    def test_list_games(self):
        """Test listing all games."""
        Game.objects.create()
        Game.objects.create()
        response = self.client.get('/tictactoe/api/games/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_retrieve_game(self):
        """Test retrieving a single game."""
        game = Game.objects.create()
        response = self.client.get(f'/tictactoe/api/games/{game.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == game.id

    def test_make_valid_move(self):
        """Test making a valid move."""
        game = Game.objects.create()
        response = self.client.post(
            f'/tictactoe/api/games/{game.id}/move/',
            {'position': 0}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['board'][0] == 'X'
        assert response.data['current_player'] == 'O'

    def test_make_move_occupied_position(self):
        """Test moving to occupied position returns error."""
        game = Game.objects.create()
        game.make_move(0)
        response = self.client.post(
            f'/tictactoe/api/games/{game.id}/move/',
            {'position': 0}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_make_move_invalid_position(self):
        """Test invalid position returns error."""
        game = Game.objects.create()
        response = self.client.post(
            f'/tictactoe/api/games/{game.id}/move/',
            {'position': 10}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_make_move_game_over(self):
        """Test move after game over returns error."""
        game = Game.objects.create()
        # Set up winning position for X
        game.board = ['X', 'X', 'X', 'O', 'O', None, None, None, None]
        game.status = Game.STATUS_X_WINS
        game.save()

        response = self.client.post(
            f'/tictactoe/api/games/{game.id}/move/',
            {'position': 5}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'finished' in str(response.data['error']).lower()

    def test_delete_game(self):
        """Test deleting a game."""
        game = Game.objects.create()
        response = self.client.delete(f'/tictactoe/api/games/{game.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Game.objects.filter(id=game.id).exists()

    def test_retrieve_nonexistent_game(self):
        """Test retrieving non-existent game returns 404."""
        response = self.client.get('/tictactoe/api/games/999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_complete_game_flow(self):
        """Test complete game from creation to win."""
        # Create game
        response = self.client.post('/tictactoe/api/games/')
        game_id = response.data['id']

        # X moves
        moves = [0, 3, 1, 4, 2]  # X wins top row
        o_moves = [3, 4]

        for i, pos in enumerate(moves[:3]):
            response = self.client.post(
                f'/tictactoe/api/games/{game_id}/move/',
                {'position': pos}
            )
            if i < 2:  # Not the winning move yet
                assert response.status_code == status.HTTP_200_OK
                # Make O's move
                if i < len(o_moves):
                    self.client.post(
                        f'/tictactoe/api/games/{game_id}/move/',
                        {'position': o_moves[i]}
                    )

        # Check final state
        response = self.client.get(f'/tictactoe/api/games/{game_id}/')
        assert response.data['status'] == 'x_wins'
```

---

## API Endpoint Specifications

### Create Game
```
POST /tictactoe/api/games/
Response 201: {
  "id": 1,
  "board": [null, null, null, null, null, null, null, null, null],
  "current_player": "X",
  "status": "in_progress",
  "created_at": "2025-09-30T12:00:00Z",
  "updated_at": "2025-09-30T12:00:00Z"
}
```

### List Games
```
GET /tictactoe/api/games/
Response 200: [
  {...game 1...},
  {...game 2...}
]
```

### Retrieve Game
```
GET /tictactoe/api/games/{id}/
Response 200: {...game data...}
Response 404: {"detail": "Not found."}
```

### Make Move
```
POST /tictactoe/api/games/{id}/move/
Body: {"position": 0}
Response 200: {...updated game...}
Response 400: {"error": "Position already occupied"}
```

### Delete Game
```
DELETE /tictactoe/api/games/{id}/
Response 204: No Content
```

---

## Definition of Done

- [ ] GameSerializer implemented with validation
- [ ] MoveSerializer implemented
- [ ] GameViewSet with all CRUD operations
- [ ] Custom move action implemented
- [ ] URL routing configured
- [ ] All API endpoints accessible
- [ ] Proper HTTP status codes used
- [ ] Error messages are clear and helpful
- [ ] API tests written (minimum 15 tests)
- [ ] Test coverage >95% for views.py and serializers.py
- [ ] Type hints used
- [ ] Docstrings for all classes and methods
- [ ] PEP 8 compliant

---

## Validation Steps

1. Run `pytest tictactoe/tests/test_api.py -v` - all tests pass
2. Run `pytest tictactoe/tests/test_api.py --cov=tictactoe` - >95% coverage
3. Manual API testing with curl or Postman:
   - Create game
   - Make moves
   - Test error cases
4. Check DRF browsable API in browser
5. Verify all endpoints return correct status codes

---

## Dependencies

**Blocking**: T-002 (Game Model & Migrations)
**Blocked By**: T-004 (Frontend Templates use this API)

---

## Notes

- Use DRF's built-in features (don't reinvent the wheel)
- Follow REST conventions strictly
- Error messages should guide the user to correct usage
- Keep views thin - logic belongs in models
- Test both success and failure cases thoroughly
