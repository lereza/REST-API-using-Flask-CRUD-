from datetime import datetime

from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///employ.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# =========================
# BOOK MODEL
# =========================
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)


# =========================
# NOTE MODEL
# =========================
class Note(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}-{self.title}"


with app.app_context():
    db.create_all()


# =========================
# HOME PAGE
# =========================
@app.route('/', methods=['GET', 'POST'])
def Home():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        note = Note(
            title=title,
            description=description
        )

        db.session.add(note)
        db.session.commit()

    allNote = Note.query.all()
    return render_template("index.html", allNote=allNote)


# =========================
# QUERY STRING DEMO
# =========================
@app.route('/qs')
def Get_qs():
    if request.args:
        req = request.args
        return " ".join(f"{k}:{v}" for k, v in req.items())

    return "No query"


# =========================
# DELETE NOTE
# =========================
@app.route('/delete/<int:sno>')
def Delete(sno):
    note = Note.query.filter_by(sno=sno).first()

    if note:
        db.session.delete(note)
        db.session.commit()

    allNote = Note.query.all()
    return render_template("index.html", allNote=allNote)


# =========================
# UPDATE NOTE
# =========================
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def Update(sno):
    note = Note.query.filter_by(sno=sno).first()

    if request.method == 'POST':
        note.title = request.form['title']
        note.description = request.form['description']

        db.session.commit()

        return redirect("/")

    return render_template("update.html", note=note)


# ==================================================
# BOOK REST API
# ==================================================

# GET ALL BOOKS
@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()

    return jsonify([
        {
            "id": book.id,
            "title": book.title,
            "author": book.author
        }
        for book in books
    ]), 200


# GET SINGLE BOOK
@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    book = db.session.get(Book, id)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author
    }), 200


# CREATE BOOK
@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    if 'title' not in data or 'author' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_book = Book(
        title=data['title'],
        author=data['author']
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "message": "Book created",
        "id": new_book.id
    }), 201


# UPDATE BOOK
@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = db.session.get(Book, id)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    if 'title' not in data or 'author' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    book.title = data['title']
    book.author = data['author']

    db.session.commit()

    return jsonify({
        "message": "Book updated"
    }), 200


# DELETE BOOK
@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = db.session.get(Book, id)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({
        "message": "Book deleted"
    }), 200


if __name__ == '__main__':
    app.run(debug=True)