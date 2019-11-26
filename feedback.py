import os
import django
from django.core.mail import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import date, timedelta


api_key = "K5_zpUoEf7tPJvKRp6e8UrGB5lLzW6Ik5iFZ4E9xn6PnqafYRSHFGac6QOfdLLw67bj66fDkaZEXXNiHMm65nujAFr3SBNu7PcupsYc8_gXI59fsGkH__Z04L-3IXXYx"
headers = {"Authorization": "Bearer %s" % api_key}
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
from homepage.models import UserRequestMatch  # noqa: E402


def compose_email(user1, user2, match):
    html_content = (
        "<p>Hi "
        + user1.first_name
        + ",</p>"
        + "Thank you for using Lunch Ninja!<br>"
        + "Please take a moment to complete our short survey about your most recent lunch experience with <b>"
        + user2.first_name
        + "</b>.<br>"
        + "http://lunch-ninja.herokuapp.com/"
        + "feedback"
        + "/"
        + str(match.id)
        + "-"
        + str(user1.id)
        # + " <button href\"http://127.0.0.1:8000/feedback\" class=\"btn btn-warning\">Take the survey</button><br>"
        + "<br><br>"
        + "Best,<br>"
        + "LunchNinja"
    )
    html_content = html_content + '<p><img src="cid:myimage2" /></p>'
    return html_content


def send_email(html_content, attendee):
    img_data = open("homepage/static/img/ninja.jpg", "rb").read()
    html_part = MIMEMultipart(_subtype="related")
    # body = MIMEText('<p>Hello <img src="cid:myimage" /></p>', _subtype='html')
    body = MIMEText(html_content, _subtype="html")
    html_part.attach(body)
    # Now create the MIME container for the image
    img = MIMEImage(img_data, "jpg")
    img.add_header("Content-Id", "<myimage2>")  # angle brackets are important
    img.add_header("Content-Disposition", "inline", filename="myimage2")
    html_part.attach(img)
    msg = EmailMessage(
        "LunchNinja experience survey", None, "teamstellarse@gmail.com", attendee
    )
    msg.attach(
        html_part
    )  # Attach the raw MIMEBase descendant. This is a public method on EmailMessage
    print("sending out feedback")
    msg.send()


def prepare_feedback():
    # tomorrow = date.today() + timedelta(days=1)
    # Change feedback sending day to today for SE testing day
    tomorrow = date.today()
    # (tz=timezone.get_current_timezone()) + timedelta(1)
    print(tomorrow)
    # yesterday = datetime.strftime(datetime.now() - timedelta(1), "%Y-%m-%d")
    # matches = UserRequestMatch.objects.filer(match_time = yesterday)
    matches = UserRequestMatch.objects.filter(match_time__date=tomorrow)
    for each in matches:
        print(each.id)
        user1 = each.user1
        user2 = each.user2
        html_content1 = compose_email(user1, user2, each)
        html_content2 = compose_email(user2, user1, each)
        to1 = [user1.email]
        to2 = [user2.email]
        send_email(html_content1, to1)
        send_email(html_content2, to2)


prepare_feedback()
