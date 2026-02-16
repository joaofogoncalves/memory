#!/usr/bin/env python3
"""Verify LinkedIn Post Archiver setup and dependencies."""

import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.9+."""
    if sys.version_info < (3, 9):
        print("✗ Python 3.9+ required")
        print(f"  Current version: {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'requests',
        'yaml',
        'dotenv',
        'PIL',
        'slugify',
        'dateutil',
        'tqdm',
        'coloredlogs'
    ]

    all_installed = True
    for package in required_packages:
        try:
            if package == 'PIL':
                __import__('PIL')
            elif package == 'yaml':
                __import__('yaml')
            elif package == 'dotenv':
                __import__('dotenv')
            elif package == 'dateutil':
                __import__('dateutil')
            else:
                __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} not installed")
            all_installed = False

    return all_installed


def check_directory_structure():
    """Check if all required directories exist."""
    required_dirs = [
        'scraper',
        'config',
        'posts',
        'cache',
        'logs'
    ]

    all_exist = True
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✓ {dir_name}/")
        else:
            print(f"✗ {dir_name}/ missing")
            all_exist = False

    return all_exist


def check_config_files():
    """Check if configuration files exist."""
    required_files = [
        'requirements.txt',
        'config/config.yaml',
        '.env.example',
        '.gitignore'
    ]

    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False

    return all_exist


def check_env_file():
    """Check if .env file is configured."""
    env_path = Path('.env')

    if not env_path.exists():
        print("⚠ .env file not found")
        print("  Create .env from .env.example and add your credentials")
        return False

    # Check if it has the required keys
    with open(env_path) as f:
        content = f.read()

    required_keys = ['LINKEDIN_CLIENT_ID', 'LINKEDIN_CLIENT_SECRET', 'LINKEDIN_REDIRECT_URI']
    has_all_keys = all(key in content for key in required_keys)

    if not has_all_keys:
        print("⚠ .env file missing required keys")
        return False

    # Check if values are filled in
    if 'your_client_id' in content or 'your_secret' in content:
        print("⚠ .env file has placeholder values")
        print("  Update .env with your actual LinkedIn app credentials")
        return False

    print("✓ .env file configured")
    return True


def main():
    """Run all setup verification checks."""
    print("=" * 60)
    print("LinkedIn Post Archiver - Setup Verification")
    print("=" * 60)

    checks = [
        ("Python Version", check_python_version),
        ("\nDependencies", check_dependencies),
        ("\nDirectory Structure", check_directory_structure),
        ("\nConfiguration Files", check_config_files),
        ("\nEnvironment Variables", check_env_file),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 40)
        result = check_func()
        results.append(result)

    print("\n" + "=" * 60)

    if all(results):
        print("✓ Setup verification complete! Ready to use.")
        print("\nNext steps:")
        print("  1. Run: python scraper/main.py --auth")
        print("  2. Then: python scraper/main.py --fetch")
    else:
        print("✗ Setup incomplete. Please fix the issues above.")
        print("\nTo install dependencies:")
        print("  pip install -r requirements.txt")
        print("\nTo configure credentials:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your LinkedIn app credentials")

    print("=" * 60)


if __name__ == '__main__':
    main()
