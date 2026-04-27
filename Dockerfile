FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY .env* ./
COPY electionguide-ai-*.json ./

# Expose port
ENV PORT=8080
EXPOSE 8080

# Run the server
CMD ["python", "backend/main.py"]
