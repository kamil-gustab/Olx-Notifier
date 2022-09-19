import smtplib
import ssl
from email.message import EmailMessage


def get_passes():
    with open('passes.txt', 'r') as f:
        file = f.readlines()
        recipient = file[0].strip()
        username = file[1].strip()
        password = file[2].strip()

    return recipient, username, password


def send_mail(data):
    recipient_email, sender_email, sender_password = get_passes()

    msg = EmailMessage()
    msg.set_content(f'''
    We found new ad(s) from olx:\n
    Link(s): {data}
    
    Message sent automatically by Olx Notifier.
    Visit project at: https://github.com/kamil-gustab/Olx-Notifier
    ''')

    msg['Subject'] = 'New ad found!'
    msg['From'] = 'Olx Notifier'
    msg['To'] = recipient_email

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)
