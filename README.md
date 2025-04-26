
# Authenticator

User authentication API built with Django and Django REST Framework, using JWT for authentication and automatic documentation via Swagger. The project is fully dockerized and uses PostgreSQL as the database.

---

## 📦 Technologies Used

- [Python](https://www.python.org/) 3.x
- [Django](https://www.djangoproject.com/)
- [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [drf-yasg (Swagger)](https://drf-yasg.readthedocs.io/en/stable/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [PostgreSQL](https://www.postgresql.org/)

---

## 🚀 How to Run the Project

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

2. Create the `.env` file at the project root:

```env
DJANGO_SECRET_KEY='your-secret-key'
DEBUG=False
# TO RUN TETS, COMMENT THE LINE ABOVE AND UNCOMMENT THE LINE BELLOW:
# DEBUG=True
DJANGO_LOGLEVEL=info
DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost'
DATABASE_ENGINE=postgresql_psycopg2
DATABASE_NAME=db_name
DATABASE_USERNAME=db_username
DATABASE_PASSWORD=db_password
DATABASE_HOST=db
DATABASE_PORT=5432
```

3. Create virtual enviroment:

```bash
python -m venv .venv
```

4. Active virtual enviroment:

| Plataform | Shell          | Command |
|:------:|:------------------ |:---------------------------------|
| POSIX   | bash/zsh        | ```$ source <venv>/bin/activate```      |
| POSIX   | fish        | ```$ source <venv>/bin/activate.fish```      |
| POSIX   | csh/tcsh        | ```$ source <venv>/bin/activate.csh```      |
| POSIX   | pwsh        | ```$ <venv>/bin/Activate.ps1```      |
| Windows   | cmd.exe        | ```C:\> <venv>\Scripts\activate.bat```      |
 Windows   | PowerShell        | ```PS C:\> <venv>\Scripts\Activate.ps1```      |

5. Install project dependency.

```bash
pip install -r requirements.txt
```

6. Start the Docker containers:

```bash
docker-compose up --build
```

7. Access:

- Django API: http://localhost:8000/api/
- Swagger UI: http://localhost:8000/swagger/
- Redoc: http://localhost:8000/redoc/

---

## 🛠 Project Structure

```
backend/
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── autenticator/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── authapi/ 
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── middleware.py.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
└── staticfiles
```

---

## 📚 API Endpoints

| Method | Endpoint             | Description                          |
|:------:|:--------------------- |:------------------------------------|
| POST   | `/api/register/`       | Register a new user                 |
| GET    | `/api/me/`             | Fetch the logged-in user's info     |
| POST   | `/api/login/`          | Log in and obtain JWT tokens        |
| POST   | `/api/logout/`         | Log out and blacklist refresh token |
| POST   | `/api/token/refresh/`  | Refresh the access token            |

---

## ✉️ Usage Examples

### 📥 Register User

```bash
POST /api/register/
Content-Type: application/json

{
  "first_name": "YourFirstName",
  "last_name": "YourLastName",
  "email": "email@example.com",
  "password": "strong_password"
}
```

**Response:**

```json
{
    "id": 1,
    "username": "YourFirstNameYourLastName25042402174450",
    "email": "email@example.com"
}
```

### 🔐 User Login

```bash
POST /api/login/
Content-Type: application/json

{
  "email": "email@example.com",
  "password": "strong_password"
}
```

**Response:**

```json
{
  "token": {
    "refresh_token": "your_refresh_token",
    "access_token": "your_access_token"
  }
}
```

### 🔐 User Logout

```bash
POST /api/logout/
Content-Type: application/json

{
  "token": "your_refresh_token"
}
```

### 👤 Fetch Logged-in User Info

```bash
GET /api/me/
Authorization: Bearer your_access_token
```

### 🔄 Refresh Access Token

```bash
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token"
}
```

---

## 🐳 Docker Containers

- **db**: PostgreSQL database (port 5432)
- **django-web**: Django application (port 8000)

---

## 📜 Useful Commands

- Start containers:

  ```bash
  docker-compose up --build
  ```

- Stop containers:

  ```bash
  docker-compose down
  ```

- Run migrations:

  ```bash
  docker-compose exec django-web python manage.py migrate
  ```

- Create superuser:

  ```bash
  docker-compose exec django-web python manage.py createsuperuser
  ```

---

## 🧩 Notes

- API documentation is available at `/swagger/` and `/redoc/`.
- The project requires environment variables for secure configuration.
- All tokens follow the JWT standard (access and refresh).

---

> Made with ❤️ using Django + DRF + Docker.