# DiscoveryOS

> **"Transform Customer Insights into an Actionable, Prioritized Product Roadmap."**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2%2B-61DAFB.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.0%2B-646CFF.svg)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.3%2B-38B2AC.svg)](https://tailwindcss.com/)

DiscoveryOS is a full-stack, AI-powered product discovery intelligence platform. Product teams are routinely inundated with disjointed feedback scattered across support tickets, user interview recordings, sales call notes, and NPS survey verbatims. DiscoveryOS automates the synthesis pipeline: ingesting raw customer insights, embedding semantics with sentence transformers, clustering feedback into coherent feature themes, identifying user segment distributions (Enterprise, Mid-Market, SMB), and calculating multidimensional priority scores (1–10) in an interactive executive command deck.

---

## 🚀 Key Features

1. **Semantic Insight Clustering**: Groups thousands of unstructured user feedback items into coherent feature themes using Sentence-Transformers embeddings and unsupervised density clustering.
2. **Dynamic User Segmentation**: Maps feedback to customer tiers (Enterprise, Mid-Market, SMB, Self-Serve) to evaluate revenue-weighted demand.
3. **Calibrated Priority Scoring Engine**: Computes deterministic priority scores ($1.0 - 10.0$) using weighted Impact, Urgency, Confidence, and Effort factors:
   $$\text{Priority} = f(\text{Impact}, \text{Urgency}, \text{Confidence}, \text{Effort})$$
4. **Interactive Executive Dashboard**: Built with React 18, Vite, and Recharts, featuring real-time KPI metrics, segment distribution donuts, priority heatmaps, and filterable theme tables.
5. **Zero-Friction Local Database**: Defaults out of the box to zero-configuration SQLite (`discoveryos.db`), with immediate production support for PostgreSQL via SQLAlchemy.
6. **Asynchronous REST API Backend**: FastAPI server with automated Swagger/OpenAPI documentation (`/docs`), CORS middleware, and structured Pydantic schemas.
7. **Production Clean Repository Architecture**: Fully sanitized codebase free of committed bytecode, binaries, or virtualenv artifacts, featuring complete test coverage.

---

## 🛠 Tech Stack

- **Backend Framework**: FastAPI, Uvicorn
- **AI & NLP Pipeline**: Sentence-Transformers, Scikit-Learn, HDBSCAN, OpenAI / Anthropic integrations
- **Data Persistence**: SQLAlchemy, SQLite3 / PostgreSQL, Pydantic v2
- **Frontend Dashboard**: React 18, Vite, Recharts, Tailwind CSS, Lucide Icons, Axios
- **Testing**: Pytest automated regression suite

---

## 🏗 Architecture & Directory Structure

```
DiscoveryOS/
├── src/
│   ├── api/
│   │   └── reportService.js  # REST API client and report service
│   ├── components/           # Modular React dashboard widgets
│   │   ├── DashboardLayout.jsx
│   │   ├── Header.jsx
│   │   ├── KPICard.jsx
│   │   ├── SegmentChart.jsx
│   │   ├── ThemeChart.jsx
│   │   ├── ThemeDetailModal.jsx
│   │   ├── ThemeGrid.jsx
│   │   ├── RecentThemesTable.jsx
│   │   ├── LoadingSpinner.jsx
│   │   └── ErrorAlert.jsx
│   ├── App.jsx               # Main React application entry
│   ├── index.css             # Tailwind CSS tokens
│   └── main.jsx              # Vite client bootstrap
├── tests/
│   └── test_discovery.py     # Automated scoring and schema unit tests
├── clustering.py             # Semantic embedding and clustering pipeline
├── database.py               # SQLAlchemy database session manager
├── embeddings.py             # Vector embedding generation utilities
├── main.py                   # FastAPI application instance & endpoints
├── models.py                 # SQLAlchemy relational ORM models
├── schemas.py                # Pydantic request and response schemas
├── scoring.py                # Quantitative priority score calculation engine
├── server.py                 # Backend runner with auto-port discovery
├── themes.py                 # Theme extraction & synthesis logic
├── package.json              # Frontend dependencies and scripts
├── requirements.txt          # Python backend dependencies
├── vite.config.js            # Vite development & build configuration
├── tailwind.config.js        # Tailwind configuration
├── .gitignore                # Production ignore patterns
├── LICENSE                   # MIT License
└── README.md                 # Project documentation
```

---

## ⚡ Getting Started

### Prerequisites

- Python `3.10` or `3.11`
- Node.js `v18+` or `v20+`
- `npm` or `pnpm`

### 1. Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/chakriburidi237-crypto/DiscoveryOS.git
   cd DiscoveryOS
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the FastAPI server:
   ```bash
   python server.py
   ```
   Interactive Swagger documentation will be available at [http://localhost:5000/docs](http://localhost:5000/docs).

### 2. Frontend Setup

In a new terminal window:

1. Install frontend packages:
   ```bash
   npm install
   ```

2. Launch the Vite development server:
   ```bash
   npm run dev
   ```
   Open [http://localhost:5173](http://localhost:5173) in your web browser.

---

## 🧪 Automated Testing

Execute the backend unit test suite:

```bash
pytest tests/ -v
```

Expected output:
```
tests/test_discovery.py::test_scoring_algorithm PASSED
tests/test_discovery.py::test_schema_validation PASSED
======================== 2 passed in 0.35s ========================
```

---

## 📄 License and Copyright\n\nAll rights reserved © 2026 Chakradhar Buridi.

