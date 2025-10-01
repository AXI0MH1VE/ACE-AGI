# AxiomHive 4D ACE Deployment Guide

## 🚀 Sovereign Core Cycle 20 - axiomhive.co

**Deployment Date:** 2025-09-20
**Status:** Ready for cPanel deployment
**Target:** GoDaddy shared hosting
**System:** 4D ACE (Updated from Grok)

## 📋 Overview

This deployment transforms the empty axiomhive.co placeholder into a live 4D ACE assistant with:
- Flask-based web application
- 4D causal graph processing
- Neural-symbolic decomposition
- Proactive fact integration
- Real-time coherence calculation

## 🏗️ Architecture

### Core Components
- **axiomhive_ace_flask.py** - Main Flask application
- **python/agents/causal_agent.py** - 4D causal graph builder
- **src/orchestrator.py** - Cognitive orchestrator for decomposition
- **passenger_wsgi_ace.py** - cPanel WSGI entry point

### Key Endpoints
- `GET /` - Home page with system status
- `POST /ace-4d` - Main 4D ACE processing endpoint
- `GET/POST /facts` - Facts management
- `GET /health` - System health check

## 📦 Deployment Steps (cPanel - ~15 minutes)

### Step 1: Access cPanel
1. Go to [godaddy.com](https://godaddy.com)
2. Navigate to **Hosting** → **Manage** → **cPanel**
3. Log in with your credentials

### Step 2: Upload Files
1. In cPanel, go to **Files** → **File Manager**
2. Navigate to `/public_html/`
3. Click **Upload** and upload the following files:
   - `axiomhive_ace_flask.py`
   - `passenger_wsgi_ace.py`
   - `requirements.txt`
   - `python/agents/causal_agent.py`
   - `src/orchestrator.py`

### Step 3: Setup Python Application
1. In cPanel, go to **Software** → **Setup Python App**
2. Click **Create Application**
3. Configure:
   - **Python Version:** 3.12 (or latest available)
   - **Application Root:** `/public_html`
   - **Application URL:** `axiomhive.co`
   - **Application Startup File:** `passenger_wsgi_ace.py`
   - **Environment Variables:**
     - `FLASK_ENV=production`
     - `SECRET_KEY=your-secret-key-here`

### Step 4: Install Dependencies
1. In the Python App interface, click **Run Pip Install**
2. Enter: `pip install -r requirements.txt`
3. Wait for installation to complete (~5-10 minutes)

### Step 5: Configure WSGI
1. Edit `passenger_wsgi_ace.py` and update the `INTERP` path:
   ```python
   INTERP = "/home/<your-username>/virtualenv/python/bin/python"
   ```
2. Replace `<your-username>` with your actual cPanel username

### Step 6: Restart Application
1. In Python App interface, click **Restart**
2. Wait for restart to complete

### Step 7: Test Deployment
Test the endpoints:

```bash
# Health check
curl https://axiomhive.co/health

# Main 4D ACE endpoint
curl -X POST https://axiomhive.co/ace-4d \
  -H "Content-Type: application/json" \
  -d '{"command": "plan SF move and gym membership"}'

# Facts integration
curl -X POST https://axiomhive.co/facts \
  -H "Content-Type: application/json" \
  -d '{"new_fact": "Research SF fitness centers"}'
```

## 🔧 Configuration

### Environment Variables
Set these in cPanel Python App settings:
```env
FLASK_ENV=production
SECRET_KEY=axiomhive-ace-4d-nexus-2025
PORT=5000
DEBUG=False
```

### Memory Optimization
For shared hosting, monitor memory usage:
- Start with minimal dependencies
- Comment out heavy packages in `requirements.txt` if needed
- Use CPU fallback for ML models

## 📊 Monitoring

### Health Check
Visit `https://axiomhive.co/health` for system status

### Logs
Check cPanel error logs at:
- `/home/<username>/logs/error_log`
- `/home/<username>/logs/access_log`

### Performance Metrics
- Response time: < 1 second for /ace-4d
- Coherence score: > 0.95
- Memory usage: < 512MB (shared hosting limit)

## 🚀 Upgrade Path (VPS - Full Features)

### When to Upgrade
- Memory usage consistently > 400MB
- Need for Docker containers
- Require Rust binary performance
- Want Qdrant vector database

### VPS Upgrade Steps
1. In cPanel: **Hosting** → **Upgrade** → **VPS**
2. Choose plan (~$5/month)
3. SSH into new VPS
4. Deploy full stack:

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone and deploy
git clone <repository-url>
cd axiomhive-ace
docker-compose up -d

# Install Rust components
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo build --release

# Configure Nginx
sudo apt install nginx
sudo cp nginx.conf /etc/nginx/sites-available/axiomhive.co
sudo ln -s ../sites-available/axiomhive.co /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## 🛠️ Troubleshooting

### Common Issues

**500 Internal Server Error:**
- Check Python app logs in cPanel
- Verify all dependencies installed
- Check file permissions (755 for Python files)

**Module Not Found Errors:**
- Reinstall requirements: `pip install -r requirements.txt --force-reinstall`
- Check Python path in passenger_wsgi_ace.py

**Memory Limits:**
- Reduce model sizes in orchestrator
- Use lighter alternatives for ML packages
- Consider VPS upgrade

**Permission Denied:**
- Set file permissions: `chmod 755 *.py`
- Check cPanel file ownership

### Debug Mode
Temporarily enable debug:
```python
application.config['DEBUG'] = True
```

## 📈 Performance Optimization

### Shared Hosting Optimizations
- Use in-memory storage for graphs
- Cache frequent queries
- Optimize ML model loading
- Use async processing where possible

### Monitoring Commands
```bash
# Check memory usage
ps aux | grep python

# Check disk usage
du -sh *

# Monitor logs
tail -f /home/<username>/logs/error_log
```

## 🔒 Security

- Use HTTPS (configure in cPanel)
- Set strong SECRET_KEY
- Validate all inputs
- Rate limiting on API endpoints
- Regular dependency updates

## 📞 Support

For deployment issues:
1. Check cPanel error logs
2. Verify all steps completed
3. Test with minimal configuration first
4. Contact GoDaddy support for hosting issues

---

**Deployment Status:** ✅ Ready
**Last Updated:** 2025-09-20
**Version:** Sovereign Core Cycle 20
**System:** 4D ACE
**Attribution:** @AxiomHive @devdollzai
