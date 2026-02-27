# AniVerse Core — Media Social Tracking API

A RESTful API built with **Django 5** and **Django REST Framework** that allows users to track, rate, and review anime titles. The API integrates with the **AniList GraphQL API** to dynamically fetch anime metadata while storing only user-generated content (reviews, ratings, watchlists) in its own database. This decoupled architecture keeps the backend lightweight and ensures anime information is always up-to-date.

---

## 🚀 Features

- **User Authentication** — Token-based auth with registration and login
- **Review System** — Full CRUD for anime reviews with 1-10 ratings
- **Watchlist Tracking** — Personal anime lists with 5 status categories
- **Community Stats** — Aggregated ratings and review counts per anime
- **AniList Integration** — Dynamically fetches anime titles and metadata
- **Ownership Protection** — Custom permissions ensure users can only edit their own content
- **Pagination & Filtering** — Query parameters for search, filtering, and sorting

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Web Framework | Django 5.0.6 |
| API Toolkit | Django REST Framework 3.15.2 |
| Authentication | DRF Token Authentication |
| External API | AniList GraphQL API |
| Database (Dev) | SQLite |
| Database (Prod) | PostgreSQL |
| HTTP Client | Requests 2.31.0 |

---

## 📁 Project Structure
```
aniverse-core/
├── apps/
│   ├── authentication/     # User registration & login
│   ├── reviews/            # Review CRUD + AniList integration
│   ├── watchlist/          # Personal watchlist tracking
│   └── stats/              # Community analytics
├── config/
│   ├── settings.py         # Django settings
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py
├── tests.py                # Comprehensive test suite (29 tests)
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/aniverse-core.git
cd aniverse-core
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows (Git Bash)
source venv/Scripts/activate

# Activate on Windows (Command Prompt)
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Database Migrations
```bash
python manage.py migrate
```

### Step 5: (Optional) Create an Admin User
```bash
python manage.py createsuperuser
```
Follow the prompts to create credentials. Access the admin panel at `http://127.0.0.1:8000/admin/`.

### Step 6: Start the Development Server
```bash
python manage.py runserver
```

The API will be available at **`http://127.0.0.1:8000/`**

---

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

---

## 🔐 Authentication Endpoints

### Register a New User
**Endpoint:** `POST /api/auth/register/`  
**Auth Required:** No

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response (201 Created):**
```json
{
  "message": "Account created successfully.",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

---

### Login
**Endpoint:** `POST /api/auth/login/`  
**Auth Required:** No

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful.",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

---

## 📝 Review Endpoints

### List All Reviews
**Endpoint:** `GET /api/reviews/`  
**Auth Required:** No

**Query Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `media_id` | Filter by AniList anime ID | `?media_id=16498` |
| `search` | Search within comments | `?search=amazing` |
| `ordering` | Sort by field (`rating`, `created_at`) | `?ordering=-rating` |

**Response (200 OK):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "username": "johndoe",
      "media_id": 16498,
      "anime_title": "Attack on Titan",
      "rating": 9,
      "comment": "An absolute masterpiece!",
      "created_at": "2026-02-27T10:30:00Z",
      "updated_at": "2026-02-27T10:30:00Z"
    }
  ]
}
```

---

### Create a Review
**Endpoint:** `POST /api/reviews/`  
**Auth Required:** Yes (Token)

**Request Body:**
```json
{
  "media_id": 16498,
  "rating": 9,
  "comment": "An absolute masterpiece!"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user": 1,
  "username": "johndoe",
  "media_id": 16498,
  "anime_title": "Attack on Titan",
  "rating": 9,
  "comment": "An absolute masterpiece!",
  "created_at": "2026-02-27T10:30:00Z",
  "updated_at": "2026-02-27T10:30:00Z"
}
```

---

### Get a Single Review
**Endpoint:** `GET /api/reviews/<id>/`  
**Auth Required:** No

