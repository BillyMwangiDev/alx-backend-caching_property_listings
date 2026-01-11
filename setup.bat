@echo off
REM Setup script for ALX Backend Caching Property Listings (Windows)

echo Setting up ALX Backend Caching Property Listings...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo Please edit .env file with your configuration
)

REM Start Docker services
echo Starting Docker services (PostgreSQL and Redis)...
docker-compose up -d

REM Wait for services to be ready
echo Waiting for services to be ready...
timeout /t 5 /nobreak >nul

REM Run migrations
echo Running database migrations...
python manage.py migrate

echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Create a superuser: python manage.py createsuperuser
echo 3. Run the server: python manage.py runserver
echo 4. Access the API at: http://localhost:8000/properties/

pause
