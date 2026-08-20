import re

expression = input("Enter a logical expression: ").strip()

patterns = [
    r'^[A-Za-z]+\([a-zA-Z0-9]+\)$',
    r'^(∀|∃)[a-zA-Z]+\([a-zA-Z0-9]+\)$',
    r'^[A-Za-z]+\([a-zA-Z0-9]+\)\s*(∧|∨|→)\s*[A-Za-z]+\([a-zA-Z0-9]+\)$',
    r'^(∀|∃)[a-zA-Z]+\([a-zA-Z0-9]+\)\s*(→|∧|∨)\s*[A-Za-z]+\([a-zA-Z0-9]+\)$'
]

valid = False

for pattern in patterns:
    if re.fullmatch(pattern, expression):
        valid = True
        break

print("\nFOPC Parser Result")
print("------------------")
print("Expression:", expression)

if valid:
    print("Status: Valid FOPC Expression")

    predicates = re.findall(r'[A-Za-z]+\([a-zA-Z0-9]+\)', expression)

    print("Predicates:")
    for predicate in predicates:
        print("-", predicate)

    variables = re.findall(r'\(([a-zA-Z0-9]+)\)', expression)

    print("Variables/Constants:")
    for value in variables:
        print("-", value)

else:
    print("Status: Invalid FOPC Expression")