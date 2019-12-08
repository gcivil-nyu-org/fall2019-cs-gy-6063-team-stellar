import os
import shutil


def prepare():
    db = "db.sqlite3"
    homepage_migration = "homepage\\migrations"
    user_account = "user_account\\migrations"
    try:
        os.remove(db)
    except Exception:
        pass
    try:
        shutil.rmtree(homepage_migration)
    except Exception:
        pass
    try:
        shutil.rmtree(user_account)
    except Exception:
        pass
    os.system("python datasource/dataprocess/database.py")
    os.system("python manage.py makemigrations homepage")
    os.system("python manage.py makemigrations user_account")
    os.system("python manage.py migrate")
    os.system("python addquestions.py")
    os.system("python create_users.py")
    os.system("python create_userrequests.py")


if __name__ == "__main__":
    prepare()
