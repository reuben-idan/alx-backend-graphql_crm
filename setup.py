#!/usr/bin/env python
"""
Setup script for the GraphQL CRM project.
This script helps users set up the project environment and database.
"""

import os
import sys
import subprocess
import django
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_django():
    """Setup Django environment."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
    django.setup()

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install project dependencies."""
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    return True

def run_migrations():
    """Run Django migrations."""
    setup_django()
    if not run_command("python manage.py migrate", "Running database migrations"):
        return False
    return True

def create_superuser():
    """Create a superuser account."""
    print("👤 Creating superuser account...")
    print("Please enter the following information:")
    
    username = input("Username (default: admin): ").strip() or "admin"
    email = input("Email (default: admin@example.com): ").strip() or "admin@example.com"
    password = input("Password (default: admin123): ").strip() or "admin123"
    
    setup_django()
    from django.contrib.auth.models import User
    
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        print(f"✅ Superuser '{username}' created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create superuser: {e}")
        return False

def seed_database():
    """Seed the database with sample data."""
    if not run_command("python seed_db.py", "Seeding database with sample data"):
        return False
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up GraphQL CRM Project")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("❌ Setup failed at database migration")
        sys.exit(1)
    
    # Create superuser
    create_superuser_choice = input("\nCreate superuser account? (y/n, default: y): ").strip().lower()
    if create_superuser_choice != 'n':
        if not create_superuser():
            print("❌ Setup failed at superuser creation")
            sys.exit(1)
    
    # Seed database
    seed_choice = input("\nSeed database with sample data? (y/n, default: y): ").strip().lower()
    if seed_choice != 'n':
        if not seed_database():
            print("❌ Setup failed at database seeding")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n🚀 Next steps:")
    print("   1. Start the development server:")
    print("      python manage.py runserver")
    print("\n   2. Access the application:")
    print("      GraphQL Playground: http://127.0.0.1:8000/graphql")
    print("      Django Admin: http://127.0.0.1:8000/admin")
    print("\n   3. Try sample GraphQL queries from the README")
    print("\n📚 For more information, see the README.md file")

if __name__ == "__main__":
    main() 