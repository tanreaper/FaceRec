import smtplib, ssl
import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str

OTP = get_random_string(8)
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "smtp.paul123@gmail.com"
receiver_email = "paulsapto@gmail.com"
password = "Abcd12341!"
message = """\
Subject: OTP

This is your OTP Number: {}""".format(OTP)

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)