FROM --platform=linux/arm/v8 python:alpine

RUN apt-get update && apt-get install
RUN install -y build-essentials

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app .

CMD ["python", "./app/main.py"]

