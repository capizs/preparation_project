from flask import *
from flask_restful import Api

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from forms.user import RegisterForm, LoginForm

from data.users import User
from data.tasks import Tasks
from data.answers import Answer
from forms.tasks import AnswerForm

from data import db_session

from random import randint, shuffle

app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/tasks.db")
    app.run()


@app.route("/")
def index():
    return render_template("index.html", title="Главная")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            "login.html", message="Неправильный логин или пароль", form=form
        )
    return render_template("login.html", title="Авторизация", form=form)


@app.route("/register", methods=["GET", "POST"])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=True)
        return redirect("/")
    return render_template("register.html", title="Регистрация", form=form)


@app.route("/logout")
def logout():
    logout_user()

    return redirect("/")


@app.route("/profile/id=<int:user_id>")
def profile(user_id):
    db_sess = db_session.create_session()
    user_info = db_sess.query(Answer).filter(Answer.user_id == user_id).all()
    wrong_answers = sorted([x.task_id for x in user_info])

    return render_template(
        "profile.html",
        user=load_user(user_id),
        wrong_answers=wrong_answers,
        title="Профиль",
    )


@app.route("/tasks/id=<int:task_id>", methods=["GET", "POST"])
def tasks(task_id):
    db_sess = db_session.create_session()
    task = db_sess.query(Tasks).get(task_id)
    db_sess = db_session.create_session()
    user_info = db_sess.query(Answer).filter(Answer.user_id == current_user.id).all()
    answers = sorted([x.task_id for x in user_info])

    form = AnswerForm()
    if form.validate_on_submit():
        answer = form.answer.data

        if answer == task.answers:
            answer = 1
            if task.id in answers:
                db_sess = db_session.create_session()
                db_sess.query(Answer).filter(Answer.task_id == task.id).delete()
                db_sess.commit()
        else:
            if task.id not in answers:
                db_sess = db_session.create_session()
                ans = Answer(user_id=current_user.id, task_id=task.id)
                db_sess.add(ans)
                db_sess.commit()

        return render_template("tasks.html", task=task, answer=answer, title="Ответ")

    return render_template("tasks.html", task=task, form=form, answer=0, title="Задачa")


@app.errorhandler(404)
def not_found(error):
    return """
        <h1>
        Ошибка 404<br>
        Уупс, а такой страницы нет (っ◔◡◔)っ
        </h1>
        <a href="/">
            Перейти на главную
        </a>
    """


if __name__ == "__main__":
    main()
