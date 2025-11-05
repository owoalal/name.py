import tkinter as tk

# Basic phonetic mapping (expand as needed)
phonetic_map = {
    "salam": "سلام",
    "kitab": "كتاب",
    "ana": "أنا",
    "anta": "أنت",
    "bint": "بنت",
    "walad": "ولد",
    "hubb": "حب",
    "qalb": "قلب",
    "noor": "نور",
    "hayat": "حياة",
    e# Add more mappings or use lettr-by-letter if preferred
}

def transliterate_text():
    latin_text = entry.get("1.0", tk.END).strip()
    words = latin_text.split()
    result = []

    for word in words:
        arabic_word = phonetic_map.get(word.lower(), word)
        result.append(arabic_word)

    output.delete("1.0", tk.END)
    output.insert(tk.END, ' '.join(result))

# GUI setup
root = tk.Tk()
root.title("Offline Arabic Phonetic Typing (Yamli-style)")
root.geometry("600x400")

tk.Label(root, text="Type in English (Phonetic):").pack()
entry = tk.Text(root, height=5, width=70)
entry.pack()

tk.Button(root, text="Convert to Arabic", command=transliterate_text).pack(pady=10)

tk.Label(root, text="Arabic Output:").pack()
output = tk.Text(root, height=5, width=70)
output.pack()

root.mainloop()
