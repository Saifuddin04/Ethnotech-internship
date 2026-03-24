from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models.user_model import User

from routes.auth_routes import auth_bp
from routes.game_routes import game_bp
from routes.leaderboard_routes import leaderboard_bp

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


app.register_blueprint(auth_bp)
app.register_blueprint(game_bp)
app.register_blueprint(leaderboard_bp)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

print(Config.MONGO_URI)