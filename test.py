from email.mime.text import MIMEText
from email.header import Header
import smtplib


def send_email(email, text):
    smtp_host = 'smtp.yandex.ru'
    login, password = 'bshelf.shop@yandex.ru', 'password_to_app'

    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = Header('Заказ', 'utf-8')
    msg['From'] = login
    msg['To'] = email
    sender = smtplib.SMTP(smtp_host, 587)
    sender.set_debuglevel(1)
    sender.starttls()
    sender.login(login, password)
    try:
        sender.sendmail(
        msg['From'], msg['To'], msg.as_string())
    except:
        return 'Error'

print(send_email('nikita.glushin@yandex.ru', 'Привет'))
