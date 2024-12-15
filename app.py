from flask import Flask, render_template, request, redirect, url_for, session
import csv
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret_key"

# Function to load questions from the CSV file
def load_questions():
    questions = []
    with open("question_bank.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append({
                "sno": int(row["sno"]),
                "question": row["question"],
                "mark": int(row["mark"]),
                "answer": row["answer"],
                "type": row["type"],
                "choices": [row["choiceA"], row["choiceB"], row["choiceC"], row["choiceD"]]
            })
    return questions


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        student_id = request.form["student_id"]
        num_simple = int(request.form["num_simple"])
        num_medium = int(request.form["num_medium"])
        num_hard = int(request.form["num_hard"])

        question_bank = load_questions()
        simple_questions = [q for q in question_bank if q["type"] == "simple"]
        medium_questions = [q for q in question_bank if q["type"] == "medium"]
        hard_questions = [q for q in question_bank if q["type"] == "hard"]

        selected_questions = random.sample(simple_questions, min(num_simple, len(simple_questions))) + \
                             random.sample(medium_questions, min(num_medium, len(medium_questions))) + \
                             random.sample(hard_questions, min(num_hard, len(hard_questions)))

        session["questions"] = selected_questions
        session["user"] = {"name": name, "student_id": student_id}

        return redirect(url_for("test"))

    return render_template("index.html")


@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        responses = []
        user = session["user"]
        questions = session["questions"]

        for question in questions:
            response = request.form.get(str(question["sno"]), "")
            responses.append({
                "sno": question["sno"],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "username": user["name"],
                "question": question["question"],
                "answer": question["answer"],
                "response": response
            })

        # Save responses to CSV
        with open("user-responses.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["sno", "date", "username", "question", "answer", "response"])
            if f.tell() == 0:
                writer.writeheader()
            writer.writerows(responses)

        return redirect(url_for("result"))

    questions = session.get("questions", [])
    return render_template("test.html", questions=questions)


@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/quiz_master")
def quiz_master():
    # Load responses from user-responses.csv to create a list of test takers
    test_takers = {}
    with open("user-responses.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["username"], row["date"].split(" ")[0])  # Username and date
            test_takers[key] = {"name": row["username"], "date": row["date"].split(" ")[0]}
    
    return render_template("quiz_master.html", test_takers=test_takers.values())


@app.route("/quiz_master/view/<username>/<date>")
def view_results(username, date):
    # Load responses for the specific user and date
    results = []
    with open("user-responses.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username and row["date"].startswith(date):
                results.append(row)
    
    return render_template("view_results.html", results=results, username=username, date=date)


if __name__ == "__main__":
    app.run(debug=True)
