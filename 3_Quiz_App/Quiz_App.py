import tkinter as tk
from tkinter import ttk, messagebox

QUESTIONS = [
    {"question": "What does GUI stand for?",
    "options": ["General User Interface", "Graphical User Interface",
                "Global Unified Interface", "None of the above"],
    "answer": 1},
    {"question": "Which widget displays text in Tkinter?",
    "options": ["Button", "Entry", "Label", "Frame"],
    "answer": 2},
    {"question": "What does .pack() do?",
    "options": ["Saves the file", "Places widget in the window",
                "Deletes the widget", "Changes widget color"],
    "answer": 1},
    {"question": "Which variable holds True/False in Tkinter?",
    "options": ["StringVar", "IntVar", "BooleanVar", "DoubleVar"],
    "answer": 2},
    {"question": "What is root.mainloop() for?",
    "options": ["Closes the window", "Keeps the window open and responsive",
                "Creates a new widget", "Saves window settings"],
    "answer": 1},
]


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("500x380")
        self.root.resizable(False, False)
        
        self.questions = QUESTIONS
        self.current = 0
        self.score = 0
        
        self.build_ui()
        self.load_question()
    
    def build_ui(self):
        self.progress = ttk.Progressbar(self.root, length=460, maximum=len(self.questions))
        self.progress.pack(pady=(20, 10))

        self.question_label = tk.Label(self.root, text="", wraplength=440, font=("Arial", 13, "bold"), justify="left")
        self.question_label.pack(padx=20, pady=(10, 20), anchor="w")

        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack(padx=30, anchor="w")

        self.selected = tk.IntVar(value=-1)

        self.submit_btn = ttk.Button(self.root, text="Submit", command=self.submit)
        self.submit_btn.pack(pady=30)

    def load_question(self):
        q = self.questions[self.current]
        
        self.progress["value"] = self.current
        
        self.question_label.config(text=f"Q{self.current + 1}. {q['question']}")
        
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        self.selected.set(-1)
        
        for i, option in enumerate(q["options"]):
            ttk.Radiobutton(self.options_frame, text=option, variable=self.selected, value=i).pack(anchor="w", pady=3)
    
    def submit(self):
        if self.selected.get() == -1:
            messagebox.showerror("No Answer", "Please select an option first!")
            return
        
        correct = self.questions[self.current]["answer"]
        if self.selected.get() == correct:
            self.score += 1
        
        self.current += 1
        
        if self.current < len(self.questions):
            self.load_question()
        else:
            self.show_result()
    
    def show_result(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        self.submit_btn.pack_forget()
        
        self.progress["value"] = len(self.questions)
        
        total = len(self.questions)
        self.question_label.config(text=f"Quiz complete!\n\nYour score: {self.score}/{total}", font=("Arial", 16, "bold"))



if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()