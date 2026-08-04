import re

text = """Meeting on 12/09/2026
Call 9876543210
#NLP
@OpenAI
natural language processing"""

print("1. Search Date")
print("2. Search Phone Number")
print("3. Search Hashtag")
print("4. Search Mention")
print("5. Search Prefix")
print("6. Search Suffix")

choice = int(input("Enter your choice: "))

if choice == 1:
    result = re.findall(r'\b\d{2}/\d{2}/\d{4}\b', text)
    print(result)

elif choice == 2:
    result = re.findall(r'\b[6-9]\d{9}\b', text)
    print(result)

elif choice == 3:
    result = re.findall(r'#\w+', text)
    print(result)

elif choice == 4:
    result = re.findall(r'@\w+', text)
    print(result)

elif choice == 5:
    prefix = input("Enter Prefix: ")
    result = re.findall(r'\b' + prefix + r'\w*', text, re.IGNORECASE)
    print(result)

elif choice == 6:
    suffix = input("Enter Suffix: ")
    result = re.findall(r'\b\w*' + suffix + r'\b', text, re.IGNORECASE)
    print(result)

else:
    print("Invalid Choice")
