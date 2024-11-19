from enum import UNIQUE

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

app.config['SQLALCHEMY-DATABASE-URL'] = "sqlite:///books-collection.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)
all_books = []

class Book(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    title:Mapped[str] = mapped_column(String(250), nullable=False,unique=True)
    author:Mapped[str] = mapped_column(String(250),nullable=False)
    rating:Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()


@app.route('/', methods=["POST","GET"])
def home():
    if request.method == "POST":
        data = request.form
        dicti = {
            'title':data["name"],
            'author':data["author"],
            'rating':data["rating"],
        }
        all_books.append(dicti)
    return render_template("index.html",books = all_books)


@app.route("/add")
def add():
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)

