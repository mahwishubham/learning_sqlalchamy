# Import Flask
import os
import requests

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from data_models import db, Author, Book
from dotenv import load_dotenv
from sqlalchemy.orm import joinedload

load_dotenv()  # loads .env file into the bash environment variables ( printenv )
API_KEY = os.getenv("API_KEY")  # reading the key from environment.


# Create the Flask app instance
app = Flask(__name__)

# Configure the database connection URI
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/m_azizi/Desktop/masterschool/learning_sqlalchamy/data/library234.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Add this line to suppress the warning

# Initialize the db with the Flask app
db.init_app(app)


def get_book_cover(title):
    url = f"https://www.googleapis.com/books/v1/volumes?q={title}&key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            item = data['items'][0]
            if 'volumeInfo' in item and 'imageLinks' in item['volumeInfo']:
                return item['volumeInfo']['imageLinks']['thumbnail']

    return "https://images.unsplash.com/photo-1532012197267-da84d127e765"


@app.route('/')
def home():
    # Get the sorting parameter if provided
    sort_by = request.args.get('sort_by', 'title')
    
    # Query all books and load their associated authors
    books_query = Book.query.options(joinedload(Book.author))
    
    # Apply sorting based on the provided parameter
    if sort_by == 'title':
        books_query = books_query.order_by(Book.title.asc())
    elif sort_by == 'author':
        books_query = books_query.join(Author).order_by(Author.name.asc())
    
    books = books_query.all()

    message = request.args.get('message')
    return render_template('home.html', books=books, message=message)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'GET':
        return render_template('add_author.html')
    elif request.method == 'POST':
        try:
            name = request.form['name']
            birth_date = datetime.strptime(request.form['birthdate'], "%Y-%m-%d")
            date_of_death = request.form['date_of_death'] or None
            if date_of_death:
                date_of_death = datetime.strptime(request.form['date_of_death'], "%Y-%m-%d")
            new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
            print(new_author)
            db.session.add(new_author)
            db.session.commit()

            # Retrieve the updated list of authors
            authors = Author.query.all()

            return render_template('add_author.html', author=new_author, authors=authors)
        except Exception as e:
            print(e)
            return "Exception"


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'GET':
        authors = Author.query.all()
        return render_template('add_book.html', authors=authors)

    elif request.method == 'POST':
        try:
            isbn = request.form['isbn']
            title = request.form['title']
            publication_year = int(request.form['publication_year'])
            author_id = -1 if request.form['author_id'] == "new" else int(request.form['author_id'])
            new_author_name = request.form['new_author_name']

            # getting the thumbnail from Google
            thumbnail = get_book_cover(title)

            if author_id == -1:
                # Check if the author already exists
                existing_author = Author.query.filter_by(name=new_author_name).first()
                if existing_author:
                    author_id = existing_author.id
                else:
                    # Create a new author and associate the book with it
                    new_author = Author(name=new_author_name)
                    db.session.add(new_author)
                    db.session.commit()
                    author_id = new_author.author_id  # Use the newly created author's ID

            new_book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id, thumbnail=thumbnail)
            print(new_book)
            db.session.add(new_book)
            db.session.commit()

            books = Book.query.options(joinedload(Book.author)).all()

            return render_template('home.html', books=books)
        except Exception as e:
            return f"An error occurred: {str(e)}"

@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    
    if not query:
        return redirect(url_for('home'))

    # Use the LIKE operator to perform a case-insensitive search
    books = Book.query.options(joinedload(Book.author)).filter(
        Book.title.ilike(f"%{query}%")
    ).all()

    if not books:
        return render_template('home.html', message=f"No books found for the query: {query}")

    return render_template('home.html', books=books)

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    # Find the book in the database
    book = Book.query.get(book_id)

    if not book:
        return redirect(url_for('home'))

    # Check if the author has any other books
    author = Author.query.get(book.author_id)
    other_books = Book.query.filter_by(author_id=author.author_id).all()

    # If there's only one book by the author, delete the author too
    if len(other_books) == 1:
        db.session.delete(author)

    # Delete the book
    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('home', message="Book deleted successfully!"))


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
