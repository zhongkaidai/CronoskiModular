import tkinter as tk

from viewRun import *
from viewClas import *
from PIL import Image
from PIL import ImageTk

class Menu_frame:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Canvas(master, width=1024, height=768)
        self.frame.pack(fill='both', expand=True)

        self.image_ski = Image.open("/home/pi/Desktop/CronoskiModular/ski_tavil.png")
        self.image = self.image_ski.resize((1024, 768), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.image)
        self.panel = tk.Label(self.frame, image=self.img)
        self.panel.place(x=0, y=0)

        self.lbl = tk.Label(self.frame, text="Desconnecta i torna a connectar\nel receptor de senyals i clica OK", font=("Quicksand", 34), padx=10, pady=10)
        self.lbl.place(relx=0.5, rely=0.5, anchor='center')
        self.button = tk.Button(self.frame, text="OK", command=self.mostra, padx=30, pady=30,
                        bg='#808080', fg="white", font=("Quicksand", "40", "bold"))
        self.button.place(relx=0.5, rely=0.7, anchor='center')

    def mostra(self):
        self.lbl.place_forget()
        self.button.place_forget()
        button1 = tk.Button(self.frame, text="Fer run", command=self.windowRun, pady=24,
                         width=14, bg='#808080', fg="white", font=("Quicksand", "26", "bold"))
        button1.place(x=self.resize(700, 10, 1024), y=self.resize(450, 280, 768))
        button2 = tk.Button(self.frame, text="Veure classificació", command=self.windowClas,
                         padx=19, pady=24, width=14, bg='#808080', fg="white", font=("Quicksand", "26", "bold"))
        button2.place(x=self.resize(700, 235, 1024), y=self.resize(450, 280, 768))
        button3 = tk.Button(self.frame, text="Eliminar dades", command=self.popup_clear, padx=18,
                        pady=24, width=14, bg='#808080', fg="white", font=("Quicksand", "26", "bold"))
        button3.place(x=self.resize(700, 125, 1024), y=self.resize(450, 370, 768))
        button4 = tk.Button(self.frame, text="Exit", command=self.exit, padx=10, pady=24,
                         width=14, bg='#808080', fg="white", font=("Quicksand", "26", "bold"))
        button4.place(x=self.resize(700, 360, 1024), y=self.resize(450, 370, 768))
        button5 = tk.Button(self.frame, text="Exportar a USB", command=self.popup_usb, padx=14,
                         pady=24, width=14, bg='#808080', fg="white", font=("Quicksand", "26", "bold"))
        button5.place(x=self.resize(700, 470, 1024), y=self.resize(450, 280, 768))

    def resize(self, a, b, c):
        return b * c // a

    def windowRun(self):
        self.frame.pack_forget()
        Run_frame(self.master, self.frame)

    def windowClas(self):
        self.frame.pack_forget()
        Clas_frame(self.master, self.frame)

    '''Popup per confirmar si es vol netejar la base de dades'''
    def popup_clear(self):
        self.win = tk.Toplevel()
        self.win.wm_title("Cronoski")
        w = 350  # width for the Tk root
        h = 280  # height for the Tk root

        # get screen width and height
        ws = self.master.winfo_screenwidth()  # width of the screen
        hs = self.master.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        self.win.geometry('%dx%d+%d+%d' % (w, h, x, y))

        lbl = tk.Label(self.win, text="Estàs segur?", font=("Quicksand", 30))
        lbl.pack(pady=10)
        but = tk.Button(self.win, text="Sí", command=self.clear_file, padx=25, pady=10,
                     bg='#808080', fg='#00a000', font=("Quicksand", "30", "bold"))
        but.pack(pady=10)
        but = tk.Button(self.win, text="No", command=self.win.destroy, padx=15, pady=10,
                     bg='#808080', fg="red", font=("Quicksand", "30", "bold"))
        but.pack(pady=10)

    '''Mètode per netejar la base de dades'''
    def clear_file(self):
        tx.clear_file()
        self.win.destroy()

    '''Popup per saber si l'exportació a USB s'ha fet correctament'''
    def popup_usb(self):
        self.win = tk.Toplevel()
        self.win.wm_title("Cronoski")
        w = 300  # width for the Tk root
        h = 180  # height for the Tk root

        # get screen width and height
        ws = self.master.winfo_screenwidth()  # width of the screen
        hs = self.master.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.win.geometry('%dx%d+%d+%d' % (w, h, x, y))

        return_value = tx.export_data_to_usb()
        if (return_value == 0):
            lbl = tk.Label(self.win, text="Còpia exitosa",
                        fg='green', font=("Quicksand", 20), pady=15)
        else:
            lbl = tk.Label(self.win, text="Error, comprova les\ncondicions de l'USB",
                        fg='red', font=("Quicksand", 20))

        lbl.pack(pady=(10, 5))
        but = tk.Button(self.win, text="OK", command=self.win.destroy, padx=10, pady=10,
                    bg='#808080', fg="white", font=("Quicksand", "30", "bold"))
        but.pack()

    '''Mètode per tancar l'aplicació'''
    def exit(self):
        self.master.destroy()
