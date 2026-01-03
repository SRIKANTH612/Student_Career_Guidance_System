from flask import Flask, render_template, request, redirect, url_for, session
from ml_model import CareerModel, COURSES
from resume_parser import parse_resume
from google_ai import generate_ai_insights
from db import init_db, get_db
from collections import Counter

app = Flask(__name__)
app.secret_key = "career_secret_key"

init_db()

model = CareerModel()
model.train_model("data/training_data.csv")


@app.route("/")
def root():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (request.form["username"], request.form["password"])
        ).fetchone()
        conn.close()
        if user:
            session["user_id"] = user[0]
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/index", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        skills = request.form.get("skills", "")

        if "resume" in request.files and request.files["resume"].filename:
            extracted = parse_resume(request.files["resume"])
            skills += "," + ",".join(extracted)

        predictions = model.predict_career(skills)
        best_career = predictions[0][0]

        student_skills = [s.strip().lower() for s in skills.split(",") if s]
        required = model.career_skills[best_career]
        missing = list(set(required) - set(student_skills))
        readiness = int((len(student_skills) / len(required)) * 100)

        ai_text = generate_ai_insights(best_career, missing)

        courses = {s: COURSES.get(s, []) for s in missing}

        conn = get_db()
        conn.execute(
            "INSERT INTO students (user_id, name, career, readiness, missing_skills) VALUES (?,?,?,?,?)",
            (session["user_id"], name, best_career, readiness, ",".join(missing))
        )
        conn.commit()
        conn.close()

        return render_template(
            "result.html",
            name=name,
            predictions=predictions[:3],
            missing_skills=missing,
            readiness=readiness,
            ai_text=ai_text,
            courses=courses
        )

    return render_template("index.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect(url_for("admin"))
    return render_template("admin_login.html")


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = get_db()
    rows = conn.execute("SELECT career FROM students").fetchall()
    conn.close()

    career_counts = Counter(r[0] for r in rows)
    return render_template("admin.html", career_counts=career_counts)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
