import tkinter as tk
import imprimirClas as ic

class Clas_frame2:
    def __init__(self, master, frame_anterior):
        self.master = master
        self.frame = tk.Frame(self.master, width=1024, height=768, bg="#F5FCFF")
        self.frame.pack(fill='both', expand=True)

        ic.imprimir_clas(self.master, self.frame, 2)

        button1 = tk.Button(self.frame, text="Back", command=lambda: self.frame_clas_back(frame_anterior), padx=8, pady=28, width=18, bg="#7AD7F0", fg="white", font=("Quicksand", "26", "bold"))
        button1.grid(row=2, columnspan=5, pady=20)

    '''Mètode per tornar al menú de classificació principal des d'un menú de classificació específic'''
    def frame_clas_back(self, frame_anterior):
        self.frame.pack_forget()
        frame_anterior.pack(fill='both', expand=True)