
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("students.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    init_db()

    if request.method == "POST":
        name = request.form["name"]
        department = request.form["department"]

        conn = sqlite3.connect("students.db")
        conn.execute(
            "INSERT INTO students (name, department) VALUES (?, ?)",
            (name, department)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    conn = sqlite3.connect("students.db")
    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()
    conn.close()

    return render_template("index.html", students=students)

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
