import tkinter as tk

from PIL import Image, ImageTk

from viewClas1 import *
from viewClas2 import *
from viewClas3 import *
from viewClas4 import *
import numpad as np


class Clas_frame:
    def __init__(self, master, frame_anterior):
        self.master = master
        self.frame = tk.Frame(self.master, width=1024, height=768, bg="#F5FCFF")
        self.frame.pack(fill='both', expand=True)
        title_label_class = tk.Label(self.frame, text="Classificacions", font=(
            "Quicksand", 38, "bold"), bg="#F5FCFF")
        title_label_class.grid(row=0, columnspan=4, pady=(100, 70))

        width = 120
        height = 120
        img = Image.open("/home/pi/Desktop/CronoskiModular/clas_total.jpeg")
        img = img.resize((width, height), Image.ANTIALIAS)
        photoImg = ImageTk.PhotoImage(img)
        self.button1 = tk.Button(self.frame, text="Classificacio\ntotal", image=photoImg, command=self.windowClas1)
        self.button1.image = photoImg
        self.button1.grid(row=1, column=0, padx=65, pady=60)

        img = Image.open("/home/pi/Desktop/CronoskiModular/clas_millor_run.jpeg")
        img = img.resize((width, height), Image.ANTIALIAS)
        photoImg = ImageTk.PhotoImage(img)
        self.button2 = tk.Button(self.frame, text="Millor run\nde cada player", image=photoImg, command=self.windowClas2)
        self.button2.image = photoImg
        self.button2.grid(row=1, column=1, padx=65, pady=60)

        img = Image.open("/home/pi/Desktop/CronoskiModular/clas_primer_run.jpeg")
        img = img.resize((width, height), Image.ANTIALIAS)
        photoImg = ImageTk.PhotoImage(img)
        self.button3 = tk.Button(self.frame, text="Primer run\nde cada player", image=photoImg, command=self.windowClas3)
        self.button3.image = photoImg
        self.button3.grid(row=1, column=2, padx=65, pady=60)

        img = Image.open("/home/pi/Desktop/CronoskiModular/clas_personal.jpeg")
        img = img.resize((width, height), Image.ANTIALIAS)
        photoImg = ImageTk.PhotoImage(img)
        self.button4 = tk.Button(self.frame, text="Tots els runs\nd'un player", image=photoImg, command=self.popup_dorsal_clas)
        self.button4.image = photoImg
        self.button4.grid(row=1, column=3, padx=65, pady=60)
        self.button6 = tk.Button(self.frame, text="Back", command=lambda: self.frame_back_classificacio(frame_anterior),
                         padx=5, pady=28, width=15, bg="#7AD7F0", fg="white", font=("Quicksand", "18", "bold"))
        self.button6.grid(row=2, columnspan=8, padx=10, pady=40)

    def frame_back_classificacio(self, frame_anterior):
        self.frame.pack_forget()
        frame_anterior.pack(fill='both', expand=True)

    def windowClas1(self):
        self.frame.pack_forget()
        Clas_frame1(self.master, self.frame)

    def windowClas2(self):
        self.frame.pack_forget()
        Clas_frame2(self.master, self.frame)

    def windowClas3(self):
        self.frame.pack_forget()
        Clas_frame3(self.master, self.frame)

    '''Popup per indicar el dorsal del player que volem la classificació'''

    def popup_dorsal_clas(self):
        self.win = tk.Toplevel()
        if (tk.Toplevel.winfo_exists(self.win)):
            self.win.destroy()
        self.win = tk.Toplevel()
        self.win.wm_title("Cronoski")

        self.frame.bind('<Button-1>', lambda event: np.close_numpad(event, self.win), add="+")
        self.frame.bind('<Button-1>', lambda event: self.win.destroy(), add="+")
        self.button1.bind('<Button-1>', lambda event: np.close_numpad(event, self.win), add="+")
        self.button1.bind('<Button-1>', lambda event: self.win.destroy(), add="+")
        self.button2.bind('<Button-1>', lambda event: np.close_numpad(event, self.win), add="+")
        self.button2.bind('<Button-1>', lambda event: self.win.destroy(), add="+")
        self.button3.bind('<Button-1>', lambda event: np.close_numpad(event, self.win), add="+")
        self.button3.bind('<Button-1>', lambda event: self.win.destroy(), add="+")
        self.button4.bind('<Button-1>', lambda event: np.close_numpad(event, self.win), add="+")
        self.button4.bind('<Button-1>', lambda event: self.win.destroy(), add="+")
        self.button6.bind('<Button-1>', lambda event: np.close_numpad(event, self.win), add="+")
        self.button6.bind('<Button-1>', lambda event: self.win.destroy(), add="+")

        w = 500  # width for the Tk root
        h = 300  # height for the Tk root

        # get screen width and height
        ws = self.master.winfo_screenwidth()  # width of the screen
        hs = self.master.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2) - 120

        self.win.geometry('%dx%d+%d+%d' % (w, h, x, y))

        lbl = tk.Label(self.win, text="Escriu el dorsal del player:",
                    font=("Quicksand", 30))
        lbl.pack(pady=(10, 5))
        self.ent = tk.Entry(self.win, font="Quicksand 44 bold", justify="center")
        self.ent.pack(pady=2, ipadx=10, ipady=10)
        self.ent.bind('<Button-1>', lambda event: np.run_numpad(event, self.ent, self.master, self.win))
        but = tk.Button(self.win, text="OK", command=lambda: self.windowClas4(self.ent.get(
        )), padx=10, pady=10, bg='#808080', fg="white", font=("Quicksand", "30", "bold"))
        but.pack()
        self.lbl2 = tk.Label(self.win, text="El dorsal no està entre 1 i 999",
                     fg='Red', font=("Quicksand", 20))
        self.lbl3 = tk.Label(self.win, text="El dorsal no pot estar buit",
                     fg='Red', font=("Quicksand", 20))
        self.win.bind("<Return>", lambda event: self.windowClas4(self.ent.get()))

    def windowClas4(self, id):
        if id != '':
            dorsal = int(id)
            if 1 <= dorsal <= 999:
                self.win.destroy()
                self.frame.pack_forget()
                Clas_frame4(self.master, dorsal, self.frame)
            else:
                self.lbl2.pack(pady=(10, 5))
                self.lbl3.pack_forget()
        else:
            self.lbl3.pack(pady=(10, 5))
            self.lbl2.pack_forget()