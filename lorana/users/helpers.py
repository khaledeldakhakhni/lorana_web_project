import os
from flask_mail import Message
from lorana import  mail
from flask import  url_for


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Lorana password reset request",
                  sender=os.environ.get('EMAIL_USERNAME'),
                  recipients =[user.email],
                  body=f""" To reset your password visit {url_for('reset_password',token=token ,_external=True)}""")
    mail.send(msg)