**Response (200 OK):**
```json
{
  "id": 1,
  "user": 1,
  "username": "johndoe",
  "media_id": 16498,
  "anime_title": "Attack on Titan",
  "rating": 9,
  "comment": "An absolute masterpiece!",
  "created_at": "2026-02-27T10:30:00Z",
  "updated_at": "2026-02-27T10:30:00Z"
}
```

---

### Update a Review
**Endpoint:** `PUT /api/reviews/<id>/` or `PATCH /api/reviews/<id>/`  
**Auth Required:** Yes (Owner only)

**Request Body (PATCH):**
```json
{
  "rating": 10
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user": 1,
  "username": "johndoe",
  "media_id": 16498,
  "anime_title": "Attack on Titan",
  "rating": 10,
  "comment": "An absolute masterpiece!",
  "created_at": "2026-02-27T10:30:00Z",
  "updated_at": "2026-02-27T11:00:00Z"
}
```

---

### Delete a Review
**Endpoint:** `DELETE /api/reviews/<id>/`  
**Auth Required:** Yes (Owner only)

**Response (204 No Content)**

---

### Get Popular Anime List
**Endpoint:** `GET /api/reviews/anime-list/`  
**Auth Required:** No

**Query Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `limit` | Number of results (max 50) | `?limit=10` |

**Response (200 OK):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 16498,
      "title": "Attack on Titan",
      "cover_image": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx16498-buvcRTBx4NSm.jpg",
      "average_score": 85,
      "episodes": 25
    },
    {
      "id": 1535,
      "title": "Death Note",
      "cover_image": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx1535-kUgkcrfOrkUM.jpg",
      "average_score": 84,
      "episodes": 37
    }
  ]
}
```

---

## 📋 Watchlist Endpoints

### Get Your Watchlist
**Endpoint:** `GET /api/watchlist/`  
**Auth Required:** Yes

**Query Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `status` | Filter by status | `?status=watching` |
| `ordering` | Sort by field | `?ordering=-added_at` |

**Response (200 OK):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "media_id": 16498,
      "anime_title": "Attack on Titan",
      "status": "watching",
      "status_display": "Watching",
      "added_at": "2026-02-27T10:00:00Z",
      "updated_at": "2026-02-27T10:00:00Z"
    }
  ]
}
```

---

### Add to Watchlist
**Endpoint:** `POST /api/watchlist/`  
**Auth Required:** Yes

**Request Body:**
```json
{
  "media_id": 16498,
  "status": "watching"
}
```

**Status Options:**
- `plan_to_watch`
- `watching`
- `completed`
- `on_hold`
- `dropped`

**Response (201 Created):**
```json
{
  "id": 1,
  "media_id": 16498,
  "anime_title": "Attack on Titan",
  "status": "watching",
  "status_display": "Watching",
  "added_at": "2026-02-27T10:00:00Z",
  "updated_at": "2026-02-27T10:00:00Z"
}
```

---

### Update Watchlist Entry
**Endpoint:** `PATCH /api/watchlist/<id>/`  
**Auth Required:** Yes (Owner only)

**Request Body:**
```json
{
  "status": "completed"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "media_id": 16498,
  "anime_title": "Attack on Titan",
  "status": "completed",
  "status_display": "Completed",
  "added_at": "2026-02-27T10:00:00Z",
  "updated_at": "2026-02-27T12:00:00Z"
}
```

---

### Remove from Watchlist
**Endpoint:** `DELETE /api/watchlist/<id>/`  
**Auth Required:** Yes (Owner only)

**Response (204 No Content)**

---

## 📊 Stats Endpoint

### Get Community Stats for an Anime
**Endpoint:** `GET /api/stats/<media_id>/`  
**Auth Required:** No

