from flask import Flask
from config import Config
from database import db
from routes.auth import auth_bp
from routes.habit import habit_bp
from routes.pages import pages_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(habit_bp)
    app.register_blueprint(pages_bp)

    return app

app = create_app()
if __name__ == "__main__":
    app.run()
