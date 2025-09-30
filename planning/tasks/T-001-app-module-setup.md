# T-001: Django App Module Setup

**Related Story**: S-001 (Portable Django App Module)
**Estimate**: 2 hours
**Priority**: High
**Status**: 📋 PENDING

---

## AI Coding Brief

**Role**: Django Package Developer
**Objective**: Create the foundational structure for a reusable Django app package named django-tictactoe
**User Request**: "Create a standalone Django project to be a plugin module"

---

## Constraints

**Allowed File Paths**:
- `/home/nwheelo/projects/django-tictactoe/`
- All files within this directory

**Forbidden Paths**:
- System directories
- Other projects

**Technical Constraints**:
- Must follow Django app conventions
- Must be pip-installable
- Must work with Django 4.x and 5.x
- Python 3.8+ compatibility

---

## Deliverables

### 1. Project Structure

Create the following directory structure:
```
django-tictactoe/
├── tictactoe/                  # Main Django app
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── admin.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── templates/
│   │   └── tictactoe/
│   │       └── .gitkeep
│   ├── static/
│   │   └── tictactoe/
│   │       └── .gitkeep
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py
│       ├── test_api.py
│       └── test_views.py
├── planning/                   # Already exists
│   ├── stories/
│   └── tasks/
├── setup.py
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── LICENSE
├── MANIFEST.in
├── .gitignore
├── pytest.ini
└── .github/
    └── workflows/
        └── tests.yml
```

### 2. Package Configuration Files

**setup.py**:
- Package name: django-tictactoe
- Version: 1.0.0
- Author information
- License: MIT
- Dependencies: Django>=4.0, djangorestframework>=3.14
- Python requires: >=3.8
- Include package data (templates, static)

**requirements.txt**:
```
Django>=4.0,<6.0
djangorestframework>=3.14,<4.0
```

**requirements-dev.txt**:
```
pytest>=7.0
pytest-django>=4.5
pytest-cov>=4.0
black>=23.0
flake8>=6.0
```

**MANIFEST.in**:
```
include LICENSE
include README.md
include requirements.txt
recursive-include tictactoe/templates *
recursive-include tictactoe/static *
recursive-include tictactoe/migrations *.py
```

**pytest.ini**:
```
[pytest]
DJANGO_SETTINGS_MODULE = tests.settings
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --cov=tictactoe --cov-report=html --cov-report=term-missing
```

**.gitignore**:
- Python cache files
- Virtual environment
- Database files
- Coverage reports
- IDE files

### 3. Django App Configuration

**tictactoe/__init__.py**:
```python
__version__ = '1.0.0'
default_app_config = 'tictactoe.apps.TictactoeConfig'
```

**tictactoe/apps.py**:
```python
from django.apps import AppConfig

class TictactoeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tictactoe'
    verbose_name = 'Tic-Tac-Toe Game'
```

### 4. Initial Placeholder Files

**tictactoe/models.py**:
```python
from django.db import models

# Game model will be implemented in T-002
```

**tictactoe/admin.py**:
```python
from django.contrib import admin

# Admin configuration will be implemented in T-002
```

**tictactoe/views.py**:
```python
from rest_framework import viewsets

# ViewSets will be implemented in T-003
```

**tictactoe/serializers.py**:
```python
from rest_framework import serializers

# Serializers will be implemented in T-003
```

**tictactoe/urls.py**:
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'tictactoe'

router = DefaultRouter()
# ViewSets will be registered in T-003

urlpatterns = [
    path('api/', include(router.urls)),
]
```

### 5. README.md (Initial)

- Project description
- Features overview
- Installation instructions
- Quick start guide
- API endpoint listing (to be detailed in T-003)
- Contributing guidelines
- License information

### 6. LICENSE

MIT License file

### 7. Test Configuration

Create `tests/` directory at project root with:
- `tests/settings.py` - Minimal Django settings for testing
- `tests/__init__.py`

---

## Definition of Done

- [ ] All directories and files created as specified
- [ ] setup.py includes all necessary configuration
- [ ] requirements.txt lists all dependencies
- [ ] Django app structure follows conventions
- [ ] Package can be installed with `pip install -e .`
- [ ] README contains installation instructions
- [ ] .gitignore covers common Python/Django artifacts
- [ ] pytest.ini configured for Django testing
- [ ] LICENSE file present (MIT)
- [ ] MANIFEST.in includes templates and static files
- [ ] All placeholder files have correct imports
- [ ] App can be added to INSTALLED_APPS without errors

---

## Validation Steps

1. Install in development mode: `pip install -e .`
2. Verify package installed: `pip list | grep django-tictactoe`
3. Create test Django project
4. Add 'tictactoe' to INSTALLED_APPS
5. Run `python manage.py check` - should pass
6. Run `python manage.py migrate` - should work (no migrations yet)
7. Import tictactoe package: `python -c "import tictactoe; print(tictactoe.__version__)"`

---

## Test Cases

### Test: Package Installation
```python
def test_package_installation():
    """Test that package can be imported."""
    import tictactoe
    assert tictactoe.__version__ == '1.0.0'
```

### Test: App Configuration
```python
def test_app_config():
    """Test that app config is correct."""
    from tictactoe.apps import TictactoeConfig
    assert TictactoeConfig.name == 'tictactoe'
    assert TictactoeConfig.verbose_name == 'Tic-Tac-Toe Game'
```

### Test: URL Configuration
```python
def test_url_configuration():
    """Test that URL configuration loads without errors."""
    from tictactoe.urls import urlpatterns
    assert urlpatterns is not None
```

---

## Dependencies

**Blocking**: None (first task)
**Blocked By**: None

---

## Notes

- Keep this task focused on structure only
- No game logic implementation yet
- Ensure all files are properly namespaced
- Follow PEP 8 style guidelines
- Use type hints where applicable
- Keep README concise but informative
