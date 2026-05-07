# BBSUL Student Portal - Modern Fillable Form System

A modern, modular web application for collecting student information with Excel export capabilities.

## Features

- **Modern UI**: Built with Tailwind CSS for a responsive, beautiful interface
- **Modular Architecture**: Separated concerns with Python Flask backend, SQLite database, Excel handler, and Jinja2 templates
- **Student Registration**: Generate dummy credentials (email/password) for each student
- **One-time Submission**: Each student can submit the form only once
- **Admin Dashboard**: View all submissions, expandable detail rows, Excel download
- **Excel Integration**: Data saved to columns in Excel template format
- **Authentication**: Secure admin login, student session management

## Project Structure

```
BBSUL STUDENT DATA/
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── data/
│   ├── Template Current Students (1).xlsx  # Excel template (input)
│   └── submissions.xlsx                   # Output with all data
├── templates/                # HTML Jinja2 templates
│   ├── index.html           # Landing page
│   ├── student_login.html   # Student login
│   ├── register.html        # Generate student credentials
│   ├── form.html            # Student fillable form
│   ├── already_submitted.html
│   ├── admin_login.html     # Admin auth
│   └── admin_dashboard.html # Admin view & download
└── students.db              # SQLite database (created on first run)
```

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Place Excel template:**
   - The template `Template Current Students (1).xlsx` should be in the `data/` folder
   - It will be automatically loaded and used as a base

3. **Run the application:**
   ```bash
   python app.py
   ```
   The app runs at http://127.0.0.1:5000

## Usage

### Admin Access

- **URL:** http://127.0.0.1:5000/admin/login
- **Email:** rishabh@bbsul.edu.pk
- **Password:** abc1234

Admin can:
- View all student submissions in a dashboard
- Expand each row to see full details
- Download the complete Excel file with all data

### Student Flow

**Step 1: Generate Student Credentials**

- Go to main page → "I am a Student" → "Create New Student Account"
- Enter student's full name
- System generates:
  - Username: `name@bbsul.edu.pk` format
  - Password: Random 8-character token
- Write down credentials for the student

**Step 2: Student Login**

- Go to main page → "I am a Student" → "Student Login"
- Enter email and password

**Step 3: Fill the Form**

- Complete the 24-field form organized in 4 sections
- Required fields marked with asterisks (*)
- CNIC auto-formatted as XXXXX-XXXXXXX-X
- Submit → success message

**Step 4: One-time Restriction**

- If student tries to login again, they see "Already Submitted" page
- System prevents duplicate submissions

## Form Fields

The form maps exactly to the 24 Excel columns:

| Section | Fields |
|---------|--------|
| Personal Info | Student Name, Father Name, Gender, Roll No, DOB, Admission Date, Nationality, CNIC, Passport, Phone, Email |
| Domicile & Address | District, Province, Mailing Address, City |
| SSC Details | Degree Name, Board, Total Marks, Obtained Marks |
| HSSC Details | Degree Name, Nomenclature (required), Board, Total Marks, Obtained Marks |

## Excel Output

- Output file: `data/submissions.xlsx`
- Uses the template structure with all columns
- Each submission appends a new row
- Compatible with the original template format
- Downloadable from admin dashboard

## Admin Credentials

Default admin account:
- Email: rishabh@bbsul.edu.pk
- Password: abc1234

**Note:** On first login, admin password is hashed and stored in the database.

## Database Schema

Using SQLite (students.db):

- **Student**: id, username (unique), password_hash, full_name, created_at
- **Submission**: id, student_id (FK), submitted_at, all 24 form fields
- **Admin**: id, email (unique), password_hash

## Technical Stack

- **Backend**: Python Flask 3.0 with Flask-Login
- **Database**: SQLAlchemy ORM (SQLite)
- **Excel**: openpyxl
- **Frontend**: HTML5 + Tailwind CSS (CDN)
- **Templates**: Jinja2

## Key Routes

| Route | Purpose | Access |
|-------|---------|--------|
| `/` | Landing page | Public |
| `/student/register` | Generate credentials | Public |
| `/student/login` | Student login | Students only |
| `/student/form` | Fillable form | Students only |
| `/admin/login` | Admin auth | Admin only |
| `/admin/dashboard` | View submissions | Admin only |
| `/admin/download-excel` | Export Excel | Admin only |

## Safety Features

- **One-time form**: Students cannot submit twice
- **Password hashing**: All passwords stored securely with werkzeug
- **Session management**: Flask sessions for student and admin
- **Input validation**: Required fields, email format
- **CSRF protection**: Flask-WTF not used but sessions validated

## Customization

- **Change admin credentials**: Edit `app.py` → admin login check (line ~195)
- **Update Excel columns**: Modify `ExcelHandler.EXCEL_COLUMNS` list
- **Styling**: Tailwind CDN - can be customized in templates
- **Form fields**: Edit `form.html` and Submission model in `app.py`

## Troubleshooting

**Port already in use:**
```bash
# Flask defaults to port 5000. Change by editing app.run(port=xxxx) in app.py
```

**Excel template not found:**
- Ensure `data/Template Current Students (1).xlsx` exists
- If not, provide own template with correct column headers

**Database errors:**
- Delete `students.db` and restart app to reset
- Or use `flask shell` to query manually

**Missing submissions.xlsx:**
- Created automatically on first submission
- Or create empty file with headers

## License

For BBSUL internal use.
