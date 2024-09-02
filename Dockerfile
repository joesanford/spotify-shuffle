FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint to the Python interpreter
ENTRYPOINT ["python", "shuffle.py"]

# Default arguments to pass to the script
CMD []
