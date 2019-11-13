import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
from user_account.models import LunchNinjaUser  # noqa: E402

if __name__ == "__main__":
    user = LunchNinjaUser(
        username="yixin",
        email="yh3244@nyu.edu",
        school="Tandon School of Engineering",
        department="Computer Science",
        first_name="Yixin",
        last_name="Hu",
        is_active=True,
    )
    user.set_password("1234mnbv")
    user.save()
    user2 = LunchNinjaUser(
        username="up293@nyu.edu",
        email="up293@nyu.edu",
        school="Tandon School of Engineering",
        department="Computer Science",
        first_name="Utkarsh",
        last_name="Prakash",
        is_active=True,
    )
    user2.set_password("Stellar123!")
    user2.save()
    user3 = LunchNinjaUser(
        username="ss12933@nyu.edu",
        email="ss12933@nyu.edu",
        school="Tandon School of Engineering",
        department="Computer Science",
        first_name="Shaurya",
        last_name="Sethi",
        is_active=True,
    )
    user3.set_password("Stellar123!")
    user3.save()
    user4 = LunchNinjaUser(
        username="xh1255@nyu.edu",
        email="xh1255@nyu.edu",
        school="Tandon School of Engineering",
        department="Computer Science",
        first_name="Xinchi",
        last_name="Huang",
        is_active=True,
    )
    user4.set_password("Stellar123!")
    user4.save()
    user5 = LunchNinjaUser(
        username="bv640@nyu.edu",
        email="bv640@nyu.edu",
        school="Tandon School of Engineering",
        department="Computer Science",
        first_name="Bhaskar",
        last_name="V",
        is_active=True,
    )
    user5.set_password("Stellar123!")
    user5.save()
    #
    # user6 = LunchNinjaUser(
    #     username="ab7289@nyu.edu",
    #     email="ab7289@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Alex",
    #     last_name="Biehl",
    #     is_active=True,
    # )
    # user6.set_password("1234zxcv")
    # user6.save()
    # user7 = LunchNinjaUser(
    #     username="ah4896@nyu.edu",
    #     email="ah4896@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Abdullah",
    #     last_name="Hanif",
    #     is_active=True,
    # )
    # user7.set_password("1234zxcv")
    # user7.save()
    # user8 = LunchNinjaUser(
    #     username="as10686@nyu.edu",
    #     email="as10686@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Abhishek",
    #     last_name="Sharma",
    #     is_active=True,
    # )
    # user8.set_password("1234zxcv")
    # user8.save()
    # user9 = LunchNinjaUser(
    #     username="ag7335@nyu.edu",
    #     email="ag7335@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Ayushi",
    #     last_name="Gupta",
    #     is_active=True,
    # )
    # user9.set_password("1234zxcv")
    # user9.save()
    # user10 = LunchNinjaUser(
    #     username="cj1436@nyu.edu",
    #     email="cj1436@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Chuhan",
    #     last_name="Jin",
    #     is_active=True,
    # )
    # user10.set_password("1234zxcv")
    # user10.save()
    # user11 = LunchNinjaUser(
    #     username="dbc291@nyu.edu",
    #     email="dbc291@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Daisy",
    #     last_name="Crego",
    #     is_active=True,
    # )
    # user11.set_password("1234zxcv")
    # user11.save()
    # user12 = LunchNinjaUser(
    #     username="dgopstein@nyu.edu",
    #     email="dgopstein@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Dan",
    #     last_name="Gopstein",
    #     is_active=True,
    # )
    # user12.set_password("1234zxcv")
    # user12.save()
    # user13 = LunchNinjaUser(
    #     username="de846@nyu.edu",
    #     email="de846@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="David",
    #     last_name="Ecker",
    #     is_active=True,
    # )
    # user13.set_password("1234zxcv")
    # user13.save()
    # user14 = LunchNinjaUser(
    #     username="gc2505@nyu.edu",
    #     email="gc2505@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Garima",
    #     last_name="C",
    #     is_active=True,
    # )
    # user14.set_password("1234zxcv")
    # user14.save()
    # user15 = LunchNinjaUser(
    #     username="jx692@nyu.edu",
    #     email="jx692@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Jack",
    #     last_name="Xu",
    #     is_active=True,
    # )
    # user15.set_password("1234zxcv")
    # user15.save()
    # user16 = LunchNinjaUser(
    #     username="gcivil@nyu.edu",
    #     email="gcivil@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Gennadiy",
    #     last_name="Civil",
    #     is_active=True,
    # )
    # user16.set_password("1234zxcv")
    # user16.save()
    # user17 = LunchNinjaUser(
    #     username="jw6254@nyu.edu",
    #     email="jw6254@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Jason",
    #     last_name="Woo",
    #     is_active=True,
    # )
    # user17.set_password("1234zxcv")
    # user17.save()
    # user18 = LunchNinjaUser(
    #     username="js10853@nyu.edu",
    #     email="js10853@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Justin",
    #     last_name=" Snider",
    #     is_active=True,
    # )
    # user18.set_password("1234zxcv")
    # user18.save()
    # user19 = LunchNinjaUser(
    #     username="kss486@nyu.edu",
    #     email="kss486@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Kavin",
    #     last_name="Shah",
    #     is_active=True,
    # )
    # user19.set_password("1234zxcv")
    # user19.save()
    # user20 = LunchNinjaUser(
    #     username="mfl340@nyu.edu",
    #     email="mfl340@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Michael",
    #     last_name="Lally",
    #     is_active=True,
    # )
    # user20.set_password("1234zxcv")
    # user20.save()
    # user21 = LunchNinjaUser(
    #     username="ms11342@nyu.edu",
    #     email="ms11342@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="M",
    #     last_name="S",
    #     is_active=True,
    # )
    # user21.set_password("1234zxcv")
    # user21.save()
    # user22 = LunchNinjaUser(
    #     username="mma525@nyu.edu",
    #     email="mma525@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Muhammad",
    #     last_name="Afzal",
    #     is_active=True,
    # )
    # user22.set_password("1234zxcv")
    # user22.save()
    # user23 = LunchNinjaUser(
    #     username="mok232@nyu.edu",
    #     email="mok232@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Muhammad",
    #     last_name="Khan",
    #     is_active=True,
    # )
    # user23.set_password("1234zxcv")
    # user23.save()
    # user24 = LunchNinjaUser(
    #     username="pp2224@nyu.edu",
    #     email="pp2224@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Patryk",
    #     last_name="Pietraszko",
    #     is_active=True,
    # )
    # user24.set_password("1234zxcv")
    # user24.save()
    # user25 = LunchNinjaUser(
    #     username="mks629@nyu.edu",
    #     email="mks629@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Melisa",
    #     last_name="Savich",
    #     is_active=True,
    # )
    # user25.set_password("1234zxcv")
    # user25.save()
    # user26 = LunchNinjaUser(
    #     username="svk304@nyu.edu",
    #     email="svk304@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Snehal",
    #     last_name="Kenjale",
    #     is_active=True,
    # )
    # user26.set_password("1234zxcv")
    # user26.save()
    # user27 = LunchNinjaUser(
    #     username="rri223@nyu.edu",
    #     email="rri223@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Rajeev",
    #     last_name="Ilavala",
    #     is_active=True,
    # )
    # user27.set_password("1234zxcv")
    # user27.save()
    # user28 = LunchNinjaUser(
    #     username="sgg339@nyu.edu",
    #     email="sgg339@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Suraj",
    #     last_name="Gaikwad",
    #     is_active=True,
    # )
    # user28.set_password("1234zxcv")
    # user28.save()
    # user29 = LunchNinjaUser(
    #     username="tt1894@nyu.edu",
    #     email="tt1894@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Tara",
    #     last_name="Tran",
    #     is_active=True,
    # )
    # user29.set_password("1234zxcv")
    # user29.save()
    # user30 = LunchNinjaUser(
    #     username="vs2165@nyu.edu",
    #     email="vs2165@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Varsha",
    #     last_name="Sivakumar",
    #     is_active=True,
    # )
    # user30.set_password("1234zxcv")
    # user30.save()
    # user31 = LunchNinjaUser(
    #     username="vd908@nyu.edu",
    #     email="vd908@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Vedanth",
    #     last_name="Dasari",
    #     is_active=True,
    # )
    # user31.set_password("1234zxcv")
    # user31.save()
    # user32 = LunchNinjaUser(
    #     username="vm1564@nyu.edu",
    #     email="vm1564@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Viktor",
    #     last_name="Moros",
    #     is_active=True,
    # )
    # user32.set_password("1234zxcv")
    # user32.save()
    # user33 = LunchNinjaUser(
    #     username="yfs219@nyu.edu",
    #     email="yfs219@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Yi-Fan",
    #     last_name="Shih",
    #     is_active=True,
    # )
    # user33.set_password("1234zxcv")
    # user33.save()
    # user34 = LunchNinjaUser(
    #     username="yonguk@nyu.edu",
    #     email="yonguk@nyu.edu",
    #     school="Tandon School of Engineering",
    #     department="Computer Science",
    #     first_name="Yonguk",
    #     last_name="Jeong",
    #     is_active=True,
    # )
    # user34.set_password("1234zxcv")
    # user34.save()
    user35 = LunchNinjaUser(
        username="123@nyu.edu",
        email="123@nyu.edu",
        school="Tandon School of Engineering",
        department="Computer Science",
        first_name="first",
        last_name="last",
        is_active=True,
    )
    user35.set_password("Stellar123!")
    user35.save()
