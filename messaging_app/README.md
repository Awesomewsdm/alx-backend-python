# Messaging App - Docker Compose Setup

This Django messaging application is configured to run with Docker Compose using MySQL as the database.

## Project Structure

```
messaging_app/
├── docker-compose.yml      # Multi-container setup with Django + MySQL
├── Dockerfile             # Django app container configuration
├── .env                   # Environment variables (DO NOT commit to git)
├── .env.example          # Template for environment variables
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
├── messaging_app/       # Django project settings
│   ├── settings.py     # Updated to use environment variables
│   └── ...
└── messaging/          # Django app with models, views, etc.
    └── ...
```

## Services

### `web` - Django Application
- Builds from the Dockerfile in the current directory
- Runs on port 8000
- Connects to MySQL database
- Uses environment variables from .env file

### `db` - MySQL Database
- Uses MySQL 8.0 image
- Configured with environment variables:
  - `MYSQL_DATABASE`: Database name
  - `MYSQL_USER`: Application database user
  - `MYSQL_PASSWORD`: Application user password
  - `MYSQL_ROOT_PASSWORD`: Root user password
- Data persisted in `mysql_data` volume
- Exposed on port 3306 (for development access)

## Setup Instructions

### 1. Environment Configuration

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

Edit `.env` and set secure passwords:

```bash
# MySQL Database Configuration
MYSQL_DB=messaging_app
MYSQL_USER=messaging_user
MYSQL_PASSWORD=your_secure_password_here
MYSQL_ROOT_PASSWORD=your_secure_root_password_here

# Database connection for Django
DB_ENGINE=django.db.backends.mysql
DB_NAME=messaging_app
DB_USER=messaging_user
DB_PASSWORD=your_secure_password_here
DB_HOST=db
DB_PORT=3306
```

**Important**: Never commit the `.env` file to version control. It's already in `.gitignore`.

### 2. Build and Start Services

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 3. Run Database Migrations

After the services are up, run Django migrations:

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create a superuser (optional)
docker-compose exec web python manage.py createsuperuser
```

### 4. Access the Application

- **Django Application**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **MySQL Database**: localhost:3306 (if you need direct access)

## Available Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes (WARNING: This deletes data)
docker-compose down -v

# View logs
docker-compose logs web
docker-compose logs db

# Execute commands in containers
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py test
docker-compose exec db mysql -u root -p

# Rebuild containers
docker-compose build --no-cache
docker-compose up --build
```

## Database Connection

The Django application connects to MySQL using these settings from environment variables:

- **Host**: `db` (Docker Compose service name)
- **Port**: `3306`
- **Database**: `messaging_app`
- **User**: `messaging_user`
- **Password**: Set in `.env` file

## Verification Steps

To verify that the setup is working correctly:

1. **Check service health**:
   ```bash
   docker-compose ps
   ```
   All services should show "healthy" status.

2. **Test database connection**:
   ```bash
   docker-compose exec web python manage.py dbshell
   ```

3. **Run Django checks**:
   ```bash
   docker-compose exec web python manage.py check
   ```

4. **Test the messaging app**:
   ```bash
   docker-compose exec web python manage.py test messaging
   ```

## Troubleshooting

### Database Connection Issues

If you get database connection errors:

1. Ensure MySQL service is healthy:
   ```bash
   docker-compose logs db
   ```

2. Check if the database is ready:
   ```bash
   docker-compose exec db mysql -u root -p -e "SHOW DATABASES;"
   ```

3. Verify environment variables:
   ```bash
   docker-compose exec web env | grep DB_
   ```

### Permission Issues

If you encounter permission issues:

```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

### Clean Start

To completely reset the environment:

```bash
# Stop and remove everything
docker-compose down -v --remove-orphans

# Remove images (optional)
docker-compose down --rmi all

# Start fresh
docker-compose up --build
```

## Security Notes

- The `.env` file contains sensitive information and is excluded from Git
- In production, use strong passwords and consider using Docker secrets
- The MySQL root password should be different from the application user password
- Consider using a reverse proxy (nginx) in production

## Development Workflow

1. Make code changes in your local directory
2. Changes are automatically reflected due to volume mounting
3. For requirements changes, rebuild:
   ```bash
   docker-compose build web
   docker-compose up
   ```
4. For database schema changes:
   ```bash
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```