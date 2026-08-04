import re

email = input("Enter Email: ")
password = input("Enter Password: ")
mobile = input("Enter Mobile Number: ")

email_pattern = r'^[A-Za-z][A-Za-z0-9._]*@[A-Za-z]+\.(com|org|edu|net|in)$'
password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%&!])[A-Za-z\d@#$%&!]{8,}$'
mobile_pattern = r'^[6-9]\d{9}$'

if re.match(email_pattern, email):
    print("Valid Email")
else:
    print("Invalid Email")

if re.match(password_pattern, password):
    print("Strong Password")
else:
    print("Weak Password")

if re.match(mobile_pattern, mobile):
    print("Valid Mobile Number")
else:
    print("Invalid Mobile Number")
