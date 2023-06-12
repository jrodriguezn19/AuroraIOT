FROM python:3.10.6

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install python3-dev -y

# Install pipenv
RUN pip3 install --upgrade pip 
RUN pip3 install pipenv

# Install application dependencies
COPY Pipfile Pipfile.lock /app/
# We use the --system flag so packages are installed into the system python
# and not into a virtualenv. Docker containers don't need virtual environments. 
RUN pipenv install --system --dev


#ENV DJANGO_SETTINGS_MODULE=AuroraIOT.settings.prod

# Copy the application files into the image
COPY . /app/

# Expose port 8000 on the container
EXPOSE 8000

#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]

CMD ["gunicorn", "AuroraIOT.wsgi", "0.0.0.0:8000"]