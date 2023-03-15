from flask import Flask, render_template, redirect, url_for, flash, send_file
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TEMPLATES_FOLDER'] = 'templates'
app.config['SECRET_KEY'] = "top_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class Addform(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    adress = StringField(label="Adress", validators=[DataRequired()])
    rating = SelectField(label="Rating", choices=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"])
    wifi = SelectField(label="Wifi", choices=["None", "📶", "📶📶", "📶📶📶", "📶📶📶📶", "📶📶📶📶📶"])
    plugs = StringField(label="Number of plugs", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

class Caffes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    adress = db.Column(db.String, unique=True, nullable=False)
    rating = db.Column(db.String)
    wifi = db.Column(db.String)
    plugs = db.Column(db.String)

# with app.app_context():
#     db.create_all()
#     db.session.commit()

@app.route("/")
def home():
    all_caffes = db.session.query(Caffes).all()
    return render_template("index.html", all_caffes=all_caffes)

@app.route("/add", methods=["POST", "GET"])
def add():
    form = Addform()
    if form.validate_on_submit():
        new_caffe = Caffes(name=form.name.data, adress=form.adress.data, rating=form.rating.data,
                           wifi=form.wifi.data, plugs=form.plugs.data)

        if Caffes.query.filter_by(name=form.name.data).first():
            flash("Caffe with this name already exists.")
        elif Caffes.query.filter_by(name=form.adress.data).first():
            flash("Caffe with this adress already exists.")
        else:
            db.session.add(new_caffe)
            db.session.commit()
            flash("Caffe successfully added!")
            return redirect(url_for("home"))
    return render_template("add.html", form=form)

if (__name__) == "__main__":
    app.run(debug=True)