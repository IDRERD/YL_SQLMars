import datetime

import flask
from data import db_session
from data.users import User
from data.news import News
from data.mars_explorer.jobs import Jobs
from flask import render_template, url_for, redirect, request
from forms.user import RegisterForm

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
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


@app.route("/jobs")
def jobs():
    dbs = db_session.create_session()
    jbs = dbs.query(Jobs).all()
    cls = dbs.query(User).all()
    return render_template("jobs.html", title="Works log", jobs=jbs, colonists=cls)


if __name__ == "__main__":
    main()