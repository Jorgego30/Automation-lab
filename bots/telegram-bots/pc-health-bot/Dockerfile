# Set the image to run docker
FROM python:3.12-slim

# Set the enviroment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Creates workdir 
WORKDIR /app

# Copy only requirements to optimice layers cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of pc-health-bot code
COPY . .

# Starts the bot
CMD ["python", "main.py"]