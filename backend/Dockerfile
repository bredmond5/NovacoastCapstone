FROM python:latest

ENV FLASK_APP dms
ENV FLASK_RUN_HOST 0.0.0.0

WORKDIR /opt/app

RUN apt update && apt install -y libgeoip-dev

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN chmod u+x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
CMD ["flask", "run"]