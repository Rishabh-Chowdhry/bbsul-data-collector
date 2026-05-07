"""
Migration script to enforce:
1. UNIQUE constraint on student_id
2. NOT NULL constraints on all fields (mandatory)

Run this when upgrading from optional-fields to all-mandatory schema.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Submission
from sqlalchemy import text

def safe_str(value):
    """Convert None to empty string for string fields."""
    if value is None:
        return ''
    return str(value)

def migrate():
    with app.app_context():
        print("Starting migration to enforce all fields as mandatory...")

        # Check current schema
        inspector = db.inspect(db.engine)
        try:
            columns = inspector.get_columns('submission')
            nullable_cols = [c['name'] for c in columns if c['nullable'] and c['name'] != 'id']
            if not nullable_cols:
                print("All fields already NOT NULL. Only checking unique constraint...")
        except Exception as e:
            print(f"Table may not exist yet: {e}")
            return

        # Get all existing submissions BEFORE changing schema
        submissions = Submission.query.all()
        print(f"Found {len(submissions)} submissions to migrate")

        # Create new table with full NOT NULL constraints
        db.engine.execute(text("""
            CREATE TABLE submission_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL UNIQUE,
                submitted_at DATETIME,
                student_name VARCHAR(200) NOT NULL,
                father_name VARCHAR(200) NOT NULL,
                gender VARCHAR(20) NOT NULL,
                roll_no VARCHAR(50) NOT NULL,
                admission_date VARCHAR(50) NOT NULL,
                nationality VARCHAR(100) NOT NULL,
                cnic_number VARCHAR(50) NOT NULL,
                passport_number VARCHAR(50) NOT NULL,
                date_of_birth VARCHAR(50) NOT NULL,
                phone_number VARCHAR(50) NOT NULL,
                email VARCHAR(200) NOT NULL,
                domicile_district VARCHAR(200) NOT NULL,
                domicile_province VARCHAR(200) NOT NULL,
                mailing_address TEXT NOT NULL,
                city VARCHAR(200) NOT NULL,
                ssc_degree_name VARCHAR(200) NOT NULL,
                ssc_board_name VARCHAR(200) NOT NULL,
                ssc_total_marks VARCHAR(50) NOT NULL,
                ssc_obtained_marks VARCHAR(50) NOT NULL,
                hssc_degree_name VARCHAR(200) NOT NULL,
                hssc_degree_nomenclature VARCHAR(50) NOT NULL,
                hssc_board_name VARCHAR(200) NOT NULL,
                hssc_total_marks VARCHAR(50) NOT NULL,
                hssc_obtained_marks VARCHAR(50) NOT NULL,
                FOREIGN KEY(student_id) REFERENCES student (id)
            )
        """))

        # Copy data, deduplicate, and fill NULLs with empty strings
        seen = set()
        duplicate_count = 0
        null_fixed = 0

        for sub in submissions:
            if sub.student_id in seen:
                duplicate_count += 1
                print(f"  Duplicate removed: student_id={sub.student_id}")
                continue

            # Prepare data with safe defaults for NULL values
            data = {
                'id': sub.id,
                'student_id': sub.student_id,
                'submitted_at': sub.submitted_at,
                'student_name': safe_str(sub.student_name),
                'father_name': safe_str(sub.father_name),
                'gender': safe_str(sub.gender),
                'roll_no': safe_str(sub.roll_no),
                'admission_date': safe_str(sub.admission_date),
                'nationality': safe_str(sub.nationality),
                'cnic_number': safe_str(sub.cnic_number),
                'passport_number': safe_str(sub.passport_number),
                'date_of_birth': safe_str(sub.date_of_birth),
                'phone_number': safe_str(sub.phone_number),
                'email': safe_str(sub.email),
                'domicile_district': safe_str(sub.domicile_district),
                'domicile_province': safe_str(sub.domicile_province),
                'mailing_address': safe_str(sub.mailing_address),
                'city': safe_str(sub.city),
                'ssc_degree_name': safe_str(sub.ssc_degree_name),
                'ssc_board_name': safe_str(sub.ssc_board_name),
                'ssc_total_marks': safe_str(sub.ssc_total_marks),
                'ssc_obtained_marks': safe_str(sub.ssc_obtained_marks),
                'hssc_degree_name': safe_str(sub.hssc_degree_name),
                'hssc_degree_nomenclature': safe_str(sub.hssc_degree_nomenclature),
                'hssc_board_name': safe_str(sub.hssc_board_name),
                'hssc_total_marks': safe_str(sub.hssc_total_marks),
                'hssc_obtained_marks': safe_str(sub.hssc_obtained_marks),
            }

            # Count NULLs that were fixed
            for key, val in data.items():
                if key not in ['id', 'student_id', 'submitted_at'] and sub.__dict__.get(key) is None:
                    null_fixed += 1

            db.engine.execute(text("""
                INSERT INTO submission_new (
                    id, student_id, submitted_at, student_name, father_name, gender, roll_no,
                    admission_date, nationality, cnic_number, passport_number, date_of_birth,
                    phone_number, email, domicile_district, domicile_province, mailing_address,
                    city, ssc_degree_name, ssc_board_name, ssc_total_marks, ssc_obtained_marks,
                    hssc_degree_name, hssc_degree_nomenclature, hssc_board_name,
                    hssc_total_marks, hssc_obtained_marks
                ) VALUES (
                    :id, :student_id, :submitted_at, :student_name, :father_name, :gender,
                    :roll_no, :admission_date, :nationality, :cnic_number, :passport_number,
                    :date_of_birth, :phone_number, :email, :domicile_district, :domicile_province,
                    :mailing_address, :city, :ssc_degree_name, :ssc_board_name, :ssc_total_marks,
                    :ssc_obtained_marks, :hssc_degree_name, :hssc_degree_nomenclature,
                    :hssc_board_name, :hssc_total_marks, :hssc_obtained_marks
                )
            """), data)
            seen.add(sub.student_id)

        # Swap tables
        db.engine.execute(text("DROP TABLE submission"))
        db.engine.execute(text("ALTER TABLE submission_new RENAME TO submission"))
        db.session.commit()

        print("Migration complete!")
        print(f"  Migrated: {len(seen)} submissions")
        if duplicate_count > 0:
            print(f"  Removed duplicates: {duplicate_count}")
        if null_fixed > 0:
            print(f"  Fixed NULL values: {null_fixed} fields set to empty string")
        print("  All fields are now MANDATORY (NOT NULL).")
        print("  Unique constraint on student_id enforced.")

if __name__ == '__main__':
    migrate()
