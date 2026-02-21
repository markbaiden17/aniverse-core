# AniVerse Core — Media Social Tracking API

A RESTful API built with **Django 5** and **Django REST Framework** that allows users to track, rate, and review anime titles. The API follows a decoupled architecture — it stores no anime metadata directly, but instead references titles by their unique ID from the external [Kitsu API](https://kitsu.docs.apiary.io/), keeping the backend lightweight and focused on user data.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Web Framework | Django 5.0.6 |
| API Toolkit | Django REST Framework 3.15.2 |
| Authentication | DRF Token Authentication |
| Database (Dev) | SQLite |
| Database (Prod) | PostgreSQL |
| Deployment | PythonAnywhere (upcoming) |

---

## Project Structure
```
aniverse-core/
├── apps/
│   ├── authentication/     # Register & login endpoints
│   ├── reviews/            # Review CRUD + custom permissions
│   ├── watchlist/          # Personal watchlist tracking
│   └── stats/              # Community analytics endpoint
├── config/
│   ├── settings.py         # Project settings
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── .gitignore
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/aniverse-core.git
cd aniverse-core
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (Git Bash)
source venv/Scripts/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Start the development server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Create a new user account | No |
| POST | `/api/auth/login/` | Obtain an authentication token | No |

**Register request body:**
```json
{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password"
}
```

**Login / Register response:**
```json
{
  "message": "Account created successfully.",
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "your_email@example.com"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

---

### Reviews

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/reviews/` | List all reviews (paginated) | No |
| POST | `/api/reviews/` | Submit a new review | Yes |
| GET | `/api/reviews/<id>/` | Retrieve a single review | No |
| PUT / PATCH | `/api/reviews/<id>/` | Update a review | Owner only |
| DELETE | `/api/reviews/<id>/` | Delete a review | Owner only |

**Create review request body:**
```json
{
  "media_id": 1,
  "rating": 9,
  "comment": "An absolute masterpiece."
}
```

**Review response:**
```json
{
  "id": 1,
  "user": 1,
  "username": "your_username",
  "media_id": 1,
  "rating": 9,
  "comment": "An absolute masterpiece.",
  "created_at": "2026-02-15T20:53:32.187669Z",
  "updated_at": "2026-02-15T20:53:32.187697Z"
}
```

**Query parameters for `GET /api/reviews/`:**

| Parameter | Description | Example |
|-----------|-------------|---------|
| `media_id` | Filter reviews by Kitsu anime ID | `?media_id=1` |
| `search` | Search within review comments | `?search=masterpiece` |
| `ordering` | Sort results by field | `?ordering=-rating` |

---

### Watchlist

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/watchlist/` | Get your personal watchlist | Yes |
| POST | `/api/watchlist/` | Add a title to your watchlist | Yes |
| PATCH | `/api/watchlist/<id>/` | Update watching status | Owner only |
| DELETE | `/api/watchlist/<id>/` | Remove from watchlist | Owner only |

**Add to watchlist request body:**
```json
{
  "media_id": 1,
  "status": "watching"
}
```

**Status options:**
- `plan_to_watch`
- `watching`
- `completed`
- `on_hold`
- `dropped`

**Watchlist response:**
```json
{
  "id": 1,
  "media_id": 1,
  "status": "watching",
  "status_display": "Watching",
  "added_at": "2026-02-21T20:25:12.643378Z",
  "updated_at": "2026-02-21T20:25:12.643415Z"
}
```

**Query parameters for `GET /api/watchlist/`:**

| Parameter | Description | Example |
|-----------|-------------|---------|
| `status` | Filter by watching status | `?status=completed` |
| `ordering` | Sort by field | `?ordering=-added_at` |

---

### Stats (Analytics)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/stats/<media_id>/` | Get community stats for an anime | No |

**Stats response:**
```json
{
  "media_id": 1,
  "average_rating": 8.5,
  "total_reviews": 12,
  "rating_distribution": {
    "1": 0, "2": 0, "3": 1, "4": 0, "5": 1,
    "6": 2, "7": 2, "8": 3, "9": 2, "10": 1
  }
}
```

If no reviews exist for the given `media_id`, the response returns:
```json
{
  "media_id": 99999,
  "average_rating": null,
  "total_reviews": 0,
  "rating_distribution": {
    "1": 0, "2": 0, "3": 0, "4": 0, "5": 0,
    "6": 0, "7": 0, "8": 0, "9": 0, "10": 0
  },
  "detail": "No reviews found for this title."
}
```

---

## Authentication

Include the token in the `Authorization` header for all protected endpoints:
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## Validation & Error Handling

| Scenario | Status Code | Response |
|----------|-------------|----------|
| Missing or invalid token | `401 Unauthorized` | `{"detail": "Authentication credentials were not provided."}` |
| Editing another user's review/watchlist | `403 Forbidden` | `{"detail": "You do not have permission to modify or delete another user's review."}` |
| Rating outside 1–10 range | `400 Bad Request` | `{"rating": ["Rating must be an integer between 1 and 10."]}` |
| Duplicate review for same anime | `400 Bad Request` | `{"media_id": ["You have already submitted a review for this title."]}` |
| Duplicate watchlist entry | `400 Bad Request` | `{"media_id": ["This title is already in your watchlist."]}` |
| Resource not found | `404 Not Found` | `{"detail": "No Review matches the given query."}` |

---

## Testing with curl

**Register:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ -H "Content-Type: application/json" -d '{"username": "your_username", "email": "your_email@example.com", "password": "your_password"}'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}'
```

**Create a review (replace TOKEN with your actual token):**
```bash
curl -X POST http://127.0.0.1:8000/api/reviews/ -H "Content-Type: application/json" -H "Authorization: Token TOKEN" -d '{"media_id": 1, "rating": 9, "comment": "Amazing anime!"}'
```

**Add to watchlist:**
```bash
curl -X POST http://127.0.0.1:8000/api/watchlist/ -H "Content-Type: application/json" -H "Authorization: Token TOKEN" -d '{"media_id": 1, "status": "watching"}'
```

**Get stats for an anime:**
```bash
curl http://127.0.0.1:8000/api/stats/1/
```

---

## Upcoming Features

- **Unit Tests** — full test suite covering all endpoints, validation, and permissions
- **Production Deployment** — live API hosted on PythonAnywhere with PostgreSQL