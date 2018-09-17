FROM python:2.7-alpine
COPY ./Hongkong /etc/localtime
WORKDIR /app
ADD . /app
VOLUME ["/app/raw/entry", "/app/upload"]
EXPOSE 8081
CMD ["python", "server.py"]
