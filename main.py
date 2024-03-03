import datetime
from data.login import LoginForm
from data.news_form import NewsForm
import flask
from data import db_session
from data.users import User
from data.jobs import Jobs
#from data.news import News
from flask import render_template, url_for, redirect, request, make_response, abort, session
from forms.user import RegisterForm
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from data.job_form import JobForm

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/mars.db")
    # app.register_blueprint(news_api.blueprint)
    app.run()


@app.route("/")
@app.route("/index")
def index():
    dbs = db_session.create_session()
    jobs = dbs.query(Jobs).all()
    team_leaders = [dbs.query(User).get(job.team_leader) for job in jobs]
    if not jobs or not len(jobs):
        return "Jobs not found"
    #if current_user.is_authenticated:
    #    news = db_sess.query(News).filter(
    #        (News.user == current_user) | (News.is_private != True))
    #else:
    #    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", jobs=jobs, team_leaders=team_leaders)


@app.route('/register', methods=['GET', 'POST'])
def register():
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
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
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


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(f"You have visited the site {visits_count + 1} times")
        res.set_cookie("visits_count", str(visits_count + 1), max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response("You visited this site first time in last 2 years")
        res.set_cookie("visits_count", "1", max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@login_manager.user_loader
def load_user(user_id):
    dbs = db_session.create_session()
    return dbs.query(User).get(user_id)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        dbs = db_session.create_session()
        user = dbs.query(User).filter(User.email.is_(form.email.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect("/")
        else:
            return render_template("login.html", message="Login or email is not valid", form=form)
    return render_template("login.html", title="Authorization", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route("/add_job", methods=["POST", "GET"])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        dbs = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        # job.start_date = form.start_date.data
        # job.end_date = form.end_date.data
        dbs.add(job)
        dbs.commit()
        return redirect("/")
    return render_template("add_job.html", title="Добавление работы", form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(flask.jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(flask.jsonify({"error": "Bad request"}), 400)


if __name__ == "__main__":
    main()