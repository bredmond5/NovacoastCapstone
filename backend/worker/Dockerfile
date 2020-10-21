FROM python:3.7

COPY . /opt/app
WORKDIR /opt/app

RUN apt update && apt install -y libgeoip-dev

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "worker.py"]