queries = {
    "Apple accessories": ("Technology Brand", "iPhone Charger"),
    "Mouse wireless": ("Computer Device", "Bluetooth Mouse"),
    "Java tutorial": ("Programming Language", "Coding Lessons"),
    "Python course": ("Programming Language", "Software Development Training")
}

for query, (sense, result) in queries.items():
    print(query)
    print("Sense:", sense)
    print("Clicked Result:", result)
    print()