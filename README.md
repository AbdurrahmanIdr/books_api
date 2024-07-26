# Books API

## Overview

The Books API is a RESTful API built with Flask and SQLAlchemy that allows users to perform CRUD (Create, Read, Update, Delete) operations on a collection of books. This project demonstrates the use of Flask for backend development, SQLAlchemy for ORM, and various RESTful principles for API design.

## Features

- **Create a Book**: Add new books to the collection.
- **Retrieve All Books**: Get a list of all books in the collection.
- **Retrieve a Single Book**: Get details of a specific book by its ID.
- **Update a Book**: Modify the details of an existing book.
- **Delete a Book**: Remove a book from the collection.

## Requirements

- Python 3.12+
- Flask
- Flask-SQLAlchemy
- Gunicorn

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/AbdurrahmanIdr/books_api.git
   cd books_api
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory of the project and add the following environment variables:

   ```
   FLASK_SQLALCHEMY_DATABASE_URI=sqlite:///memory.db
   FLASK_SQLALCHEMY_TRACK_MODIFICATIONS=False
   FLASK_SQLALCHEMY_ECHO=True
   ```

5. **Initialize the Database**

   Run the following command to create the necessary database tables:

   ```bash
   flask shell
   >>> from extensions import db
   >>> db.create_all()
   ```

## Usage

1. **Run the Application**

   ```bash
   flask run
   ```

   The application will start and be accessible at `http://127.0.0.1:5000`.

2. **Endpoints**

   - **GET /books**: Retrieve all books.
   - **POST /books**: Create a new book. Requires a JSON payload with `name`, `type`, and `available` fields.
   - **GET /books/<id>**: Retrieve a book by its ID.
   - **PUT /books/<id>**: Update a book by its ID. Requires a JSON payload with `name`, `type`, and `available` fields.
   - **DELETE /books/<id>**: Delete a book by its ID.

## Example Requests

- **Create a Book**:

   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"name": "The Great Gatsby", "type": "fiction", "available": "true"}' http://127.0.0.1:5000/books/books
   ```

- **Retrieve All Books**:

   ```bash
   curl http://127.0.0.1:5000/books/books
   ```

- **Retrieve a Single Book**:

   ```bash
   curl http://127.0.0.1:5000/books/books/1
   ```

- **Update a Book**:

   ```bash
   curl -X PUT -H "Content-Type: application/json" -d '{"name": "The Great Gatsby", "type": "classic", "available": "true"}' http://127.0.0.1:5000/books/books/1
   ```

- **Delete a Book**:

   ```bash
   curl -X DELETE http://127.0.0.1:5000/books/books/1
   ```

## Deployment

To deploy the Books API to Render:

1. Create a `requirements.txt` file:

   ```bash
   pip freeze > requirements.txt
   ```

2. Create a `Procfile` with the following content:

   ```
   web: gunicorn app:create_app()
   ```

3. Push your code to a Git repository (e.g., GitHub).

4. Go to the [Render Dashboard](https://dashboard.render.com/), create a new web service, and connect your Git repository.

5. Configure the build and start commands, set environment variables, and deploy the service.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
