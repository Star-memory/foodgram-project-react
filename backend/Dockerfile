FROM python:3.9.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "--bind", "0.0.0.0:9001", "foodgram.wsgi"]