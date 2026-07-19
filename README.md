# DiscoveryOS - AI Product Discovery Intelligence System

## 🎯 Overview

**DiscoveryOS** is a full-stack AI-powered product discovery intelligence system that analyzes customer insights, identifies themes, segments users, and calculates priority scores in real-time through an interactive dashboard.

### ✨ Key Features

- 🔍 **Insight Analysis**: Process and analyze customer insights with AI
- 📊 **Theme Detection**: Automatic clustering of insights into themes
- 👥 **User Segmentation**: Intelligent user segment identification
- 📈 **Priority Scoring**: AI-calculated priority scores for insights
- 🎨 **Interactive Dashboard**: Real-time visualization with charts and tables
- 🔄 **Live Data Sync**: WebSocket-ready architecture for live updates
- 🛡️ **CORS Enabled**: Cross-origin support for multi-port development

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+** & **npm**
- **SQLite** (bundled)

### Installation & Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/chakriburidi237-crypto/discoveryos.git
cd discoveryos
```

#### 2. Backend Setup
```bash
# Install Python dependencies
pip install flask flask-cors flask-limiter

# Initialize database (creates discoveryos.db with sample data)
python init_db.py

# Start the backend server (runs on port 5000)
python server.py
```

#### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server (runs on port 5177)
npm run dev
```

### 🌐 Access the Dashboard

Once both servers are running:
- **Frontend**: http://localhost:5177
- **Backend API**: http://localhost:5000

---

## 📁 Project Structure

```
discoveryos/
├── server.py              # Flask backend server
├── main.py                # Core business logic & AI processing
├── database.py            # Database initialization & queries
├── init_db.py             # Database seeding with sample data
├── discoveryos.db         # SQLite database (auto-created)
├── .env.example           # Environment variables template
│
└── frontend/              # React + Vite dashboard
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── src/
    │   ├── main.jsx
    │   ├── App.jsx
    │   ├── index.css
    │   ├── api/
    │   │   └── reportService.js
    │   └── components/
    │       ├── Header.jsx
    │       ├── ErrorAlert.jsx
    │       ├── ErrorBoundary.jsx
    │       ├── LoadingSpinner.jsx
    │       ├── ThemeCard.jsx
    │       ├── ThemeChart.jsx
    │       └── SegmentSection.jsx
    └── .env.development
```

---

## 🔌 API Endpoints

### Insights
- `GET /api/insights` - Retrieve all insights

### Themes
- `GET /api/themes` - Get theme analysis results

### Segments
- `GET /api/segments` - Retrieve user segments

### System
- `GET /api/health` - Health check endpoint
- `GET /api/stats` - System statistics

---

## 📊 Dashboard Features

### KPI Cards
- Total Insights analyzed
- Themes detected
- Segments identified
- Average Priority Score

### Visualizations
- **Bar Chart**: Insights by Theme
- **Pie Chart**: Segment Distribution
- **Theme Cards Grid**: Detailed theme information
- **Sortable Table**: Complete insights data with filtering

### Live Data
All charts and tables update automatically as data changes.

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in root directory:

```env
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_PATH=./discoveryos.db
CORS_ORIGINS=http://localhost:5173,http://localhost:5174,http://localhost:5175,http://localhost:5176,http://localhost:5177
MAX_REQUESTS=100
```

---

## 🐛 Troubleshooting

### CORS Errors
If you see CORS errors, ensure both servers are running and the `CORS_ORIGINS` environment variable includes your frontend port.

**Solution**: Backend automatically includes ports 5173-5177 by default.

### Database Issues
If the database is corrupted or needs reset:
```bash
rm discoveryos.db
python init_db.py
```

### Frontend Not Loading
Ensure Node.js dependencies are installed:
```bash
cd frontend
npm install
npm run dev
```

---

## 📈 Data Model

### Insights Table
- `id`: Unique identifier
- `content`: Insight text
- `theme`: Associated theme
- `segment`: User segment
- `priority_score`: AI-calculated priority (1-10)
- `created_at`: Timestamp

### Themes Table
- `id`: Theme identifier
- `name`: Theme name
- `insight_count`: Number of insights
- `avg_priority`: Average priority score

### Segments Table
- `id`: Segment identifier
- `name`: Segment name
- `user_count`: Number of users
- `key_characteristics`: Segment description

---

## 🔐 Security

- CORS properly configured for development
- Rate limiting enabled (100 requests per minute)
- Input validation on all endpoints
- Error handling with safe error messages

---

## 📝 Sample Data

The system comes pre-loaded with:
- ✅ **4 Themes** (AI, Personalization, Performance, Integration)
- ✅ **39 Insights** (analyzed and scored)
- ✅ **1 Segment** (Power Users - Enterprise)
- ✅ **Priority Scores** (calculated and ready for display)

---

## 🎓 Example API Usage

```bash
# Get all insights
curl http://localhost:5000/api/insights

# Get themes
curl http://localhost:5000/api/themes

# Get segments
curl http://localhost:5000/api/segments

# Health check
curl http://localhost:5000/api/health
```

---

## 🚀 Deployment

### Docker Setup (Optional)
Create `Dockerfile` for containerized deployment:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server.py"]
```

### Production Build
```bash
cd frontend
npm run build
# Output: dist/ folder ready for deployment
```

---

## 📞 Support & Documentation

For detailed setup, API documentation, and troubleshooting:
- Backend health check: http://localhost:5000/api/health
- View sample data: http://localhost:5000/api/insights
- Dashboard: http://localhost:5177

---

## 📄 License

Open source - feel free to use and modify.

---

## 👨‍💻 Author

Created by Chakri (crypto developer) - https://github.com/chakriburidi237-crypto

---

## ✅ System Status

```
✅ Backend API:    http://localhost:5000    HEALTHY
✅ Frontend:       http://localhost:5177    LOADED
✅ Database:       discoveryos.db           ACTIVE
✅ CORS:           FIXED (ports 5173-5177)
✅ Data:           4 themes, 39 insights, live ready
```

**Everything is connected and working! 🎉**
