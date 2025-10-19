# Advance Containers — Flask + PostgreSQL

This project containerizes a simple Flask API and PostgreSQL database using Docker Compose.

## How to Run

1. **Clone or unzip the project**
   ```powershell

   cd advance-containers

2. **Create environment file**

Copy-Item .env.example .env
###edit .env and set your own POSTGRES_PASSWORD

3. **Build and start containers**
   
docker compose up -d --build

4. **Check services**

docker compose ps ### web should be Up (port 8000), db should be healthy

## Test API
Health:
Invoke-RestMethod -Uri http://localhost:8000/ -Method Get

## Create User
$body = @{ id = 1; first_name = "A"; last_name = "B" } | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/user -Method Post -ContentType 'application/json' -Body $body

## Get User
Invoke-RestMethod -Uri http://localhost:8000/user/1 -Method Get

Or run quick test:
.\scripts\test-api.ps1

## Components
+ Flask (Python) → exposes /user and /user/<id> endpoints.

+ PostgreSQL (Docker) → stores user data, initialized via db/init.sql.

+ Docker Compose → orchestrates both containers.

+ Volume → ensures DB persistence.

+ Logs → stored in app/logs/app.log.

## Security Highlights
+ Non-root user in web container.

+ Read-only filesystem & dropped privileges.

+ Secrets stored in .env (not in code).

## Stop / Clean Up
docker compose down -v
