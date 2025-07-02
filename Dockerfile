FROM python:3.11-slim

LABEL maintainer="Washdentx <washdentx@gmail.com>"
LABEL description="MCP Super Root Maestro v2.1.0 - 308 Endpoints Cybersecurity Arsenal"
LABEL version="2.1.0"

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV MCP_VERSION=2.1.0
ENV MCP_ENVIRONMENT=production

# Crear usuario no-root
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Cambiar propietario de archivos
RUN chown -R mcpuser:mcpuser /app

# Cambiar a usuario no-root
USER mcpuser

# Exponer puerto
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Comando por defecto
CMD ["python", "mcp-server.py"]