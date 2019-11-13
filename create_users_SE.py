import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
from user_account.models import LunchNinjaUser  # noqa: E402
from homepage.models import Department, School  # noqa: E402

team_stellar = [
    {
        "username": "yixin",
        "email": "yh3244@nyu.edu",
        "first_name": "Yixin",
        "last_name": "Hu",
    },
    {
        "username": "up293@nyu.edu",
        "email": "up293@nyu.edu",
        "first_name": "Utkarsh",
        "last_name": "Prakash",
    },
    {
        "username": "ss12933@nyu.edu",
        "email": "ss12933@nyu.edu",
        "first_name": "Shaurya",
        "last_name": "Sethi",
    },
    {
        "username": "xh1255@nyu.edu",
        "email": "xh1255@nyu.edu",
        "first_name": "Xinchi",
        "last_name": "Huang",
    },
    {
        "username": "bv640@nyu.edu",
        "email": "bv640@nyu.edu",
        "first_name": "Bhaskar",
        "last_name": "V",
    },
]

software_engineering = [
    {
        "username": "ab7289@nyu.edu",
        "email": "ab7289@nyu.edu",
        "first_name": "Alex",
        "last_name": "Biehl",
    },
    {
        "username": "ah4896@nyu.edu",
        "email": "ah4896@nyu.edu",
        "first_name": "Abdullah",
        "last_name": "Hanif",
    },
    {
        "username": "as10686@nyu.edu",
        "email": "as10686@nyu.edu",
        "first_name": "Abhishek",
        "last_name": "Sharma",
    },
    {
        "username": "ag7335@nyu.edu",
        "email": "ag7335@nyu.edu",
        "first_name": "Ayushi",
        "last_name": "Gupta",
    },
    {
        "username": "cj1436@nyu.edu",
        "email": "cj1436@nyu.edu",
        "first_name": "Chuhan",
        "last_name": "Jin",
    },
    {
        "username": "dbc291@nyu.edu",
        "email": "dbc291@nyu.edu",
        "first_name": "Daisy",
        "last_name": "Crego",
    },
    {
        "username": "dgopstein@nyu.edu",
        "email": "dgopstein@nyu.edu",
        "first_name": "Dan",
        "last_name": "Gopstein",
    },
    {
        "username": "de846@nyu.edu",
        "email": "de846@nyu.edu",
        "first_name": "David",
        "last_name": "Ecker",
    },
    {
        "username": "gc2505@nyu.edu",
        "email": "gc2505@nyu.edu",
        "first_name": "Garima",
        "last_name": "C",
    },
    {
        "username": "jx692@nyu.edu",
        "email": "jx692@nyu.edu",
        "first_name": "Jack",
        "last_name": "Xu",
    },
    {
        "username": "gcivil@nyu.edu",
        "email": "gcivil@nyu.edu",
        "first_name": "Gennadiy",
        "last_name": "Civil",
    },
    {
        "username": "jw6254@nyu.edu",
        "email": "jw6254@nyu.edu",
        "first_name": "Jason",
        "last_name": "Woo",
    },
    {
        "username": "js10853@nyu.edu",
        "email": "js10853@nyu.edu",
        "first_name": "Justin",
        "last_name": " Snider",
    },
    {
        "username": "kss486@nyu.edu",
        "email": "kss486@nyu.edu",
        "first_name": "Kavin",
        "last_name": "Shah",
    },
    {
        "username": "mfl340@nyu.edu",
        "email": "mfl340@nyu.edu",
        "first_name": "Michael",
        "last_name": "Lally",
    },
    {
        "username": "ms11342@nyu.edu",
        "email": "ms11342@nyu.edu",
        "first_name": "M",
        "last_name": "S",
    },
    {
        "username": "mma525@nyu.edu",
        "email": "mma525@nyu.edu",
        "first_name": "Muhammad",
        "last_name": "Afzal",
    },
    {
        "username": "mok232@nyu.edu",
        "email": "mok232@nyu.edu",
        "first_name": "Muhammad",
        "last_name": "Khan",
    },
    {
        "username": "pp2224@nyu.edu",
        "email": "pp2224@nyu.edu",
        "first_name": "Patryk",
        "last_name": "Pietraszko",
    },
    {
        "username": "mks629@nyu.edu",
        "email": "mks629@nyu.edu",
        "first_name": "Melisa",
        "last_name": "Savich",
    },
    {
        "username": "svk304@nyu.edu",
        "email": "svk304@nyu.edu",
        "first_name": "Snehal",
        "last_name": "Kenjale",
    },
    {
        "username": "rri223@nyu.edu",
        "email": "rri223@nyu.edu",
        "first_name": "Rajeev",
        "last_name": "Ilavala",
    },
    {
        "username": "sgg339@nyu.edu",
        "email": "sgg339@nyu.edu",
        "first_name": "Suraj",
        "last_name": "Gaikwad",
    },
    {
        "username": "tt1894@nyu.edu",
        "email": "tt1894@nyu.edu",
        "first_name": "Tara",
        "last_name": "Tran",
    },
    {
        "username": "vs2165@nyu.edu",
        "email": "vs2165@nyu.edu",
        "first_name": "Varsha",
        "last_name": "Sivakumar",
    },
    {
        "username": "vd908@nyu.edu",
        "email": "vd908@nyu.edu",
        "first_name": "Vedanth",
        "last_name": "Dasari",
    },
    {
        "username": "vm1564@nyu.edu",
        "email": "vm1564@nyu.edu",
        "first_name": "Viktor",
        "last_name": "Moros",
    },
    {
        "username": "yfs219@nyu.edu",
        "email": "yfs219@nyu.edu",
        "first_name": "Yi-Fan",
        "last_name": "Shih",
    },
    {
        "username": "yonguk@nyu.edu",
        "email": "yonguk@nyu.edu",
        "first_name": "Yonguk",
        "last_name": "Jeong",
    },
]


# This function generates random users and save them to database
def generateuser(user_info):
    for user in user_info:
        # school
        school = School.objects.get(pk=13).name

        # department
        department = Department.objects.get(pk=284).name
        email = user["email"]
        user = LunchNinjaUser(
            username=email.split("@")[0],
            email=email,
            school=school,
            department=department,
            first_name=user["first_name"],
            last_name=user["last_name"],
            is_active=True,
        )
        print(user.email)
        password = "Stellar123!"
        user.set_password(password)
        user.save()


if __name__ == "__main__":
    generateuser(team_stellar + software_engineering)
