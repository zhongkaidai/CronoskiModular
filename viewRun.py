import tkinter as tk

from PIL import ImageTk, Image
import backend as cs
from entrada import *
import text as tx
import time
import datetime
import numpad as np
import RPi.GPIO as GPIO
import threading


class Run_frame:
    def __init__(self, master, frame_anterior):
        GPIO.setmode(GPIO.BOARD)           # Set's GPIO pins to BCM GPIO numbering
        self.START_PIN = 22          # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
        GPIO.setup(self.START_PIN, GPIO.IN)           # Set our input pin to be an input 
        self.STOP_PIN = 18           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
        GPIO.setup(self.STOP_PIN, GPIO.IN)           # Set our input pin to be an input  
        self.thr = True

        self.master = master
        self.frame = tk.Frame(self.master, width=1024, height=768, bg="#F5FCFF")
        self.frame.pack(fill='both', expand=True)

        self.order = 1

        dorsal_title = tk.Label(self.frame, text="DORSAL",
                             font=("Quicksand", 38, "bold"), bg="#F5FCFF")
        dorsal_title.grid(row=0, column=0, padx=10, pady=30)
        self.lbl_dorsal0 = tk.Label(self.frame, text="", font=(
            "Freemono", 38), bg="#F5FCFF")
        self.lbl_dorsal0.grid(row=1, column=0, pady=26)
        self.lbl_dorsal1 = tk.Label(self.frame, text="", font=(
            "Freemono", 38), bg="#F5FCFF")
        self.lbl_dorsal1.grid(row=2, column=0, pady=26)
        self.lbl_dorsal2 = tk.Label(self.frame, text="", font=(
            "Freemono", 38), bg="#F5FCFF")
        self.lbl_dorsal2.grid(row=3, column=0, pady=26)
        self.lbl_dorsal3 = tk.Label(self.frame, text="", font=(
            "Freemono", 38), bg="#F5FCFF")
        self.lbl_dorsal3.grid(row=4, column=0, pady=26)

        self.pendent = [None] * 4

        self.counter0 = 0
        self.counter1 = 0
        self.counter2 = 0
        self.counter3 = 0
        temps_title = tk.Label(self.frame, text="TEMPS",
                            font=("Quicksand", 38, "bold"), bg="#F5FCFF")
        temps_title.grid(row=0, column=1, padx=65, pady=15)
        self.lbl_temps0 = tk.Label(self.frame, text="", font=(
            "Freemono", 38), bg="#F5FCFF")
        self.lbl_temps0.grid(row=1, column=1, padx=5, pady=35)
        self.lbl_temps1 = tk.Label(self.frame, text="", font=(
            "Freemono", 38), bg="#F5FCFF")
        self.lbl_temps1.grid(row=2, column=1, padx=5, pady=35)
        self.lbl_temps2 = tk.Label(self.frame, text="", font=(
            "Freemono", 38), bg="#F5FCFF")
        self.lbl_temps2.grid(row=3, column=1, padx=5, pady=35)
        self.lbl_temps3 = tk.Label(self.frame, text="", font=(
            "Freemono", 38), bg="#F5FCFF")
        self.lbl_temps3.grid(row=4, column=1, padx=5, pady=35)
        self.lbl_temps3.grid(row=4, column=1)

        run_title = tk.Label(self.frame, text="RUN", font=(
            "Quicksand", 38, "bold"), bg="#F5FCFF")
        run_title.grid(row=0, column=2, padx=30, pady=15)
        self.lbl_run0 = tk.Label(self.frame, text="", font=("Freemono", 38), bg="#F5FCFF")
        self.lbl_run0.grid(row=1, column=2, pady=15)
        self.lbl_run1 = tk.Label(self.frame, text="", font=("Freemono", 38), bg="#F5FCFF")
        self.lbl_run1.grid(row=2, column=2, pady=15)
        self.lbl_run2 = tk.Label(self.frame, text="", font=("Freemono", 38), bg="#F5FCFF")
        self.lbl_run2.grid(row=3, column=2, pady=15)
        self.lbl_run3 = tk.Label(self.frame, text="", font=("Freemono", 38), bg="#F5FCFF")
        self.lbl_run3.grid(row=4, column=2, pady=15)

        class_title = tk.Label(self.frame, text="CLASS",
                            font=("Quicksand", 38, "bold"), bg="#F5FCFF")
        class_title.grid(row=0, column=3, padx=30, pady=15)
        self.lbl_clas0 = tk.Label(self.frame, text="", font=("Freemono", 38), bg="#F5FCFF")
        self.lbl_clas0.grid(row=1, column=3, pady=15)
        self.lbl_clas1 = tk.Label(self.frame, text="", font=("Freemono", 38), bg="#F5FCFF")
        self.lbl_clas1.grid(row=2, column=3, pady=15)
        self.lbl_clas2 = tk.Label(self.frame, text="", font=("Freemono", 38), bg="#F5FCFF")
        self.lbl_clas2.grid(row=3, column=3, pady=15)
        self.lbl_clas3 = tk.Label(self.frame, text="", font=("Freemono", 38), bg="#F5FCFF")
        self.lbl_clas3.grid(row=4, column=3, pady=15)

        self.button1 = tk.Button(self.frame, text="Add", command=self.popup_dorsal_run, padx=8, pady=20,
                         width=14, bg='#808080', fg="white", font=("Quicksand", "26", "bold"))
        self.button1.grid(row=5, column=0, columnspan=2, pady=10)
        self.button2 = tk.Button(self.frame, text="Start", command=lambda: self.start_run(), padx=8, pady=8, width=8, bg='#808080',
                         fg="white", font=("Helvetica", "35", "bold"))
        self.button2.grid(row=5, column=1, pady=(20, 10))
        self.button3 = tk.Button(self.frame, text="Stop", command=lambda: self.stop_run(), padx=8, pady=8, width=8, bg='#808080',
                         fg="white", font=("Helvetica", "35", "bold"))
        self.button3.grid(row=5, column=2, pady=(20, 10))
        self.button4 = tk.Button(self.frame, text="Back", command=lambda: self.frame_back_run(frame_anterior), padx=8, pady=20,
                         width=14, bg="#7AD7F0", fg="white", font=("Quicksand", "26", "bold"))
        self.button4.grid(row=5, column=2, columnspan=2, pady=10)

        width = 65
        height = 65
        img = Image.open("/home/pi/Desktop/CronoskiModular/delete.jpg")
        img = img.resize((width, height), Image.ANTIALIAS)
        photoImg = ImageTk.PhotoImage(img)
        self.button5 = tk.Button(self.frame, image=photoImg, bg='white', command=lambda: self.elim_dorsal(0))
        self.button5.image = photoImg
        self.button5.grid(row=1, column=4, padx=10, pady=(20, 10))
        self.button6 = tk.Button(self.frame, image=photoImg, bg='white', command=lambda: self.elim_dorsal(1))
        self.button6.image = photoImg
        self.button6.grid(row=2, column=4, padx=10, pady=(20, 10))
        self.button7 = tk.Button(self.frame, image=photoImg, bg='white', command=lambda: self.elim_dorsal(2))
        self.button7.image = photoImg
        self.button7.grid(row=3, column=4, padx=10, pady=(20, 10))
        self.button8 = tk.Button(self.frame, image=photoImg, bg='white', command=lambda: self.elim_dorsal(3))
        self.button8.image = photoImg
        self.button8.grid(row=4, column=4, padx=10, pady=(20, 10))

        if self.thr:
            t1 = threading.Thread(target=self.listen, daemon=True)
            t1.start()
            self.thr = False

    '''Mètode que llegeix constantment els pins de start i stop'''
    def listen(self):
        start = GPIO.input(self.START_PIN)
        stop = GPIO.input(self.STOP_PIN)
        while True:
            #print(GPIO.input(self.START_PIN))
            if (GPIO.input(self.START_PIN) != start):
                time.sleep(0.2)
                if (GPIO.input(self.START_PIN) != start):
                    print("Start")
                    self.start_run()
                    start = (start+1)%2
            if (GPIO.input(self.STOP_PIN) != stop):
                time.sleep(0.2)
                if (GPIO.input(self.STOP_PIN) != stop):
                    print("Stop")
                    self.stop_run()
                    stop = (stop+1)%2
            time.sleep(0.3)

    '''Popup per afegir un player introduïnt el dorsal i prement ok'''
    def popup_dorsal_run(self):
        self.win = tk.Toplevel()
        if (tk.Toplevel.winfo_exists(self.win)):
            self.win.destroy()
        self.win = tk.Toplevel()
        self.win.wm_title("Cronoski")

        self.frame.bind('<Button-1>', lambda event: np.close_numpad(event, self.win), add="+")
        self.frame.bind('<Button-1>', lambda event: self.win.destroy(), add="+")
        self.button1.bind('<Button-1>', lambda event: np.close_numpad(event, self.win), add="+")
        self.button1.bind('<Button-1>', lambda event: self.win.destroy(), add="+")
        self.button4.bind('<Button-1>', lambda event: np.close_numpad(event, self.win), add="+")
        self.button4.bind('<Button-1>', lambda event: self.win.destroy(), add="+")
        self.button5.bind('<Button-1>', lambda event: np.close_numpad(event, self.win), add="+")
        self.button5.bind('<Button-1>', lambda event: self.win.destroy(), add="+")
        self.button6.bind('<Button-1>', lambda event: np.close_numpad(event, self.win), add="+")
        self.button6.bind('<Button-1>', lambda event: self.win.destroy(), add="+")
        self.button7.bind('<Button-1>', lambda event: np.close_numpad(event, self.win), add="+")
        self.button7.bind('<Button-1>', lambda event: self.win.destroy(), add="+")
        self.button8.bind('<Button-1>', lambda event: np.close_numpad(event, self.win), add="+")
        self.button8.bind('<Button-1>', lambda event: self.win.destroy(), add="+")

        w = 500  # width for the Tk root
        h = 300  # height for the Tk root

        # get screen width and height
        ws = self.master.winfo_screenwidth()  # width of the screen
        hs = self.master.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2) - 120

        self.win.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.lbl = tk.Label(self.win, text="Escriu el dorsal del player:",
                    font=("Quicksand", 30))
        self.lbl.pack(pady=(10, 5))
        self.ent = tk.Entry(self.win, font="Quicksand 44 bold", justify="center")
        self.ent.pack(pady=2, ipadx=10, ipady=10)
        self.ent.bind('<Button-1>', lambda event: np.run_numpad(event, self.ent, self.master, self.win))
        self.but = tk.Button(self.win, text="OK", command=lambda: self.afegir_dorsal(self.ent.get()),
                     padx=10, pady=10, bg='#808080', fg="white", font=("Quicksand", "30", "bold"))
        self.but.pack()
        self.lbl2 = tk.Label(self.win, text="El dorsal no està entre 1 i 999",
                     fg='Red', font=("Quicksand", 20))
        self.lbl3 = tk.Label(self.win, text="No pot haver dorsals repetits en una mateixa pantalla",
                     fg='Red', font=("Quicksand", 15))
        self.lbl4 = tk.Label(self.win, text="El dorsal no pot estar buit",
                     fg='Red', font=("Quicksand", 20))
        self.win.bind("<Return>", lambda event: self.afegir_dorsal(self.ent.get()))

    '''Retorna true si id(dorsal) està en el vector de pendents, altrament, retorna false'''
    def exists_in_pendent(self, id):
        for i in range(len(self.pendent)):
            if self.pendent[i] is not None and self.pendent[i].dorsal == id:
                return True
        return False


    '''Afegir un dorsal a una entrada donant el dorsal en format string, es guarda en el vector de pendents'''
    def afegir_dorsal(self, text):
        if text != '':
            dorsal = int(text)
            if 1 <= dorsal <= 999:
                if not self.exists_in_pendent(dorsal):
                    pos = cs.primeraPosLliure(self.pendent)
                    if 0 <= pos < 4:
                        next_run = int(tx.get_run_number(text))
                        entrada = Entrada(dorsal)
                        self.pendent[pos] = entrada
                        self.pendent[pos].run = next_run
                        self.pendent[pos].ordre = self.order
                        self.order += 1

                        if next_run < 10:
                            zeros_run = '0'
                        else:
                            zeros_run = ''
                        if pos == 0:
                            self.lbl_dorsal0.configure(text=dorsal)
                            self.lbl_run0.configure(text=zeros_run + str(next_run))
                        elif pos == 1:
                            self.lbl_dorsal1.configure(text=dorsal)
                            self.lbl_run1.configure(text=zeros_run + str(next_run))
                        elif pos == 2:
                            self.lbl_dorsal2.configure(text=dorsal)
                            self.lbl_run2.configure(text=zeros_run + str(next_run))
                        else:
                            self.lbl_dorsal3.configure(text=dorsal)
                            self.lbl_run3.configure(text=zeros_run + str(next_run))
                        print("Entrada afegida a la posicio " + str(pos))
                    self.win.destroy()
                else:
                    self.lbl3.pack(pady=(10, 5))
                    self.lbl2.pack_forget()
                    self.lbl4.pack_forget()
            else:
                self.lbl2.pack(pady=(10, 5))
                self.lbl3.pack_forget()
                self.lbl4.pack_forget()
        else:
            self.lbl4.pack(pady=(10, 5))
            self.lbl2.pack_forget()
            self.lbl3.pack_forget()

    '''Elimina l'entrada de la posició pos[0:3] del vector de pendents'''

    def elim_dorsal(self, pos):
        if self.pendent[pos] is not None:
            self.pendent[pos] = None
            if pos == 0:
                self.counter0 = 0
                self.lbl_dorsal0.configure(text="")
                self.lbl_temps0.configure(text="")
                self.lbl_run0.configure(text="")
                self.lbl_clas0.configure(text="")
            elif pos == 1:
                self.counter1 = 0
                self.lbl_dorsal1.configure(text="")
                self.lbl_temps1.configure(text="")
                self.lbl_run1.configure(text="")
                self.lbl_clas1.configure(text="")
            elif pos == 2:
                self.counter2 = 0
                self.lbl_dorsal2.configure(text="")
                self.lbl_temps2.configure(text="")
                self.lbl_run2.configure(text="")
                self.lbl_clas2.configure(text="")
            else:
                self.counter3 = 0
                self.lbl_dorsal3.configure(text="")
                self.lbl_temps3.configure(text="")
                self.lbl_run3.configure(text="")
                self.lbl_clas3.configure(text="")

            print("Entrada de la posicio " + str(pos) + " eliminada")

    '''Senyal de start a la primera entrada possible, comença a comptar el temps'''

    def start_run(self):
        def start(lbl, pos, super_ini_time0, super_ini_time1, super_ini_time2, super_ini_time3, ini_time0, ini_time1,
                  ini_time2, ini_time3):
            if pos != -1:
                if pos == 0:
                    time2 = time.time()
                    if time2 - ini_time0 >= 0.01:
                        self.counter0 = time2 - super_ini_time0
                        ms0 = self.counter0 % 1
                        min0, sec0 = divmod(self.counter0, 60)
                        hr0, min0 = divmod(min0, 60)
                        lbl.config(text=str("%02d:%02d" %
                                            (min0, sec0)) + str("%.3f" % ms0)[1:])
                        if self.pendent[pos] is not None:
                            if self.pendent[pos].estat != "stop":
                                ini_time0 = time2
                                lbl.after(10, lambda: start(lbl, pos, super_ini_time0, super_ini_time1,
                                                            super_ini_time2, super_ini_time3, ini_time0, ini_time1,
                                                            ini_time2, ini_time3))
                            elif self.pendent[pos].estat == "stop":
                                ms0 = self.pendent[pos].temps % 1
                                min0, sec0 = divmod(self.pendent[pos].temps, 60)
                                hr0, min0 = divmod(min0, 60)
                                lbl.config(text=str("%02d:%02d" %
                                        (min0, sec0)) + str("%.3f" % ms0)[1:])
                                self.counter0 = 0
                        else:
                            self.counter0 = 0
                            self.lbl_temps0.configure(text="")
                    else:
                        lbl.after(10, lambda: start(lbl, pos, super_ini_time0, super_ini_time1,
                                                    super_ini_time2, super_ini_time3, ini_time0, ini_time1, ini_time2,
                                                    ini_time3))

                elif pos == 1:
                    time2_1 = time.time()
                    if time2_1 - ini_time1 >= 0.01:
                        self.counter1 = time2_1 - super_ini_time1
                        ms1 = self.counter1 % 1
                        min1, sec1 = divmod(self.counter1, 60)
                        hr1, min1 = divmod(min1, 60)
                        lbl.config(text=str("%02d:%02d" %
                                            (min1, sec1)) + str("%.3f" % ms1)[1:])
                        if self.pendent[pos] is not None:
                            if self.pendent[pos].estat != "stop":
                                ini_time1 = time2_1
                                lbl.after(1, lambda: start(lbl, pos, super_ini_time0, super_ini_time1,
                                                           super_ini_time2, super_ini_time3, ini_time0, ini_time1,
                                                           ini_time2, ini_time3))
                            elif self.pendent[pos].estat == "stop":
                                ms1 = self.pendent[pos].temps % 1
                                min1, sec1 = divmod(self.pendent[pos].temps, 60)
                                hr1, min1 = divmod(min1, 60)
                                lbl.config(text=str("%02d:%02d" %
                                        (min1, sec1)) + str("%.3f" % ms1)[1:])
                                self.counter1 = 0
                        else:
                            self.counter1 = 0
                            self.lbl_temps1.configure(text="")
                    else:
                        lbl.after(10, lambda: start(lbl, pos, super_ini_time0, super_ini_time1,
                                                    super_ini_time2, super_ini_time3, ini_time0, ini_time1, ini_time2,
                                                    ini_time3))

                elif pos == 2:
                    time2_2 = time.time()
                    if time2_2 - ini_time2 >= 0.01:
                        self.counter2 = time2_2 - super_ini_time2
                        ms2 = self.counter2 % 1
                        min2, sec2 = divmod(self.counter2, 60)
                        hr2, min2 = divmod(min2, 60)
                        lbl.config(text=str("%02d:%02d" %
                                            (min2, sec2)) + str("%.3f" % ms2)[1:])
                        if self.pendent[pos] is not None:
                            if self.pendent[pos].estat != "stop":
                                ini_time2 = time2_2
                                lbl.after(1, lambda: start(lbl, pos, super_ini_time0, super_ini_time1,
                                                           super_ini_time2, super_ini_time3, ini_time0, ini_time1,
                                                           ini_time2, ini_time3))
                            elif self.pendent[pos].estat == "stop":
                                ms2 = self.pendent[pos].temps % 1
                                min2, sec2 = divmod(self.pendent[pos].temps, 60)
                                hr2, min2 = divmod(min2, 60)
                                lbl.config(text=str("%02d:%02d" %
                                        (min2, sec2)) + str("%.3f" % ms2)[1:])
                                self.counter2 = 0
                        else:
                            self.counter2 = 0
                            self.lbl_temps2.configure(text="")
                    else:
                        lbl.after(10, lambda: start(lbl, pos, super_ini_time0, super_ini_time1,
                                                    super_ini_time2, super_ini_time3, ini_time0, ini_time1, ini_time2,
                                                    ini_time3))

                elif pos == 3:
                    time2_3 = time.time()
                    if time2_3 - ini_time2 >= 0.01:
                        self.counter3 = time2_3 - super_ini_time3
                        ms3 = self.counter3 % 1
                        min3, sec3 = divmod(self.counter3, 60)
                        hr3, min3 = divmod(min3, 60)
                        lbl.config(text=str("%02d:%02d" %
                                            (min3, sec3)) + str("%.3f" % ms3)[1:])
                        if self.pendent[pos] is not None:
                            if self.pendent[pos].estat != "stop":
                                ini_time3 = time2_3
                                lbl.after(1, lambda: start(lbl, pos, super_ini_time0, super_ini_time1,
                                                           super_ini_time2, super_ini_time3, ini_time0, ini_time1,
                                                           ini_time2, ini_time3))
                            elif self.pendent[pos].estat == "stop":
                                ms3 = self.pendent[pos].temps % 1
                                min3, sec3 = divmod(self.pendent[pos].temps, 60)
                                hr3, min3 = divmod(min3, 60)
                                lbl.config(text=str("%02d:%02d" %
                                        (min3, sec3)) + str("%.3f" % ms3)[1:])
                                self.counter3 = 0
                        else:
                            self.counter3 = 0
                            self.lbl_temps3.configure(text="")
                    else:
                        lbl.after(10, lambda: start(lbl, pos, super_ini_time0, super_ini_time1,
                                                    super_ini_time2, super_ini_time3, ini_time0, ini_time1, ini_time2,
                                                    ini_time3))

        pos = cs.primeraPosCreate(self.pendent)
        if pos != -1:
            ini_time0 = ini_time1 = ini_time2 = ini_time3 = super_ini_time0 = super_ini_time1 = super_ini_time2 = super_ini_time3 = 0
            if pos == 0:
                super_ini_time0 = time.time()
                ini_time0 = super_ini_time0
                lbl = self.lbl_temps0
            elif pos == 1:
                super_ini_time1 = time.time()
                ini_time1 = super_ini_time1
                lbl = self.lbl_temps1
            elif pos == 2:
                super_ini_time2 = time.time()
                ini_time2 = super_ini_time2
                lbl = self.lbl_temps2
            elif pos == 3:
                super_ini_time3 = time.time()
                ini_time3 = super_ini_time3
                lbl = self.lbl_temps3
            self.pendent[pos].estat = "start"
            print("Comptador començat en l'entrada " + str(pos))
            start(lbl, pos, super_ini_time0, super_ini_time1, super_ini_time2,
                  super_ini_time3, ini_time0, ini_time1, ini_time2, ini_time3)

    def mesAntic(self):
        if cs.primeraPosStart == -1:
            return -1

        pos = -1
        trobat = False
        antic = 0
        for i in range(len(self.pendent)):
            if not trobat:
                if self.pendent[i] is not None:
                    if self.pendent[i].estat == "start":
                        pos = i
                        antic = self.pendent[i].ordre
                        trobat = True
            else:
                break

        for i in range(len(self.pendent)):
            if i <= pos:
                pass
            else:
                if self.pendent[i] is not None:
                    if self.pendent[i].ordre < antic and self.pendent[i].estat == "start":
                        antic = self.pendent[i].ordre
                        pos = i
        return pos

    '''Senyal de stop a la primera entrada possible, es para el temps i surt per pantalla la classificacio de la run'''

    def stop_run(self):
        pos = self.mesAntic()
        if pos != -1:
            self.pendent[pos].estat = "stop"
            if pos == 0:
                self.pendent[pos].temps = self.counter0-0.8
            elif pos == 1:
                self.pendent[pos].temps = self.counter1-0.8
            elif pos == 2:
                self.pendent[pos].temps = self.counter2-0.8
            elif pos == 3:
                self.pendent[pos].temps = self.counter3-0.8
            dorsal = str(self.pendent[pos].dorsal)
            rnumber = tx.get_run_number(dorsal)
            data = str(datetime.datetime.now())
            temps = str(self.pendent[pos].temps)

            textinput = dorsal + ',' + rnumber + ',' + data + ',' + temps + '\n'
            tx.add_text(textinput)

            for i in range(len(self.pendent)):
                if self.pendent[i] is not None:
                    clas = tx.get_clas(str(self.pendent[i].dorsal), str(self.pendent[i].run))
                    if clas != -1:
                        if clas < 10:
                            zeros_clas = '00'
                        elif 10 <= clas < 100:
                            zeros_clas = '0'
                        else:
                            zeros_clas = ''

                        if i == 0:
                            self.lbl_clas0.configure(text=zeros_clas + str(clas))
                        elif i == 1:
                            self.lbl_clas1.configure(text=zeros_clas + str(clas))
                        elif i == 2:
                            self.lbl_clas2.configure(text=zeros_clas + str(clas))
                        elif i == 3:
                            self.lbl_clas3.configure(text=zeros_clas + str(clas))

            print("Comptador aturat en l'entrada " + str(pos))

    def frame_back_run(self, frame_anterior):
        self.frame.pack_forget()
        frame_anterior.pack()
        #viewMenu.Menu_frame(self.master)