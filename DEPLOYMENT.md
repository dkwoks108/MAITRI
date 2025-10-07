# MAITRI Deployment Guide

## Overview

This guide covers deploying MAITRI - AI Assistant for Astronauts to production environments.

## Architecture

- **Frontend**: Static HTML/CSS/JS served via Vercel, Netlify, or GitHub Pages
- **Backend**: FastAPI server on Render, Railway, or Google Cloud Run
- **Storage**: Google Drive API for session logs and alerts

## Frontend Deployment

### Option 1: Vercel (Recommended)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
vercel --prod
```

3. Configure API URL:
   - Set environment variable `API_URL` to your backend URL

### Option 2: Netlify

1. Create `netlify.toml`:
```toml
[build]
  publish = "."
  
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

2. Deploy via Netlify CLI or drag-and-drop in dashboard

### Option 3: GitHub Pages

1. Push code to GitHub repository
2. Go to Settings > Pages
3. Select branch and root directory
4. Access at `https://username.github.io/repository-name/`

## Backend Deployment

### Option 1: Render (Recommended)

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: maitri-backend
    env: python
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "cd backend && python main.py"
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
```

2. Connect GitHub repo to Render
3. Deploy automatically on push

### Option 2: Railway

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Deploy:
```bash
railway login
railway init
railway up
```

### Option 3: Google Cloud Run

1. Create `Dockerfile` in backend/:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

2. Build and deploy:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/maitri
gcloud run deploy --image gcr.io/PROJECT_ID/maitri --platform managed
```

## Google Drive Configuration

### Setup Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project "MAITRI"
3. Enable Google Drive API
4. Create Service Account:
   - Name: "maitri-storage"
   - Role: "Editor"
5. Create key (JSON format)
6. Download as `credentials.json`

### Configure Storage

1. Upload `credentials.json` to backend deployment:
   - **Render**: Add as secret file
   - **Railway**: Add via environment variables
   - **Cloud Run**: Mount as secret

2. Create Google Drive folder "MAITRI_Data"
3. Share folder with service account email

## Environment Variables

Set these in your deployment platform:

### Backend
```
HOST=0.0.0.0
PORT=8000
GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json
USE_GPU=false
LOG_LEVEL=INFO
```

### Frontend
```
API_URL=https://your-backend.onrender.com
```

## SSL/HTTPS

### Backend
- Render/Railway: Automatic HTTPS
- Custom domain: Add SSL certificate via platform

### Frontend
- Vercel/Netlify: Automatic HTTPS
- GitHub Pages: Automatic HTTPS

## Monitoring

### Health Checks

Backend includes health check endpoint:
```
GET https://your-backend.onrender.com/
```

### Logging

- Backend logs to stdout
- Configure platform-specific logging
- Use log aggregation (e.g., Logtail, Papertrail)

### Alerts

- Set up uptime monitoring (e.g., UptimeRobot)
- Configure email/SMS alerts for downtime

## Performance Optimization

### Frontend
- Enable CDN for static assets
- Compress images
- Minify CSS/JS (optional)

### Backend
- Use gunicorn with multiple workers:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```
- Enable response caching
- Use model caching

## Security

### API Security
- Enable CORS with specific origins
- Add API rate limiting
- Implement authentication (optional)

### Data Security
- Encrypt sensitive data
- Use HTTPS only
- Secure Google credentials

## Scaling

### Backend
- Increase worker count
- Use horizontal scaling
- Add load balancer

### Storage
- Monitor Google Drive quota
- Implement data cleanup/archival
- Consider database for metadata

## Backup

### Session Data
- Regular exports from Google Drive
- Local backup script
- Cloud storage backup

### Configuration
- Version control for configs
- Document all env variables
- Maintain deployment checklist

## Troubleshooting

### Common Issues

**Backend won't start:**
- Check Python version (3.10+)
- Verify all dependencies installed
- Check logs for errors

**Model download fails:**
- Ensure sufficient disk space
- Check internet connectivity
- Use model cache

**Google Drive not working:**
- Verify credentials.json exists
- Check service account permissions
- Ensure API enabled

**CORS errors:**
- Update allowed origins in backend
- Verify API URL in frontend
- Check HTTPS/HTTP mismatch

## Testing Deployment

1. Test health endpoint:
```bash
curl https://your-backend.onrender.com/
```

2. Test analyze endpoint:
```bash
curl -X POST https://your-backend.onrender.com/analyze \
  -F "frame=@test_image.jpg" \
  -F "voice=@test_audio.webm"
```

3. Test frontend:
- Open in browser
- Start detection
- Send chat message
- Verify emotion tracking

## Cost Estimation

### Free Tier
- Frontend (Vercel/Netlify): Free
- Backend (Render): 750 hours/month free
- Google Drive: 15GB free
- Total: $0/month

### Paid Tier
- Frontend: $20-50/month
- Backend: $7-25/month
- Storage: Free or $2-10/month
- Total: ~$30-85/month

## Support

For deployment issues:
1. Check logs
2. Review documentation
3. Open GitHub issue
4. Contact support

## Updates

To update deployment:
1. Push to main branch (auto-deploy)
2. Or manually trigger deployment
3. Monitor for errors
4. Test critical functionality

## Rollback

If deployment fails:
1. Identify issue in logs
2. Revert to previous version
3. Fix issue locally
4. Redeploy

---

Last updated: 2024
