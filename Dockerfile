FROM python:3.9.18

WORKDIR /app

COPY ./src/server.py .

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "server.py"]