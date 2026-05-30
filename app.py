from flask import Flask, render_template, request
from types_data import TYPES, QUESTIONS, MONTH_FLAVOR
from collections import Counter

app = Flask(__name__)


def determine_type(answers, birth_month):
    counts = Counter(answers)
    # 最多得票タイプを取得
    top = counts.most_common()

    if not top:
        return "ハーフ", birth_month

    # 同点が複数ある場合 → ハーフ判定
    if len(top) >= 2 and top[0][1] == top[1][1]:
        result_type = "ハーフ"
    else:
        result_type = top[0][0]

    return result_type, birth_month


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", questions=QUESTIONS)


@app.route("/result", methods=["POST"])
def result():
    try:
        birth_month = int(request.form.get("birth_month", 1))
    except ValueError:
        birth_month = 1

    answers = [request.form.get(q["id"]) for q in QUESTIONS]
    answers = [a for a in answers if a]

    result_type, month = determine_type(answers, birth_month)
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
