FROM python:3.11-bookworm

RUN apt-get update -y
RUN apt-get upgrade -y
RUN pip install pip -U

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
