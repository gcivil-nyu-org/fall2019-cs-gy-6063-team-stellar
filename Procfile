release: python manage.py makemigrations
release: python manage.py migrate --noinput
release: python database.py
web: gunicorn lunchNinja.wsgi --log-file -