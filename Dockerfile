FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

# set display port to avoid crash
ENV DISPLAY=:99

# install selenium
RUN pip install selenium==3.8.0

ARG PORT
CMD python manage.py cleartables
CMD python manage.py collectstatic
CMD daphne polypoker.asgi:application --port $PORT --bind 0.0.0.0
