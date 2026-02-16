# UDMTEK - PLC Translation & Analysis Platform

## Project Overview

UDMTEK is a comprehensive industrial automation analysis platform featuring world's first PLC translation technology. It converts multiple vendor PLC protocols to a unified UDML (Unified Device Machine Language) for AI-powered root cause analysis and predictive maintenance.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                            │
│  ┌──────────────────────┐  ┌──────────────────────┐             │
│  │ Control Logic        │  │ Dashboard &          │             │
│  │ Visualization        │  │ Reporting            │             │
│  └──────────────────────┘  └──────────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ REST API / WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Backend Layer                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ PLC Protocol Parsers                                     │   │
│  │ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │   │
│  │ │Siemens │ │Mitsu-  │ │Rockwell│ │  LS    │ │ Omron  │ │   │
│  │ │SIMATIC │ │bishi   │ │RSLogix │ │  XGT   │ │        │ │   │
│  │ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ UDML Translator - Unified Device Machine Language       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ AI/ML Engine                                             │   │
│  │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │   │
│  │ │ Root Cause   │ │ Predictive   │ │ Process      │     │   │
│  │ │ Analysis     │ │ Maintenance  │ │ Optimization │     │   │
│  │ └──────────────┘ └──────────────┘ └──────────────┘     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Data Processing Pipeline                                 │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ Real-time    │ │ Historical   │ │ Security &   │            │
│  │ Data         │ │ Data         │ │ Access       │            │
│  │ Collection   │ │ Storage      │ │ Control      │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
udmtek-project/
├── frontend/                 # React-based web interface
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   └── utils/           # Utility functions
│   └── public/              # Static assets
│
├── backend/                 # Python/FastAPI backend
│   ├── parsers/            # PLC protocol parsers
│   │   ├── siemens.py
│   │   ├── mitsubishi.py
│   │   ├── rockwell.py
│   │   ├── ls.py
│   │   └── omron.py
│   ├── udml/               # UDML translator
│   ├── ai_engine/          # AI/ML models
│   │   ├── rca/           # Root Cause Analysis
│   │   ├── predictive/    # Predictive Maintenance
│   │   └── optimization/  # Process Optimization
│   ├── pipeline/          # Data processing
│   └── api/               # REST API endpoints
│
├── infrastructure/         # Infrastructure components
│   ├── data_collection/   # Real-time data collectors
│   ├── storage/           # Database configurations
│   └── security/          # Authentication & authorization
│
├── config/                # Configuration files
├── docs/                  # Documentation
└── tests/                 # Test suites
```

## Technology Stack

### Frontend
- **Framework**: React 18+ with TypeScript
- **State Management**: Redux Toolkit
- **UI Library**: Material-UI (MUI)
- **Visualization**: D3.js, Recharts
- **Build Tool**: Vite

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Task Queue**: Celery + Redis
- **ML Framework**: PyTorch, scikit-learn
- **API Protocol**: REST + WebSocket

### Infrastructure
- **Database**: PostgreSQL (structured data), TimescaleDB (time-series)
- **Cache**: Redis
- **Message Queue**: RabbitMQ
- **Monitoring**: Prometheus + Grafana

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (optional)

### Installation

1. Clone the repository
```bash
git clone https://github.com/your-org/udmtek-project.git
cd udmtek-project
```

2. Setup Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Setup Frontend
```bash
cd frontend
npm install
```

4. Configure Environment
```bash
cp config/.env.example config/.env
# Edit config/.env with your settings
```

5. Run Development Servers
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

## Features

### 1. Multi-Vendor PLC Support
- Siemens SIMATIC (S7-300, S7-400, S7-1200, S7-1500)
- Mitsubishi MELSEC (FX, Q, L series)
- Rockwell RSLogix 5000
- LS XGT Series
- Omron (CP, CJ, NJ series)

### 2. UDML Translation
- Binary PLC code to unified language
- Standardized instruction set
- Cross-platform logic analysis

### 3. AI-Powered Analysis
- **Root Cause Analysis**: Automatic fault detection and diagnosis
- **Predictive Maintenance**: Failure prediction and maintenance scheduling
- **Process Optimization**: Performance analysis and improvement recommendations

### 4. Real-time Monitoring
- Live PLC data streaming
- Alert and notification system
- Historical trend analysis

## Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Backend linting
cd backend
flake8 .
black .
mypy .

# Frontend linting
cd frontend
npm run lint
npm run type-check
```

## Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Production Build
```bash
# Frontend
cd frontend
npm run build

# Backend
cd backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under a commercial license. See [LICENSE](LICENSE) for details.

## Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/your-org/udmtek-project/issues)
- Email: support@udmtek.com

## Roadmap

- [x] Core PLC parsers (Siemens, Mitsubishi, Rockwell, LS, Omron)
- [x] UDML translator engine
- [x] Basic AI/ML models
- [ ] Advanced predictive models
- [ ] Cloud deployment support
- [ ] Mobile application
- [ ] Additional PLC vendor support

---

**UDMTEK** - Transforming Industrial Automation with AI
