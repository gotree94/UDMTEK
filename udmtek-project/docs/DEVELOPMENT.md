# UDMTEK Development Guide

## Project Structure

```
udmtek-project/
├── backend/                    # Python FastAPI backend
│   ├── parsers/               # PLC protocol parsers
│   │   ├── __init__.py
│   │   ├── siemens.py        # Siemens SIMATIC parser
│   │   ├── mitsubishi.py     # Mitsubishi MELSEC parser
│   │   ├── rockwell.py       # Rockwell RSLogix parser
│   │   ├── ls.py             # LS XGT parser
│   │   └── omron.py          # Omron parser
│   ├── udml/                  # UDML translator
│   │   ├── __init__.py
│   │   └── translator.py     # Main translation engine
│   ├── ai_engine/             # AI/ML models
│   │   ├── rca/              # Root Cause Analysis
│   │   │   └── root_cause_analyzer.py
│   │   ├── predictive/       # Predictive Maintenance
│   │   │   └── predictive_maintenance.py
│   │   └── optimization/     # Process Optimization
│   ├── pipeline/              # Data processing pipeline
│   ├── api/                   # REST API endpoints
│   │   └── routes/
│   ├── main.py                # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile            # Backend container
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # Page components
│   │   │   └── Dashboard.jsx
│   │   ├── services/         # API services
│   │   └── App.jsx           # Main application
│   ├── package.json          # Node.js dependencies
│   └── Dockerfile            # Frontend container
│
├── infrastructure/            # Infrastructure components
│   ├── data_collection/      # Real-time data collectors
│   ├── storage/              # Database configurations
│   ├── security/             # Auth & access control
│   └── monitoring/           # Prometheus & Grafana configs
│
├── config/                    # Configuration files
├── docs/                      # Documentation
├── tests/                     # Test suites
├── docker-compose.yml         # Multi-container orchestration
└── README.md                  # Main documentation
```

## Development Setup

### Prerequisites

- **Docker & Docker Compose**: Latest version
- **Python 3.11+**: For backend development
- **Node.js 18+**: For frontend development
- **PostgreSQL 14+**: Database (or use Docker)
- **Redis 7+**: Cache and task queue (or use Docker)

### Quick Start with Docker

1. **Clone the repository**
```bash
git clone <repository-url>
cd udmtek-project
```

2. **Start all services**
```bash
docker-compose up -d
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Grafana: http://localhost:3001 (admin/admin)
- Prometheus: http://localhost:9090

### Local Development (without Docker)

#### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set environment variables**
```bash
export DATABASE_URL=postgresql://user:password@localhost:5432/udmtek
export REDIS_URL=redis://localhost:6379/0
export SECRET_KEY=your-secret-key
```

4. **Run database migrations**
```bash
alembic upgrade head
```

5. **Start the backend server**
```bash
uvicorn main:app --reload
```

#### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Set environment variables**
Create `.env` file:
```
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

3. **Start development server**
```bash
npm run dev
```

## Core Components

### 1. PLC Parsers

Each parser converts vendor-specific binary PLC code to structured format.

**Example: Siemens Parser**
```python
from parsers.siemens import SiemensSIMATICParser, SiemensModel

parser = SiemensSIMATICParser(SiemensModel.S7_1500)
blocks = parser.parse_project(project_binary_data)

for block in blocks:
    print(f"Block: {block.block_name}")
    print(f"Instructions: {len(block.instructions)}")
```

**Supported PLCs:**
- Siemens SIMATIC (S7-300, S7-400, S7-1200, S7-1500)
- Mitsubishi MELSEC (FX, Q, L series)
- Rockwell RSLogix 5000
- LS XGT Series
- Omron (CP, CJ, NJ series)

### 2. UDML Translator

Translates vendor-specific instructions to unified UDML format.

**Example:**
```python
from udml.translator import UDMLTranslator

translator = UDMLTranslator()
udml_program = translator.translate("siemens", plc_instructions)

# Analyze complexity
complexity = translator.analyze_complexity(udml_program)
print(f"Total instructions: {complexity['total_instructions']}")
print(f"Cyclomatic complexity: {complexity['cyclomatic_complexity']}")

# Export to JSON
translator.export_json(udml_program, "output.json")
```

