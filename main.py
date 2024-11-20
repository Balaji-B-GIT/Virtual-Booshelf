from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    title:Mapped[str] = mapped_column(String(250), nullable=False,unique=True)
    author:Mapped[str] = mapped_column(String(250),nullable=False)
    rating:Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f'<{self.id}>'

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    # Read all DB Data
    all_books = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
    return render_template("index.html", books = all_books)


@app.route("/add", methods=["POST","GET"])
def add():
    if request.method == "POST":
        data = request.form
        title = data["name"]
        author = data["author"]
        rating = data["rating"]

        # Add record
        new_book = Book(title = title,author = author, rating = rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["POST","GET"])
def edit(id):
    book_selected = Book.query.get(id)
    if request.method == "POST":
        book_selected.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html",book = book_selected)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    # DELETE A RECORD BY ID
    book_to_delete = Book.query.get(book_id)
    # Alternative way to select the book to delete.
    # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

