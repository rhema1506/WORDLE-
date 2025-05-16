Wordle Game - Backend (Django + PostgreSQL)
Description
Backend for the Wordle game, implemented on Django and PostgreSQL. Supports the game with English and Russian words of different lengths (4, 5, 6 letters). Includes REST API with Swagger documentation.

Technologies
Python 3.12

Django

Django REST Framework

PostgreSQL

Docker + Docker Compose

Swagger (drf_yasg)

Installing and running via Docker
1. Install Docker and Docker Compose
Installing Docker
Installing Docker Compose

2. Clone the repository
bash

Copy

Edit
git clone <your-repository-url>
cd wordle_backend
3. Launch containers
bash

Copy

Edit
docker-compose up --build
4. Perform the migration
bash

Copy

Edit
docker-compose exec backend python manage.py migrate
5. Create a superuser to access the admin panel
bash

Copy

Edit
docker-compose exec backend python manage.py createsuperuser
6. Open in browser
Admin: http://localhost:8000/admin/

Swagger UI: http://localhost:8000/swagger/

ReDoc UI: http://localhost:8000/redoc/

API
Main endpoints:
URL	Method	Description	Authentication
/api/game/start/	POST	Start a new game	Yes
/api/game/guess/{game_id}/	POST	Make a guess	Yes
/api/game/leaderboard/	GET	Get top 10 players	Yes
/api/game/stats/	GET	Get user statistics	Yes

Models
WordList - words (divided by length and language)

Game — the user's current game

Leaderboard — user statistics

Testing
Run the tests with:

bash

Copy

Edit
docker-compose exec backend python manage.py test
License
The project is licensed under MIT.

