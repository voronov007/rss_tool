# SendCloud RSS Tool

## Tech stack
- Django 2.1
- Python 3.6
- Celery
    - Redis as queue engine
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
### Permissions check
User make request to the website, but redirects to login/register page if user is not logged in.
Auth check was done in custom middleware (`AuthMiddleware`). Only login/register pages allowed to be 
viewed by not login users. 

### Login/Register
`User` model was modified to accept `email` and `password` as inputs. Django forms used for login/logout.

### Index page
Index page is user RSS feeds. User may comment them

### RSS parser
There is a menu link which brings you to the form with RSS url input field.
When `save` button is pressed parsing start in async mode. For this purpose `celery` is used
with `redis` queue engine. User get notification that parser was start.

### Explore
Use `explore` link to explore other users feeds. 
On the listed page you may see users that have feeds and a number of feeds that he has.
User can add feed to favorites or comment feeds.

### Favorites
Use `favorites` link to view your favorite feeds. Here you may remove feed from favorites or comment feeds.

### Overall
- All db queries are optimized. There are no more than 4 db requests even for complex db queries
- Project stored in Docker and it is very easy to deploy it on local machine
- Main features covered with tests


