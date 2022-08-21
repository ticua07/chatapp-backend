FROM python:3.10.6-alpine3.16

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt
EXPOSE 8765
CMD [ "python3", "main.py" ]