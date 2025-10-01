# 📝 Flask RESTful Blog API

A RESTful API for a blogging platform built with **Flask**, supporting full CRUD operations for **Users**, **Posts**, **Comments**, and **Tags**.
Includes features like **role-based access control**, **rate limiting**, **pagination**, and **database migrations**.

---

## 🔧 Features

-   ✅ CRUD operations for users, blog posts, comments, and tags
-   ✅ Role-based access control for admin-only routes
-   ✅ Pagination support with Flask-Smorest
-   ✅ Rate limiting with Flask-Limiter
-   ✅ Database ORM via Flask-SQLAlchemy
-   ✅ Schema migrations with Alembic
-   ✅ Modular structure with Flask Blueprints

---

## 📦 Tech Stack

| Tech             | Purpose                                    |
| ---------------- | ------------------------------------------ |
| Python + Flask   | Web framework                              |
| Flask-SQLAlchemy | ORM for database models                    |
| SQLite           | Lightweight relational DB                  |
| Alembic          | For DB migrations                          |
| Flask-Smorest    | Blueprint + Schema validation + Pagination |
| Flask-Limiter    | Rate limiting support                      |
| Marshmallow      | Data serialization and validation          |

---

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   `pip` installed

### Installation

```bash
git clone https://github.com/fore-site/blog-api.git
cd blog-api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Run Migrations

Read the [alembic documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html) in order to set up the configuration

```bash
alembic init alembic
alembic revision -m "Initial migration"
alembic upgrade head
```

### Start the App

```bash
flask run
```

The API will be available at: `http://localhost:5000/api/v1`

---

## 🔐 Authentication & Authorization

-   **JWT-based auth**
-   **Role-based access control**:

    -   `admin`: Full access to all endpoints
    -   `member`: Restricted to personal actions (e.g. editing own posts)

Example:

```json
{
    "username": "jack",
    "role": "admin"
}
```

---

## 📚 API Documentation

> Full API schema available in Swagger

### 📌 Base URL

```
http://localhost:5000/api/v1/
```

### 📖 Swagger UI (Interactive Docs)

Thanks to **Flask-Smorest**, interactive API documentation is available via **Swagger UI**.

🧭 Access it at:

```
http://localhost:5000/swagger-ui
```

This interface provides:

-   Complete endpoint listing
-   Schemas and request/response formats
-   Built-in testing capabilities

> Tip: Use it to explore available endpoints and try out requests directly in your browser.

---

## ⚙️ Environment Variables Summary

Add the following to your `.env` or config file:

```env
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key
DATABASE_URI=sqlite:///data.db

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_EXPIRES=15m
JWT_REFRESH_TOKEN_EXPIRES=30d

# Redis for token revocation
REDIS_URL=redis://localhost:6379/0
```

## 🔐 Authentication & Authorization

### 🔒 Token Revocation (Logout Support)

This API uses **Redis** to store and check **revoked JWTs**, making logout and token invalidation secure and reliable.

#### ✅ How It Works

-   When a user logs out, their **access** or **refresh** token is added to a Redis **blocklist**.
-   For each protected request, the token is checked against Redis.
-   If found in the blocklist, access is denied with a `401 Unauthorized`.

### 📦 Redis Integration

-   Redis is required and should be running on `localhost:6379` by default.
-   You can configure the Redis URI via environment variable:

    ```env
    REDIS_URL=redis://localhost:6379/0
    ```

---

### 🧪 Logout Endpoint Example

```http
POST /logout
Authorization: Bearer <access_token>
```

**Response:**

```json
{
    "message": "Access token revoked"
}
```

> You can also revoke refresh tokens by inserting the refresh token in the authorization header.

---

### 🔁 Refresh Token Flow

To get a new access token using a refresh token:

```http
POST /refresh
Authorization: Bearer <refresh_token>
```

If the refresh token is **not revoked**, a new access token will be issued.

---

### 📬 Example Endpoints

#### Users

-   `GET /users` — List all users (admin only)
-   `GET /users/<id>` — Get single user
-   `GET /profile` — Get self (current user)
-   `PATCH /profile` — Update user/self
-   `PATCH /users/<id>/suspend` — Suspend user (admin only)
-   `PATCH /users/<id>/restore` — Restore user (admin only)
-   `DELETE /profile` — Delete/deactivate current user account

#### Posts

-   `POST /posts` — Create post
-   `GET /posts` — List posts (supports pagination)
-   `GET /posts/<id>` — Get post
-   `PUT /posts/<id>` — Update post
-   `DELETE /posts/<id>` — Delete post (admin and member roles)
-   `PUT /posts/<int:post_id>/tags/<int:tag_id>` — Link post with tag
-   `DELETE /admin/posts/<int:post_id>/tags/<int:tag_id>` — Unlink tag from post (admin)

#### Comments

-   `POST /posts/<id>/comments` — Add comment
-   `GET /posts/<id>comments` — Get comments for a post
-   `GET /posts/<post_id>/comments/<comment_id>` — GET single comment for a post
-   `PUT /posts/<post_id>/comments/<comment_id>` — Edit comment for a post
-   `DELETE /posts/<post_id>/comments/<comment_id>` — Delete single comment for a post (admin and member roles)

#### Tags

-   `POST /tags` — Add a new tag (admin)
-   `GET /tags` — List tags
-   `GET /tags/<id>` — Get single tag
-   `PUT /tags/<id>` — Edit tag (admin)
-   `DELETE /tags/<id>` — Delete tag (admin)

---

## 🔐 Auth Endpoints Overview

| Method | Endpoint    | Description                            |
| ------ | ----------- | -------------------------------------- |
| POST   | `/register` | Register a new user                    |
| POST   | `/login`    | Get JWT access + refresh tokens        |
| POST   | `/logout`   | Revoke access and refresh tokens       |
| POST   | `/refresh`  | Get new access token via refresh token |

---

## 📈 Pagination

Paginated endpoints support:

```http
GET /posts?page=2&page_size=10
```

> Response will include header metadata "X-Pagination"

---

## 🧠 Future Improvements

-   [ ] Add support for likes/upvotes on posts
-   [ ] Email/password auth with password reset
-   [ ] Search functionality for posts and tags

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 📧 Contact

For any questions, feel free to reach out at:
📫 [ogunsanu17@gmail.com](mailto:ogunsanu17@gmail.com)
