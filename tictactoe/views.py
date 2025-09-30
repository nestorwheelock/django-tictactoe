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
