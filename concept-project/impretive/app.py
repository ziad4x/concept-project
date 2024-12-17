# app.py
import tkinter as tk
from gui import FinanceApp

def main():
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
