# ples-be

Backend of the website of Reprezentační ples UTB, the ball of Tomas Bata University in Zlín run by Studentská unie UTB. It is a Django REST API with the same paths and JSON as the old Laravel `web-ples-be`, but with Bearer-token login instead of a cookie.

The public site reads the live seat map, the landing page content and the site settings, and visitors book hairdressers and make-up artists ("makers"). Staff log in to sell standing places and seats. In the Django admin, staff manage ball editions, seats, reservations, makers and the landing page content.

Used by the frontend project `ples-fe`.

## Stack

- Python 3.12, Django 5.1 and Django REST Framework
- Auth: DRF token auth, sent as `Authorization: Bearer <token>` (staff users only)
- `django-cors-headers` (all origins allowed on `/api/`), `dj-database-url`, `psycopg 3`
- PostgreSQL 16
- gunicorn (3 workers) with WhiteNoise serving the static files
- Docker Compose (services `db` and `web`)
- `uv` for dependencies (`pyproject.toml`, `uv.lock`), `ruff` and `mypy` for linting

## Project structure

```
ples-be/
├── docker-compose.yml     db (Postgres) + web (Django, gunicorn)
├── Makefile               shortcuts for docker compose
├── .env.example           all settings
└── api/
    ├── Dockerfile
    ├── pyproject.toml
    ├── manage.py
    ├── config/            settings, root urls, wsgi
    ├── common/            shared error classes and handler, serializer base, middleware, base repositories
    └── apps/
        ├── user/          staff accounts, login, logout, token auth
        ├── reservations/  events, seats, staff reservations, public seat map, seed_data command
        ├── salons/        makers, services, blocked times, bookings, confirmation e-mail
        ├── content/       landing page texts, contacts, ticket sales info
        └── site_config/   key-value settings of the site (for example TICKET_URL)
```

Inside an app the request goes controller (DRF `ViewSet`) → service (business rules) → repository (database queries) → model. DTOs (`dtos.py`) hold request and response serializers and small dataclasses. Services are plain classes created once in each app's `services/__init__.py`.

## Requirements

- Docker with Compose v2
- `make` (optional, on Windows use Git Bash)
- `uv` (only for `make lint`)

## Run locally

```bash
cp .env.example .env
```

Edit `.env` for local use:

