import importlib
import sys
from pathlib import Path


def test_package_imports():
    """Test that tictactoe package can be imported."""
    import tictactoe
    assert tictactoe is not None


def test_package_version():
    """Test that package has version defined."""
    import tictactoe
    assert hasattr(tictactoe, '__version__')
    assert tictactoe.__version__ == '1.0.0'


def test_app_config_exists():
    """Test that TictactoeConfig exists and is properly configured."""
    from tictactoe.apps import TictactoeConfig
    assert TictactoeConfig.name == 'tictactoe'
    assert TictactoeConfig.verbose_name == 'Tic-Tac-Toe Game'


def test_url_configuration_loads():
    """Test that URL configuration loads without errors."""
    from tictactoe.urls import urlpatterns, app_name
    assert urlpatterns is not None
    assert app_name == 'tictactoe'


def test_models_module_exists():
    """Test that models module can be imported."""
    from tictactoe import models
    assert models is not None


def test_views_module_exists():
    """Test that views module can be imported."""
    from tictactoe import views
    assert views is not None


def test_serializers_module_exists():
    """Test that serializers module can be imported."""
    from tictactoe import serializers
    assert serializers is not None


def test_admin_module_exists():
    """Test that admin module can be imported."""
    from tictactoe import admin
    assert admin is not None


def test_migrations_directory_exists():
    """Test that migrations directory exists."""
    migrations_path = Path(__file__).parent.parent / 'migrations'
    assert migrations_path.exists()
    assert migrations_path.is_dir()
    assert (migrations_path / '__init__.py').exists()


def test_templates_directory_exists():
    """Test that templates directory exists."""
    templates_path = Path(__file__).parent.parent / 'templates' / 'tictactoe'
    assert templates_path.exists()
    assert templates_path.is_dir()


def test_static_directory_exists():
    """Test that static directory exists."""
    static_path = Path(__file__).parent.parent / 'static' / 'tictactoe'
    assert static_path.exists()
    assert static_path.is_dir()
