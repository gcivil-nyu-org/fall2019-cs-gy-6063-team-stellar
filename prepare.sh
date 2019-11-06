rm -f db.sqlite3
rm -rf homepage/migrations
rm -rf user_account/migrations
python datasource/dataprocess/database.py
python manage.py makemigrations homepage
python manage.py makemigrations user_account
python manage.py migrate
