# BBSUL Student Portal - Quick Start

## Development (Local)

```bash
# 1. Install Python 3.11+
python --version

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Open http://127.0.0.1:5000

**Admin:** rishabh@bbsul.edu.pk / abc1234

---

## Production Deployment (Choose One)

### Option A: Docker (Easiest - 5 minutes)

```bash
# Windows
.\deploy.ps1

# Linux/Mac
./deploy.sh
```

That's it. App runs at http://localhost:5000

---

### Option B: Railway.app (Cloud - Free Tier)

1. Push code to GitHub
2. Go to https://railway.app → New Project → Deploy from GitHub
3. Add environment variable:
   - Key: `SECRET_KEY`
   - Value: `(generate with: python -c "import secrets; print(secrets.token_hex(32))")`
4. Deploy

---

### Option C: Render.com (Cloud - Free Tier)

1. Create Web Service → Connect GitHub
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `gunicorn -w 4 -b 0.0.0.0:5000 run:app`
4. Add Env Var: `SECRET_KEY=your-random-key-here`
5. Deploy

---

### Option D: VPS/Manual (Ubuntu)

```bash
# 1. Install Python
sudo apt update && sudo apt install python3 python3-pip python3-venv -y

# 2. Clone & setup
git clone <your-repo>
cd BBSUL-STUDENT-DATA
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Set secret key
export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
export FLASK_ENV=production

# 4. Initialize DB
python3 -c "from app import init_db; init_db()"

# 5. Test
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# 6. Systemd service (auto-start on boot)
sudo nano /etc/systemd/system/bbsul.service
# Paste content from DEPLOYMENT.md
sudo systemctl enable bbsul
sudo systemctl start bbsul
```

---

## File Structure After Deployment

```
/app
├── app.py              # Main Flask app
├── run.py              # Production entry point
├── config.py           # Environment configs
├── requirements.txt    # Dependencies
├── docker-compose.yml  # Docker stack
├── Dockerfile          # Container build
├── Procfile            # Heroku/Railway
├── data/               # Excel files (persistent volume)
│   ├── Template Current Students (1).xlsx
│   └── submissions.xlsx
├── students.db         # SQLite database
└── templates/          # HTML templates
```

---

## What Each File Does

| File | Purpose |
|------|---------|
| `app.py` | All routes, models, Excel logic |
| `run.py` | Production startup (imports app, calls init_db) |
| `config.py` | Development/production config classes |
| `Dockerfile` | Container image definition |
| `docker-compose.yml` | Orchestrates services (web, optional nginx, db) |
| `deploy.sh` / `deploy.ps1` | One-click deployment scripts |
| `Procfile` | Heroku/Railway process declaration |
| `.dockerignore` | Files to exclude from image |
| `.env.example` | Environment variables template |

---

## Verify Deployment

1. **Check container health:**
   ```bash
   docker-compose ps
   # web container should say "healthy"
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f web
   ```

3. **Test endpoint:**
   ```bash
   curl http://localhost:5000/
   # Should return HTML
   ```

4. **Admin panel:**
   - Visit http://localhost:5000/admin/login
   - Login with admin credentials

---

## Common Issues

**"Address already in use":**
- Port 5000 occupied
- Change in docker-compose.yml: `"8080:5000"` → use http://localhost:8080

**"Database is locked":**
- SQLite doesn't handle concurrent writes well in multi-worker setup
- Switch to PostgreSQL (see DEPLOYMENT.md section 4)

**"ModuleNotFoundError":**
- Ensure you ran `pip install -r requirements.txt` inside container/venv
- For Docker: `docker-compose exec web pip install -r requirements.txt`

**"SECRET_KEY not set":**
- In production, must set SECRET_KEY env var
- For Docker: edit `.env` file
- For manual: `export SECRET_KEY=xxx`

---

## Next Steps After Deployment

1. **Change admin password** (edit in DB or add admin panel feature)
2. **Set up backup** for `data/submissions.xlsx` and `students.db`
3. **Enable HTTPS** (add nginx + Let's Encrypt in docker-compose)
4. **Monitor logs** with log rotation
5. **Set up email** (optional - add `MAIL_*` config)
6. **Add custom domain** (point DNS to server)

---

**Total deployment time:** ~5 minutes with Docker

**Questions?** Check DEPLOYMENT.md for detailed instructions on SSL, PostgreSQL, scaling, and systemd services.
