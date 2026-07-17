import re

# Input from user
register_no = input("Enter Register Number: ")
email = input("Enter Institutional Email: ")
course_code = input("Enter Course Code: ")
semester = input("Enter Semester (1-8): ")
mobile = input("Enter Mobile Number: ")

status = True

# Register Number Validation (Example: 192472213)
if re.fullmatch(r'\d{9}', register_no):
    print("Register Number: Valid")
else:
    print("Register Number: Invalid")
    status = False

# Institutional Email Validation (Example: student@saveetha.com)
if re.fullmatch(r'[A-Za-z0-9._%+-]+@saveetha\.com', email):
    print("Institutional Email: Valid")
else:
    print("Institutional Email: Invalid")
    status = False

# Course Code Validation (Example: CSE101, AI205)
if re.fullmatch(r'[A-Z]{2,4}\d{3}', course_code):
    print("Course Code: Valid")
else:
    print("Course Code: Invalid")
    status = False

# Semester Validation (1 to 8)
if re.fullmatch(r'[1-8]', semester):
    print("Semester: Valid")
else:
    print("Semester: Invalid")
    status = False

# Mobile Number Validation
if re.fullmatch(r'[6-9]\d{9}', mobile):
    print("Mobile Number: Valid")
else:
    print("Mobile Number: Invalid")
    status = False

# Final Registration Status
print("\n----- Registration Status -----")
if status:
    print("Registration Successful")
else:
    print("Registration Failed")
