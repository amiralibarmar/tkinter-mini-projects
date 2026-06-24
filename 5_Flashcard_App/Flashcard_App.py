import tkinter as tk
from tkinter import ttk, messagebox

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.root.geometry("560x520")
        self.root.resizable(False, False)
        self.root.config(bg="#f0f4f8")
        
        self.cards = [
            {"question": "What is the capital of France?", "answer": "Paris"},
            {"question": "What is 12 x 12?", "answer": "144"},
            {"question": "What language is Tkinter built for?", "answer": "Python"},
            {"question": "What does OOP stand for?", "answer": "Object-Oriented Programming"},
            {"question": "What color is the sky?", "answer": "Blue"},
        ]
        
        self.current = 0
        self.showing_question = True
        
        self.score = 0
        self.answered = 0
        
        self.card_answered = False
        
        self.build_ui()
        
        self.show_card()
    
    def build_ui(self):
        self.canvas = tk.Canvas(self.root, width=500, bg="#f0f4f8", highlightthickness=0)
        self.canvas.pack(pady=40)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 13), padding=10, background="#e5e7eb", foreground="#1f2937", borderwidth=0)
        style.map("TButton", background=[("active", "#d1d5db")])
        style.configure("Flip.TButton", background="#6366f1", foreground="white", borderwidth=0)
        style.map("Flip.TButton", background=[("active", "#4f46e5")])
        
        self.btn_frame = tk.Frame(self.root, bg="#f0f4f8")
        self.btn_frame.pack(pady=10)
        
        ttk.Button(self.btn_frame, text="◀ Prev", command=self.prev_card).pack(side="left", padx=10)
        ttk.Button(self.btn_frame, text="Flip 🔄", command=self.flip_card).pack(side="left", padx=10)
        self.next_btn = ttk.Button(self.btn_frame, text="Next ▶", command=self.next_card)
        self.next_btn.pack(side="left", padx=10)
        
        self.finish_btn = ttk.Button(self.btn_frame, text="Finish 🏁", command=self.finish)
        self.finish_btn.pack(in_=self.btn_frame, side="left", padx=10)
        
        score_frame = tk.Frame(self.root, bg="#f0f4f8")
        score_frame.pack(pady=5)
        
        ttk.Button(score_frame, text="✅ Know it", command=self.know_it).pack(side="left", padx=10)
        ttk.Button(score_frame, text="❌ Don't know", command=self.dont_know).pack(side="left", padx=10)
        
        self.score_label = ttk.Label(self.root, text="score: 0 / 0", font=("Helvetica", 13), background="#f0f4f8")
        self.score_label.pack(pady=5)
        
        
    
    def flip_card(self):
        self.showing_question = not self.showing_question
        self.show_card()
    
    def prev_card(self):
        self.current = (self.current - 1) % (len(self.cards))
        self.showing_question = True
        self.show_card()
    
    def next_card(self):
        if not self.showing_question and not self.card_answered:
            self.answered += 1
            self.score_label.config(text=f"Score: {self.score} / {self.answered}")
        self.current = (self.current + 1) % (len(self.cards))
        self.showing_question = True
        self.card_answered = False
        self.show_card()
    
    def show_card(self):
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(20, 20, 480, 280, fill="white", outline="#d1d5db", width=2)
        
        if self.showing_question:
            label = "QUESTION"
            label_color = "#6366f1"
            text = self.cards[self.current]["question"]
        
        else:
            label = "ANSWER"
            label_color = "#10b981"
            text = self.cards[self.current]["answer"]
        
        self.canvas.create_text(250, 60, text=label, font=("Helvetica", 13, "bold"), fill=label_color)
        self.canvas.create_text(250, 160, text=text, font=("Helvetica", 18), fill="#1f2937", width=400)
        
        counter = f"{self.current + 1} / {len(self.cards)}"
        self.canvas.create_text(250, 260, text=counter, font=("Helvetica", 11), fill="#9ca3af")
        
        if self.current == len(self.cards) - 1:
            self.next_btn.config(state="disabled")
            self.finish_btn.config(state="normal")
        else:
            self.next_btn.config(state="normal")
            self.finish_btn.config(state="disabled")
    
    def know_it(self):
        if not self.showing_question:
            self.score += 1
            self.answered += 1
            self.card_answered = True
            self.score_label.config(text=f"Score: {self.score} / {self.answered}")
            if self.current != len(self.cards) - 1:
                self.next_card()
    
    def dont_know(self):
        if not self.showing_question:
            self.answered += 1
            self.card_answered = True
            self.score_label.config(text=f"Score: {self.score} / {self.answered}")
            if self.current != len(self.cards) - 1:
                self.next_card()
    
    def finish(self):
        if self.score == len(self.cards):
            messagebox.showinfo("Perfect!", "Perfect! 🎉\n\nAmazing! You all of them correct!")
            self.reset()
        else:
            retry = messagebox.askyesno("Result", f"Result\n\nYou got {self.score} out of {len(self.cards)}.\nWhant to try again?")
            if retry:
                self.reset()
            else:
                self.root.destroy()
    
    def reset(self):
        self.current = 0
        self.score = 0
        self.answered = 0
        self.showing_question = True
        self.card_answered = False
        self.score_label.config(text="Score: 0 / 0")
        self.show_card()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()