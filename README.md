# 🔥 MCP Super Root Maestro v2.2.0

## El Ecosistema de Ciberseguridad Más Avanzado del Mundo

### ✅ 328+ Endpoints Especializados
- **Reconnaissance & OSINT**: 61 endpoints
- **System Administration**: 87 endpoints  
- **Process Management**: 20+ endpoints ⭐ **NEW**
- **Web Security Testing**: 28 endpoints
- **Wireless & Crypto**: 16 endpoints
- **MCP Integration**: 14 endpoints
- **Ultra Admin Operations**: 12 endpoints

### 🚀 Quick Start
```bash
git clone https://github.com/Washdentx/MCP_Super_Root_Maestro.git
cd MCP_Super_Root_Maestro
python mcp-server.py
```

### 🌐 Live Demo
- **Health**: http://localhost:8001/health
- **Docs**: http://localhost:8001/docs
- **Status**: http://localhost:8001/status

### 🐳 Docker Deployment
```bash
docker run -p 8001:8001 mcp-super-root-maestro:latest
```

### 🔧 Features
- **42 Microservices**: Arquitectura modular completa
- **MCP Bridge**: Integración Claude AI
- **OAuth2 Security**: Autenticación avanzada
- **Real-time Monitoring**: Prometheus + Grafana
- **Auto-scaling**: Balanceador inteligente

### 🌐 API Endpoints Documentados

#### 📍 Core Endpoints
| Endpoint | Método | Descripción | Ejemplo |
|----------|--------|-------------|---------|
| `/` | GET | Endpoint principal del sistema | `curl http://localhost:8090/` |
| `/health` | GET | Health check del sistema | `curl http://localhost:8090/health` |
| `/status` | GET | Status completo del sistema | `curl http://localhost:8090/status` |
| `/endpoints` | GET | Lista de endpoints disponibles | `curl http://localhost:8090/endpoints` |

#### 🔒 Security Endpoints  
| Endpoint | Método | Descripción | Auth Required |
|----------|--------|-------------|---------------|
| `/protected` | GET | Endpoint protegido OAuth2 | Bearer Token |

#### 📊 Monitoring Endpoints
| Endpoint | Método | Descripción | Uso |
|----------|--------|-------------|-----|
| `/metrics` | GET | Métricas Prometheus | Monitoreo sistema |

#### 🔄 Real-time Endpoints
| Endpoint | Protocolo | Descripción | URL |
|----------|-----------|-------------|-----|
| `/ws` | WebSocket | Conexiones tiempo real | `ws://localhost:8090/ws` |
| `/broadcast` | POST | Broadcast a WebSocket clientes | JSON message |

#### ⚡ Process Management Endpoints ⭐ **NEW v2.2.0**
| Endpoint | Método | Descripción | Ejemplo |
|----------|--------|-------------|---------|
| `/system/pkill/{process_name}` | POST | Mata procesos por nombre | `curl -X POST http://localhost:8001/system/pkill/nginx` |
| `/system/killall/{process_name}` | POST | Mata todos los procesos exactos | `curl -X POST http://localhost:8001/system/killall/python` |
| `/system/kill/{pid}` | POST | Mata proceso por PID | `curl -X POST http://localhost:8001/system/kill/1234` |
| `/system/processes` | GET | Lista procesos activos | `curl http://localhost:8001/system/processes` |
| `/system/processes/search/{pattern}` | GET | Busca procesos por patrón | `curl http://localhost:8001/system/processes/search/node` |
| `/system/stats` | GET | Estadísticas del sistema | `curl http://localhost:8001/system/stats` |
| `/system/service/{action}/{service}` | POST | Gestiona servicios systemd | `curl -X POST http://localhost:8001/system/service/restart/nginx` |
| `/system/command/safe` | POST | Ejecuta comandos seguros | `curl -X POST -d '{"cmd":"ps aux"}' http://localhost:8001/system/command/safe` |
| `/system/network/ports/{port}` | GET | Verifica puerto específico | `curl http://localhost:8001/system/network/ports/8080` |

#### 📚 Documentation Endpoints
| Endpoint | Método | Descripción | URL |
|----------|--------|-------------|-----|
| `/docs` | GET | Swagger UI interactiva | http://localhost:8090/docs |
| `/redoc` | GET | ReDoc documentation | http://localhost:8090/redoc |
| `/openapi.json` | GET | OpenAPI specification | http://localhost:8090/openapi.json |

### 🐳 Docker Services URLs

#### 🚀 Main Services
- **API Principal**: http://localhost:8090
- **Servidor Directo**: http://localhost:8003
- **Load Balancer**: http://localhost:8090 (Nginx)

#### 📊 Monitoring Stack
- **Grafana**: http://localhost:3002 (admin/mcpadmin)
- **Prometheus**: http://localhost:9091
- **Portainer**: http://localhost:9001

#### 📖 Documentation
- **Swagger UI**: http://localhost:8081
- **API Docs**: http://localhost:8090/docs

#### 💾 Data Services
- **Redis**: localhost:6380
- **PostgreSQL**: localhost:5432

### 📦 Backup Completo
**MEGA**: https://mega.nz/file/WwBggYCT#MfqFnkHLjAXZE84zmRg-MIwkO9yMxy0FQ6HEGF07Lmw
- **Tamaño**: 1.4GB (79,779 archivos)
- **SHA256**: db9be760d4df9e62e151444154742ef463d4c6c9a42724e438ed60c054864bc0

### 🛠️ Claude Code MCP Settings

Para agregar MCP Super Root Maestro a Claude Code, agregar a `settings.json`:

```json
{
  "mcpServers": {
    "mcp-super-root-maestro": {
      "httpUrl": "http://localhost:8090",
      "description": "MCP Super Root Maestro v2.1.0 - 308 Endpoints"
    },
    "mcp-server-direct": {
      "httpUrl": "http://localhost:8003", 
      "description": "MCP Server Direct Access"
    },
    "swagger-docs": {
      "httpUrl": "http://localhost:8081",
      "description": "Swagger Documentation"
    },
    "grafana-monitoring": {
      "httpUrl": "http://localhost:3002",
      "description": "Grafana Dashboards"
    },
    "prometheus-metrics": {
      "httpUrl": "http://localhost:9091", 
      "description": "Prometheus Metrics"
    },
    "portainer-management": {
      "httpUrl": "http://localhost:9001",
      "description": "Docker Management"
    }
  }
}
```

### 🛡️ Disclaimer
**Para investigación defensiva únicamente**

---
**🎯 Generated with Claude Code**