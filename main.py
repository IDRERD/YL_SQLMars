import flask
from data import db_session
from data.users import User
from data.news import News
from flask import render_template, url_for, redirect, request
from forms.user import RegisterForm

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    captain = User()
    captain.surname = "Scott"
    captain.name = "Ridley"
    captain.age = 21
    captain.position = "captain"
    captain.speciality = "research engineer"
    captain.address = "module_1"
    captain.email = "scott_chief@mars.org"
    dbs = db_session.create_session()
    dbs.add(captain)
    dbs.commit()
    c1 = User()
    c1.surname = "Watney"
    c1.name = "Mark"
    c1.age = 25
    c1.email = "mwatney_99@mars.org"
    c1.address = "module_2"
    c1.speciality = "mechanical engineer"
    c2 = User()
    c2.surname = "Sanders"
    c2.name = "Teddy"
    c2.age = 32
    c3 = User()
    c3.surname = "Weir"
    c3.name = "Andy"
    c3.age = 23
    c3.speciality = "astrogeologist"
    dbs.add(c1)
    dbs.add(c2)
    dbs.add(c3)
    dbs.commit()
    app.run()


@app.route("/")
@app.route("/index")
def index():
    pass
    # db_sess = db_session.create_session()
    # news = db_sess.query(News).filter(News.is_private != True)
    # return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)



if __name__ == "__main__":
    main()