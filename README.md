# Library Management System API

This web application provides a backend built with the **FastAPI** framework. The system supports library management (authors, genres, books, and reviews) and provides real-time server monitoring.

## Project features

1.  **Full CRUD through the REST API**: Create, read, update, and delete operations for all database entities.
2.  **SQL database**: PostgreSQL integration using SQLAlchemy (ORM), with proper support for foreign keys and cascading deletes.
3.  **Asynchronous WebSocket**: Server status (CPU, RAM, and timestamp) is returned in JSON format every 5 seconds.
4.  **Monitoring page**: A frontend dashboard visualizes WebSocket data in real time.
5.  **Unit tests**: A complete set of automated tests prepared with `pytest`.
6.  **Type annotations and documentation**: Fully typed code and Swagger documentation.

---

## Technologies and requirements

* **Language**: Python 3.10+
* **Framework**: FastAPI
* **Database**: PostgreSQL + SQLAlchemy (ORM)
* **Frontend**: Jinja2 templates, Tailwind CSS
* **Testing**: Pytest + HTTPX

---

## Installation and setup

### 1. Configuration

Install and start Docker Desktop.

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Then change the secret values in `.env`. Example `.env` file:

```env
DB_PASSWORD=your_database_password
DATABASE_URL=postgresql+psycopg://library_user:your_database_password@localhost:5432/library
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

The `DATABASE_URL` shown above is the address used from the host machine.
When running with Docker Compose, the backend automatically uses `db:5432`.

### 2. Starting the application
Start PostgreSQL and the backend with a single command:

```bash
docker compose up --build
```

Docker Compose will automatically:

* start PostgreSQL,
* wait for the database to become ready,
* build and start the backend,
* make the API available at http://127.0.0.1:8000.

The `.env` file must contain at least `DB_PASSWORD`, `JWT_SECRET_KEY`,
`JWT_ALGORITHM`, and `ACCESS_TOKEN_EXPIRE_MINUTES`. Inside the backend
container, the database address is automatically set to `db:5432`.

To run the containers in the background, use:

```bash
docker compose up --build -d
```
After startup, the application will be available at http://127.0.0.1:8000.

---

## Usage
* **Interactive documentation (Swagger):** http://127.0.0.1:8000/docs
* **Monitoring dashboard:** http://127.0.0.1:8000/monitor

---

## Testing
The project includes unit tests that verify CRUD operations, database relationships,
and Pydantic model validation. To run the tests, use:
```bash
  pytest
```

---

## Project structure

```text
library_api/
├── app/                # Main backend code (FastAPI)
│   ├── api/            # Routing: API (JSON) and views (HTML)
│   ├── core/           # Database and application configuration
│   ├── crud/           # Database operation logic
│   ├── models/         # Database table models (SQLAlchemy)
│   └── schemas/        # Data validation schemas (Pydantic)
├── templates/          # Frontend files (HTML)
├── tests/              # Unit tests (pytest)
├── requirements.txt    # List of dependencies to install
└── README.md           # Project documentation