# BBSUL Student Portal - Quick Start Guide

## System Overview

A complete web-based student data collection system with:
- Student credential generation (dummy login/password)
- One-time form submission per student
- Admin dashboard with full data view
- Excel export with column-perfect formatting
- Delete individual submissions
- Flush all data (clear everything)

## Quick Start

```bash
# Install dependencies (already done)
pip install -r requirements.txt

# Run the application
python app.py
```

Access at: http://127.0.0.1:5000

## Admin Access

**Login:** http://127.0.0.1:5000/admin/login
- Email: `rishabh@bbsul.edu.pk`
- Password: `abc1234`

**Admin Features:**
- View all student submissions in expandable table rows
- Delete individual submissions (red Delete button)
- Flush ALL data (clears all submissions and resets Excel)
- Download complete Excel file

## Student Workflow

### Step 1: Create Student Account

Go to home page → "I am a Student" → "Create New Student Account"
- Enter student's full name
- System generates:
  - **Username:** `name@bbsul.edu.pk` (email format)
  - **Password:** Random 8-char token (displayed on screen)

**Write these down** - they are shown only once!

### Step 2: Student Logs In

Student goes to: home page → "I am a Student" → "Student Login"
- Enter their email and password

### Step 3: Fill the Form

24 fields across 4 sections:
1. **Personal Info** (name, father, gender, roll no, DOB, admission date, nationality, CNIC, passport, phone, email)
2. **Domicile & Address** (district, province, address, city)
3. **SSC Details** (degree, board, total & obtained marks)
4. **HSSC Details** (degree, nomenclature*, board, total & obtained marks)

Fields with `*` are required.

**Auto-formatting:** CNIC field auto-formats as `XXXXX-XXXXXXX-X`

Submit → Success message

### Step 4: Restriction

If student tries to login again → "Already Submitted" page. One submission per student enforced.

## Data Management

### Delete Individual Submission (Admin)

1. Login as admin
2. In submissions table, click "View" to expand row
3. Click red "Delete" button → Confirmed

### Flush All Data (Admin)

1. Click red "Flush All Data" button in top navbar
2. Confirm → All submissions deleted, Excel reset to headers only

**Note:** Student accounts remain after deletion. Students can re-submit if their submission record is deleted.

### What Gets Deleted

| Action | Submissions | Student Accounts | Excel Output |
|--------|-------------|------------------|--------------|
| Delete One | Only that row | Kept | Updated |
| Flush All | All rows | Kept | Reset to headers |
| Manual DB delete | Depends | Depends | Depends |

### Reset Everything (Complete Fresh Start)

Stop server and run:

```bash
# Delete database and output
del students.db
del data\submissions.xlsx

# Restart server - fresh state
python app.py
```

## File Structure

```
BBSUL STUDENT DATA/
├── app.py                     # Main application (381 lines)
├── requirements.txt           # Dependencies
├── README.md                 # Full documentation
├── data/
│   ├── Template Current Students (1).xlsx   # Input template
│   └── submissions.xlsx                     # Output (auto-created)
├── templates/
│   ├── index.html              # Landing page
│   ├── student_login.html      # Student auth
│   ├── register.html           # Generate credentials
│   ├── form.html               # Student form (24 fields)
│   ├── already_submitted.html  # One-time restriction
│   ├── admin_login.html        # Admin auth
│   └── admin_dashboard.html    # Admin view + controls
└── students.db                 # SQLite database (auto-created)
```

## Excel Column Mapping

Form fields map exactly to these 24 columns:

| # | Excel Column | Form Field |
|---|--------------|------------|
| 1 | Student Name | student_name (required) |
| 2 | FatherName | father_name |
| 3 | Gender | gender (M/F/Other) |
| 4 | RollNo | roll_no |
| 5 | Admission Date | admission_date |
| 6 | Nationality | nationality |
| 7 | CNIC Number | cnic_number (auto-format) |
| 8 | Passport Number | passport_number |
| 9 | Date of Birth | date_of_birth |
| 10 | PhoneNumber | phone_number |
| 11 | Email | email |
| 12 | Domicile District | domicile_district |
| 13 | Domicile Province | domicile_province |
| 14 | Mailing Address | mailing_address |
| 15 | City (Mailing Address) | city |
| 16 | SSC Degree Name | ssc_degree_name |
| 17 | SSC Board Name | ssc_board_name |
| 18 | SSC Total Marks | ssc_total_marks |
| 19 | SSC Obtained Marks | ssc_obtained_marks |
| 20 | HSSC Degree Name | hssc_degree_name |
| 21 | HSSC Degree Nomenclature | hssc_degree_nomenclature (required) |
| 22 | HSSC Board Name | hssc_board_name |
| 23 | HSSC Total Marks | hssc_total_marks |
| 24 | HSSC Obtained Marks | hssc_obtained_marks |

Each submission appends exactly one row to `data/submissions.xlsx`.

## Security

- **Passwords:** Hashed with werkzeug (bcrypt-style)
- **CSRF Protection:** All POST forms validated
- **Session-based auth:** Flask sessions, secure cookies
- **One-time submission:** Enforced at database level (one Submission per Student)
- **Admin-only delete:** Routes protected with @login_required

## Routes Summary

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Landing page |
| `/student/register` | GET, POST | Generate student credentials |
| `/student/login` | GET, POST | Student authentication |
| `/student/form` | GET, POST | Fillable form |
| `/student/logout` | GET | End student session |
| `/admin/login` | GET, POST | Admin authentication |
| `/admin/dashboard` | GET | View all submissions |
| `/admin/download-excel` | GET | Export Excel |
| `/admin/delete-submission/<id>` | POST | Delete single row |
| `/admin/flush-all` | POST | Clear all submissions |
| `/admin/logout` | GET | End admin session |

## Troubleshooting

**"Already Submitted" but need to edit?**
- Admin can delete the submission from dashboard → student can re-submit

**Need to clear all data?**
- Admin: Use "Flush All Data" button
- Or delete `students.db` + `data/submissions.xlsx` and restart

**Excel not downloading?**
- Check that `data/submissions.xlsx` exists (created on first submission)
- If missing, submit at least one form first

**Port 5000 in use?**
Edit `app.py` line 355: `app.run(debug=True, port=5000)` → change port

**Template errors?**
- Ensure `templates/` folder contains all 7 HTML files
- Check Flask logs for specific error

**Database locked?**
- Ensure no other process is using `students.db`
- Delete it and restart to reset

## Next Steps

1. Test with sample student registration
2. Verify Excel output matches template columns
3. Test admin delete and flush functions
4. Deploy to production server (use gunicorn/uWSGI + nginx)
5. Add email notifications (optional)
6. Add form validation patterns (CNIC, phone regex)

---

**Ready to use.** Start server and navigate to http://127.0.0.1:5000
