import os
import csv
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DATABASE CONFIG FOR RENDER
database_url = os.environ.get("DATABASE_URL")

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ==========================
# DATABASE MODEL
# ==========================

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(50), unique=True, nullable=False)
    dob = db.Column(db.String(20), nullable=False)

# ==========================
# CREATE TABLES
# ==========================

with app.app_context():
    db.create_all()

# ==========================
# ROUTES
# ==========================

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        userid = request.form["userid"]

        student = Student.query.filter_by(userid=userid).first()

        if not student:
            return "User ID not found in database"

        return f"User Found: {student.userid} | DOB: {student.dob}"

    return """
        <h2>NIE Result Portal</h2>
        <form method="POST">
            <input type="text" name="userid" placeholder="Enter User ID" required>
            <button type="submit">Search</button>
        </form>
    """

# ==========================
# BULK UPLOAD ROUTE
# ==========================

@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    file = request.files["file"]

    if not file:
        return "No file uploaded"

    stream = file.stream.read().decode("UTF8").splitlines()
    reader = csv.DictReader(stream)

    count = 0

    for row in reader:
        userid = row["userid"].strip()
        dob = row["dob"].strip()

        existing = Student.query.filter_by(userid=userid).first()

        if not existing:
            student = Student(userid=userid, dob=dob)
            db.session.add(student)
            count += 1

    db.session.commit()

    return f"{count} students inserted successfully."

# ==========================
# VIEW ALL STUDENTS
# ==========================

@app.route("/all_students")
def all_students():
    students = Student.query.all()
    return "<br>".join([s.userid for s in students])

# ==========================
# RUN
# ==========================

if __name__ == "__main__":
    app.run(debug=True)
