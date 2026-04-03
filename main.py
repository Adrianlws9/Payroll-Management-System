import tkinter as tk
from gui import PayrollSystemGUI

def main():
    root = tk.Tk()
    app = PayrollSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()