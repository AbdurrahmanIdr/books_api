from flask import Blueprint, request, jsonify
from extensions import db
from models import Books

books_bp = Blueprint("books", __name__)

book_list = [
    {"id": 1, "name": "The Russian", "type": "fiction", "available": True},
    {"id": 2, "name": "Just as I Am", "type": "non-fiction", "available": False},
    {"id": 3, "name": "The Vanishing Half", "type": "fiction", "available": True},
    {"id": 4, "name": "The Midnight Library",
        "type": "fiction", "available": True},
    {"id": 5, "name": "Untamed", "type": "non-fiction", "available": True},
    {
        "id": 6,
        "name": "Viscount Who Loved Me",
        "type": "fiction",
        "available": True,
    },
]


@books_bp.get("/books")
def books_get():
    books = db.session.execute(db.select(Books)).scalars().all()

    if len(books) > 0:
        book_comp = [bk.to_dict() for bk in books]
        return jsonify(book_comp), 201

    return jsonify({"message": "Nothing found on the db"}), 404


@books_bp.post("/books")
def create_book():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid JSON"}), 400

        book = Books()
        book.name = data.get('name')
        book.available = True if data.get('available') == 'true' else False
        book.type = data.get('type')

        db.session.add(book)
        db.session.commit()

        return jsonify({"message": "Book created successfully"}), 201

    except Exception as e:
        return jsonify({"message": "Failed to create book", "error": str(e)}), 400


@books_bp.route("/books/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_book(id):
    book = db.session.execute(db.select(Books).where(
        Books.id == id)).scalar_one_or_none()
    if book is None:
        return jsonify({"message": f"Book with id {id} not found"}), 404

    if request.method == "GET":
        return jsonify(book.to_dict()), 200

    if request.method == "PUT":
        try:
            data = request.get_json()
            if not data:
                return jsonify({"message": "Invalid JSON"}), 400

            book.name = data.get('name')
            book.available = True if data.get('available') == 'true' else False
            book.type = data.get('type')

            db.session.commit()
            return jsonify({'message': f'Book with id {id} updated successfully'}), 200

        except Exception as e:
            return jsonify({"message": "Failed to update book", "error": str(e)}), 400

    if request.method == "DELETE":
        try:
            db.session.delete(book)
            db.session.commit()
            return jsonify({'message': f'Book with id {id} deleted successfully'}), 200

        except Exception as e:
            return jsonify({"message": "Failed to delete book", "error": str(e)}), 400
