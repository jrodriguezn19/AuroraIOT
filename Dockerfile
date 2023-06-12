FROM python:3.10.6

#FROM python:3.9.17-slim-bullseye

#FROM python:3.10.12-slim-buster

#55MB 
#FROM python:3.10.12-alpine3.18   

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install python3-dev -y

#Alpine 183 MB
#RUN apk update && add --no-cache python3-dev postgresql-dev gcc musl-dev
#RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

RUN pip3 install --upgrade pip 

# Install pipenv
RUN pip3 install pipenv

# Install application dependencies
#COPY Pipfile Pipfile.lock /app/

# Copy the application files into the image
COPY . /app/

# We use the --system flag so packages are installed into the system python
# and not into a virtualenv. Docker containers don't need virtual environments. 
RUN pipenv install --system --dev
#RUN pip3 install -r requirements.txt

#ENV DJANGO_SETTINGS_MODULE=AuroraIOT.settings.prod

# Expose port 8000 on the container
EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]

#CMD ["gunicorn", "AuroraIOT.wsgi", "0.0.0.0:8000"]