## Zaytun - Classifieds & Messaging API

A modern, OLX-style marketplace backend built with FastAPI.  
Zaytun provides a clean REST API for managing users, listings, categories, favourites, messages between users, and an internal wallet balance for paid features.

---

- **Online Code**
  - `https://github1s.com/AkromAbdaliev/Zaytun` (replace with your actual repo URL)

---

## 🌟 Features

- **User Management**
  - User registration and login with JWT access tokens stored in **HTTP-only cookies**
  - Secure password hashing with `passlib`
  - Email + optional phone & geolocation (GeoPoint) support
  - **Role-based access control** with `user` and `admin` roles

- **Listings & Categories**
  - CRUD operations for **categories**
  - CRUD operations for **listings**
  - Listings linked to categories and owners
  - Geolocation field for listings (PostGIS `Geography(POINT)`), ready for location-based searches
  - Active/inactive flag for soft disabling listings

- **Favourites**
  - Users can **favourite** listings
  - Unique `(user_id, listing_id)` constraint to prevent duplicates
  - API to add/remove and list favourites

- **Messaging (Listing-based conversations)**
  - Users can **send messages** about a specific listing
  - Messages are **always tied to a listing** (not a free chat app)
  - Inbox endpoint for the receiver
  - Thread endpoint per `(listing_id, other_user_id)` between two participants
  - Mark message as read
  - Access checks:
    - Only listing owner and the other participant can participate in and view the thread
    - Cannot send messages to yourself

- **Wallet (Internal Balance)**
  - Per-user wallet with integer `balance`
  - Auto-creation of wallet on first access
  - Endpoints to **top up** and **spend** balance
  - Safety checks for insufficient balance
  - Can be extended later for paid promotions, bumps, or featured listings

- **Admin & Roles**
  - `UserRole` enum with `user` and `admin`
  - **Admin-only** endpoints for managing users (listing all users, updating roles, etc.)
  - Simple `require_roles(...)` dependency to protect admin routes

- **Database Migrations**
  - Alembic for versioned schema migrations
  - Initial migrations for users, categories, listings, favourites, messages, wallet
  - Additional migration for user roles

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Async Driver**: asyncpg
- **Geo**: GeoAlchemy2 + PostGIS for location fields

### Authentication & Security
- **Password Hashing**: `passlib` (PBKDF2 SHA256)
- **JWT Tokens**: `python-jose`
- **Auth Transport**: Access token stored as HTTP-only cookie

### Migrations & Validation
- **Migrations**: Alembic
- **Schema Validation**: Pydantic v2
- **Settings Management**: Pydantic Settings

---

## 📋 Requirements

- Python 3.10+ (recommended)
- PostgreSQL with PostGIS extension
- (Optional) Make / psql CLI tools for DB management

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AkromAbdaliev/Zaytun
cd Zaytun
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_db_user
DB_PASS=your_db_password
DB_NAME=zaytun_db

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
```

### 5. Setup Database

```bash
# Create database (example with psql)
createdb zaytun_db

# Run migrations
alembic upgrade head
```

Make sure PostgreSQL has **PostGIS** enabled for the database if you want to use geolocation fields.

### 6. Start the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

---

## 📖 API Documentation

Once the server is running, interactive documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 🔑 Authentication

The API uses JWT tokens stored in an **HTTP-only cookie** named `access_token`.

### Register

```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_password",
  "phone": "string or null",
  "location": "POINT(lon lat)"  // optional, WKT format
}
```

### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_password"
}
```

On success, the API sets an `access_token` cookie (HTTP-only) and also returns `{ "access_token": "..." }` in the body.

### Logout

```http
POST /auth/logout
```

This clears the `access_token` cookie on the client.

### Get Current User

```http
GET /auth/me
```

Requires a valid `access_token` cookie.

---

## 🔗 Core API Endpoints (Overview)

This is a **high-level** overview of important endpoints. For full details, see Swagger UI.

### Auth & Users

| Endpoint        | Method | Path          | Description                            | Access        |
|----------------|--------|---------------|----------------------------------------|---------------|
| Register       | POST   | `/auth/register` | Register a new user                  | Public        |
| Login          | POST   | `/auth/login`    | Authenticate and get access token    | Public        |
| Logout         | POST   | `/auth/logout`   | Logout user (remove auth cookie)     | Authenticated |
| Me             | GET    | `/auth/me`       | Current user profile                 | Authenticated |
| List Users     | GET    | `/user`          | List all users                       | Admin         |
| Get User       | GET    | `/user/{id}`     | Get user details by ID               | Admin         |
| Create User    | POST   | `/user`          | Create user (by admin)               | Admin         |
| Update User    | PUT    | `/user/{id}`     | Update user (role, flags, etc.)      | Admin         |
| Delete User    | DELETE | `/user/{id}`     | Delete user                           | Admin         |

### Categories

| Endpoint              | Method | Path                 | Description                 | Access  |
|-----------------------|--------|----------------------|-----------------------------|---------|
| List Categories       | GET    | `/category`          | Get all categories          | Public  |
| Get Category By ID    | GET    | `/category/{id}`     | Get category details        | Public  |
| Create Category       | POST   | `/category`          | Create category             | Admin\* |
| Update Category       | PUT    | `/category/{id}`     | Update category             | Admin\* |
| Delete Category       | DELETE | `/category/{id}`     | Delete category             | Admin\* |

