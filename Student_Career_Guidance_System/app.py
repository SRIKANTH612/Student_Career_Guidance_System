from flask import Flask, render_template, request, redirect, url_for, session
from ml_model import CareerModel, COURSES
from google_ai import generate_ai_insights
from resume_parser import parse_resume
from db import init_db, get_db
from collections import Counter

app = Flask(__name__)
app.secret_key = "secret"

init_db()
model = CareerModel()
model.train_model("data/training_data.csv")

@app.route("/")
def root():
    return redirect(url_for("index") if "user_id" in session else url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        c = get_db()
        u = c.execute("SELECT * FROM users WHERE username=? AND password=?",
                      (request.form["username"],request.form["password"])).fetchone()
        c.close()
        if u:
            session["user_id"] = u[0]
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/index", methods=["GET","POST"])
def index():
    if "user_id" not in session: return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        skills = request.form.get("skills","")
        if "resume" in request.files and request.files["resume"].filename:
            skills += "," + ",".join(parse_resume(request.files["resume"]))
        preds = model.predict_career(skills)
        best = preds[0][0]
        student = [s.strip().lower() for s in skills.split(",") if s.strip()]
        miss = list(set(model.career_skills[best]) - set(student))
        ready = int((len(student)/len(model.career_skills[best]))*100)
        ai = generate_ai_insights(best, miss)
        c = get_db()
        c.execute("INSERT INTO students (user_id,name,career,readiness,missing_skills) VALUES (?,?,?,?,?)",
                  (session["user_id"],name,best,ready,",".join(miss)))
        c.commit(); c.close()
        return render_template("result.html", name=name, predictions=preds[:3],
                               missing_skills=miss, readiness=ready, ai_text=ai,
                               courses={m:COURSES.get(m,[]) for m in miss})
    return render_template("index.html")

@app.route("/admin/login", methods=["GET","POST"])
def admin_login():
    if request.method=="POST" and request.form["username"]=="admin" and request.form["password"]=="admin123":
        session["admin"]=True; return redirect(url_for("admin"))
    return render_template("admin_login.html")

@app.route("/admin")
def admin():
    if not session.get("admin"): return redirect(url_for("admin_login"))
    c = get_db()
    rows = c.execute("SELECT career FROM students").fetchall()
    c.close()
    counts = Counter(r[0] for r in rows)
    return render_template("admin.html", career_counts=counts)

@app.errorhandler(404)
def nf(e): return render_template("404.html"),404

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
