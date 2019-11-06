import sqlite3
import csv
import math
import os.path

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
    conn = sqlite3.connect(directory_path + "/../../db.sqlite3")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS homepage_school")
    cur.execute("CREATE TABLE homepage_school (name VARCHAR, id INTEGER PRIMARY KEY)")

    filepath = directory_path + "/../School.csv"
    with open(
        filepath, "r", encoding="UTF-8-sig"
    ) as fin:  # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # comma is default delimiter
        to_db = [(i["schoolname"], i["id"]) for i in dr]
    cur.executemany("INSERT INTO homepage_school (name, id) VALUES (?, ?);", to_db)
    conn.commit()
    conn.close()
    print("imported school data")


def importdepartment():
    conn = sqlite3.connect(directory_path + "/../../db.sqlite3")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS homepage_department")
    cur.execute("DROP TABLE IF EXISTS department")
    cur.execute(
        "CREATE TABLE homepage_department (name VARCHAR, school INTEGER, id INTEGER PRIMARY KEY, description VARCHAR)"
    )
    filepath2 = directory_path + "/../Department.csv"
    with open(
        filepath2, "r", encoding="UTF-8-sig"
    ) as fin2:  # `with` statement available in 2.5+
        dr2 = csv.DictReader(fin2)  # comma is default delimiter
        to_db2 = [
            (i["departmentname"], i["School"], i["id"], i["Description"]) for i in dr2
        ]
    cur.executemany(
        "INSERT INTO homepage_department (name, school, id, description) VALUES (?, ?, ?, ?);",
        to_db2,
    )
    conn.commit()
    conn.close()
    print("imported department data")


def importrestaurant():
    conn = sqlite3.connect(directory_path + "/../../db.sqlite3")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS homepage_restaurant")
    cur.execute(
        "CREATE TABLE homepage_restaurant (id INTEGER PRIMNARY KEY, name VARCHAR, cuisine VARCHAR, score INTEGER, borough VARCHAR, building VARCHAR, street VARCHAR, zipcode INTEGER, phone INTEGER, latitude float, longitude float)"  # noqa: E501
    )
    filepath3 = (
        directory_path + "/../DOHMH_New_York_City_Restaurant_Inspection_Results.csv"
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
                    cur.execute(
                        "SELECT COUNT(*) FROM homepage_restaurant WHERE id == "
                        + str(rid)
                    )
                    count = cur.fetchone()
                    if int(count[0]) == 0:
                        cur.execute(
                            "INSERT INTO homepage_restaurant (id, name, cuisine, score, borough, building, street, zipcode, phone, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",  # noqa: E501
                            (
                                i["CAMIS"],
                                i["DBA"],
                                i["CUISINE DESCRIPTION"],
                                i["SCORE"],
                                i["BORO"],
                                i["BUILDING"],
                                i["STREET"],
                                i["ZIPCODE"],
                                i["PHONE"],
                                i["Latitude"],
                                i["Longitude"],
                            ),
                        )
                    else:
                        cur.execute(
                            "SELECT score FROM homepage_restaurant WHERE id == "
                            + str(rid)
                        )
                        score = cur.fetchone()
                        if int(i["SCORE"]) < int(score[0]):
                            cur.execute(
                                "UPDATE homepage_restaurant SET score = "
                                + i["SCORE"]
                                + " WHERE id = "
                                + str(rid)
                            )
    conn.commit()
    conn.close()
    print("imported restaurant data")


def importcuisine():
    conn = sqlite3.connect(directory_path + "/../../db.sqlite3")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS cuisine")
    cur.execute("DROP TABLE IF EXISTS homepage_cuisine")
    cur.execute("CREATE TABLE homepage_cuisine (name VARCHAR, id INTEGER PRIMARY KEY)")
    cur.execute("SELECT DISTINCT cuisine FROM homepage_restaurant")
    count = cur.fetchall()
    id = 0
    for each in count:
        cur.execute(
            "INSERT INTO homepage_cuisine (name, id) VALUES (?, ?)", (each[0], id)
        )
        id = id + 1

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
