#!/bin/bash
# 🚀 MCP Super Root Maestro - Deploy Script v2.1.0

echo "🔥 MCP Super Root Maestro v2.1.0 - Deployment Started"
echo "===================================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker y Docker Compose disponibles${NC}"

# Verificar archivo .env
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Archivo .env no encontrado, copiando .env.example${NC}"
    cp .env.example .env
    echo -e "${BLUE}📝 Edita el archivo .env con tus configuraciones antes de continuar${NC}"
    read -p "Presiona Enter cuando hayas configurado .env..."
fi

# Detener servicios existentes
echo -e "${BLUE}🛑 Deteniendo servicios existentes...${NC}"
docker-compose down --remove-orphans

# Construir imágenes
echo -e "${BLUE}🔨 Construyendo imágenes Docker...${NC}"
docker-compose build --no-cache

# Iniciar servicios
echo -e "${BLUE}🚀 Iniciando servicios MCP...${NC}"
docker-compose up -d

# Esperar a que los servicios estén listos
echo -e "${BLUE}⏳ Esperando servicios...${NC}"
sleep 30

# Verificar salud de servicios
echo -e "${BLUE}🔍 Verificando salud de servicios...${NC}"

services=("nginx-lb:80" "mcp-server:8001" "redis:6379" "postgres:5432")
for service in "${services[@]}"; do
    if docker-compose ps | grep -q "${service%:*}.*Up"; then
        echo -e "${GREEN}✅ ${service%:*} está funcionando${NC}"
    else
        echo -e "${RED}❌ ${service%:*} tiene problemas${NC}"
    fi
done

# Mostrar URLs de acceso
echo ""
echo -e "${GREEN}🎉 Deployment completado! URLs de acceso:${NC}"
echo "=============================================="
echo -e "${BLUE}🌐 API Principal:${NC} http://localhost:80"
echo -e "${BLUE}📚 Swagger UI:${NC} http://localhost:80/docs"
echo -e "${BLUE}📊 Grafana:${NC} http://localhost:3000 (admin/mcpadmin)"
echo -e "${BLUE}📈 Prometheus:${NC} http://localhost:9090"
echo -e "${BLUE}🐳 Portainer:${NC} http://localhost:9000"
echo -e "${BLUE}🔍 Swagger Docs:${NC} http://localhost:8080"
echo ""

# Verificar endpoint principal
echo -e "${BLUE}🔍 Verificando endpoint principal...${NC}"
if curl -s http://localhost:80/health | grep -q "healthy"; then
    echo -e "${GREEN}✅ API funcionando correctamente${NC}"
else
    echo -e "${RED}❌ API no responde correctamente${NC}"
fi

echo ""
echo -e "${GREEN}🎯 MCP Super Root Maestro v2.1.0 desplegado exitosamente${NC}"
echo -e "${BLUE}📋 Para ver logs: docker-compose logs -f${NC}"
echo -e "${BLUE}🛑 Para detener: docker-compose down${NC}"