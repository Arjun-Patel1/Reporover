# Use a lightweight Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install common libraries so the Agent can use them
RUN pip install --no-cache-dir \
    beautifulsoup4 \
    requests \
    pandas \
    numpy \
    lxml

# Keep the container alive so we can exec commands
CMD ["tail", "-f", "/dev/null"]