**Response (200 OK):**
```json
{
  "media_id": 16498,
  "average_rating": 8.75,
  "total_reviews": 4,
  "rating_distribution": {
    "1": 0, "2": 0, "3": 0, "4": 0, "5": 0,
    "6": 0, "7": 1, "8": 1, "9": 1, "10": 1
  }
}
```

**If no reviews exist:**
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

## 🔒 Authentication

All protected endpoints require a token in the `Authorization` header:
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## ⚠️ Error Handling

| Scenario | Status Code | Response |
|----------|-------------|----------|
| Missing/invalid token | `401 Unauthorized` | `{"detail": "Authentication credentials were not provided."}` |
| Editing another user's content | `403 Forbidden` | `{"detail": "You do not have permission to modify or delete another user's review."}` |
| Rating outside 1-10 range | `400 Bad Request` | `{"rating": ["Rating must be an integer between 1 and 10."]}` |
| Duplicate review | `400 Bad Request` | `{"media_id": ["You have already submitted a review for this title."]}` |
| Duplicate watchlist entry | `400 Bad Request` | `{"media_id": ["This title is already in your watchlist."]}` |
| Resource not found | `404 Not Found` | `{"detail": "Not found."}` |

---

## 🧪 Running Tests

The project includes a comprehensive test suite with 29 tests covering all functionality:
```bash
python manage.py test
```

**Test Coverage:**
- User registration and login validation
- Review CRUD operations
- Rating validation (1-10 range)
- Duplicate prevention
- Ownership permissions
- Watchlist privacy
- Stats aggregation accuracy

---

## 🌐 AniList Integration

The API integrates with the **AniList GraphQL API** to fetch anime metadata:

- **Anime titles** are dynamically retrieved when viewing reviews or watchlist entries
- **Popular anime list** endpoint pulls top anime from AniList
- All anime data is **cached** to reduce API calls
- Integration is **fault-tolerant** — if AniList is down, the API still functions (titles just won't display)

---

## 📖 Usage Examples with curl

### Register and Get Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'
```

### Create a Review
```bash
curl -X POST http://127.0.0.1:8000/api/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{"media_id": 16498, "rating": 9, "comment": "Amazing anime!"}'
```

### Get Popular Anime
```bash
curl http://127.0.0.1:8000/api/reviews/anime-list/?limit=5
```

### Add to Watchlist
```bash
curl -X POST http://127.0.0.1:8000/api/watchlist/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{"media_id": 16498, "status": "watching"}'
```

### Get Stats
```bash
curl http://127.0.0.1:8000/api/stats/16498/
```

---

## 🚀 Deployment

### PythonAnywhere Setup (Coming Soon)

1. Upload code via Git
2. Create PostgreSQL database
3. Set environment variables (`DEBUG=False`, `SECRET_KEY`, database credentials)
4. Run migrations: `python manage.py migrate`
5. Configure WSGI file
6. Collect static files: `python manage.py collectstatic`

---

## 👨‍💻 Developer Notes

### Key Design Decisions

**Decoupled Architecture:**  
User data (reviews, watchlists) is stored locally, while anime metadata is fetched on-demand from AniList. This keeps the database lean and ensures anime info is always current.

**Owner-Only Permissions:**  
Custom `IsOwnerOrReadOnly` permission class ensures users can only modify their own content. Read operations are public.

**Watchlist Privacy:**  
Watchlist queries are scoped by `request.user` at the queryset level, returning 404 (not 403) for cross-user access attempts to prevent information leakage.

**Rating Validation:**  
Enforced at both serializer and database levels with Django validators.

**Caching:**  
AniList API calls are cached using `@lru_cache` to minimize external requests and improve response times.

---

## 📄 License

This project is open source and available for educational purposes.

---

## 🤝 Contributing

This is a capstone project submission. Contributions are not currently accepted, but feel free to fork and experiment!

---

## 📧 Contact

**Developer:** Mark Baiden  
**GitHub:** https://github.com/markbaiden17/aniverse-core  
**Email:** markbaiden17@gmail.com