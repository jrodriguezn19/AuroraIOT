FROM python:3.10.6

WORKDIR /AuroraIOT/

COPY . .

RUN pip3 install -r requirements.txt

CMD ["./manage.py", "runserver"]