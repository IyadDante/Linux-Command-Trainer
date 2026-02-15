from flask import Flask, render_template, request, session
import json
import random
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# -------------------------
# Load Questions
# -------------------------

def load_questions():
    with open("questions.json", "r") as f:
        return json.load(f)

all_questions = load_questions()

# -------------------------
# Load / Save Stats
# -------------------------

def load_stats():
    if not os.path.exists("stats.json"):
        return {}
    try:
        with open("stats.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_stats(stats):
    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=4)

stats = load_stats()

# -------------------------
# Helpers
# -------------------------

def normalize(text):
    return " ".join(text.strip().split())

def adaptive_choice(filtered):
    weighted_pool = []

    for q in filtered:
        key = f"{q['category']}_{q['difficulty']}"
        stat = stats.get(key, {"correct": 0, "wrong": 0})
        attempts = stat["correct"] + stat["wrong"]

        if attempts == 0:
            weight = 3
        else:
            accuracy = stat["correct"] / attempts
            weight = 5 if accuracy < 0.6 else 1

        weighted_pool.extend([q] * weight)

    return random.choice(weighted_pool)

# -------------------------
# Route
# -------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    if "score" not in session:
        session["score"] = 0
        session["total"] = 0

    if "current_question" not in session:
        session["current_question"] = None

    if "selected_category" not in session:
        session["selected_category"] = "All"

    if "selected_difficulty" not in session:
        session["selected_difficulty"] = "All"

    action = request.form.get("action")

    # Update selected filters
    if request.method == "POST":
        session["selected_category"] = request.form.get("category", "All")
        session["selected_difficulty"] = request.form.get("difficulty", "All")

    category = session["selected_category"]
    difficulty = session["selected_difficulty"]

    # Filter questions
    filtered = [
        q for q in all_questions
        if (category == "All" or q["category"] == category)
        and (difficulty == "All" or q["difficulty"] == difficulty)
    ]

    result = None

    # APPLY FILTERS
    if action == "apply":
        if filtered:
            session["current_question"] = adaptive_choice(filtered)
        else:
            session["current_question"] = None

    # CHECK ANSWER
    elif action == "check" and session["current_question"]:
        question = session["current_question"]
        user_answer = normalize(request.form["user_answer"])
        correct_answers = [normalize(a) for a in question["answer"]]

        key = f"{question['category']}_{question['difficulty']}"

        if key not in stats:
            stats[key] = {"correct": 0, "wrong": 0}

        session["total"] += 1

        if user_answer in correct_answers:
            session["score"] += 1
            stats[key]["correct"] += 1
            result = "Correct ✅"
        else:
            stats[key]["wrong"] += 1
            result = f"Wrong ❌ | Correct: {correct_answers[0]}"

        save_stats(stats)

    # NEXT QUESTION
    elif action == "next":
        if filtered:
            session["current_question"] = adaptive_choice(filtered)

    # First load
    if not session["current_question"] and filtered:
        session["current_question"] = adaptive_choice(filtered)

    question = session["current_question"]

    categories = sorted(set(q["category"] for q in all_questions))
    difficulties = sorted(set(q["difficulty"] for q in all_questions))

    return render_template(
        "index.html",
        question=question,
        result=result,
        score=session["score"],
        total=session["total"],
        categories=categories,
        difficulties=difficulties,
        selected_category=category,
        selected_difficulty=difficulty
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
