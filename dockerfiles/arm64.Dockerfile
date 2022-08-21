FROM --platform=linux/arm/v8 python:alpine

RUN apk add --update-cache
RUN apk add --update alpine-sdk
RUN apk --no-cache --update add build-base linux-headers

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app .

CMD ["python", "./app/main.py"]

