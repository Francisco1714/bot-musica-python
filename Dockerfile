# Usa una imagen de Python 3.9 basada en Debian Buster (ligera y estable)
FROM python:3.9-slim-buster

# Instalación de ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copia el archivo requirements.txt (suponiendo que lo tienes en tu proyecto)
COPY requirements.txt .

# Instala las dependencias de tu bot desde el archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del bot en el contenedor
COPY . .

# Comando para ejecutar el bot
CMD ["python", "bot.py"]
