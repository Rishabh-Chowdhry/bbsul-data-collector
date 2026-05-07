# BBSUL Student Portal - Deployment Guide

## Quick Deploy (Docker)

### 1. Prerequisites
- Docker Desktop installed (Windows/Mac) or Docker Engine (Linux)
- At least 2GB free RAM
- Port 5000 available

### 2. One-Command Deployment

```bash
# On Windows PowerShell:
.\deploy.ps1

# On Linux/Mac:
chmod +x deploy.sh
./deploy.sh
```

This will:
1. Check Docker installation
2. Create `.env` file from `.env.example`
3. Build the Docker image
4. Start the container
5. Show access details

### 3. Access the Application

**URL:** http://localhost:5000

**Admin Login:**
- Email: `rishabh@bbsul.edu.pk`
- Password: `abc1234`

**Student Flow:**
1. Home → "Create New Student Account"
2. Enter student name → get credentials
3. Student logs in with those credentials
4. Fill form → submit (once only)

### 4. Production Considerations

#### Change the Secret Key
Edit `.env` file:
```env
SECRET_KEY=your-very-long-random-string-here-minimum-32-chars
```

Generate a strong key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### Use PostgreSQL (Recommended for Production)

Update `.env`:
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

Update `docker-compose.yml` to add PostgreSQL service:
```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: bbsul_students
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  web:
    build: .
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@db:5432/bbsul_students
```

### 5. Deploy to Cloud Platforms

#### Railway.app (Easiest - Free Tier)

1. Push code to GitHub
2. Go to https://railway.app
3. Create new project → Deploy from GitHub repo
4. Set environment variables:
   - `SECRET_KEY` (required)
   - `FLASK_ENV=production`
   - `DATABASE_URL` (Railway provides PostgreSQL)
5. Deploy

#### Render.com (Free Tier)

1. Create new Web Service
2. Connect GitHub repo
3. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -b 0.0.0.0:5000 run:app`
4. Add environment variables (SECRET_KEY)
5. Deploy

#### PythonAnywhere (Free Tier)

1. Upload files via Files → Upload
2. Open Bash console
3. Create virtualenv: `mkvirtualenv --python=/usr/bin/python3.11 bbsul`
4. Install: `pip install -r requirements.txt`
5. Configure web app in dashboard
6. Set WSGI file to import `run:app` (need to create `run.py`)
7. Reload web app

### 6. With SSL/HTTPS (Production)

Use Nginx reverse proxy with Let's Encrypt:

Create `nginx.conf`:
```nginx
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    upstream flask_app {
        server web:5000;
    }

    server {
        listen 80;
        server_name yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        location / {
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

Uncomment nginx service in `docker-compose.yml` and mount SSL certs.

### 7. Backup Strategy

#### Automated Backup Script

Create `backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR=./backups
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T web python -c "
from app import app, db
import shutil, datetime
shutil.copy('data/submissions.xlsx', f'/backups/submissions_$DATE.xlsx')
" 2>/dev/null || echo 'Manual backup required'
```

Add to crontab:
```bash
0 2 * * * /path/to/backup.sh
```

### 8. Monitoring

#### Health Check
The Docker image includes a health check that pings `/`. View status:
```bash
docker-compose ps
```

#### Logs
```bash
# Real-time logs
docker-compose logs -f web

# Last 100 lines
docker-compose logs --tail=100 web
```

#### Database Size
```bash
docker-compose exec web ls -lh students.db
```

### 9. Scaling

To handle more traffic, increase Gunicorn workers in `Dockerfile`:
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "8", "--timeout", "120", "run:app"]
```

Rule of thumb: `(2 x CPU_cores) + 1`

### 10. Troubleshooting

**Port already in use:**
```bash
# Change port in docker-compose.yml from "5000:5000" to "8080:5000"
# Then access via http://localhost:8080
```

**Database locked:**
```bash
docker-compose down
docker-compose up -d
```

**Container keeps restarting:**
```bash
docker-compose logs web
# Check for SECRET_KEY error
```

**Permission denied on data folder:**
```bash
# On host, ensure proper permissions
chmod -R 755 ./data
```

### 11. Update Application

1. Pull latest code
2. Rebuild and restart:
```bash
docker-compose pull  # if using remote image
docker-compose build
docker-compose up -d
```

### 12. Security Checklist

- [ ] Change default admin password (via admin panel → future feature)
- [ ] Set strong SECRET_KEY in .env (min 32 chars)
- [ ] Use HTTPS (add nginx + SSL)
- [ ] Enable firewall (only 80/443 open)
- [ ] Use PostgreSQL instead of SQLite for concurrent access
- [ ] Set up regular backups
- [ ] Monitor logs for suspicious activity
- [ ] Keep Docker images updated

## Alternative: Manual Deployment (No Docker)

If you prefer not to use Docker:

```bash
# On your server
git clone <your-repo>
cd BBSUL-STUDENT-DATA

# Install Python 3.11+
python3 --version

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
export FLASK_ENV=production

# Initialize database
python3 -c "from app import app, init_db; init_db()"

# Start production server
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Or use systemd service (Linux)
# Create /etc/systemd/system/bbsul.service
```

### systemd Service File

```ini
[Unit]
Description=BBSUL Student Portal
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/bbsul
Environment="SECRET_KEY=your-secret-key"
ExecStart=/usr/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable bbsul
sudo systemctl start bbsul
sudo systemctl status bbsul
```

---

**Need help?** Check the logs first:
```bash
docker-compose logs web | tail -50
```
