release: sh -c "py manage.py makemigrations rec && py manage.py migrate --noinput"
web: waitress-serve --port=$PORT rec.wsgi:application