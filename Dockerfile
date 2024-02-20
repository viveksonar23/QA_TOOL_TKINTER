FROM python:3.11
WORKDIR /app

RUN apt-get update -y && apt-get install python3-tk -y
RUN pip install mysql mysql-connector-python
COPY . /app

RUN pip install /app

CMD ["python", "main.py"]
