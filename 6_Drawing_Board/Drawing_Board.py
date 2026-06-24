import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
from PIL import ImageGrab

class DrawingBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Board")
        self.root.geometry("1100x650")

        # State
        self.current_tool = "pen"
        self.color = "black"
        self.brush_size = 3
        self.start_x = None
        self.start_y = None
        self.temp_item = None

        self.build_toolbar()
        self.build_canvas()

    def build_toolbar(self):
        self.toolbar = ttk.Frame(self.root, padding=5)
        self.toolbar.pack(side="top", fill="x")

        self.tool_buttons = {}
        tools = ["Pen", "Eraser", "Line", "Rectangle", "Oval"]

        for tool in tools:
            btn = tk.Button(
                self.toolbar, text=tool, width=8,
                command=lambda t=tool.lower(): self.set_tool(t)
            )
            btn.pack(side="left", padx=3)
            self.tool_buttons[tool.lower()] = btn

        ttk.Separator(self.toolbar, orient="vertical").pack(side="left", fill="y", padx=6)

        tk.Button(
            self.toolbar, text="Color", width=6,
            command=self.pick_color
        ).pack(side="left", padx=(3, 1))

        self.color_swatch = tk.Label(
            self.toolbar, bg=self.color, width=3, relief="solid", bd=1
        )
        self.color_swatch.pack(side="left", padx=(0, 3))

        ttk.Label(self.toolbar, text="Size:").pack(side="left", padx=(10, 2))
        self.size_label = ttk.Label(self.toolbar, text=str(self.brush_size), width=2)
        self.size_label.pack(side="left", padx=(0, 2))
        
        self.size_slider = ttk.Scale(self.toolbar, from_=1, to=20, orient="horizontal", length=100, command=self.update_brush_size)
        
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side="left")
        
        ttk.Separator(self.toolbar, orient="vertical").pack(side="left", fill="y", padx=6)

        tk.Button(
            self.toolbar, text="Clear", width=6,
            command=lambda: self.canvas.delete("all")
        ).pack(side="left", padx=3)
        
        tk.Button(self.toolbar, text="Save", width=6, command=self.save_image).pack(side="left", padx=3)

        self.set_tool("pen")

    def build_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="white", cursor="crosshair")
        self.canvas.pack(fill="both", expand=True)
        self.bind_events()
    
    def bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
    
    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
    
    def on_drag(self, event):
        x, y = event.x, event.y
        
        if self.current_tool == "pen":
            self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.color, width=self.brush_size, capstyle="round", smooth=True)
            self.start_x, self.start_y = x, y
        elif self.current_tool == "eraser":
            size = self.brush_size * 3
            self.canvas.create_oval(x-size, y-size, x+size, y+size, fill="white", outline="white")
        
        else:
            if self.temp_item:
                self.canvas.delete(self.temp_item)
            
            if self.current_tool == "line":
                self.temp_item = self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.color, width=self.brush_size)
            elif self.current_tool == "rectangle":
                self.temp_item = self.canvas.create_rectangle(self.start_x, self.start_y, x, y, outline=self.color, width=self.brush_size)
            elif self.current_tool == "oval":
                self.temp_item = self.canvas.create_oval(self.start_x, self.start_y, x, y, outline=self.color, width=self.brush_size)
    
    def on_release(self, event):
        self.temp_item = None
        self.start_x = None
        self.start_y = None

    def set_tool(self, tool):
        self.current_tool = tool
        for name, btn in self.tool_buttons.items():
            btn.config(font=("Helvetica", 10), relief="raised")
        self.tool_buttons[tool].config(font=("Helvetica", 10, "bold"), relief="sunken")

    def pick_color(self):
        result = colorchooser.askcolor(color=self.color)
        if result[1]:
            self.color = result[1]
            self.color_swatch.config(bg=self.color)
    
    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*png"), ("All Files", "*.*")], title="Save Drawing")
        
        if not file_path:
            return
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
        img.save(file_path)
    
    def update_brush_size(self, v):
        self.brush_size = int(float(v))
        self.size_label.config(text=str(self.brush_size))


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingBoard(root)
    root.mainloop()