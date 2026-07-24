<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2DD4BF,100:6366F1&height=200&section=header&text=DiscoveryOS&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=AI%20Product%20Discovery%20Intelligence%20System&descAlignY=55&descSize=17" width="100%"/>

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

<br/>

> ### 🔍 *"Turn a flood of customer insights into a ranked, themed, actionable roadmap"*
> **Insight Clustering • Segment Intelligence • Live Priority Scoring**

<br/>

</div>

## 🎯 What Is This Project?

**DiscoveryOS** is a full-stack AI-powered product discovery intelligence system. It ingests raw customer insights, automatically clusters them into themes, identifies which user segments they belong to, and calculates a priority score for each one — all visualized in a live, interactive dashboard.

Product teams are usually buried in scattered feedback: support tickets, interview notes, survey responses. DiscoveryOS is a first pass at the infrastructure that turns that noise into a structured, prioritized view of what to build next.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Insight Analysis** | Ingests and processes raw customer insights through an AI pipeline |
| 📊 **Theme Detection** | Automatically clusters insights into coherent themes |
| 👥 **User Segmentation** | Identifies which user segment each insight is coming from |
| 📈 **Priority Scoring** | AI-calculated 1–10 priority score for every insight |
| 🎨 **Interactive Dashboard** | Real-time charts, KPI cards, and a sortable insights table |
| 🔄 **Live Data Sync** | WebSocket-ready architecture for future live updates |
| 🛡️ **CORS-Enabled** | Configured for multi-port local development out of the box |

---

## 🏗️ Project Structure

```
discoveryos/
│
├── server.py               # Flask backend server
├── main.py                 # Core business logic & AI processing
├── database.py             # Database initialization & queries
├── init_db.py               # Database seeding with sample data
├── discoveryos.db           # SQLite database (auto-created)
├── .env.example              # Environment variables template
│
└── frontend/                 # React + Vite dashboard
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

## 📊 How Insights Flow Through The System

```
Raw customer insight submitted
        ↓
AI pipeline analyzes content (main.py)
        ↓
Insight clustered into a Theme
        ↓
Insight mapped to a User Segment
        ↓
Priority Score (1–10) calculated
        ↓
Stored in SQLite (discoveryos.db)
        ↓
Dashboard fetches via REST API and renders live
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend** | Flask, Flask-CORS, Flask-Limiter | REST API, cross-origin support, rate limiting |
| **AI Processing** | Python (`main.py`) | Theme clustering, segmentation, priority scoring |
| **Persistence** | SQLite | Insights, themes, and segments storage |
| **Frontend** | React 18 + Vite | Interactive dashboard |
| **Styling** | Tailwind CSS | Dashboard UI |
| **Charts** | Theme & segment visualizations | Bar chart, pie chart, sortable table |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+ & npm
- SQLite (bundled, no separate install needed)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/chakriburidi237-crypto/discoveryos.git
cd discoveryos

# 2. Install backend dependencies
pip install flask flask-cors flask-limiter

# 3. Initialize the database (creates discoveryos.db with sample data)
python init_db.py
```

---

## ▶️ Running the Application

### Terminal 1 — Backend

```bash
python server.py
# API starts at http://localhost:5000
```

### Terminal 2 — Frontend

```bash
cd frontend
npm install
npm run dev
# Dashboard starts at http://localhost:5177
```

Once both are running, open **http://localhost:5177** to view the dashboard.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/insights` | Retrieve all insights |
| `GET` | `/api/themes` | Get theme analysis results |
| `GET` | `/api/segments` | Retrieve user segments |
| `GET` | `/api/health` | Health check endpoint |
| `GET` | `/api/stats` | System-wide statistics |

### Example — fetching insights:

```bash
curl http://localhost:5000/api/insights
```

---

## 📈 Data Model

**Insights**
- `id`, `content`, `theme`, `segment`, `priority_score` (1–10), `created_at`

**Themes**
- `id`, `name`, `insight_count`, `avg_priority`

**Segments**
- `id`, `name`, `user_count`, `key_characteristics`

---

## 🎨 Dashboard Features

- **KPI Cards** — total insights, themes detected, segments identified, average priority score
- **Bar Chart** — insights grouped by theme
- **Pie Chart** — segment distribution
- **Theme Cards Grid** — detailed per-theme breakdown
- **Sortable Table** — full insights data with filtering

---

## 🔧 Configuration

Create a `.env` file in the root directory:

```env
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_PATH=./discoveryos.db
CORS_ORIGINS=http://localhost:5173,http://localhost:5174,http://localhost:5175,http://localhost:5176,http://localhost:5177
MAX_REQUESTS=100
```

---

## 🔐 Security

- CORS properly scoped for local development
- Rate limiting enabled (100 requests/minute)
- Input validation on all endpoints
- Error handling with safe, non-leaking error messages

---

## 🐛 Troubleshooting

**CORS errors** — make sure both servers are running; `CORS_ORIGINS` already covers ports 5173–5177 by default.

**Database issues** — reset with:
```bash
rm discoveryos.db
python init_db.py
```

**Frontend not loading** — reinstall dependencies:
```bash
cd frontend
npm install
npm run dev
```

---

## 📝 Sample Data

Pre-loaded out of the box with:
- ✅ 4 Themes (AI, Personalization, Performance, Integration)
- ✅ 39 Insights (analyzed and scored)
- ✅ 1 Segment (Power Users – Enterprise)
- ✅ Priority scores calculated and ready to display

---

## 🚀 Deployment

### Docker (optional)

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
# Output: dist/ folder, ready for deployment
```

---

## 🔮 Future Improvements

- [ ] 🔗 Real-time WebSocket updates instead of polling
- [ ] 🧠 Swap in a production LLM for theme detection and priority scoring
- [ ] 👥 Multi-segment support beyond the current single-segment demo
- [ ] 🔐 Authentication and multi-tenant workspace support
- [ ] 📊 Historical trend view for priority scores over time
- [ ] 🐳 Dockerize backend + frontend for one-command spin-up

---

## 👨‍💻 Developer

<div align="center">

**Surya Chakradhar Buridi**

*AI/ML Engineer | B.E. Artificial Intelligence & Machine Learning @ KIET*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/surya-chakradhar-buridi-767548355)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/chakriburidi237-crypto)

</div>

---

## 📄 License

Open source — feel free to use and modify.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6366F1,100:2DD4BF&height=100&section=footer" width="100%"/>

*Built by Surya Chakradhar Buridi — Kakinada Institute of Engineering and Technology (KIET)*

</div>
