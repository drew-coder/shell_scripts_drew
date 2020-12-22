#!/usr/bin/env python3
import smtplib
from email.message import EmailMessage
from smtplib import SMTP

# Prepare email message with 'email' library. First message format
msg = EmailMessage()
msg.set_content('Hello')  # Send message
msg['Subject'] = 'Content'
msg['From'] = "jojoachim27@gmail.com"
msg['To'] = 'mayaoffsetmatrix@gmail.com'

# Preparing SMTP logins details in variables
user = "ae222cea3d66f3"
password = '3b8ffbf7d5c90f'
sender = 'jojoachim27@gmail.com'
receiver = 'mayaoffsetmatrix@gmail.com'

# Second Message format
message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}

This is a test e-mail message."""

# Port for mailtrap server is 2525 or 587 [or 465 for SSL].
with smtplib.SMTP('smtp.mailtrap.io', 587) as server:  # Create SMTP obj that manages connection to SMTP server.
    server.starttls()  # Add layer of encryption
    server.login(user, password)  # login to the server(mailtrap.com): Username and pwd needed.
    server.send_message(msg)
    print('Mail sent')
