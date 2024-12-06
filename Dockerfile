FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update
# установка pip
RUN pip install --upgrade pip

# назначение рабочей дирректории
WORKDIR /app

# Создание папки со статикой
RUN mkdir /app/static

# копирование и установка requirements.txt
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

# копирование всего проекта
COPY /weather .
# запуск проекта
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "weather.wsgi:application"]
