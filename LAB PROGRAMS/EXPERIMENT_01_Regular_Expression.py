import re

# Sample text
text = "Natural Language Processing is an exciting field of Artificial Intelligence."

# Pattern to search
pattern = "Language"

# Search for the pattern
result = re.search(pattern, text)

if result:
    print("Word found:", result.group())
else:
    print("Word not found")

# Find all words starting with 'A'
matches = re.findall(r'\bA\w+', text)

print("Words starting with 'A':")
print(matches)