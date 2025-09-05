from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Meme.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Meme(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        desc = request.form['desc']
        meme = Meme(title=title, desc=desc)
        db.session.add(meme)
        db.session.commit()

    allmeme = Meme.query.all()
    return render_template("index.html", allmeme=allmeme)

@app.route("/products")
def products():
    return "<p>This is a product page!</p>"

@app.route("/show")
def show():
    allmeme = Meme.query.all()
    print(allmeme)
    return "<p>This is a payment page!</p>"

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc = request.form['desc']
        meme = Meme.query.filter_by(sno=sno).first()
        meme.title = title
        meme.desc = desc
        db.session.add(meme)
        db.session.commit()
        return redirect("/")

    meme = Meme.query.filter_by(sno=sno).first()
    return render_template("update.html", meme=meme)

@app.route("/delete/<int:sno>")
def delete(sno):
    meme = Meme.query.filter_by(sno=sno).first()
    db.session.delete(meme)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # creates Meme.db if not exists
        print("Database created successfully!")
app.run(debug=True, port=8000)
