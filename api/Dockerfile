# Python image
FROM python:3.9

WORKDIR /app

# Copy application script
COPY main.py /app

# Install dependencies
RUN pip install fastapi uvicorn python-jose requests pyjwt[crypto] 

# Expose port
EXPOSE 8000

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]