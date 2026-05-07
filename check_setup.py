#!/usr/bin/env python
"""
BBSUL Student Portal - Setup Verification
Run this to check if your environment is ready.
"""
import sys
import os

def check_module(module_name, display_name=None):
    """Check if a Python module is installed."""
    import_name = module_name  # Always use module_name for import
    try:
        __import__(import_name)
        print(f"  [OK] {display_name or module_name}")
        return True
    except ImportError:
        print(f"  [MISSING] {display_name or module_name}")
        return False

def main():
    print("=" * 60)
    print("BBSUL Student Portal - Environment Check")
    print("=" * 60)
    print()

    # Check Python version
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("  [WARNING] Python 3.9+ recommended")
    else:
        print("  [OK] Python version compatible")
    print()

    # Check required modules
    print("Checking Python dependencies:")
    modules = [
        ('flask', 'Flask'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('flask_login', 'Flask-Login'),
        ('openpyxl', 'openpyxl'),
        ('werkzeug', 'Werkzeug'),
    ]

    all_ok = True
    for module, name in modules:
        if not check_module(module, name):
            all_ok = False

    print()

    # Check optional production modules
    print("Optional production dependencies:")
    optional = [
        ('gunicorn', 'Gunicorn (production server)'),
        ('psycopg2', 'PostgreSQL driver'),
    ]

    for module, name in optional:
        check_module(module, name)

    print()

    # Check file structure
    print("Checking project structure:")
    required_files = [
        'app.py',
        'config.py',
        'run.py',
        'requirements.txt',
        'templates',
        'data',
        'data/Template Current Students (1).xlsx',
    ]

    for file in required_files:
        if os.path.exists(file):
            print(f"  [OK] {file}")
        else:
            print(f"  [MISSING] {file}")
            if file == 'data/Template Current Students (1).xlsx':
                print("         Place your Excel template in the data/ folder")
            all_ok = False

    print()

    # Check write permissions
    print("Checking directory permissions:")
    dirs_to_check = ['data', '.']
    for directory in dirs_to_check:
        if os.access(directory, os.W_OK):
            print(f"  [OK] {directory}/ is writable")
        else:
            print(f"  [WARNING] {directory}/ is not writable")
            all_ok = False

    print()
    print("=" * 60)

    if all_ok:
        print("[SUCCESS] Everything looks good! You can run: python run.py")
        print()
        print("Admin login: rishabh@bbsul.edu.pk / abc1234")
        return 0
    else:
        print("[ERROR] Some issues found. Please fix them before running.")
        print()
        print("To install missing packages:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == '__main__':
    sys.exit(main())
