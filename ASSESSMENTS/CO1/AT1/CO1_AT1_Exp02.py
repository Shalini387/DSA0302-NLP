import re

# Product List
products = [
    "Laptop",
    "Laptop Bag",
    "Wireless Mouse",
    "Gaming Keyboard",
    "Bluetooth Speaker",
    "Smart Phone",
    "Phone Case",
    "USB Cable",
    "Python Programming Book",
    "Java Programming Book",
    "SQL Guide",
    "Machine Learning Kit"
]

# Function for Product Search
def search_products(keyword):

    print("\nSearch Keyword:", keyword)

    # Exact Search
    exact = [p for p in products if re.fullmatch(keyword, p, re.IGNORECASE)]

    # Prefix Search
    prefix = [p for p in products if re.match(keyword, p, re.IGNORECASE)]

    # Suffix Search
    suffix = [p for p in products if re.search(keyword + r'$', p, re.IGNORECASE)]

    # Partial Search
    partial = [p for p in products if re.search(keyword, p, re.IGNORECASE)]

    print("\nExact Match:")
    print(exact if exact else "No Match")

    print("\nPrefix Match:")
    print(prefix if prefix else "No Match")

    print("\nSuffix Match:")
    print(suffix if suffix else "No Match")

    print("\nPartial Match:")
    print(partial if partial else "No Match")

    # Report
    print("\n------ Search Report ------")
    print("Exact Matches  :", len(exact))
    print("Prefix Matches :", len(prefix))
    print("Suffix Matches :", len(suffix))
    print("Partial Matches:", len(partial))


# User Input
keyword = input("Enter product keyword: ")
search_products(keyword)
