from flask import Blueprint, render_template
from db.mongo import users

leaderboard_bp = Blueprint("leaderboard", __name__)


@leaderboard_bp.route("/leaderboard")
def leaderboard():

    top_players = users.find().sort("wins", -1).limit(10)

    return render_template(
        "leaderboard.html",
        players=top_players
    )