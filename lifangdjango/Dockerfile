# docker run -p 8000:8000  server_dev/django​

FROM python:3.11.1-slim

ENV PYTHONUNBUFFERED 1 

RUN apt-get -y update 
RUN apt-get -y install vim

RUN mkdir /srv/lifang_django
ADD . /srv/lifang_django

WORKDIR /srv/lifang_django

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

#python manage.py runserver --settings=lifang_django.settings.local

#CMD ["python", "manage.py", "runserver", "--settings=lifang_django.settings.local", "0.0.0.0:8000"]
