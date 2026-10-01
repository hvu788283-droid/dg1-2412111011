FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser
ENV PORT=5000
EXPOSE 5000
CMD ["python", "app.py"]