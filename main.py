import base64
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Float, BLOB, Text, Column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Movies_project_database.db"
db.init_app(app)


class Movies(db.Model):
    id = Column (Integer,
                 primary_key=True,
                 autoincrement=True)
    title = Column (Text (250),
                    nullable=True)
    year = Column (Integer,
                   nullable=True)
    description = Column (Text (250),
                          nullable=True)
    rating = Column (Float,
                     nullable=True)
    ranking = Column (Integer,
                      nullable=True)
    review = Column (Text (350),
                     nullable=True)
    image_url = Column (BLOB,
                        nullable=True)

## Creating database only
# def create_database():
#    with app.app_context():
#       db.create_all()
# create_database()

@app.route("/")
def home():
    try:
        # Read All Records
        with app.app_context():
            Read = Movies.query.all()
        return render_template("index.html", all_data=Read, base64=base64, len=len)
    except:
        return render_template("Waiting.html")



@app.route("/add",  methods=["GET", "POST"])
def add():
    try:
        if request.method == "POST":
            with app.app_context():
                title = request.form["title"]
                year = request.form["year"]
                rating = request.form["rating"]
                ranking = request.form["ranking"]
                review = request.form["review"]
                description = request.form["description"]
                image = request.form["image"]
                with open(file=fr"C:\Users\Downloads\{image}",
                           mode="rb") as binary:
                    binary_image = binary.read()
                Write = Movies(title=title,
                year=year, description=description,rating=rating,ranking=ranking, review=review,image_url=binary_image)
                db.session.add(Write)
                db.session.commit()
                return redirect(url_for("home"))

    except:
        error = "Please review all fields as some may not have the correct format."
        return render_template ("add.html", error=error)

    else:
        return render_template("add.html")



@app.route("/edit/<int:id>", methods=["GET", "POST"])
def update(id):
        try:
            if request.method == "POST":
                update_rating = request.form["rating"]
                update_review = request.form["review"]
                with app.app_context():
                    user_id = id
                    update_details = db.session.get(Movies,  user_id)
                    update_details.rating = update_rating
                    update_details.review = update_review
                    db.session.commit()
                    return redirect(url_for("home"))
        except:
            error = "Please enter valid values. The Rating must be a number and the Review doesn't matter"
            movie = Movies.query.filter_by (id=id).first ()
            return render_template("edit.html", data=movie, error=error)

        else:
            with app.app_context():
                movie = Movies.query.filter_by(id=id).first()
            return render_template("edit.html",
                                        data=movie)


@app.route("/delete")
def delete():
    try:
        id = request.args.get("id")
        with app.app_context():
            movie_id = id
            movie_to_delete = db.session.get(Movies, movie_id)
            db.session.delete(movie_to_delete)
            db.session.commit()
            return redirect(url_for("home"))
    except:
        pass

if __name__ == '__main__':
    app.run(debug=True)
