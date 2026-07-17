import tkinter as tk
from tkinter import messagebox
from nltk.stem import PorterStemmer

# Create Porter Stemmer object
ps = PorterStemmer()

# Function to stem words
def stem_words():
    text = input_box.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Warning", "Please enter some words.")
        return

    words = text.split()

    output_box.delete("1.0", tk.END)

    output_box.insert(tk.END, "Original Word\t\tStemmed Word\n")
    output_box.insert(tk.END, "-" * 40 + "\n")

    for word in words:
        stemmed = ps.stem(word)
        output_box.insert(tk.END, f"{word:<20}{stemmed}\n")


# Main Window
root = tk.Tk()
root.title("Porter Stemmer - NLP Demo")
root.geometry("700x500")
root.resizable(False, False)

# Heading
heading = tk.Label(
    root,
    text="Porter Stemmer Demonstration",
    font=("Arial", 18, "bold")
)
heading.pack(pady=10)

# Input Label
label1 = tk.Label(
    root,
    text="Enter words separated by spaces:",
    font=("Arial", 12)
)
label1.pack()

# Input Text Box
input_box = tk.Text(root, height=5, width=70, font=("Arial", 11))
input_box.pack(pady=10)

# Button
btn = tk.Button(
    root,
    text="Stem Words",
    font=("Arial", 12, "bold"),
    command=stem_words
)
btn.pack(pady=10)

# Output Label
label2 = tk.Label(
    root,
    text="Output",
    font=("Arial", 12)
)
label2.pack()

# Output Text Box
output_box = tk.Text(root, height=12, width=70, font=("Courier New", 11))
output_box.pack(pady=10)

# Run App
root.mainloop()
