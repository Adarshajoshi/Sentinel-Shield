# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed for Spacy/Presidio
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the specific Spacy model required for the NLP engine
RUN python -m spacy download en_core_web_lg

# Copy the rest of your application code
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the application
CMD ["python", "-m", "streamlit", "run", "app/ui.py", "--server.port=8501", "--server.address=0.0.0.0"]