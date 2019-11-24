release: rm -f db.sqlite3
release: rm -rf homepage/migrations
release: rm -rf user_account/migrations
release: python datasource/dataprocess/database.py
release: python manage.py makemigrations user_account
release: python manage.py makemigrations homepage
release: python manage.py migrate
web: gunicorn lunchNinja.wsgi --log-file -
