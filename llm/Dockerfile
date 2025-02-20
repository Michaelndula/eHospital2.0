# Use a lightweight Python base image
FROM python:3.8-slim-buster

WORKDIR /llm

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "gunicorn", "-b", "0.0.0.0:5000", "--timeout", "60", "app:app" ]