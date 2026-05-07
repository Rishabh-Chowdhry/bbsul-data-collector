"""
Migration script to add unique constraint on student_id in submissions table.
Run this once if you have existing data and want to enforce single submission per student.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Submission, Student
from sqlalchemy import text

def migrate():
    with app.app_context():
        # Check if unique constraint already exists
        inspector = db.inspect(db.engine)
        constraints = inspector.get_unique_constraints('submission')
        has_unique = any(c['name'] for c in constraints if 'student_id' in str(c['column_names']))

        if has_unique:
            print("Unique constraint already exists on submission.student_id")
            return

        # SQLite: need to recreate table with constraint
        print("Adding unique constraint to submission.student_id...")

        # Get all existing submissions
        submissions = Submission.query.all()

        # Create a temporary table with new schema
        db.engine.execute(text("""
            CREATE TABLE submission_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL UNIQUE,
                submitted_at DATETIME,
                student_name VARCHAR(200) NOT NULL,
                father_name VARCHAR(200),
                gender VARCHAR(20),
                roll_no VARCHAR(50),
                admission_date VARCHAR(50),
                nationality VARCHAR(100),
                cnic_number VARCHAR(50),
                passport_number VARCHAR(50),
                date_of_birth VARCHAR(50),
                phone_number VARCHAR(50),
                email VARCHAR(200),
                domicile_district VARCHAR(200),
                domicile_province VARCHAR(200),
                mailing_address TEXT,
                city VARCHAR(200),
                ssc_degree_name VARCHAR(200),
                ssc_board_name VARCHAR(200),
                ssc_total_marks VARCHAR(50),
                ssc_obtained_marks VARCHAR(50),
                hssc_degree_name VARCHAR(200),
                hssc_degree_nomenclature VARCHAR(50),
                hssc_board_name VARCHAR(200),
                hssc_total_marks VARCHAR(50),
                hssc_obtained_marks VARCHAR(50),
                FOREIGN KEY(student_id) REFERENCES student (id)
            )
        """))

        # Copy data (only first submission per student will succeed)
        duplicate_count = 0
        seen_students = set()

        for sub in submissions:
            if sub.student_id in seen_students:
                duplicate_count += 1
                print(f"  WARNING: Skipping duplicate submission for student_id={sub.student_id}")
                continue
            db.engine.execute(text("""
                INSERT INTO submission_new (
                    id, student_id, submitted_at, student_name, father_name, gender, roll_no,
                    admission_date, nationality, cnic_number, passport_number, date_of_birth,
                    phone_number, email, domicile_district, domicile_province, mailing_address,
                    city, ssc_degree_name, ssc_board_name, ssc_total_marks, ssc_obtained_marks,
                    hssc_degree_name, hssc_degree_nomenclature, hssc_board_name,
                    hssc_total_marks, hssc_obtained_marks
                ) VALUES (:id, :student_id, :submitted_at, :student_name, :father_name, :gender,
                          :roll_no, :admission_date, :nationality, :cnic_number, :passport_number,
                          :date_of_birth, :phone_number, :email, :domicile_district,
                          :domicile_province, :mailing_address, :city, :ssc_degree_name,
                          :ssc_board_name, :ssc_total_marks, :ssc_obtained_marks,
                          :hssc_degree_name, :hssc_degree_nomenclature, :hssc_board_name,
                          :hssc_total_marks, :hssc_obtained_marks)
            """), {
                'id': sub.id,
                'student_id': sub.student_id,
                'submitted_at': sub.submitted_at,
                'student_name': sub.student_name,
                'father_name': sub.father_name,
                'gender': sub.gender,
                'roll_no': sub.roll_no,
                'admission_date': sub.admission_date,
                'nationality': sub.nationality,
                'cnic_number': sub.cnic_number,
                'passport_number': sub.passport_number,
                'date_of_birth': sub.date_of_birth,
                'phone_number': sub.phone_number,
                'email': sub.email,
                'domicile_district': sub.domicile_district,
                'domicile_province': sub.domicile_province,
                'mailing_address': sub.mailing_address,
                'city': sub.city,
                'ssc_degree_name': sub.ssc_degree_name,
                'ssc_board_name': sub.ssc_board_name,
                'ssc_total_marks': sub.ssc_total_marks,
                'ssc_obtained_marks': sub.ssc_obtained_marks,
                'hssc_degree_name': sub.hssc_degree_name,
                'hssc_degree_nomenclature': sub.hssc_degree_nomenclature,
                'hssc_board_name': sub.hssc_board_name,
                'hssc_total_marks': sub.hssc_total_marks,
                'hssc_obtained_marks': sub.hssc_obtained_marks,
            })
            seen_students.add(sub.student_id)

        # Drop old table, rename new
        db.engine.execute(text("DROP TABLE submission"))
        db.engine.execute(text("ALTER TABLE submission_new RENAME TO submission"))

        # Commit the transaction
        db.session.commit()

        print(f"Migration complete. Unique constraint added.")
        if duplicate_count > 0:
            print(f"  {duplicate_count} duplicate submissions were removed.")
            print("  (Only the first submission per student was kept)")

if __name__ == '__main__':
    migrate()
