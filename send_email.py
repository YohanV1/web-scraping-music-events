import os
import smtplib
import ssl
from email.message import EmailMessage

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    email_message = EmailMessage()
    email_message["Subject"] = "New Event!"
    email_message.set_content(message)

    username = "yohanvvinu@gmail.com"
    password = os.getenv("PASSWORD")

    receiver = "yohanvvinu@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, email_message.as_string())
    print("Email sent!")


if __name__ == '__main__':
    send_email("hi")