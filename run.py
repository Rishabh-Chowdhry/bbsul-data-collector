#!/usr/bin/env python
"""
Production entry point for BBSUL Student Portal.
Use: gunicorn -w 4 -b 0.0.0.0:5000 run:app
"""
from app import app, init_db

# Initialize database on startup
init_db()
