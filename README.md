# 🖥️ Tkinter Mini Projects

A collection of **10 desktop GUI applications** built with Python and Tkinter, ranging from beginner to advanced level.

---

## 📋 Projects Overview

| # | Project | Level | Key Concepts |
|---|---------|-------|--------------|
| 01 | [Calculator](#1-calculator) | 🟢 Beginner | Grid layout, keyboard bindings, StringVar |
| 02 | [Unit Converter](#2-unit-converter) | 🟢 Beginner | Combobox, live conversion with trace |
| 03 | [Quiz App](#3-quiz-app) | 🟢 Beginner | Radiobuttons, Progressbar, messagebox |
| 04 | [Password Generator](#4-password-generator) | 🟡 Medium | Scale, Checkbuttons, right-click context menu |
| 05 | [Flashcard App](#5-flashcard-app) | 🟡 Medium | Canvas card flip, score tracking |
| 06 | [Drawing Board](#6-drawing-board) | 🟡 Medium | Canvas drawing, shapes, colorchooser, file save |
| 07 | [Expense Tracker](#7-expense-tracker) | 🔴 Advanced | Treeview, CSV save/load, dark theme, OOP |
| 08 | [Text Editor](#8-text-editor) | 🔴 Advanced | Full menu system, Find & Replace, status bar |
| 09 | [Snake Game](#9-snake-game) | 🔴 Advanced | Game loop with `after()`, full OOP, animations |
| 10 | [Personal Task Manager](#10-personal-task-manager) | 🔴 Advanced | Treeview, priority/status columns, JSON save/load |

---

## Requirements

```bash
pip install pillow   # required for Drawing Board (screenshot save)
```

All other projects use only Python's standard library — no extra installs needed.

---

## Projects

### 1. Calculator

A clean desktop calculator with full keyboard support.

**Features:**
- Basic arithmetic operations (`+`, `-`, `*`, `/`)
- Keyboard bindings (numbers, operators, Enter, Backspace, Escape)
- Error handling for invalid expressions

![Calculator](screenshots/01_calculator.png)

---

### 2. Unit Converter

Converts between units across multiple categories in real time.

**Features:**
- Categories: Length, Weight, Temperature
- Live conversion as you type (via `StringVar.trace`)
- Clean layout with `ttk.Combobox`

![Unit Converter](screenshots/02_unit_converter.png)

---

### 3. Quiz App

An interactive multiple-choice quiz with score tracking.

**Features:**
- 5 Tkinter-themed questions
- Progress bar showing quiz completion
- Final score popup with `messagebox`

![Quiz App](screenshots/03_quiz_app.png)

---

### 4. Password Generator

Generates secure random passwords with customizable options.

**Features:**
- Adjustable length via slider (6–32 characters)
- Toggle: Uppercase, Digits, Symbols
- Right-click context menu to copy password

![Password Generator](screenshots/04_password_generator.png)

---

### 5. Flashcard App

A study tool for flipping through flashcards with score tracking.

**Features:**
- Animated card flip (question → answer)
- "Know it / Don't know" scoring system
- Next / Previous navigation
- Finish screen with reset option

![Flashcard App](screenshots/05_flashcard_app.png)

---

### 6. Drawing Board

A canvas-based drawing app with shape tools and color picker.

**Features:**
- Tools: Pen, Eraser, Line, Rectangle, Oval
- Color picker with `colorchooser`
- Adjustable brush size
- Save canvas as image (`filedialog` + PIL)

![Drawing Board](screenshots/06_drawing_board.png)

---

### 7. Expense Tracker

A dark-themed expense manager with persistent CSV storage.

**Features:**
- Add, delete, and view expenses in a `ttk.Treeview` table
- Save/load data from CSV file
- Keyboard shortcuts: `Cmd+S` (save), `Cmd+O` (open), `Delete` (remove), `Enter` (add)
- Color-coded dark UI (Catppuccin-inspired theme)

![Expense Tracker](screenshots/07_expense_tracker.png)

---

### 8. Text Editor

A fully functional desktop text editor with rich features.

**Features:**
- File menu: New, Open, Save, Save As
- Edit menu: Undo, Redo, Cut, Copy, Paste
- Format menu: Font family, size, bold, italic
- Find & Replace dialog (separate class)
- Status bar showing line/column count
- Unsaved changes warning on close

![Text Editor](screenshots/08_text_editor.png)

---

### 9. Snake Game

A complete Snake game with animations, difficulty settings, and full OOP design.

**Features:**
- Full OOP architecture: `Snake`, `Food`, `TheGame` classes
- Start screen, game-over screen, and win screen
- Difficulty scale (speed control)
- HUD with score display
- Snake eyes animation
- Background grid
- 6 edge-case bugs fixed

![Snake Game Start](screenshots/09_snake_game_start.png)
![Snake Game Play](screenshots/09_snake_game_play.png)

---

### 10. Personal Task Manager

A feature-rich task manager with priority levels and persistent storage.

**Features:**
- `ttk.Treeview` with Priority and Status columns
- Right-click context menu (edit, delete, mark done)
- `ttk.Notebook` tabs (All / Active / Done)
- Color-coded priorities: High 🔴, Medium 🟠, Low 🟢
- Save/load tasks from JSON file
- Dark purple theme

![Personal Task Manager](screenshots/10_task_manager.png)

---

## 📁 Project Structure

```
tkinter-mini-projects/
├── 1_Calculator/
│   └── Calculator.py
├── 2_Unit_Converter/
│   └── Unit_Converter.py
├── 3_Quiz_App/
│   └── Quiz_App.py
├── 4_Password_Generator/
│   └── Password_Generator.py
├── 5_Flashcard_App/
│   └── Flashcard_App.py
├── 6_Drawing_Board/
│   └── Drawing_Board.py
├── 7_Expense_Tracker/
│   └── Expense_Tracker.py
├── 8_Text_Editor/
│   └── Text_Editor.py
├── 9_Snake_Game/
│   └── Snake_Game.py
├── 10_Personal_Task_Manager/
│   └── TaskManagerApp.py
├── screenshots/
│   └── (add screenshots here)
└── README.md
```

---

## 🚀 How to Run

```bash
# Clone the repo
git clone https://github.com/your-username/tkinter-mini-projects.git
cd tkinter-mini-projects

# Run any project
python 1_Calculator/Calculator.py
```

---

## 🛠️ Built With

- **Python 3.x**
- **Tkinter** — standard GUI library
- **Pillow** — image handling (Drawing Board only)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

Built by **Amirali**
