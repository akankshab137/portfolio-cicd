# URL Shortener

A minimal URL shortener built with Flask and SQLite. Generates short codes, tracks click counts, and supports custom aliases.

## Features

- Shorten any URL to a short code
- Custom alias support
- Click tracking and analytics
- REST API endpoints
- SQLite storage (no setup required)

## API

```
POST /shorten        { "url": "https://example.com", "alias": "mylink" }
GET  /<short_code>   → redirect to original URL
GET  /stats/<code>   → click count and metadata
DELETE /<short_code> → delete the link
```

## Run Locally

```bash
pip install flask
python app.py
```

Open http://localhost:5000
