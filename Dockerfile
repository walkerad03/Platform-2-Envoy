FROM python:3.11.4

WORKDIR /app

COPY . /app
RUN mkdir -p /app/processed && mkdir -p /app/uploads

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["waitress-serve", "--port=8080", "app:app"]
