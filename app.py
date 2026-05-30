import random
from flask import Flask, render_template, request, session
from types_data import TYPES, QUESTION_POOL, MONTH_FLAVOR
from collections import Counter

app = Flask(__name__)
app.secret_key = "umbrella-parade-uranai-secret"


def pick_questions():
    selected = random.sample(QUESTION_POOL, min(3, len(QUESTION_POOL)))
    for i, q in enumerate(selected):
        q = dict(q)
        q["id"] = f"q{i+1}"
        selected[i] = q
    return selected


def determine_type(answers):
    counts = Counter(answers)
    top = counts.most_common()

    if not top:
        return "ハーフ"
    if len(top) >= 2 and top[0][1] == top[1][1]:
        return "ハーフ"
    return top[0][0]


@app.route("/", methods=["GET"])
def index():
    questions = pick_questions()
    session["questions"] = questions
    return render_template("index.html", questions=questions)


@app.route("/result", methods=["POST"])
def result():
    questions = session.get("questions", pick_questions())

    try:
        birth_month = int(request.form.get("birth_month", 1))
    except ValueError:
        birth_month = 1

    answers = [request.form.get(q["id"]) for q in questions]
    answers = [a for a in answers if a]

    result_type = determine_type(answers)
    type_data = TYPES[result_type]
    flavor = MONTH_FLAVOR.get(birth_month, "")

    return render_template(
        "result.html",
        type_name=result_type,
        type_data=type_data,
        flavor=flavor,
    )


if __name__ == "__main__":
    app.run(debug=True)
