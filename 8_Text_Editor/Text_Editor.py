import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Untitled - Text Editor")
        self.root.geometry("800x600")
        self.file_path = None
        self.is_modified =  False
        self.font_family = "Courier"
        self.font_size = 13
        self.font_bold = False
        self.font_italic = False
        
        self.setup_widgets()
        self.setup_menu()
        self.setup_status_bar()
    
    def setup_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)
        
        self.text_area = tk.Text(frame, wrap="word", undo=True, font=("Courier", 13), padx=6, pady=6)
        
        scrollbar = ttk.Scrollbar(frame, command=self.text_area.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.text_area.pack(side="left", fill="both", expand=True)
        
        self.text_area.config(yscrollcommand=scrollbar.set)
    
    def setup_menu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        self.build_file_menu()
        self.build_edit_menu()
        self.build_format_menu()
    
    def setup_status_bar(self):
        self.status_bar = tk.Label(self.root, text="Words: 0  |  Ln 1, Col 0", anchor="e", padx=6, pady=3)
        self.status_bar.pack(side="bottom", fill="x")
        
        self.text_area.bind("<KeyRelease>", self._on_key)
        self.text_area.bind("<ButtonRelease>", self.update_status)
    
    def build_file_menu(self):
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
    
    def build_edit_menu(self):
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo, accelerator="Cmd+Z")
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo, accelerator="Cmd+Shift+Z")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"), accelerator="Cmd+X")
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"), accelerator="Cmd+C")
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"), accelerator="Cmd+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Cmd+A")
        
        edit_menu.add_separator()
        edit_menu.add_command(label="Find & Replace", command=self.open_find_replace, accelerator="Cmd+F")
        
        self.root.bind("<Command-z>", lambda e: self.text_area.edit_undo())
        self.root.bind("<Command-Z>", lambda e: self.text_area.edit_redo())
        self.root.bind("<Command-a>", lambda e: self.select_all())
        self.root.bind("<Command-f>", lambda e: self.open_find_replace())
    
    def build_format_menu(self):
        format_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Format", menu=format_menu)
        
        format_menu.add_command(label="Font Family", command=self.change_font_family)
        format_menu.add_command(label="Font Size", command=self.change_font_size)
        format_menu.add_separator()
        format_menu.add_command(label="Bold", command=self.toggle_bold)
        format_menu.add_command(label="Italic", command=self.toggle_italic)
    
    def _confirm_discard(self):
        if not self.is_modified:
            return True
        return messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Discard them?")

    def new_file(self):
        if not self._confirm_discard():
            return
        self.text_area.delete("1.0", "end")
        self.file_path = None
        self.is_modified = False
        self.root.title("Untitled - Text Editor")
    
    def open_file(self):
        if not self._confirm_discard():
            return
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        
        if path:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", content)
            self.file_path = path
            self.is_modified = False
            self.root.title(f"{path} - Text Editor")
    
    def save_file(self):
        if self.file_path:
            content = self.text_area.get("1.0", "end-1c")
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.is_modified = False
            self.root.title(f"{self.file_path} - Text Editor")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            self.file_path = path
            self.save_file()
    
    def select_all(self):
        self.text_area.tag_add("sel", "1.0", "end")
        self.text_area.mark_set("insert", "end")
    
    def open_find_replace(self):
        FindReplaceDialog(self)
    
    def apply_font(self):
        style = []
        if self.font_bold:
            style.append("bold")
        if self.font_italic:
            style.append("italic")
        self.text_area.config(font=(self.font_family, self.font_size) if not style else (self.font_family, self.font_size, " ".join(style)))
    
    def change_font_family(self):
        family = simpledialog.askstring("Font Family", "Enter font name:", initialvalue=self.font_family)
        if family:
            self.font_family = family
            self.apply_font()
    
    def change_font_size(self):
        size = simpledialog.askinteger("Font Size", "Enter size:", initialvalue=self.font_size, minvalue=6, maxvalue=72)
        if size:
            self.font_size = size
            self.apply_font()
    
    def toggle_bold(self):
        self.font_bold = not self.font_bold
        self.apply_font()
    
    def toggle_italic(self):
        self.font_italic = not self.font_italic
        self.apply_font()
    
    def _on_key(self, event=None):
        self.is_modified = True
        self.update_status(event)

    def update_status(self, event=None):
        content = self.text_area.get("1.0", "end-1c")
        words = len(content.split()) if content.strip() else 0
        
        position = self.text_area.index("insert")
        line, col = position.split(".")
        
        self.status_bar.config(text=f"Words: {words}  |  Ln {line}, Col {col}")



class FindReplaceDialog:
    def __init__(self, editor):
        self.editor = editor
        self.text_area = editor.text_area
        
        self.window = tk.Toplevel(editor.root)
        self.window.title("Find & Replace")
        self.window.geometry("350x180")
        self.window.resizable(False, False)
        
        self._setup_widgets()
    
    def _setup_widgets(self):
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=2)
        
        tk.Label(self.window, text="Find:").grid(row=0, column=0, padx=8, pady=6, sticky="e")
        self.find_entry = tk.Entry(self.window, width=20)
        self.find_entry.grid(row=0, column=1, padx=8, pady=6, sticky="ew")
        
        tk.Label(self.window, text="Replace:").grid(row=1, column=0, padx=8, pady=6, sticky="e")
        self.replace_entry = tk.Entry(self.window, width=20)
        self.replace_entry.grid(row=1, column=1, padx=8, pady=6, sticky="ew")
        
        btn_frame = tk.Frame(self.window)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=6)
        
        tk.Button(btn_frame, text="Find",        command=self.find).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Replace",     command=self.replace).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Replace All", command=self.replace_all).pack(side="left", padx=4)
    
    def find(self, start="1.0"):
        self.text_area.tag_remove("found", "1.0", "end")
        word = self.find_entry.get()
        if not word:
            return None

        first = None
        idx = "1.0"
        while True:
            idx = self.text_area.search(word, idx, stopindex="end")
            if not idx:
                break
            end = f"{idx}+{len(word)}c"
            self.text_area.tag_add("found", idx, end)
            if first is None:
                first = idx
            idx = end  # move forward past this match

        if first:
            self.text_area.tag_config("found", background="yellow")
            self.text_area.see(first)
            return first
        return None
    
    def replace(self):
        idx = self.find()
        if idx:
            word = self.find_entry.get()
            end = f"{idx}+{len(word)}c"
            self.text_area.delete(idx, end)
            self.text_area.insert(idx, self.replace_entry.get())
    
    def replace_all(self):
        self.text_area.tag_remove("found", "1.0", "end")
        word = self.find_entry.get()
        replacement = self.replace_entry.get()
        if not word:
            return
        start = "1.0"
        while True:
            idx = self.text_area.search(word, start, stopindex="end")
            if not idx:
                break
            end = f"{idx}+{len(word)}c"
            self.text_area.delete(idx, end)
            self.text_area.insert(idx, replacement)
            start = f"{idx}+{len(replacement)}c"



if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()