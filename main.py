import tkinter as tk
from viewMenu import *

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.title("Cronoski")
    root.geometry("1024x768")
    app = Menu_frame(root)
    root.mainloop()

if __name__ == '__main__':
    main()

