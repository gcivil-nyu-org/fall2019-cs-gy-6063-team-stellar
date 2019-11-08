import sqlite3
import csv
import math
import os.path
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
service = {1: "Daily", 2: "Weekly", 3: "Monthly"}
from homepage.models import School, Department, Cuisine , Restaurant # noqa: E402
directory_path = os.path.dirname(__file__)


# Thanks to https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
def getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the earth in km
    dLat = deg2rad(lat2 - lat1)  # deg2rad below
    dLon = deg2rad(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(deg2rad(lat1)) * math.cos(
        deg2rad(lat2)
    ) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    # Distance in km
    return d


def deg2rad(deg):
    return deg * (math.pi / 180)


def importschool():
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    # cur.execute("DROP TABLE IF EXISTS homepage_school")
    # cur.execute("CREATE TABLE homepage_school (name VARCHAR, id INTEGER PRIMARY KEY)")

    filepath = "datasource/School.csv"
    with open(
            filepath, "r", encoding="UTF-8-sig"
    ) as fin:
        dr = csv.DictReader(fin)  # comma is default delimiter
        for i in dr:
            s = School(name = i["schoolname"], id = i["id"])
            s.save()
    conn.commit()
    conn.close()
    print("imported school data")


def importdepartment():
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    # cur.execute("DROP TABLE IF EXISTS homepage_department")
    # cur.execute(
    #     "CREATE TABLE homepage_department (name VARCHAR, school INTEGER, id INTEGER PRIMARY KEY, description VARCHAR)"
    # )
    filepath2 = "datasource/Department.csv"
    with open(
        filepath2, "r", encoding="UTF-8-sig"
    ) as fin2:  # `with` statement available in 2.5+
        dr2 = csv.DictReader(fin2)  # comma is default delimiter
        for each in dr2:
            s = School.objects.filter(id = each["School"]).first()
            d = Department(name = each["departmentname"], school= s, id = each["id"], description= each["Description"])
            d.save()
    conn.commit()
    conn.close()
    print("imported department data")


def importrestaurant():
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    # cur.execute("DROP TABLE IF EXISTS homepage_restaurant")
    # cur.execute(
    #     "CREATE TABLE homepage_restaurant (id INTEGER PRIMNARY KEY, name VARCHAR, cuisine VARCHAR, score INTEGER, borough VARCHAR, building VARCHAR, street VARCHAR, zipcode INTEGER, phone INTEGER, latitude float, longitude float)"  # noqa: E501
    # )
    filepath3 = (
        "datasource/DOHMH_New_York_City_Restaurant_Inspection_Results.csv"
    )

    with open(
        filepath3, "r", encoding="UTF-8-sig"
    ) as fin3:  # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr3 = csv.DictReader(fin3)  # comma is default delimiter
        lat = [40.694340, 40.729010, 40.737570]
        log = [-73.986110, -73.996470, -73.978070]
        for i in dr3:
            if (
                i["Latitude"] in ("", None)
                or i["Longitude"] in ("", None)
                or i["SCORE"] in ("", None)
            ):
                continue
            rid = int(i["CAMIS"])

            latitude = float(i["Latitude"])
            longitude = float(i["Longitude"])
            score = int(i["SCORE"])
            if score > 30:
                continue
            for j in range(3):
                distance = getDistanceFromLatLonInKm(
                    lat[j], log[j], latitude, longitude
                )
                if distance <= 1.5:
                    count = Restaurant.objects.filter(id = rid).count()
                    if int(count) == 0:
                        r = Restaurant(id = i["CAMIS"], name = i["DBA"], cuisine= i["CUISINE DESCRIPTION"],
                                       score = int(i["SCORE"]), borough= i["BORO"], building= i["BUILDING"],
                                       street= i["STREET"], zipcode= i["ZIPCODE"], phone= i["PHONE"],
                                       latitude= i["Latitude"], longitude = i["Longitude"]
                                       )
                        r.save()
                    else:
                        r = Restaurant.objects.filter(id = rid).first()
                        if int(i["SCORE"]) < r.score:
                            r.score = int(i["SCORE"])
                            r.save()
    conn.commit()
    conn.close()
    print("imported restaurant data")


def importcuisine():
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    # cur.execute("DROP TABLE IF EXISTS homepage_cuisine")
    # cur.execute("CREATE TABLE homepage_cuisine (name VARCHAR, id INTEGER PRIMARY KEY)")
    # cur.execute("SELECT DISTINCT cuisine FROM homepage_restaurant")
    # count = cur.fetchall()
    cuisinelist = Restaurant.objects.values("cuisine").distinct()
    for each in cuisinelist:
        c = Cuisine(name = each)
        c.save()
    conn.commit()
    conn.close()
    print("imported cuisine data")


def main():
    importschool()
    importdepartment()
    importrestaurant()
    importcuisine()
    return ()


main()
