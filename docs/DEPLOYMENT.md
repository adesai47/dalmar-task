# Deployment Guide

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Git

## Quick Start

### Option 1: Automated Startup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd dalmar-task

# Run the startup script
./start.sh
```

This script will:
- Set up Python virtual environment
- Install backend dependencies
- Start the FastAPI backend
- Install frontend dependencies
- Start the Next.js frontend

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend
python run.py
```

The backend will be available at `http://localhost:8000`

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Environment Configuration

### Backend Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
CHROMA_PERSIST_DIRECTORY=./data/chroma_db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=info
```

### Frontend Environment Variables

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Production Deployment

### Docker Deployment

#### Backend Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "run.py"]
```

#### Frontend Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

#### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/data:/app/data
    environment:
      - CHROMA_PERSIST_DIRECTORY=/app/data/chroma_db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
```

### Cloud Deployment

#### AWS Deployment

1. **EC2 Instance Setup:**
   ```bash
   # Update system
   sudo yum update -y
   
   # Install Python 3.11
   sudo yum install python3.11 python3.11-pip -y
   
   # Install Node.js
   curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
   sudo yum install nodejs -y
   
   # Install PM2 for process management
   sudo npm install -g pm2
   ```

2. **Application Setup:**
   ```bash
   # Clone repository
   git clone <repository-url>
   cd dalmar-task
   
   # Setup backend
   cd backend
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Setup frontend
   cd ../frontend
   npm install
   npm run build
   ```

3. **PM2 Configuration:**
   ```json
   {
     "apps": [
       {
         "name": "rag-backend",
         "script": "python",
         "args": "run.py",
         "cwd": "/path/to/dalmar-task/backend",
         "env": {
           "PYTHONPATH": "/path/to/dalmar-task/backend"
         }
       },
       {
         "name": "rag-frontend",
         "script": "npm",
         "args": "start",
         "cwd": "/path/to/dalmar-task/frontend"
       }
     ]
   }
   ```

#### Heroku Deployment

1. **Backend (Heroku):**
   ```bash
   # Create Procfile
   echo "web: python run.py" > Procfile
   
   # Create requirements.txt (already exists)
   
   # Deploy
   heroku create rag-backend-app
   git subtree push --prefix backend heroku main
   ```

2. **Frontend (Vercel/Netlify):**
   ```bash
   # Build command
   npm run build
   
   # Publish directory
   .next
   
   # Environment variables
   NEXT_PUBLIC_API_URL=https://rag-backend-app.herokuapp.com
   ```

### Load Balancer Configuration

#### Nginx Configuration

```nginx
upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Monitoring and Logging

### Health Checks

```bash
# Backend health check
curl http://localhost:8000/api/health

# Frontend health check
curl http://localhost:3000/api/health
```

### Log Monitoring

```bash
# Backend logs
tail -f backend/logs/app.log

# Frontend logs
tail -f frontend/.next/server.log
```

### Performance Monitoring

- Use tools like New Relic, DataDog, or Prometheus
- Monitor API response times
- Track vector database performance
- Monitor web search fallback usage

## Security Considerations

### Production Security

1. **Environment Variables:**
   - Never commit `.env` files
   - Use secure secret management
   - Rotate API keys regularly

2. **Network Security:**
   - Use HTTPS in production
   - Configure CORS properly
   - Implement rate limiting

3. **Data Security:**
   - Encrypt sensitive data
   - Regular backups
   - Access controls

### SSL/TLS Configuration

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
}
```

## Backup and Recovery

### Database Backup

```bash
# Backup ChromaDB
cp -r backend/data/chroma_db backup/chroma_db_$(date +%Y%m%d)

# Restore ChromaDB
cp -r backup/chroma_db_20240115 backend/data/chroma_db
```

### Application Backup

```bash
# Full application backup
tar -czf rag_backup_$(date +%Y%m%d).tar.gz dalmar-task/

# Restore application
tar -xzf rag_backup_20240115.tar.gz
```

## Troubleshooting

### Common Issues

1. **Port Conflicts:**
   ```bash
   # Check port usage
   lsof -i :8000
   lsof -i :3000
   
   # Kill processes
   kill -9 <PID>
   ```

2. **Python Dependencies:**
   ```bash
   # Reinstall dependencies
   pip install --force-reinstall -r requirements.txt
   ```

3. **Node.js Dependencies:**
   ```bash
   # Clear cache and reinstall
   npm cache clean --force
   rm -rf node_modules
   npm install
   ```

4. **ChromaDB Issues:**
   ```bash
   # Clear database
   rm -rf backend/data/chroma_db
   # Restart backend to recreate
   ```

### Log Analysis

```bash
# Backend error logs
grep "ERROR" backend/logs/app.log

# Frontend build errors
npm run build 2>&1 | tee build.log
```

## Scaling

### Horizontal Scaling

1. **Multiple Backend Instances:**
   - Use load balancer
   - Shared ChromaDB storage
   - Session management

2. **Database Scaling:**
   - ChromaDB clustering
   - Read replicas
   - Caching layer

3. **CDN Integration:**
   - Static asset delivery
   - Global content distribution
   - Reduced latency

