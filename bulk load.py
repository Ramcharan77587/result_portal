import csv
from app import app, db, Student

def bulk_insert(csv_file):
    with app.app_context():
        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)

            count = 0

            for row in reader:
                userid = row['userid'].strip()
                dob = row['dob'].strip()

                existing = Student.query.filter_by(userid=userid).first()
                if not existing:
                    student = Student(userid=userid, dob=dob)
                    db.session.add(student)
                    count += 1

            db.session.commit()
            print(f"{count} students inserted successfully.")

if __name__ == "__main__":
    bulk_insert("students.csv")
