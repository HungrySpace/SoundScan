from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class OldRec(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # nullable=False - нельзя создавать пустое значение
    result = db.Column(db.String(30))
    comment = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<OldRec %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        comment = request.form['comment']
        result = 'Null'

        # записываем в бд значения
        article = OldRec(comment=comment, result=result)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "Fail"
    else:
        return render_template("index.html")


@app.route('/project')
def project():
    return render_template("project.html")


# @app.route('/history')
# def history():
#     return render_template("history.html")

@app.route('/history')
def history():
    recdb = HistoryComment.query.order_by(HistoryComment.date).all()
    return render_template("history.html", recdb=recdb)


if __name__ == "__main__":
    app.run(debug=True)
