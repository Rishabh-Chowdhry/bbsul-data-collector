from app import app, db
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    columns = inspector.get_columns('submission')
    print("Submission table columns:")
    for c in columns:
        print(f"  {c['name']}: nullable={c['nullable']}, type={c['type']}")
