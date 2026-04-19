# Apple Stock Price Prediction - Deployment Guide

## Overview
This guide covers deployment options for the Apple Stock Price Prediction application built with Flask backend and React frontend.

## Architecture
- **Backend**: Flask API with LSTM model for stock price prediction
- **Frontend**: React application with Chart.js for data visualization
- **Data**: 40 years of Apple stock data with technical indicators
- **Model**: LSTM neural network trained on historical data

## Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)

## Deployment Options

### 1. Docker Compose (Recommended)

**Quick Start:**
```bash
# Clone the repository
git clone <repository-url>
cd apple-stock-prediction

# Build and start all services
docker-compose up --build
```

**Services:**
- **Backend**: `http://localhost:5000`
- **Frontend**: `http://localhost:3000`
- **Redis**: `localhost:6379` (for caching)

### 2. Manual Deployment

#### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
python simple_app.py
```

#### Frontend Deployment
```bash
cd frontend
npm install
npm run build
# Serve the build directory with nginx or apache
```

### 3. Cloud Deployment

#### AWS Deployment
**Backend (Elastic Beanstalk):**
```bash
# Build Docker image
docker build -t apple-stock-backend ./backend

# Push to ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin
docker tag apple-stock-backend:latest <aws-account-id>.dkr.ecr.us-west-2.amazonaws.com/apple-stock-backend
docker push <aws-account-id>.dkr.ecr.us-west-2.amazonaws.com/apple-stock-backend
```

**Frontend (S3 + CloudFront):**
```bash
cd frontend
npm run build
aws s3 sync build/ s3://your-bucket-name --delete
aws cloudfront create-invalidation --distribution-id <distribution-id> --paths "/*"
```

#### Google Cloud Platform
**Backend (Cloud Run):**
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/apple-stock-backend
gcloud run deploy --image gcr.io/PROJECT-ID/apple-stock-backend --platform managed
```

**Frontend (Firebase Hosting):**
```bash
cd frontend
npm run build
firebase deploy --only hosting
```

#### Vercel (Frontend)
```bash
# Add vercel.json to frontend root
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://your-backend-url.com/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}

# Deploy
vercel --prod
```

## Environment Variables

### Backend
- `FLASK_ENV`: `production` or `development`
- `API_KEY`: Optional API key for rate limiting
- `REDIS_URL`: Redis connection string

### Frontend
- `REACT_APP_API_URL`: Backend API URL
- `REACT_APP_ENV`: `production` or `development`

## Monitoring and Logging

### Application Monitoring
```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Health checks
curl http://localhost:5000/health
curl http://localhost:3000
```

### Model Performance Monitoring
- Track prediction accuracy over time
- Monitor API response times
- Set up alerts for model drift

## Scaling Considerations

### Backend Scaling
- **Horizontal scaling**: Multiple backend instances behind load balancer
- **Model optimization**: Consider TensorFlow Lite for edge deployment
- **Caching**: Redis for frequent predictions

### Frontend Scaling
- **CDN**: CloudFlare or AWS CloudFront
- **Static optimization**: Gzip compression, minification
- **Progressive loading**: Load data in chunks

## Security Considerations

### API Security
- Rate limiting on prediction endpoints
- CORS configuration for frontend domain
- Input validation and sanitization
- HTTPS enforcement in production

### Data Security
- Encrypted data transmission
- Secure API key storage
- Regular dependency updates

## Backup and Recovery

### Data Backup
```bash
# Backup historical data
docker exec backend-container tar czf /backup/data-$(date +%Y%m%d).tar.gz /app/data

# Backup trained model
docker exec backend-container tar czf /backup/model-$(date +%Y%m%d).tar.gz /app/models
```

### Disaster Recovery
- Multi-region deployment
- Automated failover mechanisms
- Regular restore testing

## Performance Optimization

### Backend
- Model quantization for faster inference
- Connection pooling for database
- Asynchronous processing

### Frontend
- Code splitting for faster initial load
- Image optimization for charts
- Service worker for offline functionality

## Troubleshooting

### Common Issues
1. **CORS errors**: Check backend CORS configuration
2. **Model loading failures**: Verify model file paths and permissions
3. **Memory issues**: Monitor Docker container memory usage
4. **Slow predictions**: Check model optimization and caching

### Health Checks
```bash
# Backend health
curl -f http://localhost:5000/health || echo "Backend unhealthy"

# Frontend health
curl -f http://localhost:3000 || echo "Frontend unhealthy"
```

## Maintenance

### Model Retraining
```bash
# Schedule regular retraining with new data
cd backend
python train.py  # Retrains model with latest data
```

### Data Updates
```bash
# Update historical data
cd backend
python data_collector.py  # Fetches latest stock data
```

## Cost Optimization

### Cloud Costs
- Use spot instances for development
- Implement auto-scaling
- Optimize data transfer

### Resource Monitoring
- Set up billing alerts
- Regular usage audits
- Right-size instances

## Support and Documentation

- **API Documentation**: Available at `/` endpoint
- **Model Documentation**: Training metrics and evaluation results
- **Troubleshooting Guide**: Check logs and health endpoints

## Compliance and Legal

- **Financial Disclaimer**: Clearly displayed in application
- **Data Privacy**: No personal data collection
- **Terms of Service**: Define usage limitations

---

## Quick Deployment Commands

```bash
# Full stack deployment
git clone <repository>
cd apple-stock-prediction
docker-compose up --build -d

# Check deployment status
docker-compose ps
curl http://localhost:5000/health
curl http://localhost:3000
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Docs**: http://localhost:5000/
