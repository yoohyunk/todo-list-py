from flask import Flask
from routes.todolist import todo_bp

app = Flask(__name__)

app.register_blueprint(todo_bp, url_prefix="/")


if __name__ == '__main__':
    app.run(debug=True)
