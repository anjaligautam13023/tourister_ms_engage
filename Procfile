release: sh -c "python manage.py makemigrations rec && python manage.py migrate --noinput"
web: waitress-serve --port=$PORT rec.wsgi:application