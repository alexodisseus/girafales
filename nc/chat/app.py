from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Contest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///concurso.db'
db = SQLAlchemy(app)
engine = create_engine('sqlite:///concurso.db')
Session = sessionmaker(bind=engine)


@app.route('/')
def index():
    contests = Contest.query.all()
    return render_template('index.html', contests=contests)


@app.route('/create_contest', methods=['GET', 'POST'])
def create_contest():
    if request.method == 'POST':
        name = request.form['name']
        types = request.form['types']
        contest = Contest(name=name, types=types)
        db.session.add(contest)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_contest.html')


@app.route('/edit_contest/<int:id>', methods=['GET', 'POST'])
def edit_contest(id):
    contest = Contest.query.get_or_404(id)
    if request.method == 'POST':
        contest.name = request.form['name']
        contest.types = request.form['types']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_contest.html', contest=contest)


@app.route('/view_contest/<int:id>')
def view_contest(id):
    contest = Contest.query.get_or_404(id)
    return render_template('view_contest.html', contest=contest)


if __name__ == '__main__':
    app.run(debug=True)
