from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Django admin configuration for Game model."""

    list_display = ('id', 'status', 'current_player', 'created_at', 'updated_at')
    list_filter = ('status', 'current_player', 'created_at')
    search_fields = ('id', 'status')
    readonly_fields = ('created_at', 'updated_at', 'board_display')

    fieldsets = (
        ('Game State', {
            'fields': ('status', 'current_player', 'board')
        }),
        ('Display', {
            'fields': ('board_display',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def board_display(self, obj):
        """Display formatted board in admin."""
        return obj.get_board_display()

    board_display.short_description = 'Board Visualization'
