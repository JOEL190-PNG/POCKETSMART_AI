# PocketSmart AI

PocketSmart AI is a FastAPI + Jinja2 web application for budget-aware recommendations across:

- Home Interior Planning
- Party Budget Planning
- Jewelry Recommendations with optional outfit image analysis
- User registration/login
- JWT authentication
- Recommendation history
- Gemini-powered structured recommendations
- Safe local fallback recommendations when Gemini is unavailable

## Architecture

```text
Browser
  |
  v
FastAPI + Jinja2
  |-- auth routes
  |-- planner routes
  |-- history routes
  |
  +--> services/recommender.py
          |
          +--> services/gemini_service.py --> Gemini API
          |
          +--> services/catalog_service.py --> local simulated catalog/search links
  |
  +--> SQLite
```

The supplied project document specifies FastAPI, Jinja2, Gemini, three planners, authentication/session endpoints, history, CORS, and fallback recommendations. This implementation keeps those requirements while making the project runnable as a single application.

## Important model note

The source document names **Gemini 1.5 Flash Pro**. The Gemini model/API landscape changes over time, so the application does **not hard-code a discontinued model.** Set `GEMINI_MODEL` in `.env` to a model available to your Gemini API account. The example `.env.example` uses `gemini-2.5-flash`.

The implementation uses Google's current `google-genai` Python SDK style rather than the older `google-generativeai` package.

## 1. Requirements

- Python 3.11+
- VS Code
- A Gemini API key for live AI recommendations (optional; fallback mode works without it)

## 2. VS Code setup

Open the `pocketsmart_ai` folder in VS Code.

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=replace-with-a-long-random-secret
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash
DATABASE_URL=sqlite:///./pocketsmart.db
USE_MOCK_AI=false
CORS_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
```

If you leave `GEMINI_API_KEY` blank, set:

```env
USE_MOCK_AI=true
```

## 3. Run

```bash
uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

## 4. Test

Run:

```bash
pytest -q
```

The tests use mock AI behavior and do not require a Gemini key.

## 5. Main API endpoints

### Public/auth

- `GET /`
- `GET /health`
- `POST /register`
- `POST /login`
- `POST /token`
- `POST /logout`
- `GET /session-info`
- `GET /session-data`

### Planners

- `GET /home-planner`
- `POST /generate-home`
- `GET /party-planner`
- `POST /generate-party`
- `GET /jewelry-planner`
- `POST /generate-jewelry`
- `GET /recommendations-details/{history_id}`

### History

- `GET /history`
- `GET /dashboard`

## 6. Recommendation behavior

The project document describes product/service sources such as Amazon, Flipkart, IKEA, Swiggy, Zomato, and OYO. This implementation deliberately uses **simulated catalog/search links** instead of scraping or pretending to have official partner APIs. Each recommendation identifies the platform and produces a search URL.

For production, replace `catalog_service.py` with licensed/official APIs or approved affiliate/product feeds.

## 7. Jewelry image upload

The Jewelry Planner accepts JPG, JPEG, PNG, and WEBP files up to 5 MB. The image is sent to Gemini only when a Gemini key is configured and mock mode is disabled.

## 8. Security notes

- Passwords are hashed with bcrypt through Passlib.
- JWT access tokens are stored in an HttpOnly cookie.
- CSRF is not required for the JSON API endpoints in this starter because authentication is cookie-based; for production deployment, add CSRF protection or use Authorization headers.
- Set a strong `SECRET_KEY`.
- Do not commit `.env` or user uploads.
- SQLite is suitable for local development. Use PostgreSQL for production.

## 9. Production improvements

- PostgreSQL
- Redis-backed sessions/rate limiting
- Real vendor/product APIs
- Object storage for images
- Background jobs
- Observability
- CSRF protection
- HTTPS
- Rate limiting
- Account email verification
- Moderation and prompt-injection defenses
