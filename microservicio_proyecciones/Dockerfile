FROM python:3.12-slim

# Evita buffers y mejora logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar requirements específicos del microservicio
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el microservicio completo
COPY . .

# Levantar en 0.0.0.0:8001 para que Docker pueda exponerlo
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
