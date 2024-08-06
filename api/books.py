from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from extensions import db
from models.book import Books
from models.ext_funcs import default_insert

books_bp = Blueprint("books", __name__, url_prefix='/api/v1/books')


@books_bp.get("/")
@jwt_required()
def books_get():
    books = db.session.execute(db.select(Books)).scalars().all()

    try:
        if len(books) < 1:
            default_insert()

        book_comp = [bk.to_dict() for bk in books]
        return jsonify(book_comp), 201

    except Exception as e:
        return jsonify({"message": "Nothing found on the db",
                        "error": f"{e}"}), 404


@books_bp.post("/")
@jwt_required()
def create_book():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid JSON"}), 400

        book = Books()
        book.name = data.get("name")
        book.available = True if data.get("available") == "true" else False
        book.type = data.get("type")

        db.session.add(book)
        db.session.commit()

        return jsonify({"message": "Book created successfully"}), 201

    except Exception as e:
        return jsonify({"message": "Failed to create book", "error": str(e)}), 400


@books_bp.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def single_book(id):
    claims = get_jwt()

    if claims.get('is_staff'):
        book = db.session.execute(
            db.select(Books).where(Books.id == id)
        ).scalar_one_or_none()
        if book is None:
            return jsonify({"message": f"Book with id {id} not found"}), 404

        if request.method == "GET":
            return jsonify(book.to_dict()), 200

        if request.method == "PUT":
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"message": "Invalid JSON"}), 400

                book.name = data.get("name")
                book.available = True if data.get("available") == "true" else False
                book.type = data.get("type")

                db.session.commit()
                return jsonify({"message": f"Book with id {id} updated successfully"}), 200

            except Exception as e:
                return jsonify({"message": "Failed to update book", "error": str(e)}), 400

        if request.method == "DELETE":
            try:
                db.session.delete(book)
                db.session.commit()
                return jsonify({"message": f"Book with id {id} deleted successfully"}), 200

            except Exception as e:
                return jsonify({"message": "Failed to delete book", "error": str(e)}), 400

    return jsonify({"message": f"User {claims.get('sub', '')} not allowed to access this route"}), 401
