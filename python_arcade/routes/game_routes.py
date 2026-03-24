from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from db.mongo import users, quiz_questions
import random
from bson.objectid import ObjectId





game_bp = Blueprint("game", __name__)


@game_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@game_bp.route("/number_guess")
@login_required
def number_guess():
    return render_template("number_guess.html")

@game_bp.route("/check_guess", methods=["POST"])
@login_required
def check_guess():
    data = request.json
    guess = int(data.get("guess"))

    # Initialize game if not started
    if "target" not in session:
        session["target"] = random.randint(1, 100)
        session["attempts"] = 0

    session["attempts"] += 1

    target = session["target"]
    attempts = session["attempts"]

    if guess < target:
        return jsonify({
            "result": "low",
            "attempts": attempts
        })

    elif guess > target:
        return jsonify({
            "result": "high",
            "attempts": attempts
        })

    else:
        # 🎉 WIN
        attempts = session["attempts"]

        # 🔥 SAVE BEST SCORE IN DB
        user = users.find_one({"_id": ObjectId(current_user.id)})

        best = user.get("best_guess_score")

        if best is None or attempts < best:
            users.update_one(
                {"_id": ObjectId(current_user.id)},
                {"$set": {"best_guess_score": attempts}}
            )

        # Reset session
        session.pop("target")
        session.pop("attempts")

        return jsonify({
            "result": "correct",
            "attempts": attempts
        })
    
@game_bp.route("/reset_guess")
@login_required
def reset_guess():
    session.pop("target", None)
    session.pop("attempts", None)
    return redirect(url_for("game.number_guess"))

@game_bp.route("/reset_quiz", methods=["POST"])  # ✅ CHANGE HERE
@login_required
def reset_quiz():

    user_id = current_user.id

    # 🔥 ensure correct ObjectId
    if not isinstance(user_id, ObjectId):
        user_id = ObjectId(user_id)

    result = users.update_one(
        {"_id": user_id},
        {"$set": {
            "quiz_completed": [],
            "quiz_score": 0
        }}
    )

    print("RESET CALLED:", result.modified_count)

    return redirect(url_for("game.quiz_page"))


@game_bp.route("/quiz-page")
@login_required
def quiz_page():
    return render_template("quiz.html")

@game_bp.route("/quiz-completed")
@login_required
def quiz_completed():
    return render_template("quiz_complete.html")

@game_bp.route("/tic_tac_toe")
@login_required
def tic_tac_toe():
    return render_template("tic_tac_toe.html")