import re

def parse_fopc(expression):
    expression = expression.strip()

    patterns = [
        r'^(∀|∃)?[A-Za-z]+\([a-zA-Z0-9]+\)$',
        r'^(∀|∃)[a-zA-Z]+\([a-zA-Z0-9]+\)\s*(→|∧|∨)\s*[A-Za-z]+\([a-zA-Z0-9]+\)$',
        r'^[A-Za-z]+\([a-zA-Z0-9]+\)\s*(→|∧|∨)\s*[A-Za-z]+\([a-zA-Z0-9]+\)$'
    ]

    for pattern in patterns:
        if re.fullmatch(pattern, expression):
            return True

    return False


def extract_predicates(expression):
    return re.findall(r'[A-Za-z]+\([a-zA-Z0-9]+\)', expression)


def extract_operators(expression):
    return re.findall(r'→|∧|∨', expression)


print("================================")
print("       FOPC PARSER")
print("================================")

expression = input("Enter a logical expression: ")

print("\nFOPC Analysis")
print("----------------------------")
print("Expression:", expression)

if parse_fopc(expression):
    print("Status: Valid FOPC Expression")

    predicates = extract_predicates(expression)
    operators = extract_operators(expression)

    print("\nPredicates:")
    for predicate in predicates:
        print("-", predicate)

    if operators:
        print("\nLogical Operators:")
        for operator in operators:
            print("-", operator)

else:
    print("Status: Invalid FOPC Expression")