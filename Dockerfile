FROM python:3.12-slim

# Install dependencies
ADD requirements.txt /
RUN pip install -r requirements.txt --no-cache-dir

# Copy the project into the image
ADD demo_server.py /

# Run with uvicorn
ENTRYPOINT ["python","demo_server.py"]
