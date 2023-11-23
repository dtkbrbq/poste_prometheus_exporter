FROM python:alpine

COPY ["app.py", "requirements.txt", "./prometheus/"]
WORKDIR /prometheus

RUN pip install --upgrade pip
RUN apk update && apk add --no-cache py3-pip curl
RUN pip install -r requirements.txt

HEALTHCHECK --interval=60s --timeout=20s --retries=3 CMD curl -sS 127.0.0.1:8080 || exit 1

CMD [ "python3", "./app.py" ]

