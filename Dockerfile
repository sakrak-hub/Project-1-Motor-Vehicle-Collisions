FROM python:3.13-slim

# Install dependencies
RUN apt-get update && apt-get install -y curl build-essential

# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | bash

# Make sure uv is available
ENV PATH="/root/.local/bin:$PATH"

# Add PYTHONPATH so Python can find 'src'
ENV PYTHONPATH="/app"

# Set workdir
WORKDIR /app

# Install dependencies
RUN uv init
COPY requirements.txt .
RUN uv venv
RUN uv add -r requirements.txt

# Copy the project
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Run the app
CMD ["uv", "run", "main.py"]