FROM python:3.10.11

WORKDIR /app
COPY requirement.txt .
RUN pip install -r requirement.txt

COPY . .

ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 8000

EXPOSE 8000
ENTRYPOINT [ "flask", "run" ]