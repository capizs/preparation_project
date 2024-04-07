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
