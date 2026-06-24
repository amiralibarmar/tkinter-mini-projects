import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)

        self.expression = tk.StringVar()

        display = tk.Entry(
            self.root,
            textvariable=self.expression,
            font=("Arial", 24),
            justify="right",
            bd=10,
            relief="sunken",
            state="readonly"
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew")

        self.build_buttons()
        
        self.root.bind("<Key>", self.key_press)
        self.root.bind("<BackSpace>", self.backspace)
        self.root.bind("<Return>", lambda e: self.button_click("="))
        self.root.bind("<Escape>", lambda e: self.button_click("C"))
        
    def build_buttons(self):          
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "C", "+"],
        ]

        for row_index, row in enumerate(buttons):        
            for col_index, label in enumerate(row):
                btn = tk.Button(
                    self.root,
                    text=label,
                    font=("Arial", 18),
                    width=4,
                    height=2,
                    command=lambda v=label: self.button_click(v)
                )
                btn.grid(row=row_index + 1, column=col_index, sticky="nsew")

        eq_btn = tk.Button(
            self.root,
            text="=",
            font=("Arial", 18),
            width=4,
            height=2,
            command=lambda: self.button_click("=")
        )
        eq_btn.grid(row=5, column=2, columnspan=2, sticky="nsew")
    
    def button_click(self, value):    
        if value == "C":
            self.expression.set("")
        elif value == "=":
            self.calculate()
        else:
            if self.expression.get() in ("Error", "Can't divide by 0"):
                self.expression.set("")
            current = self.expression.get()
            self.expression.set(current + value)
        
    def calculate(self):
        expr = self.expression.get()
        if not expr or expr in ("Error", "Can't divide by 0"):
            return
        try:
            result = eval(expr)
            result = round(result, 10)
            self.expression.set(str(result))
        except ZeroDivisionError:
            self.expression.set("Can't divide by 0")
        except:
            self.expression.set("Error")
        
        
    def key_press(self, event):
        allowed = "0123456789+-*/.="
        if event.char in allowed:
            self.button_click(event.char)
    
    def backspace(self, event):
        current = self.expression.get()
        if current in ("Error", "Can't divide by 0"):
            self.expression.set("")
        else:
            self.expression.set(current[:-1])

root = tk.Tk()
app = Calculator(root)
root.mainloop()