```
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=*
DJANGO_USE_HTTPS=false
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

`DJANGO_USE_HTTPS=false` is needed because otherwise the admin cookies are marked secure and do not work over plain HTTP. The console e-mail backend prints e-mails to the web log instead of sending them.  The `POSTGRES_*` and `WEB_PORT` values from the example work as they are.

Start it and create an admin user:

```bash
make up                  # docker compose up -d --build
make superuser           # docker compose exec web python manage.py createsuperuser
```

The API login accepts only active users with `is_staff`. The superuser is staff, so it works for both the admin and the API.

- API: http://localhost:8005/api/... (the port is `WEB_PORT`)
- Admin: http://localhost:8005/admin/

On every start the `web` container runs, in this order:

1. `collectstatic --noinput`
2. `migrate`
3. `seed_data`
4. `gunicorn config.wsgi` on port 8000 inside the container

`seed_data` fills reference data, and only into tables that are empty, so it is safe to run again. It creates: the active event "Reprezentační ples UTB 2026" (date 2026-02-20, 434 standing places, prices 400 / 650 / 990 Kč for standing, seat without dinner, seat with dinner) with 132 tables of seats (tables 1-110 with dinner, tables 116-127 have 2 seats, the others 4); 5 makers with their services; 6 landing page contacts (the presale contact and 5 team contacts) with the ticket sales start date; and the setting `TICKET_URL`. It creates no users, no reservations and no landing page texts (add those in the admin).

## Make commands

| Command | What it does |
| --- | --- |
| `make up` | `docker compose up -d --build`, build and start in the background |
| `make down` | stop and remove the containers (the database volume stays) |
| `make ps` | list the containers |
| `make logs` | follow the `web` logs |
| `make psql` | open `psql` in the `db` container |
| `make shell` | open the Django shell in the `web` container |
| `make migrate` | run `migrate` |
| `make seed` | run `seed_data` |
| `make superuser` | run `createsuperuser` |
| `make lint` | `ruff check` and `mypy` in `api/` (needs `uv`) |

## Configuration

All variables are in `.env`. Compose passes the whole file to the `web` container and builds `DATABASE_URL` from the `POSTGRES_*` values.

| Variable | Example | What it does |
| --- | --- | --- |
| `DJANGO_DEBUG` | `false` | `true` turns on debug mode. Default is `false`. |
| `DJANGO_SECRET_KEY` | `change-me-to-a-long-random-string` | Django secret key. When `DJANGO_DEBUG` is not `true` the app refuses to start with the built-in dev key, so set your own. |
| `DJANGO_ALLOWED_HOSTS` | `api.example.cz` | Comma-separated host names the app answers to. Default `localhost,127.0.0.1`. |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://api.example.cz` | Comma-separated origins trusted for admin forms (with `https://`). Needed behind an HTTPS proxy. |
| `DJANGO_USE_HTTPS` | `true` | `true` marks session and CSRF cookies as secure. Use `false` over plain HTTP. |
| `POSTGRES_DB` | `ples` | Database name. |
| `POSTGRES_USER` | `ples` | Database user. |
| `POSTGRES_PASSWORD` | `change-me` | Database password. Set it before the first start, the volume keeps the first one. |
| `WEB_PORT` | `8005` | Host port mapped to the web container (port 8000 inside). Has no default, so it must be set. |
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` | E-mail backend. Use the console backend to print e-mails to the log. |
| `EMAIL_HOST` | `smtp.example.com` | SMTP server. |
| `EMAIL_PORT` | `587` | SMTP port. |
| `EMAIL_HOST_USER` | (empty) | SMTP user. |
| `EMAIL_HOST_PASSWORD` | (empty) | SMTP password. |
| `EMAIL_USE_TLS` | `true` | Use STARTTLS for SMTP. |
| `DEFAULT_FROM_EMAIL` | `Ples UTB <ples@sutb.cz>` | Sender of the booking confirmation e-mail. |
| `BALL_YEAR` | `2026` | Year written in the subject and body of the confirmation e-mail. |

## API

All paths start with `/api` and have no trailing slash. Public endpoints are throttled to 60 requests per minute, login to 20 per minute (per client).

| Method | Path | Auth | What it does |
| --- | --- | --- | --- |
| POST | `/api/login` | none | Staff login with `email` and `password`. Returns `201` with `user` and `token`. |
| POST | `/api/logout` | Bearer | Deletes the token of the user. |
| GET | `/api/pages/reservations` | none | Seat map of the active event: `availableStands`, `freeSeats`, `takenSeats` and every seat. `404` if there is no active event. |
| POST | `/api/reservations` | Bearer, staff | Reserve standing places (`stand`) and seats (`seats`, list of seat ids) with an optional `note`. Computes the price and marks the payment date. |
| GET | `/api/reservations/search/{name}` | Bearer, staff | Reservations of the active event whose name contains the text. |
| GET | `/api/pages/landing` | none | Landing page texts, team contacts and ticket sales info. `404` if the ticket sales info is not filled in. |
| GET | `/api/makers` | none | Makers, their services and for each time slot (1400 to 1830, every 30 minutes) the ids of free makers. |
| POST | `/api/makers` | none | Book a maker: `maker`, `time`, `service`, `name`, `phone`, `email`, `consent`. Blocks that time for the maker and sends a confirmation e-mail. |
| GET | `/api/config` | none | Site settings as one flat object, for example `{"TICKET_URL": "..."}`. |

Notes:

- Send the token as `Authorization: Bearer <token>`. A user has one token, so logging in again returns the same one.
- Errors use the Laravel shapes: validation `422` with `{"message": ..., "errors": {...}}`, missing or bad token `401` with `{"message": "Unauthenticated."}`, non-staff `403`, bad bookings or reservations `400` with `{"error": "..."}`, wrong login `401` with `{"message": "Bad credentials."}`.
- A reservation is refused when nothing is selected, when there are too few standing places left, when a seat does not exist or when a seat is already taken. Only one request at a time can reserve for an event (the event row is locked).
- If the confirmation e-mail fails to send, the booking stays and the error is only logged.

## Django admin

Open `/admin/` and log in with a staff user.

| Model | What staff can do |
| --- | --- |
| Users | Add and edit staff accounts. Only users with `is_staff` can log in to the API. |
| Ročníky (events) | Edit year, date, standing capacity, prices and `is_active` (only one event can be active). The list shows an overview: free and taken seats, standing places and money raised (reduced by `complimentary_value`). Action **Připravit další ročník** creates the next year as inactive, with the same prices and a copy of all seats, all free. It refuses if that year already exists. |
| Místa (seats) | Read only list, filter by event, type and free or taken. |
| Rezervace (reservations) | Search and filter; no adding or editing. Deleting one, or the action **Zrušit rezervaci**, frees its seats and standing places. |
| Kadeřnice / kosmetičky (makers), Služby (services) | Add and edit makers and what they offer. |
| Obsazené časy (blocked times) | Add a time (for example `1430`) to close it for a maker. |
| Rezervace salonu (salon bookings) | No adding or editing. Deleting one frees the time of the maker. |
| Texty úvodní stránky, Kontakty, Prodej lístků | Landing page content. A text can only change its body (its title is how the page finds it), a contact keeps its role (the role `tickets` is the presale contact, which is not shown in the team contacts), and ticket sales holds the start date and the presale contact. |
| Nastavení (settings) | Key-value settings, for example `TICKET_URL`. |

Preparing a new ball year: open Ročníky, select the last event, run **Připravit další ročník**, then edit the new event (date, prices, standing capacity) and tick `is_active` after un-ticking the old one. Update the landing page content and ticket sales, check the makers and their blocked times, and set `BALL_YEAR` in `.env`.

## Deploy

On a Linux server with Docker and Compose v2.

```bash
# copy this folder to the server, then inside it:
cp .env.example .env
```

Set in `.env`:

- `DJANGO_DEBUG=false`
- `DJANGO_SECRET_KEY` to a long random string
- `DJANGO_ALLOWED_HOSTS` to your domain, `DJANGO_CSRF_TRUSTED_ORIGINS` to `https://<your domain>`
- `DJANGO_USE_HTTPS=true`
- `POSTGRES_PASSWORD` to a strong password (before the first start)
- `WEB_PORT` (the port the proxy forwards to) and the `EMAIL_*`, `DEFAULT_FROM_EMAIL` and `BALL_YEAR` values

```bash
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

The database port is not published, only the `web` container is reachable on `WEB_PORT`. The app speaks plain HTTP and trusts the `X-Forwarded-Proto` header, so put a reverse proxy with HTTPS in front. Example Caddyfile (Caddy gets the certificate itself):

```
api.example.cz {
    reverse_proxy localhost:8005
}
```

Use your domain and your `WEB_PORT`. If you bind the port only locally, change the compose port line to `127.0.0.1:${WEB_PORT}:8000`.

Update:

```bash
git pull   # or copy the new files
docker compose up -d --build
```

Migrations and `seed_data` run automatically on start.

Logs:

```bash
docker compose logs -f web
```

Backup and restore of the database (the data lives in the `pgdata` volume; the project stores no uploaded files, so there is no media volume):

```bash
# backup
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > backup.sql

# restore: start only the database, recreate it empty, load the dump, then start everything
docker compose stop web
docker compose exec db sh -c 'dropdb -U "$POSTGRES_USER" "$POSTGRES_DB" && createdb -U "$POSTGRES_USER" "$POSTGRES_DB"'
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" "$POSTGRES_DB"' < backup.sql
docker compose up -d
```
