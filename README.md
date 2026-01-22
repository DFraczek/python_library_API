# Library Management System API

Aplikacja webowa z backendem zbudowana przy użyciu frameworka **FastAPI**. System umożliwia zarządzanie biblioteką (autorzy, gatunki, książki, recenzje) oraz oferuje monitoring parametrów serwera w czasie rzeczywistym.

## Funkcjonalności projektu

1.  **Pełny CRUD przez REST API**: Obsługa operacji Create, Read, Update, Delete dla wszystkich encji bazy danych.
2.  **Baza Danych SQL**: Integracja z SQLite przy użyciu SQLAlchemy (ORM) z poprawną obsługą kluczy obcych i kaskadowego usuwania.
3.  **Asynchroniczny WebSocket**: Zwracanie statusu serwera (CPU, RAM, Timestamp) w formacie JSON co 5 sekund.
4.  **Strona do monitoringu**: Panel frontendowy wizualizujący dane z WebSocketu w czasie rzeczywistym.
5.  **Testy Jednostkowe**: Kompletny zestaw testów automatycznych przygotowany przy użyciu `pytest`.
6.  **Type Annotation & Dokumentacja**: Pełne typowanie kodu oraz dokumentacja Swagger.

---

## Technologie i wymagania

* **Język**: Python 3.10+
* **Framework**: FastAPI
* **Baza danych**: SQLite + SQLAlchemy (ORM)
* **Frontend**: Jinja2 Templates, Tailwind CSS
* **Testy**: Pytest + HTTPX

---

## Instalacja i uruchomienie

### 1. Przygotowanie środowiska
Stwórz środowisko wirtualne i zainstaluj wymagane biblioteki:

```bash
# Tworzenie środowiska venv
python -m venv .venv
```

```bash
# Aktywacja (Windows)
.venv\Scripts\activate
```

```bash
# Instalacja bibliotek z pliku requirements
pip install -r requirements.txt
```

### 2. Uruchomienie aplikacji
Użyj serwera uvicorn, aby wystartować projekt:

```bash
  uvicorn app.main:app --reload
```
Po uruchomieniu aplikacja będzie dostępna pod adresem: http://127.0.0.1:8000

---

## Instrukcja obsługi
* **Interaktywna dokumentacja (Swagger):** http://127.0.0.1:8000/docs
* **Panel Monitoringu:** http://127.0.0.1:8000/monitor

---

## Testy
Projekt zawiera zestaw testów jednostkowych weryfikujących poprawność działania CRUD, relacji w bazie danych oraz walidacji modeli Pydantic. Aby je uruchomić, wpisz:
```bash
  python -m pytest -v
```

---

## Struktura projektu

```text
library_api/
├── app/                # Główny kod backendu (FastAPI)
│   ├── api/            # Routing: API (JSON) oraz widoki (HTML)
│   ├── core/           # Konfiguracja bazy danych i aplikacji
│   ├── crud/           # Logika operacji na bazie danych
│   ├── models/         # Modele tabel bazy danych (SQLAlchemy)
│   └── schemas/        # Schematy walidacji danych (Pydantic)
├── templates/          # Pliki frontendowe (HTML)
├── tests/              # Testy jednostkowe (pytest)
├── requirements.txt    # Lista bibliotek do zainstalowania
└── README.md           # Dokumentacja projektu