import tkinter as tk
from tkinter import ttk

class UnitConverterApp:
    CONVERSIONS = {
        "Length" : {
            "Meter" : 1,
            "Kilometer" : 1000,
            "Mile" : 1609.34,
            "Foot" : 0.3048,
            "Inch" : 0.0254
        },
        "Weight" : {
            "Kilogram" : 1,
            "Gram" : 0.001,
            "Pound" : 0.453592,
            "Ounce" : 0.0283495
        },
        "Temperature" : {
            "Celsius" : None,
            "Fahrenheit" : None,
            "Kelvin" : None
        },
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("480x280")
        self.root.resizable(False, False)
        self.build_ui()
        style = ttk.Style()
        style.theme_use("aqua")
    
    def build_ui(self):
        top = ttk.Frame(self.root)
        top.pack(fill="x", padx=20, pady=(20, 5))
        
        ttk.Label(top, text="Category:").pack(side="left")
        
        self.category_var = tk.StringVar(value="Length")
        category_combo = ttk.Combobox(top,
                                        textvariable=self.category_var,
                                        values=list(self.CONVERSIONS.keys()),
                                        state="readonly",
                                        width=14)
        category_combo.pack(side="left", padx=10)
        category_combo.bind("<<ComboboxSelected>>", self.on_category_change)
        
        mid = ttk.Frame(self.root)
        mid.pack(fill="x", padx=20, pady=5)
        
        self.input_var = tk.StringVar()
        self.input_var.trace_add("write", self.on_input_change)
        self.from_entry = ttk.Entry(mid, width=8, textvariable=self.input_var)
        self.from_entry.pack(side="left", padx=8)
        
        self.from_unit = ttk.Combobox(mid, state="readonly", width=9)
        self.from_unit.pack(side="left", padx=8)
        self.from_unit.bind("<<ComboboxSelected>>", lambda _: self.convert())
        
        swap_btn = ttk.Button(mid, text="⇄", width=3, command=self.on_swap_units)
        swap_btn.pack(side="left")
        
        self.to_unit = ttk.Combobox(mid, state="readonly", width=9)
        self.to_unit.pack(side="left", padx=8)
        self.to_unit.bind("<<ComboboxSelected>>", lambda _: self.convert())
        
        self.result_var = tk.StringVar(value="Result will appear here")
        ttk.Label(self.root, textvariable=self.result_var, font=("", 13)).pack(pady=5)
        
        ttk.Button(self.root, text="Clear", command=self.clear).pack()
        
        self.on_category_change()
    
    def on_category_change(self, event=None):
        units = list(self.CONVERSIONS[self.category_var.get()].keys())
        self.from_unit["values"] = units
        self.to_unit["values"] = units
        self.from_unit.set(units[0])
        self.to_unit.set(units[1])
        self.result_var.set("Result will appear here")
    
    def on_swap_units(self):
        from_val = self.from_unit.get()
        to_val = self.to_unit.get()
        self.from_unit.set(to_val)
        self.to_unit.set(from_val)
        self.convert()
    
    def convert(self):
        raw = self.from_entry.get().strip()
        
        try:
            value = float(raw)
        except ValueError:
            self.result_var.set("Result will appear here")
            return
        category = self.category_var.get()
        from_u = self.from_unit.get()
        to_u = self.to_unit.get()
        
        if category == "Temperature":
            result = self.convert_temperature(value, from_u, to_u)
        else:
            base = value * self.CONVERSIONS[category][from_u]
            result = base / self.CONVERSIONS[category][to_u]
        
        self.result_var.set(f"{value:g} {from_u} = {result:.4g} {to_u}")
    
    def convert_temperature(self, value, from_u, to_u):
        if from_u == "Fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_u == "Kelvin":
            celsius = value - 273.15
        else:
            celsius = value
        
        if to_u == "Fahrenheit":
            return (celsius * 9 / 5) + 32
        elif to_u == "Kelvin":
            return celsius + 273.15
        else:
            return celsius
    
    def clear(self):
        self.from_entry.delete(0, tk.END)
        self.result_var.set("Result will appear here")
    
    def on_input_change(self, *args):
        self.convert()






if __name__ == "__main__":
    root = tk.Tk()
    UnitConverterApp(root)
    root.mainloop()