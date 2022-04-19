FROM python:bullseye

RUN apt-get update
RUN apt-get upgrade
RUN pip install pip -U

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
