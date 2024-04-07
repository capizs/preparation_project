from flask import *
from flask_restful import Api

from data import db_session

app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"


def main():
    db_session.global_inits("db/tasks.db")

    app.run()


@app.route("/")
def index():
    return render_template("index.html", headline="Главная")


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
        user = User(name=form.name.data, email=form.email.data, about=form.about.data)
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


@app.route("/profile/<int:user_id>")
def profile(user_id):

    db_sess = db_session.create_session()
    # answers = (
    #     db_sess.query(User)
    #     .filter(User.)
    #     .all()
    # )
    # wrong_answers = (
    #     db_sess.query(User)
    #     .filter(User.)
    #     .all()
    # )

    # return render_template(
    #     "profile.html",
    #     user=load_user(user_id),
    #     answers=answers,
    #     wrong_answers=wrong_answers,
    # )


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
