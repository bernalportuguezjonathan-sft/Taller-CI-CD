FROM python:3.8
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY sample_app.py .
COPY templates/ templates/
EXPOSE 5050
CMD ["python", "sample_app.py"]
