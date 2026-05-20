# URL Shortener API

A production-style URL Shortener REST API built with Django and
Django REST Framework. Accepts long URLs, generates unique short
codes, and redirects users to original URLs.

---

## Tech Stack

- Python 3.10+
- Django 5.x
- Django REST Framework
- SQLite (development)
- Deployed on Render

---

## Features

- Shorten any valid URL to a unique 8-character code
- Redirect short URLs to original destinations
- Duplicate URL detection — same input returns same short code
- Click counter tracked on every redirect
- Full input validation and error handling
- Django Admin panel for database management
- Consistent JSON response structure across all endpoints

---

## Project Structure
url-shortener/
├── config/
│   ├── settings.py       # Project settings
│   └── urls.py           # Root URL routing
├── shortener/
│   ├── admin.py          # Django admin config
│   ├── exceptions.py     # Custom error handler
│   ├── models.py         # URL database model
│   ├── serializers.py    # Input validation
│   ├── urls.py           # App URL routing
│   └── views.py          # API logic
├── build.sh              # Render build script
├── manage.py
└── requirements.txt

---

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create admin user
```bash
python manage.py createsuperuser
```

### 6. Start the server
```bash
python manage.py runserver
```

---

## API Endpoints

### POST `/api/shorten/`
Shorten a long URL.

**Request:**
```json
{
    "original_url": "https://google.com"
}
```

**Response `201 Created`:**
```json
{
    "success": true,
    "status_code": 201,
    "message": "Short URL created successfully.",
    "id": 1,
    "original_url": "https://google.com",
    "short_code": "550e8400",
    "short_url": "http://127.0.0.1:8000/550e8400/"
}
```

---

### GET `/api/urls/<short_code>/`
Retrieve details of a short URL.

**Response `200 OK`:**
```json
{
    "success": true,
    "status_code": 200,
    "data": {
        "id": 1,
        "original_url": "https://google.com",
        "short_code": "550e8400",
        "created_at": "2026-05-20T10:00:00Z",
        "click_count": 5
    }
}
```

---

### GET `/<short_code>/`
Redirects to the original URL.

**Response:** `302 Redirect → https://google.com`

---

## Error Responses

All errors follow this consistent structure:

```json
{
    "success": false,
    "status_code": 400,
    "error": "Descriptive error message here."
}
```

| Status Code | Meaning |
|---|---|
| 400 | Bad Request — invalid or missing input |
| 404 | Not Found — short code does not exist |
| 405 | Method Not Allowed |

---

## Admin Panel

Visit `/admin/` and log in with your superuser credentials
to manage all URLs visually.

---

## Deployment

Live URL: `https://your-app-name.onrender.com`