from extensions import db
from models.book import Books


def default_insert():
    """default population of the database with default values for testing"""
    book_list = [
        {"id": 1, "name": "The Russian", "type": "fiction", "available": True},
        {"id": 2, "name": "Just as I Am", "type": "non-fiction", "available": False},
        {"id": 3, "name": "The Vanishing Half",
            "type": "fiction", "available": True},
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

    for a_book in book_list:
        bk = Books()
        bk.name = a_book["name"]
        bk.type = a_book["type"]
        bk.available = a_book["available"]

        db.session.add(bk)
        db.session.commit()