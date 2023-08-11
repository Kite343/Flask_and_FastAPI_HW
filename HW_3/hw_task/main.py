# Flask-SQLAlchemy

from flask import Flask, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect

from models import db, User
from forms import RegisterForm, LoginForm

# для хэширования пароля
import hashlib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# инициализация БД
db.init_app(app)

app.config['SECRET_KEY'] = b'ea959bc6bbd140100d66503aa6ac1242c6eb0e8d4c38b85c7ea9a9d2a8e60451'
# получение csrf - объекта для работы с формами
csrf = CSRFProtect(app)



@app.route('/')
def index():
    return 'Hi!'


@app.cli.command("init-db")
def init_db():
    # создать все таблицы
    db.create_all()
    # print('OK')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        # password = form.password.data
        password = hashlib.sha256(form.password.data.encode('utf-8')).hexdigest()

        # получить user из БД по email
        # existing_user = User.query.filter((User.first_name == first_name) | (User.last_name == last_name) | (User.email == email)).first()
        existing_user = User.query.filter(User.email == email).first()

        # если user существует
        if existing_user:
            error_msg = 'email already exists.'
            form.email.errors.append(error_msg)
            return render_template('register.html', form=form)

        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        # return 'Registered success!'
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = hashlib.sha256(form.password.data.encode('utf-8')).hexdigest()

        existing_user = User.query.filter(User.email == email).first()

        if existing_user and existing_user.password == password:
            return 'Добро пожаловать на сайт!'

        error_msg = 'invalid email or password.'
        form.email.errors.append(error_msg)
        return render_template('login.html', form=form)
                
    return render_template('login.html', form=form)    



if __name__ == '__main__':
    app.run(debug=True)

