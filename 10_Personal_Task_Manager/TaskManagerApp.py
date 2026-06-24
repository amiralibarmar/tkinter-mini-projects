import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

BG_COLOR    = "#1e1e2e"   
PANEL_COLOR = "#2a2a3e"   
ACCENT      = "#7c3aed"   
TEXT_COLOR  = "#cdd6f4"   
ENTRY_BG    = "#313244"   

HIGH_COLOR  = "#f38ba8"   
MED_COLOR   = "#fab387"   
LOW_COLOR   = "#a6e3a1"   
DONE_COLOR  = "#585b70"   

FONT_TITLE  = ("Helvetica", 18, "bold")
FONT_LABEL  = ("Helvetica", 10, "bold")
FONT_NORMAL = ("Helvetica", 10)
FONT_STATUS = ("Helvetica", 9)

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.configure(bg=BG_COLOR)
        
        self.tasks = []
        self.current_file = None
        self.filtered_indices = []

        self.build_menu()
        self.build_layout()
        self.build_bindings()
    
    def build_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0, bg=PANEL_COLOR, fg=TEXT_COLOR)
        file_menu.add_command(label="New", accelerator="Cmd+N", command=self.new_file)
        file_menu.add_command(label="Open", accelerator="Cmd+O", command=self.load_tasks)
        file_menu.add_command(label="Save", accelerator="Cmd+S", command=self.save_tasks)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        edit_menu = tk.Menu(menubar, tearoff=0, bg=PANEL_COLOR, fg=TEXT_COLOR)
        edit_menu.add_command(label="Delete Task", accelerator="Delete", command=self.delete_task)
        edit_menu.add_command(label="Mark Task", accelerator="Space", command=self.toggle_complete)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0, bg=PANEL_COLOR, fg=TEXT_COLOR)
        help_menu.add_command(label="About", command=lambda:messagebox.showinfo("About", "TaskManager v1.0\nBuilt with Python & Tkinter"))
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def build_layout(self):
        header = tk.Frame(self.root, bg=ACCENT, pady=10)
        header.pack(fill="x")
        
        tk.Label(header, text="📋 Task Manager", font=FONT_TITLE, bg=ACCENT, fg="white").pack()
        
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.left_panel = tk.Frame(main_frame, bg=PANEL_COLOR, width=280, relief="flat")
        self.left_panel.pack(side="left", fill="y", padx=(0, 10))
        self.left_panel.pack_propagate(False)
        
        self.right_panel = tk.Frame(main_frame, bg=PANEL_COLOR)
        self.right_panel.pack(side="left", fill="both", expand=True)
        
        self.status_var = tk.StringVar(value="No tasks yet.")
        status_bar = tk.Label(self.root, textvariable=self.status_var, font=FONT_STATUS, bg=PANEL_COLOR, fg=TEXT_COLOR, anchor="w", padx=10)
        status_bar.pack(fill="x", side="bottom")
        
        self.build_left_panel()
        self.build_right_panel()

    def build_left_panel(self):
        tk.Label(self.left_panel, text="Add New Task", font=FONT_LABEL, bg=PANEL_COLOR, fg=ACCENT).pack(pady=(15, 5))
        
        tk.Label(self.left_panel, text="Task Name:", font=FONT_NORMAL, bg=PANEL_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=15)
        self.task_var = tk.StringVar()
        task_entry = tk.Entry(self.left_panel, textvariable=self.task_var, font=FONT_NORMAL, bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat")
        task_entry.pack(fill="x", padx=15, pady=(0, 10))
        
        tk.Label(self.left_panel, text="Category:", font=FONT_NORMAL, bg=PANEL_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=15)
        self.category_var = tk.StringVar(value="Work")
        for cat in ["Work", "Personal", "Shopping"]:
            tk.Radiobutton(self.left_panel, text=cat, variable=self.category_var, value=cat, font=FONT_NORMAL, bg=PANEL_COLOR, fg=TEXT_COLOR, selectcolor=ENTRY_BG, activebackground=PANEL_COLOR).pack(anchor="w", padx=25)
        
        tk.Label(self.left_panel, text="Priority", font=FONT_NORMAL, bg=PANEL_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=15, pady=(10, 0))
        self.priority_var = tk.StringVar(value="Medium")
        for pri, color in [("High", HIGH_COLOR), ("Medium", MED_COLOR), ("Low", LOW_COLOR)]:
            tk.Radiobutton(self.left_panel, text=pri, variable=self.priority_var, value=pri, font=FONT_NORMAL, bg=PANEL_COLOR, fg=color, selectcolor=ENTRY_BG, activebackground=PANEL_COLOR).pack(anchor="w", padx=25)
        
        add_btn = tk.Label(self.left_panel, text="+ Add Task", font=FONT_LABEL, bg=ACCENT, fg="white", relief="flat", cursor="hand2", pady=8)
        add_btn.pack(fill="x", padx=15, pady=20)
        add_btn.bind("<Button-1>", lambda e:self.add_task())
    
    def build_right_panel(self):
        tk.Label(self.right_panel, text="🔍 Search:", font=FONT_NORMAL, bg=PANEL_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=15, pady=(15, 0))
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_tasks)
        search_entry = tk.Entry(self.right_panel, textvariable=self.search_var, font=FONT_NORMAL, bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat")
        search_entry.pack(fill="x", padx=15, pady=(0, 10))
        
        list_frame = tk.Frame(self.right_panel, bg=PANEL_COLOR)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.task_listbox = tk.Listbox(list_frame, font=FONT_NORMAL, bg=ENTRY_BG, fg=TEXT_COLOR, selectbackground=ACCENT, selectforeground="white", relief="flat", borderwidth=0, yscrollcommand=scrollbar.set)
        self.task_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        legend_frame = tk.Frame(self.right_panel, bg=PANEL_COLOR)
        legend_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        for text, color in [("● High", HIGH_COLOR), ("● Medium", MED_COLOR),("● Low", LOW_COLOR), ("● Done", DONE_COLOR)]:
            tk.Label(legend_frame, text=text, font=FONT_STATUS, bg=PANEL_COLOR, fg=color).pack(side="left", padx=8)
        
        
    def filter_tasks(self, *args):
        query = self.search_var.get().lower()
        self.task_listbox.delete(0, tk.END)
        self.filtered_indices = []

        for i, task in enumerate(self.tasks):
            label = f"[{task['category']}] {task['name']} ({task['priority']})"
            if task['done']:
                label = "✓ " + label

            if query in label.lower():
                self.task_listbox.insert(tk.END, label)
                self.filtered_indices.append(i)

                if task['done']:
                    color = DONE_COLOR
                elif task["priority"] == "High":
                    color = HIGH_COLOR
                elif task['priority'] == "Medium":
                    color = MED_COLOR
                else:
                    color = LOW_COLOR

                self.task_listbox.itemconfig(tk.END, fg=color)
            
    
    def add_task(self):
        name = self.task_var.get().strip()
        if not name:
            messagebox.showwarning("Empty Task", "Please enter a task name!")
            return
        
        task = {
            "name" : name,
            "category" : self.category_var.get(),
            "priority" : self.priority_var.get(),
            "done" : False
        }
        
        self.tasks.append(task)
        self.task_var.set("")
        self.refresh_list()
        
    
    def delete_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a task to delete!")
            return
        index = self.filtered_indices[selection[0]]
        task_name = self.tasks[index]["name"]
        answer = messagebox.askyesno("Delete", f"Delete '{task_name}'?")
        if answer:
            self.tasks.pop(index)
            self.refresh_list()
    
    def toggle_complete(self):
        selection = self.task_listbox.curselection()
        if not selection:
            return
        index = self.filtered_indices[selection[0]]
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self.refresh_list()
    
    def refresh_list(self):
        self.task_listbox.delete(0, tk.END)
        self.filtered_indices = list(range(len(self.tasks)))

        for task in self.tasks:
            label = f"[{task['category']}] {task['name']} ({task['priority']})"
            if task['done']:
                label = '✓ ' + label
            self.task_listbox.insert(tk.END, label)
            
            if task["done"]:
                color = DONE_COLOR
            elif task["priority"] == "High":
                color = HIGH_COLOR
            elif task['priority'] == "Medium":
                color = MED_COLOR
            else:
                color = LOW_COLOR
            
            self.task_listbox.itemconfig(tk.END, fg=color)
        
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t['done'])
        self.status_var.set(f"Total: {total} tasks. |  Done: {done}  | Remaining : {total - done}")

    def new_file(self):
        if self.tasks:
            answer = messagebox.askyesno("New", "Discard all tasks and start fresh?")
            if not answer:
                return
        self.tasks = []
        self.current_file = None
        self.refresh_list()
    
    def save_tasks(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")], title="Save Tasks")
        if not path:
            return
        with open(path, "w") as f:
            json.dump(self.tasks, f, indent=2)
        self.current_file = path
        messagebox.showinfo("Saved", f"Tasks saved to:\n{path}")
    
    def load_tasks(self):
        path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")], title="Open Tasks")
        
        if not path:
            return
        if not os.path.exists(path):
            messagebox.showerror("Error", "File not found!")
            return
        with open(path, "r") as f:
            self.tasks = json.load(f)
        self.current_file = path
        self.refresh_list()
        messagebox.showinfo("Loaded", f"Tasks loaded from\n{path}")
    def build_bindings(self):
        self.root.bind("<Command-n>", lambda e: self.new_file())
        self.root.bind("<Command-o>", lambda e: self.load_tasks())
        self.root.bind("<Command-s>", lambda e: self.save_tasks())
        self.root.bind("<Delete>", lambda e: self.delete_task())
        self.root.bind("<space>", lambda e: self.toggle_complete())
        self.task_listbox.bind("<Double-Button-1>", lambda _: self.toggle_complete())
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    app.run()

