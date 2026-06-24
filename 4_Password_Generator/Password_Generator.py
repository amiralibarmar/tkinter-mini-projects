import tkinter as tk
from tkinter import ttk
import random as ran
import string as st

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("400x320")
        self.root.resizable(False, False)
        
        self.build_ui()
    
    def build_ui(self):
        self.length_var = tk.DoubleVar(value=12)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)
        self.password_var = tk.StringVar()
        
        ttk.Label(self.root, text="Password Length:").pack(pady=(20, 0))
        self.length_display = ttk.Label(self.root, text="12", font=("Helvetica", 22, "bold"))
        self.length_display.pack()
        self.length_var.trace_add("write", lambda *args: self.length_display.config(text=str(round(self.length_var.get()))))
        ttk.Scale(self.root, from_=6, to=32, orient="horizontal", variable=self.length_var, length=300).pack()
        
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)
        ttk.Checkbutton(frame, text="Uppercase", variable=self.use_upper).grid(row=0, column=0, padx=10)
        ttk.Checkbutton(frame, text="Digits", variable=self.use_digits).grid(row=0, column=1, padx=10)
        ttk.Checkbutton(frame, text="Symbols", variable=self.use_symbols).grid(row=0, column=2, padx=10)
        
        ttk.Button(self.root, text="Generate", command=self.generate_password).pack(pady=8)
        
        tk.Entry(self.root, textvariable=self.password_var, state="readonly", width=36, font=("Courier", 13),justify="center").pack(pady=4)
        
        self.copy_btn = ttk.Button(self.root, text="Copy", command=self.copy_to_clipboard)
        self.copy_btn.pack(pady=4)
    
    def generate_password(self):
        pool = st.ascii_lowercase
        
        if self.use_upper.get():
            pool += st.ascii_uppercase
        if self.use_digits.get():
            pool += st.digits
        if self.use_symbols.get():
            pool += st.punctuation
        
        if not pool:
            self.password_var.set("Select at least one option!")
            return
        
        length = int(self.length_var.get())
        password = "".join(ran.choices(pool, k=length))
        self.password_var.set(password)
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if not password:
            return
        
        self.root.clipboard_append(password)
        
        self.copy_btn.config(text="Copied!")
        self.root.after(1500, lambda: self.copy_btn.config(text="Copy"))


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()