### 3. Root Cause Analysis

AI-powered fault detection and diagnosis.

**Example:**
```python
from ai_engine.rca.root_cause_analyzer import (
    RootCauseAnalyzer, 
    DiagnosticData
)

analyzer = RootCauseAnalyzer()

# Prepare diagnostic data
data = DiagnosticData(
    plc_signals={"temperature": 85.0, "pressure": 120.0},
    historical_data=[...],
    error_codes=["E002"],
    alarm_history=[...],
    process_parameters={...}
)

# Analyze faults
faults = analyzer.analyze(data)

for fault in faults:
    print(f"Fault: {fault.description}")
    print(f"Root Cause: {fault.root_cause}")
    print(f"Actions: {fault.recommended_actions}")
```

### 4. Predictive Maintenance

Machine learning for failure prediction and maintenance scheduling.

**Example:**
```python
from ai_engine.predictive.predictive_maintenance import (
    PredictiveMaintenanceEngine,
    EquipmentStatus,
    EquipmentHealth
)

engine = PredictiveMaintenanceEngine()

# Equipment status
status = EquipmentStatus(
    equipment_id="MOTOR_001",
    health_score=65.0,
    health_status=EquipmentHealth.FAIR,
    operating_hours=8500.0,
    sensor_readings={
        "vibration": 8.5,
        "temperature": 72.0
    }
)

# Get maintenance recommendations
recommendations = engine.predict_maintenance(status)

for rec in recommendations:
    print(f"Priority {rec.priority}: {rec.description}")
    if rec.remaining_useful_life:
        print(f"RUL: {rec.remaining_useful_life} days")
```

## API Endpoints

### PLC Parser API

```
POST /api/v1/parser/upload
- Upload PLC project file
- Returns: Parsed blocks

GET /api/v1/parser/blocks/{block_id}
- Get specific block details
```

### UDML Translator API

```
POST /api/v1/udml/translate
- Translate PLC code to UDML
- Body: {vendor: "siemens", instructions: [...]}

GET /api/v1/udml/complexity/{program_id}
- Get program complexity analysis
```

### AI Analysis API

```
POST /api/v1/ai/rca/analyze
- Perform root cause analysis
- Body: DiagnosticData

POST /api/v1/ai/predictive/maintenance
- Get maintenance recommendations
- Body: EquipmentStatus
```

### Dashboard API

```
GET /api/v1/dashboard/stats
- Get system statistics

GET /api/v1/dashboard/health-trend
- Get health trend data
```

## Testing

### Backend Tests

```bash
cd backend
pytest

# With coverage
pytest --cov=. --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm test

# With coverage
npm test -- --coverage
```

## Deployment

### Production Build

1. **Backend**
```bash
cd backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

2. **Frontend**
```bash
cd frontend
npm run build
# Serve dist/ folder with nginx
```

### Docker Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Monitoring

### Prometheus Metrics

Available at http://localhost:9090

**Key metrics:**
- `plc_parse_duration_seconds`: Parse time per PLC
- `udml_translation_count`: Number of translations
- `ai_analysis_duration_seconds`: AI analysis time
- `fault_detected_total`: Total faults detected
- `maintenance_recommendations_total`: Total recommendations

### Grafana Dashboards

Available at http://localhost:3001

**Dashboards:**
- System Overview
- PLC Health Monitoring
- AI Analysis Performance
- Maintenance Schedule

## Configuration

### Environment Variables

**Backend:**
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://host:6379/0
SECRET_KEY=your-secret-key-here
ENVIRONMENT=production
LOG_LEVEL=INFO
```

**Frontend:**
```
VITE_API_URL=https://api.udmtek.com
VITE_WS_URL=wss://api.udmtek.com
```

## Troubleshooting

### Common Issues

**1. Database connection failed**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres
```

**2. Frontend can't connect to backend**
- Verify VITE_API_URL is correct
- Check CORS settings in backend
- Ensure backend is running

**3. WebSocket connection drops**
- Check firewall settings
- Verify WebSocket URL
- Check backend logs for errors

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

Commercial License - See LICENSE file for details

## Support

- Documentation: [docs/](docs/)
- Issues: GitHub Issues
- Email: support@udmtek.com

---

**UDMTEK** - World's First PLC Translation Technology
