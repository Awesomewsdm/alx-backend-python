# Messaging App - Docker Setup

This Django messaging application has been containerized using Docker for easy deployment and development.

## Project Structure

```
messaging_app/
├── messaging_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── messaging/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── chats/
│   ├── views.py
│   ├── urls.py
│   └── ...
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── .env.example
```

## Prerequisites

- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)

### Installing Docker on Linux

```bash
# Update the package index
sudo apt-get update

# Install packages to allow apt to use a repository over HTTPS
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verify installation
sudo docker run hello-world

# Add your user to the docker group (optional, to run docker without sudo)
sudo usermod -aG docker $USER
```

## Quick Start with Docker Compose

1. **Clone and navigate to the project directory:**
   ```bash
   cd messaging_app
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Build and run the application:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   - Web application: http://localhost:8000
   - Admin panel: http://localhost:8000/admin
   - API endpoints: http://localhost:8000/messaging/

5. **Run migrations (in a new terminal):**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

6. **Create a superuser (optional):**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Manual Docker Build and Run

### 1. Build the Docker Image

```bash
# Navigate to the directory containing the Dockerfile
cd messaging_app

# Build the Docker image
docker build -t messaging-app .

# Verify the image was created
docker images
```

### 2. Run the Container

```bash
# Run the container
docker run -d \
  --name messaging-app-container \
  -p 8000:8000 \
  messaging-app

# Check if the container is running
docker ps
```

### 3. Access the Application

Open your web browser and navigate to:
- http://localhost:8000 - Main application
- http://localhost:8000/admin - Django admin
- http://localhost:8000/messaging/ - Messaging API endpoints

### 4. View Logs

```bash
# View container logs
docker logs messaging-app-container

# Follow logs in real-time
docker logs -f messaging-app-container
```

### 5. Execute Commands in the Container

```bash
# Run Django migrations
docker exec messaging-app-container python manage.py migrate

# Create a superuser
docker exec -it messaging-app-container python manage.py createsuperuser

# Collect static files
docker exec messaging-app-container python manage.py collectstatic --noinput

# Access Django shell
docker exec -it messaging-app-container python manage.py shell
```

## Docker Image Details

### Base Image
- **python:3.10-slim** - Lightweight Python 3.10 image

### Installed Dependencies
- All packages from `requirements.txt`
- System packages: postgresql-client, gcc, python3-dev, musl-dev, libpq-dev

### Security Features
- Runs as non-root user (`appuser`)
- Environment variables for secure configuration
- Health checks enabled

### Exposed Ports
- **8000** - Django development server

## Environment Variables

The application supports the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable Django debug mode | `True` |
| `SECRET_KEY` | Django secret key | Required |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `*` |
| `DATABASE_URL` | Database connection URL | SQLite |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379/0` |

## Production Considerations

### 1. Environment Variables
```bash
# Create a production .env file
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@host:port/database
```

### 2. Use a Production WSGI Server
Replace the development server with Gunicorn:

```dockerfile
# Update the CMD in Dockerfile for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "messaging_app.wsgi:application"]
```

### 3. Serve Static Files
Use a web server like Nginx to serve static files in production.

### 4. Database
Use a production database like PostgreSQL instead of SQLite.

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Stop existing containers
   docker stop messaging-app-container
   # Or use a different port
   docker run -p 8001:8000 messaging-app
   ```

2. **Permission denied:**
   ```bash
   # Make sure Docker daemon is running
   sudo systemctl start docker
   # Add user to docker group
   sudo usermod -aG docker $USER
   ```

3. **Database connection issues:**
   ```bash
   # Check if database container is running
   docker-compose ps
   # View database logs
   docker-compose logs db
   ```

### Useful Commands

```bash
# Stop all services
docker-compose down

# Remove all containers and volumes
docker-compose down -v

# Rebuild without cache
docker-compose build --no-cache

# View service logs
docker-compose logs web
docker-compose logs db

# Access container shell
docker-compose exec web bash

# Run Django commands
docker-compose exec web python manage.py <command>
```

## API Endpoints

The application provides the following API endpoints:

- `GET /` - Home page
- `GET /admin/` - Django admin interface
- `GET /messaging/threads/` - List message threads
- `POST /messaging/send/` - Send a message
- `GET /messaging/inbox/` - User inbox
- `DELETE /messaging/delete-account/` - Delete user account

## Development

### Local Development with Docker

```bash
# Start services in development mode
docker-compose up

# Apply migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Install new dependencies
docker-compose exec web pip install package-name
docker-compose exec web pip freeze > requirements.txt

# Rebuild after adding dependencies
docker-compose build web
```

### Testing

```bash
# Run tests
docker-compose exec web python manage.py test

# Run specific tests
docker-compose exec web python manage.py test messaging.tests
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

## License

This project is licensed under the MIT License.