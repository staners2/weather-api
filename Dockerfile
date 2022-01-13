FROM python:3

COPY . ./app/
WORKDIR ./app/

RUN pip3 install -r requirements.txt

EXPOSE 8000/tcp

CMD heroku ps:scale web=1
CMD python3 manage.py runserver 0.0.0.0:8000