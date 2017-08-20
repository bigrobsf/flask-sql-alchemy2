from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/flask-sql-alchemy2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

modus = Modus(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text, unique=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)

    def __init__(self, user_name, first_name, last_name, email):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return "Student {} {}'s user name is {}".format(self.first_name, self.last_name,
                                                        self.user_name)

@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route('/users', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        db.session.add(User(user_name, first_name, last_name, email))
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('index.html', users=User.query.order_by(User.user_name).all())


@app.route('/users/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def show(id):
    if id in [user.id for user in User.query.all()]:
        found_user = User.query.get(id)
        if request.method == b'PATCH':
            found_user.user_name = request.form.get('user_name')
            found_user.first_name = request.form.get('first_name')
            found_user.last_name = request.form.get('last_name')
            found_user.email = request.form.get('email')

            db.session.add(found_user)
            db.session.commit()
            return redirect(url_for('index'))

        if request.method == b'DELETE':
            db.session.delete(found_user)
            db.session.commit()

            return redirect(url_for('index'))

        return render_template('show.html', user=found_user)
    else:
        return render_template('404.html')


@app.route('/users/<int:id>/edit')
def edit(id):
    if id in [user.id for user in User.query.all()]:
        found_user = User.query.get(id)
        return render_template('edit.html', user=found_user)
    else:
        return render_template('404.html')


@app.route('/users/new')
def new():
    return render_template('new.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')



if __name__ == '__main__':
    app.run(port=3001, debug=True)