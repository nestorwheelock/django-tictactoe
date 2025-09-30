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