(\* you may want to protect these with `require_roles(UserRole.ADMIN)` similarly to users)

### Listings

| Endpoint           | Method | Path                 | Description                       | Access        |
|--------------------|--------|----------------------|-----------------------------------|---------------|
| List Listings      | GET    | `/listing`           | List active listings              | Public        |
| Get Listing        | GET    | `/listing/{id}`      | Get listing details by ID         | Public        |
| Create Listing     | POST   | `/listing`           | Create new listing                | Public/Auth\* |
| Update Listing     | PUT    | `/listing/{id}`      | Update listing                    | Public/Auth\* |
| Delete Listing     | DELETE | `/listing/{id}`      | Delete listing                    | Public/Auth\* |

(\* currently not bound to `current_user` in code; you can later restrict so only listing owners can modify their listings.)

### Favourites

| Endpoint             | Method | Path                | Description                          | Access        |
|----------------------|--------|---------------------|--------------------------------------|---------------|
| List Favourites      | GET    | `/favourite`        | List user favourites                 | Authenticated |
| Add Favourite        | POST   | `/favourite`        | Add listing to favourites            | Authenticated |
| Remove Favourite     | DELETE | `/favourite/{id}`   | Remove favourite by ID               | Authenticated |

### Messages (Listing-based)

| Endpoint                       | Method | Path                                      | Description                                             | Access        |
|--------------------------------|--------|-------------------------------------------|---------------------------------------------------------|---------------|
| Send Message                   | POST   | `/messages`                               | Send message about a listing to another user           | Authenticated |
| Inbox                          | GET    | `/messages/inbox`                         | Get messages where current user is the receiver        | Authenticated |
| Get Thread w/ User for Listing | GET    | `/messages/thread/{listing_id}/{user_id}` | Get conversation thread for a specific listing & user  | Authenticated |
| Mark Message as Read           | PATCH  | `/messages/{message_id}/read`             | Mark a message as read (receiver only)                 | Authenticated |

**Business rules:**
- `listing_id` is required when sending messages.
- Only listing owner and the other participant can see or send messages for that listing.
- A user cannot send messages to themselves.

### Wallet

| Endpoint        | Method | Path           | Description                                  | Access        |
|----------------|--------|----------------|----------------------------------------------|---------------|
| Get My Wallet  | GET    | `/wallet/me`   | Get or create wallet for current user        | Authenticated |
| Top Up Wallet  | POST   | `/wallet/topup`| Increase balance by a positive integer amount| Authenticated |
| Spend Wallet   | POST   | `/wallet/spend`| Decrease balance (fails if not enough funds) | Authenticated |

Request examples:

```http
POST /wallet/topup
Content-Type: application/json

{ "amount": 5000 }
```

```http
POST /wallet/spend
Content-Type: application/json

{ "amount": 2000 }
```

---

## 🏗️ Project Structure

```text
Zaytun/
├── app/
│   ├── admin/                 # (reserved for future admin UI/config)
│   ├── categories/            # Categories module
│   │   ├── model.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── core/                  # Core application setup
│   │   ├── config.py          # Settings & env config
│   │   ├── database.py        # Async SQLAlchemy engine & Base
│   │   ├── db.sql             # (optional SQL helpers / init script)
│   │   └── exceptions.py      # Custom HTTP exceptions
│   ├── favourites/            # Favourites module
│   │   ├── model.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── listings/              # Listings module
│   │   ├── model.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── messages/              # Messages module (per-listing conversations)
│   │   ├── model.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── migrations/            # Alembic migrations
│   ├── services/              # Shared service layer
│   │   └── base.py            # BaseService with generic CRUD helpers
│   ├── users/                 # Users & authentication
│   │   ├── auth/              # Auth router + service
│   │   │   ├── router.py
│   │   │   └── service.py
│   │   ├── dependencies.py    # get_current_user & role requirements
│   │   ├── model.py           # User & UserRole
│   │   ├── router.py          # User management (admin)
│   │   ├── schemas.py
│   │   ├── security.py        # Password hashing & JWT helper
│   │   └── service.py
│   ├── wallet/                # Wallet module
│   │   ├── model.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   └── main.py                # FastAPI application entry point
├── alembic.ini                # Alembic configuration
├── migrations/                # Alembic migrations directory
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🗄️ Database Migrations

### Create a New Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migrations

```bash
alembic downgrade -1
```

---

## 🚨 Error Handling

The API uses consistent HTTP exceptions for common error cases:

- **400**: Bad Request (e.g., invalid payload, not enough balance in wallet)
- **401**: Unauthorized (missing/invalid token, not logged in)
- **403**: Forbidden (valid token but not enough permissions / wrong role)
- **404**: Not Found (user, listing, category, favourite, message not found)
- **409**: Conflict (e.g., user already exists, favourite already added)

See `app/core/exceptions.py` for the exact exception definitions.

---

## 🛡️ Security Considerations

- Passwords are hashed using `passlib` with a strong algorithm (PBKDF2 SHA256)
- JWT tokens include expiration and are signed with a secret key
- JWT is stored in an **HTTP-only cookie** to reduce XSS token theft risk
- Secrets and database credentials are loaded from environment variables

---

## 🤝 Contributing

Contributions and suggestions are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to your fork (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 📄 License

This project is currently private; add a LICENSE file (e.g., MIT) if you plan to open source it.

---

**Built with ❤️ using FastAPI and PostgreSQL**


