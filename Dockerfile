# Usa una imagen de Python oficial como base
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios a la imagen
COPY requirements.txt .
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que la aplicación va a correr
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "Index:app", "--host", "0.0.0.0", "--port", "8000"]
