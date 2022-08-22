FROM --platform=linux/arm/v8 python:slim

RUN apt-get update
RUN apt-get install build-essential
#RUN apk --no-cache --update add build-base linux-headers
#RUN apk --no-cache --update add build-base linux-headers

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app .

CMD ["python", "./main.py"]

