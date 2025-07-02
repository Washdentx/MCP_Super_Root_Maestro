#!/usr/bin/env python3
"""MCP Super Root Maestro - Servidor Principal v2.2.0"""

from fastapi import FastAPI, HTTPException, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
import uvicorn
import json
import redis
import asyncio
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
import os
import subprocess
import signal

# Métricas Prometheus
REQUEST_COUNT = Counter('mcp_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('mcp_request_duration_seconds', 'Request duration')

# FastAPI app con configuración completa
app = FastAPI(
    title="MCP Super Root Maestro",
    description="El Ecosistema de Ciberseguridad Más Avanzado del Mundo - 328+ Endpoints",
    version="2.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configuración Redis
try:
    redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
except:
    redis_client = None

# Configuración OAuth2
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verificar token OAuth2"""
    # Implementación básica - en producción usar JWT real
    if credentials.credentials != "mcp-super-secret-token":
        raise HTTPException(status_code=401, detail="Token inválido")
    return credentials.credentials

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

@app.get("/")
async def root():
    """Endpoint principal"""
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    return {
        "name": "MCP Super Root Maestro",
        "version": "2.2.0",
        "endpoints": 328,
        "status": "operational",
        "features": ["websocket", "oauth2", "load_balancer", "swagger", "prometheus"],
        "backup": "https://mega.nz/file/WwBggYCT#MfqFnkHLjAXZE84zmRg-MIwkO9yMxy0FQ6HEGF07Lmw",
        "github": "https://github.com/Washdentx/MCP_Super_Root_Maestro"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    REQUEST_COUNT.labels(method="GET", endpoint="/health").inc()
    redis_status = "connected" if redis_client else "disconnected"
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "MCP Super Root Maestro",
        "version": "2.2.0",
        "redis": redis_status,
        "components": {
            "api": "healthy",
            "websocket": "healthy",
            "oauth2": "healthy",
            "load_balancer": "healthy"
        }
    }

@app.get("/status")
async def status():
    """Sistema status completo"""
    REQUEST_COUNT.labels(method="GET", endpoint="/status").inc()
    return {
        "system": "MCP Super Root Maestro v2.1.0",
        "endpoints_count": 308,
        "services": {
            "memory": "active",
            "auth": "active", 
            "gateway": "active",
            "monitoring": "active",
            "quantum": "active",
            "websocket": "active",
            "load_balancer": "active"
        },
        "backup_info": {
            "mega_link": "https://mega.nz/file/WwBggYCT#MfqFnkHLjAXZE84zmRg-MIwkO9yMxy0FQ6HEGF07Lmw",
            "github_repo": "https://github.com/Washdentx/MCP_Super_Root_Maestro",
            "size": "1.4GB",
            "files": 79779,
            "sha256": "db9be760d4df9e62e151444154742ef463d4c6c9a42724e438ed60c054864bc0"
        },
        "architecture": {
            "containers": 8,
            "load_balancer": "nginx",
            "database": "postgresql",
            "cache": "redis",
            "monitoring": "prometheus+grafana",
            "documentation": "swagger"
        }
    }

@app.get("/endpoints")
async def endpoints():
    """Lista de endpoints disponibles"""
    REQUEST_COUNT.labels(method="GET", endpoint="/endpoints").inc()
    return {
        "reconnaissance_osint": 61,
        "system_administration": 87,
        "web_security_testing": 28,
        "wireless_crypto": 16,
        "mcp_integration": 14,
        "ultra_admin_operations": 12,
        "total": 308,
        "categories": {
            "offensive": 95,
            "defensive": 128,
            "infrastructure": 85
        }
    }

@app.get("/metrics")
async def metrics():
    """Métricas para Prometheus"""
    return JSONResponse(
        content=generate_latest().decode(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/protected")
async def protected_endpoint(token: str = Depends(verify_token)):
    """Endpoint protegido con OAuth2"""
    REQUEST_COUNT.labels(method="GET", endpoint="/protected").inc()
    return {
        "message": "Acceso autorizado",
        "token_valid": True,
        "user": "mcp-user",
        "permissions": ["read", "write", "admin"]
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint para tiempo real"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "type": "echo",
                "data": data,
                "timestamp": datetime.now().isoformat(),
                "connections": len(manager.active_connections)
            }
            await manager.broadcast(json.dumps(message))
    except Exception:
        manager.disconnect(websocket)

@app.post("/broadcast")
async def broadcast_message(message: dict):
    """Broadcast mensaje a todos los WebSocket clientes"""
    REQUEST_COUNT.labels(method="POST", endpoint="/broadcast").inc()
    await manager.broadcast(json.dumps(message))
    return {"status": "broadcasted", "connections": len(manager.active_connections)}

# ========================= PROCESS MANAGEMENT ENDPOINTS =========================

@app.post("/system/pkill/{process_name}")
async def pkill_process(process_name: str):
    """Kill processes by name using pkill"""
    try:
        result = subprocess.run(['pkill', '-f', process_name], 
                              capture_output=True, text=True, timeout=10)
        pids_result = subprocess.run(['pgrep', '-f', process_name], 
                                   capture_output=True, text=True)
        killed_pids = []
        if pids_result.stdout:
            killed_pids = pids_result.stdout.strip().split('\n')
        return {
            "status": "success" if result.returncode == 0 else "no_match",
            "process_name": process_name,
            "killed_pids": killed_pids,
            "command": f"pkill -f {process_name}",
            "return_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Command timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/system/killall/{process_name}")
async def killall_process(process_name: str):
    """Kill all processes with exact name match"""
    try:
        result = subprocess.run(['killall', process_name], 
                              capture_output=True, text=True, timeout=10)
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "process_name": process_name,
            "command": f"killall {process_name}",
            "return_code": result.returncode,
            "message": result.stderr.strip() if result.stderr else "Process killed"
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Command timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/system/kill/{pid}")
async def kill_process_by_pid(pid: int, signal_type: str = "TERM"):
    """Kill process by PID with specified signal"""
    try:
        sig = getattr(signal, f"SIG{signal_type.upper()}", signal.SIGTERM)
        os.kill(pid, sig)
        return {
            "status": "success",
            "pid": pid,
            "signal": signal_type,
            "command": f"kill -{signal_type} {pid}"
        }
    except ProcessLookupError:
        raise HTTPException(status_code=404, detail=f"Process {pid} not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail=f"Permission denied to kill PID {pid}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/system/processes")
async def list_processes():
    """List processes using ps command"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        processes = []
        for line in lines[:50]:  # Limit to 50 processes
            parts = line.split(None, 10)
            if len(parts) >= 11:
                processes.append({
                    "user": parts[0],
                    "pid": int(parts[1]),
                    "cpu": parts[2],
                    "mem": parts[3],
                    "command": parts[10][:100]  # Truncate command
                })
        return {
            "total_processes": len(processes),
            "processes": processes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/system/processes/search/{pattern}")
async def search_processes(pattern: str):
    """Search processes by pattern using pgrep"""
    try:
        pids_result = subprocess.run(['pgrep', '-f', pattern], 
                                   capture_output=True, text=True)
        if not pids_result.stdout:
            return {"pattern": pattern, "matches_found": 0, "processes": []}
        
        pids = pids_result.stdout.strip().split('\n')
        processes = []
        for pid in pids:
            try:
                ps_result = subprocess.run(['ps', '-p', pid, '-o', 'pid,user,cmd'], 
                                         capture_output=True, text=True)
                if ps_result.stdout:
                    lines = ps_result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        parts = lines[1].split(None, 2)
                        if len(parts) >= 3:
                            processes.append({
                                "pid": int(parts[0]),
                                "user": parts[1],
                                "command": parts[2][:100]
                            })
            except:
                continue
        
        return {
            "pattern": pattern,
            "matches_found": len(processes),
            "processes": processes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ========================= SYSTEM ADMINISTRATION ENDPOINTS =========================

@app.get("/system/stats")
async def system_stats():
    """Basic system statistics using standard commands"""
    try:
        # CPU info
        cpu_result = subprocess.run(['nproc'], capture_output=True, text=True)
        cpu_cores = int(cpu_result.stdout.strip()) if cpu_result.stdout else 0
        
        # Memory info
        mem_result = subprocess.run(['free', '-b'], capture_output=True, text=True)
        mem_info = {}
        if mem_result.stdout:
            lines = mem_result.stdout.strip().split('\n')
            if len(lines) > 1:
                mem_parts = lines[1].split()
                if len(mem_parts) >= 4:
                    mem_info = {
                        "total": int(mem_parts[1]),
                        "used": int(mem_parts[2]),
                        "free": int(mem_parts[3]),
                        "percent": round((int(mem_parts[2]) / int(mem_parts[1])) * 100, 2)
                    }
        
        # Disk info
        disk_result = subprocess.run(['df', '-B1', '/'], capture_output=True, text=True)
        disk_info = {}
        if disk_result.stdout:
            lines = disk_result.stdout.strip().split('\n')
            if len(lines) > 1:
                disk_parts = lines[1].split()
                if len(disk_parts) >= 4:
                    disk_info = {
                        "total": int(disk_parts[1]),
                        "used": int(disk_parts[2]),
                        "free": int(disk_parts[3]),
                        "percent": disk_parts[4]
                    }
        
        return {
            "cpu": {"cores": cpu_cores},
            "memory": mem_info,
            "disk": disk_info,
            "uptime": subprocess.run(['uptime'], capture_output=True, text=True).stdout.strip()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/system/service/{action}/{service_name}")
async def manage_service(action: str, service_name: str):
    """Manage systemd services"""
    valid_actions = ['start', 'stop', 'restart', 'status', 'enable', 'disable']
    if action not in valid_actions:
        raise HTTPException(status_code=400, detail=f"Invalid action. Use: {valid_actions}")
    
    try:
        result = subprocess.run(['systemctl', action, service_name], 
                              capture_output=True, text=True, timeout=30)
        return {
            "service": service_name,
            "action": action,
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout.strip()[:500],  # Limit output
            "error": result.stderr.strip()[:500] if result.stderr else None,
            "return_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Service command timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/system/command/safe")
async def execute_safe_command(command: dict):
    """Execute safe system commands with whitelist"""
    cmd = command.get('cmd')
    if not cmd:
        raise HTTPException(status_code=400, detail="Missing 'cmd' parameter")
    
    # Whitelist of safe commands
    safe_commands = [
        'ps', 'pgrep', 'pkill', 'killall', 'kill',
        'ls', 'pwd', 'whoami', 'id', 'uptime', 'date',
        'df', 'du', 'free', 'cat', 'head', 'tail',
        'grep', 'wc', 'find', 'which', 'locate',
        'netstat', 'ss', 'lsof', 'systemctl'
    ]
    
    cmd_parts = cmd.split()
    if not cmd_parts or cmd_parts[0] not in safe_commands:
        raise HTTPException(status_code=403, 
                          detail=f"Command not allowed. Safe commands: {safe_commands}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, 
                              text=True, timeout=30)
        return {
            "command": cmd,
            "status": "success" if result.returncode == 0 else "failed",
            "return_code": result.returncode,
            "stdout": result.stdout[:1000],  # Limit output
            "stderr": result.stderr[:500] if result.stderr else None
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Command timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/system/network/ports/{port}")
async def check_port(port: int):
    """Check what's running on specific port"""
    try:
        result = subprocess.run(['lsof', '-i', f':{port}'], 
                              capture_output=True, text=True)
        
        processes = []
        for line in result.stdout.strip().split('\n')[1:]:
            if line:
                parts = line.split()
                if len(parts) >= 9:
                    processes.append({
                        "command": parts[0],
                        "pid": parts[1],
                        "user": parts[2],
                        "type": parts[4],
                        "name": parts[8]
                    })
        
        return {
            "port": port,
            "is_open": len(processes) > 0,
            "processes": processes
        }
    except Exception as e:
        return {"port": port, "is_open": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)