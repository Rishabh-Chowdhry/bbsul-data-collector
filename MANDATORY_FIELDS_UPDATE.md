# Mandatory Fields Update - All 24 Form Fields Required

## Change Summary

**Date:** May 7, 2026
**Change:** All 24 fields in student information form are now MANDATORY

## What Changed

### 1. Database (app.py - Submission model)
All columns changed from `nullable=True` to `nullable=False`:
- father_name, gender, roll_no, admission_date
- nationality, cnic_number, passport_number, date_of_birth
- phone_number, email, domicile_district, domicile_province
- mailing_address, city
- ssc_degree_name, ssc_board_name, ssc_total_marks, ssc_obtained_marks
- hssc_degree_name, hssc_board_name, hssc_total_marks, hssc_obtained_marks

Previously only `student_name`, `gender` and `hssc_degree_nomenclature` were required.

### 2. Form Validation (app.py - student_form route)
Changed from checking 2 required fields to checking ALL 24 fields:
```python
# Before
required_fields = ['student_name', 'hssc_degree_nomenclature']

# After
all_fields = [all 24 field names...]
missing = [f for f in all_fields if not request.form.get(f, '').strip()]
```

### 3. Form Template (templates/form.html)
Added `required` attribute and red asterisk `*` to every input/select/textarea:
- `<input ... required>` on every field
- `<label> ... <span class="text-red-500">*</span></label>` on every label

### 4. Migration Script (migrate.py & app.py)
- `migrate_submission_table()` now creates table with all NOT NULL constraints
- Existing NULL values are converted to empty strings `''` during migration
- Duplicate submissions still removed (keeps first entry)

## Database Migration

**Automatic on next startup:** The `init_db()` function detects schema changes and runs migration automatically.

**Manual migration (if needed):**
```bash
python migrate.py
```

The migration will:
1. Backup all existing submission data
2. Recreate table with all NOT NULL constraints
3. Replace NULL values with empty strings
4. Keep first submission per student only
5. Swap tables

## Impact on Existing Data

- Existing rows with NULL values: NULLs replaced with empty strings `''`
- No data loss (empty strings instead of NULL)
- All future submissions must have all fields filled

## User-Facing Changes

**Students will now see:**
- Red asterisk (*) next to every field label
- HTML5 validation prevents submission if any field empty
- Clear error message: "All fields are required. Missing: field1, field2, ..."
- Passport field placeholder changed from "(if applicable)" to "Enter number or N/A"

**Admin dashboard:**
- No change (still displays all data)
- Empty fields will show as empty (not N/A since we now have empty strings)

## Testing Checklist

- [ ] Try submitting with 1 empty field → should fail
- [ ] Try submitting with 2 empty fields → shows both in error
- [ ] Submit with all 24 fields filled → succeeds
- [ ] Verify database row has no NULL values (check via sqlite3)
- [ ] Verify Excel row contains all values (no blanks unless intentionally left empty string)

## Notes

- The CNIC field still auto-formats as you type
- The unique student_id constraint remains enforced
- One submission per student rule unchanged
- All existing functionality preserved

## Rollback

To revert to optional fields (not recommended):
1. Restore from backup of `students.db` before migration
2. Revert code to previous commit (before mandatory fields change)

---

** migration is automatic.** Just restart the app:
```bash
python app.py
```

The app will output:
```
Migrating database: enforcing unique constraint and NOT NULL on all fields...
Migration complete: X submissions migrated.
All fields now mandatory (NOT NULL).
```
