# SendCloud RSS Tool

## Tech stack
- Django 2.1
- Python 3.6
- Celery
-     Redis
- Tests (pytest)
- Docker + Docker Compose

## Deploy
 - settings for test, dev and production:
      - `ENVIRONMENT` var needs to be `PRODUCTION` for production settings
      - if `ENVIRONMENT` var needs set to `TEST` then your database will be sqllite3
 - use `docker-compose` commands to deploy local server
   - look at make file commands
   
OR
   
 - use make file commands to deploy and run local server
   - `make init` to deploy and run for the first time
   - `make start` to run the project
 
## How it works



