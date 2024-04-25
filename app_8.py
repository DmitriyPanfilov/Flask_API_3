# Создать форму для регистрации пользователей на сайте.
# Форма должна содержать поля "Имя", "Фамилия", "Email",
# "Пароль" и кнопку "Зарегистрироваться".
# При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.
import secrets
from flask import Flask, render_template, request, redirect
from models_08 import db, Users
from flask_wtf.csrf import CSRFProtect
from forms_08 import RegistrationForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///regdatabase.db'
app.config['SECRET_KEY'] = secrets.token_hex()
db.init_app(app)
csrf = CSRFProtect(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/register/', methods=['GET', 'POST'])
def reg_user():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')

        new_user = Users(firstname=firstname, lastname=lastname, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return f'<h1>Попльзователь {new_user.firstname} удачно зарегистрирован</h1>'
    return render_template('register_08.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)