FROM python:3.12-alpine
RUN pip install --upgrade pip
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./app /app
