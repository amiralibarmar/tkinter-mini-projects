import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

BG       = "#1e1e2e"
SURFACE  = "#313244"
FG       = "#36383e"
ACCENT   = "#89b4fa"
MUTED    = "#6c7086"
GREEN    = "#a6e3a1"
ENTRY_BG = "#181825"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("700x500")
        self.root.configure(bg=BG)

        self._apply_styles()
        self.build_input_frame()
        self.build_table_frame()
        
        self.root.bind("<Command-s>", lambda e: self.save_to_file())
        self.root.bind("<Command-o>", lambda e: self.load_from_file())
        self.root.bind("<Delete>", lambda e: self.delete_expense())
        self.root.bind("<Return>", lambda e: self.add_expense())
        

    def _apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TCombobox",
            fieldbackground=ENTRY_BG, background=SURFACE,
            foreground=FG, selectbackground=ACCENT, selectforeground=BG,
            arrowcolor=ACCENT,
        )
        style.map("TCombobox",
            fieldbackground=[("readonly", ENTRY_BG)],
            foreground=[("readonly", FG)],
        )

        style.configure("Treeview",
            background=ENTRY_BG, foreground=FG,
            fieldbackground=ENTRY_BG, rowheight=26,
        )
        style.configure("Treeview.Heading",
            background=SURFACE, foreground=ACCENT,
            font=("Arial", 10, "bold"), relief="flat",
        )
        style.map("Treeview",
            background=[("selected", ACCENT)],
            foreground=[("selected", BG)],
        )
        style.map("Treeview.Heading",
            background=[("active", SURFACE)],
        )

        style.configure("Vertical.TScrollbar",
            background=SURFACE, troughcolor=ENTRY_BG,
            arrowcolor=ACCENT, bordercolor=BG,
        )

    def _label(self, parent, text):
        return tk.Label(parent, text=text, bg=BG, fg=FG, font=("Arial", 10))

    def _entry(self, parent, width):
        return tk.Entry(parent, width=width, bg=ENTRY_BG, fg=FG,
                        insertbackground=FG, relief="flat",
                        highlightbackground=MUTED, highlightthickness=1,
                        highlightcolor=ACCENT)

    def _button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command,
                        bg=SURFACE, fg=FG, relief="flat",
                        activebackground=ACCENT, activeforeground=BG,
                        padx=10, pady=4, cursor="hand2", font=("Arial", 10))

    def build_input_frame(self):
        self.input_frame = tk.Frame(self.root, bg=BG, padx=10, pady=10)
        self.input_frame.pack(fill="x")

        row1 = tk.Frame(self.input_frame, bg=BG)
        row1.pack(fill="x", pady=(0, 8))

        row2 = tk.Frame(self.input_frame, bg=BG)
        row2.pack(fill="x")

        self._label(row1, "Description:").pack(side="left")
        self.desc_entry = self._entry(row1, 20)
        self.desc_entry.pack(side="left", padx=5)

        self._label(row1, "Amount:").pack(side="left", padx=(10, 0))
        self.amount_entry = self._entry(row1, 10)
        self.amount_entry.pack(side="left", padx=5)

        self._label(row1, "Category:").pack(side="left", padx=(10, 0))
        self.category_var = tk.StringVar(value="Food")
        ttk.Combobox(row1, textvariable=self.category_var, width=10,
                    values=["Food", "Transport", "Bills", "Shopping", "Other"],
                    state="readonly").pack(side="left", padx=5)

        self._label(row2, "Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w", pady=5)
        self.date_entry = self._entry(row2, 15)
        self.date_entry.grid(row=0, column=1, padx=5)

        self._button(row2, "Add Expense", self.add_expense).grid(row=0, column=2, padx=5)
        self._button(row2, "Delete Selected", self.delete_expense).grid(row=0, column=3, padx=5)

        self._button(row2, "Save", self.save_to_file).grid(row=1, column=0, padx=5, pady=4, sticky="w")
        self._button(row2, "Load", self.load_from_file).grid(row=1, column=1, padx=5, pady=4, sticky="w")

    def build_table_frame(self):
        table_frame = tk.Frame(self.root, bg=BG, padx=10, pady=5)
        table_frame.pack(fill="both", expand=True)

        columns = ("Description", "Amount", "Category", "Date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        for column, width in zip(columns, (200, 120, 130, 130)):
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor="center", width=width)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.total_label = tk.Label(self.root, text="Total: $0.00",
                                    font=("Arial", 12, "bold"), anchor="e",
                                    bg=BG, fg=GREEN)
        self.total_label.pack(fill="x", padx=10, pady=5)

    def add_expense(self):
        desc     = self.desc_entry.get().strip()
        amount   = self.amount_entry.get().strip()
        category = self.category_var.get().strip()
        date     = self.date_entry.get().strip()

        if not desc or not amount or not category or not date:
            messagebox.showerror("Missing Info", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Amount must be a number.")
            return

        self.tree.insert("", "end", values=(desc, f"${amount:.2f}", category, date))

        self.desc_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.category_var.set("Food")

        self.update_total()

    def update_total(self):
        total = 0.0
        for row in self.tree.get_children():
            amount = self.tree.item(row)["values"][1]
            total += float(str(amount).replace("$", ""))
        self.total_label.config(text=f"Total: ${total:.2f}")

    def delete_expense(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("No Selection", "Please select a row to delete.")
            return

        for row in selected:
            self.tree.delete(row)

        self.update_total()

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Description", "Amount", "Category", "Date"])
            for row in self.tree.get_children():
                writer.writerow(self.tree.item(row)["values"])

        messagebox.showinfo("Saved", "Expenses saved successfully!")

    def load_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        with open(file_path, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.tree.insert("", "end", values=row)

        self.update_total()
        messagebox.showinfo("Loaded", "Expenses loaded successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()