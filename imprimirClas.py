import tkinter as tk
from functools import partial

from PIL import Image, ImageTk

import text as tx

'''Mètode per imprimir les entrades de la classificació amb un scrollbar'''
def imprimir_grid(root, clas_frame, type_clas, dorsal=0):
    if type_clas == 1:
        contents = tx.get_all_ranking()
    elif type_clas == 2:
        contents = tx.get_best_rank()
    elif type_clas == 3:
        contents = tx.get_run_one()
    elif type_clas == 4:
        contents = tx.get_runs_player(str(dorsal))

    frame_canvas = tk.Frame(clas_frame)
    frame_canvas.grid_forget()
    frame_canvas = tk.Frame(clas_frame)
    frame_canvas.grid(row=1, columnspan=5, pady=(5, 0), sticky='nsew')
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    frame_canvas.grid_propagate(False)
    frame_canvas['borderwidth'] = 10
    frame_canvas['relief'] = 'sunken'

    canvas = tk.Canvas(frame_canvas)
    canvas.grid(row=0, column=0, sticky="news")

    vsb = tk.Scrollbar(frame_canvas, orient="vertical",
                    command=canvas.yview, bg='#bfe6ff')
    vsb.grid(row=0, column=1, sticky='nswe', ipadx=20)
    canvas.configure(yscrollcommand=vsb.set)

    # Create a frame to contain the buttons
    frame_labels = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_labels, anchor='nw')

    rows = len(contents)
    columns = 5
    labels = [[tk.Label() for j in range(columns)] for i in range(rows)]
    btn = list(range(rows))
    for i in range(0, rows):
        if i < 9:
            pos = '00'
        elif 9 <= i < 99:
            pos = '0'
        else:
            pos = ''
        labels[i][0] = tk.Label(frame_labels, text=pos +
                                                str( i +1), font=("Quicksand", 30))
        labels[i][0].grid(row=i, column=0, padx=20, pady=25)

        dorsal = int(contents[i].dorsal)
        if dorsal < 10:
            output_dorsal = '00'
        elif 10 <= dorsal < 100:
            output_dorsal = '0'
        else:
            output_dorsal = ''
        labels[i][1] = tk.Label(frame_labels, text=output_dorsal +
                                                str(dorsal), font=("Quicksand", 30))
        labels[i][1].grid(row=i, column=1, padx=70, pady=5)

        labels[i][2] = tk.Label(
            frame_labels, text=contents[i].data[:10], font=("Quicksand", 30))
        labels[i][2].grid(row=i, column=2, padx=0, pady=5)

        # cast a int per treure els decimals
        minuts = int(float(contents[i].temps) / 60)
        segons = float(contents[i].temps) % 60
        if minuts < 10:
            output_minuts = '0'
        else:
            output_minuts = ''
        if segons < 10:
            output_segons = '0'
        else:
            output_segons = ''
        labels[i][3] = tk.Label(frame_labels, text=output_minuts + str(minuts) +
                                                ':' + output_segons + str("%.3f" % segons), font=("Quicksand", 30))
        labels[i][3].grid(row=i, column=3, padx=15, pady=5)

        labels[i][4] = tk.Label(frame_labels, text='RUN ' +
                                                contents[i].run_number, font=("Quicksand", 30))
        labels[i][4].grid(row=i, column=4, padx=(10, 10), pady=5)

        cmd = partial(popup_eliminar_run, root, contents[i].dorsal,
                      contents[i].run_number, clas_frame, type_clas, dorsal)
        width = 50
        height = 50

        img = Image.open("/home/pi/Desktop/CronoskiModular/delete.jpg")
        img = img.resize((width ,height), Image.ANTIALIAS)
        photoImg = ImageTk.PhotoImage(img)
        btn[i] = tk.Button(frame_labels, image=photoImg, bg='white', command=cmd)
        btn[i].image = photoImg
        btn[i].grid(row=i, column=5)

    frame_labels.update_idletasks()

    if len(contents) != 0:
        width = sum([labels[0][j].winfo_width() for j in range(0, 5)])
        height = labels[0][0].winfo_height( ) *6 + 200
    else:
        width = 650
        height = 500

    frame_canvas.config(width=width + vsb.winfo_width(),
                        height=height)

    canvas.config(scrollregion=canvas.bbox("all"))


'''Mètode per imprimir la classificiació per la GUI'''
def imprimir_clas(root, clas_frame, type_clas, dorsal=0):
    label1 = tk.Label(clas_frame, text="POS", font=(
        "Quicksand", 35, "bold"), bg="#F5FCFF")
    label1.grid(row=0, column=0, padx=10, pady=15)
    label2 = tk.Label(clas_frame, text="DORSAL", font=(
        "Quicksand", 35, "bold"), bg="#F5FCFF")
    label2.grid(row=0, column=1, padx=20, pady=10)
    label3 = tk.Label(clas_frame, text="DATA", font=(
        "Quicksand", 35, "bold"), bg="#F5FCFF")
    label3.grid(row=0, column=2, padx=35, pady=10)
    label4 = tk.Label(clas_frame, text="TEMPS", font=(
        "Quicksand", 35, "bold"), bg="#F5FCFF")
    label4.grid(row=0, column=3, padx=27, pady=10)
    label5 = tk.Label(clas_frame, text="BAIXADA", font=(
        "Quicksand", 35, "bold"), bg="#F5FCFF")
    label5.grid(row=0, column=4, padx=(10, 60), pady=10)

    imprimir_grid(root, clas_frame, type_clas, dorsal)

'''Mètode que elimina una run i torna a imprimir la classificació'''
def elimina_i_imprimeix(root, dorsal, run_number, clas_frame, type_clas, id):
    tx.delete_single_run(dorsal, run_number)
    imprimir_grid(root, clas_frame, type_clas, id)
    win.destroy()


'''Popup per confimar si vols eliminar la run o no'''
def popup_eliminar_run(root, dorsal, run_number, clas_frame, type_clas, id):
    global win
    win = tk.Toplevel()
    win.wm_title("Cronoski")
    w = 350  # width for the Tk root
    h = 260  # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    win.geometry('%dx%d+%d+%d' % (w, h, x, y))

    lbl = tk.Label(win, text="Estàs segur?", font=("Quicksand", 30))
    lbl.pack(pady=10)
    but = tk.Button(win, text="Sí", command=lambda: elimina_i_imprimeix(root, dorsal, run_number, clas_frame,
                 type_clas, id), padx=25, pady=10, bg='#808080', fg='#00a000', font=("Quicksand", "30", "bold"))
    but.pack(pady=10)
    but = tk.Button(win, text="No", command=win.destroy, padx=15, pady=10,
                 bg='#808080', fg="red", font=("Quicksand", "30", "bold"))
    but.pack(pady=10)