FROM python:3.12-slim

# Install dependencies
ADD requirements.txt /
RUN pip install -r requirements.txt --no-cache-dir

# Copy the project into the image
ADD app /app
ADD uvicorn.sh /

# Run with uvicorn
CMD ['/uvicorn.sh']
