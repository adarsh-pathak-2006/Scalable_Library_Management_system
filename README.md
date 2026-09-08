<div align="center">

# 📚 Scalable Library Management System

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=6E56CF&center=true&vCenter=true&width=600&lines=Production-Ready+REST+API;Built+for+Scale+%7C+Built+for+Speed;Django+%7C+Celery+%7C+Redis+%7C+PostgreSQL" alt="Typing SVG" />

<br/>

[![Django](https://img.shields.io/badge/Django-5.2-0C4B33?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.17-ff1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Celery](https://img.shields.io/badge/Celery-5.6-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-NeonDB-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://neon.tech/)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)

<br/>

**A high-performance, multi-tenant Library Management REST API** engineered for scalability. Features asynchronous task processing, multi-layer caching, role-based access control, OTP-based authentication, and a fully production-hardened deployment pipeline.

🌐 **Live API:** [`https://scalable-library-management-system.onrender.com`](https://scalable-library-management-system.onrender.com/)

</div>

---

## ✨ Feature Highlights

| Feature | Implementation | Benefit |
|---|---|---|
| 🔐 **OTP Registration Flow** | Celery + Redis + Cache | Async, non-blocking, secure sign-up |
| 🚀 **Redis Caching** | `django-redis` | Reduces DB queries by up to 90% |
| 🎭 **Role-Based Permissions** | Custom DRF Permissions | Students vs Librarians access scopes |
| 🔑 **JWT Authentication** | `simplejwt` | Stateless, token-based security |
| ⚡ **Async Task Queue** | Celery + Redis Broker | Background jobs never block the API |
| 🛡️ **API Throttling** | Custom DRF Throttles | Rate-limits per role & endpoint type |
| 📦 **Auto Cart Management** | Django Signals | Cart & Profile auto-created on signup |
| 📊 **Pagination** | DRF Pagination | Efficient data loading on all list endpoints |
| 🐘 **PostgreSQL** | NeonDB (Serverless) | Production-grade, scalable cloud DB |
| 🌐 **CORS Support** | `django-cors-headers` | Plug-and-play frontend integration |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser / Mobile)               │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP Requests
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RENDER.COM (Web Service)                       │
│  ┌─────────────────────┐   ┌──────────────────────────────────┐ │
│  │    Gunicorn WSGI    │   │       Celery Worker              │ │
│  │  (Django REST API)  │   │ (Async OTP, Book Issuing Tasks)  │ │
│  └──────────┬──────────┘   └──────────────┬───────────────────┘ │
└─────────────┼──────────────────────────────┼────────────────────┘
              │                              │
    ┌─────────▼──────────┐        ┌─────────▼──────────┐
    │     NeonDB         │        │  Upstash Redis      │
    │  (PostgreSQL)      │        │  (Cache + Broker)   │
    │  User / Book data  │        │  OTP / Sessions     │
    └────────────────────┘        └────────────────────┘
```

---

## 🔌 API Reference

### 🔐 Authentication (`/auth/`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `POST` | `/auth/register/` | Register with username, email, mobile | Public |
| `POST` | `/auth/otp-verify/<code>/` | Verify OTP sent via SMS | Public |
| `POST` | `/auth/password-setup/<code>/` | Set password after OTP verification | Public |
| `POST` | `/auth/api/token/` | Obtain JWT access + refresh tokens | Public |
| `POST` | `/auth/api/token/refresh/` | Refresh access token | Public |
| `GET` | `/auth/my-profile/` | View own profile | Student |
| `PATCH` | `/auth/my-profile/` | Update own profile | Student |
| `GET/POST` | `/auth/colleges/` | List or create colleges | Admin |

### 📚 Book Store (`/bookstore/`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/bookstore/category/` | List all categories (paginated + cached) | Authenticated |
| `POST` | `/bookstore/category/` | Create a new category | Librarian |
| `GET/PATCH/DELETE` | `/bookstore/category/<id>/` | Manage a category | Authenticated / Librarian |
| `GET` | `/bookstore/book/` | List available books (paginated + cached) | Authenticated |
| `POST` | `/bookstore/book/` | Add a new book | Librarian |
| `GET/PATCH/DELETE` | `/bookstore/book/<id>/` | Manage a book | Authenticated / Librarian |

### 📖 Lending (`/lend/`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/lend/cart/` | View current cart (cached) | Student |
| `POST` | `/lend/addtocart/<book_id>/` | Add a book to cart | Student |
| `POST` | `/lend/issue/<cart_id>/` | Issue all books in cart | Student |
| `GET` | `/lend/issued-books/` | View all issued books (cached) | Student |

---

## 🔄 Registration Flow (OTP-Based)

```
1. POST /auth/register/
   └── Validates data → stores session in Redis → fires OTP Celery task (async)
   └── Returns: { session_code: 12345678 }

2. POST /auth/otp-verify/12345678/
   └── Compares OTP from Redis → marks session as verified
   └── Returns: { message: "otp verified" }

3. POST /auth/password-setup/12345678/
   └── Reads verified session → creates User, Profile, Cart in DB
   └── Returns: { message: "User registration Successful" }
```

---

## ⚙️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Framework** | Django 5.2 + Django REST Framework |
| **Database** | PostgreSQL via NeonDB (Serverless) |
| **Caching** | Redis via Upstash + `django-redis` |
| **Task Queue** | Celery 5 + Redis as Broker |
| **Auth** | JWT via `djangorestframework-simplejwt` |
| **Static Files** | WhiteNoise (no Nginx needed!) |
| **Deployment** | Render + Gunicorn |
| **Environment** | `django-environ` |

</div>

---

## 🚀 Getting Started (Local Development)

### Prerequisites
- Python 3.11+
- Redis running locally (`redis://127.0.0.1:6379`)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Scalable_Library.git
cd Scalable_Library/config
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your values
```

Your `.env` file should look like this:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=*
CORS_ALLOW_ALL_ORIGINS=True

# For local dev, use sqlite. For production, use NeonDB.
DATABASE_URL=sqlite:///db.sqlite3

# Local Redis
REDIS_URL=redis://127.0.0.1:6379/1
```

### 4. Apply Migrations & Run
```bash
python manage.py migrate
python manage.py runserver
```

### 5. Start the Celery Worker (in a separate terminal)
```bash
celery -A config worker -l info
```

---

## ☁️ Deploying to Render

1. **Set up [NeonDB](https://neon.tech)** → grab your `DATABASE_URL`.
2. **Set up [Upstash Redis](https://upstash.com)** → grab your `REDIS_URL` (starts with `rediss://`).
3. Push this repo to **GitHub**.
4. Create a new **Web Service** on Render and connect your repo.
5. Set the following in Render's dashboard:

| Setting | Value |
|---|---|
| **Build Command** | `./build.sh` |
| **Start Command** | `./start.sh` |

6. Add all environment variables from your `.env` (with `DEBUG=False` and your real NeonDB/Upstash URLs) to Render's **Environment** tab.
7. 🚀 Hit **Deploy**!

---

## 🛡️ Security & Performance Design

- **Rate Limiting**: Every endpoint is protected by custom `UserRateThrottle` classes. Sensitive endpoints like token generation (`5/min`) and registration (`30/day`) have aggressive limits to prevent abuse.
- **OTP Expiry**: OTPs expire after **10 minutes** (stored in Redis). Sessions expire after **5 minutes** of inactivity.
- **JWT Lifetimes**: Access tokens last **1 day**. Refresh tokens last **30 days** and auto-rotate with every use.
- **Cache Invalidation**: Django Signals automatically bust the cache whenever a Book, Category, CartBook, or IssuedBook is modified — ensuring clients never see stale data.
- **Stock Validation**: `CartBook.save()` raises a `ValidationError` if a requested quantity exceeds the library's physical stock.

---

## 📁 Project Structure

```
config/
├── config/                  # Project config package
│   ├── settings.py          # All settings (env-driven)
│   ├── celery.py            # Celery app initialization
│   ├── urls.py              # Root URL dispatcher
│   ├── permissions.py       # IsStudent, IsLibrarian, etc.
│   ├── throttling.py        # Custom rate limit classes
│   ├── cache_keys.py        # Centralized cache key functions
│   └── pagination.py        # Global pagination config
├── authentication/          # User, Profile, College, OTP flow
├── store/                   # Category & Book management
├── lend/                    # Cart, Issuing, IssuedBooks
├── build.sh                 # Render build script
├── start.sh                 # Render start script (Gunicorn + Celery)
├── requirements.txt
├── .env.example
└── manage.py
```

---

<div align="center">

**Built with ❤️ and engineered for production.**

If you found this useful, consider giving it a ⭐ on GitHub!

</div>
