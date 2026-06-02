# Flask Web Application with REST API Enhancement

## 📌 Project Overview
This project is a Flask-based web application enhanced with a REST API feature.  
The original application included a notes management system, and this enhancement adds a fully functional Book Management REST API.

---

## 🚀 Added Feature: Book REST API

A new REST API module was implemented to manage books using full CRUD operations:

### 📖 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/books | Retrieve all books |
| GET | /api/books/<id> | Retrieve a single book |
| POST | /api/books | Create a new book |
| PUT | /api/books/<id> | Update a book |
| DELETE | /api/books/<id> | Delete a book |

---

## ⚙️ Technologies Used
- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Pytest

---

## 🧪 Testing

The project includes a complete test suite using **pytest**:

### Test Coverage:
- Create book (positive test)
- Get all books
- Get single book
- Update book
- Delete book
- Negative tests (404, 400 cases)

### Run tests:
```bash
pytest
