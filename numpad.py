import tkinter as tk
from functools import partial

numpad = 0

'''Funció per correr el teclat numèric'''
def run_numpad(event, ent, root, win):
    global numpad, btn_funcid
    if numpad == 0:
        numpad = 1
        num_pad(ent, root, win)
        btn_funcid = win.bind('<Button-1>', lambda event: close_numpad(event, win))


'''Funció per tancar el teclat numèric'''
def close_numpad(event, win):
    global numpad, btn_funcid
    if numpad == 1:
        boot_num.destroy()
        numpad = 0
        win.unbind('<Button-1>', btn_funcid)


'''Funció que tracta l'event que es crea quan es prem un botó del teclat numèric'''
def click_numpad(btn, ent, win):
    global numpad, btn_funcid
    text = "%s" % btn
    if not text == "Del" and not text == "OK":
        ent.insert(tk.END, text)
    if text == 'Del':
        current = ent.get()[:-1]
        ent.delete(0, tk.END)
        ent.insert(0, current)
    if text == 'OK':
        boot_num.destroy()
        numpad = 0
        win.unbind('<Button-1>', btn_funcid)


'''Mètode que crea el popup amb el teclat numèric'''
def num_pad(ent, root, win):
    global pad, boot_num
    boot_num = tk.Toplevel()
    if (tk.Toplevel.winfo_exists(boot_num)):
        boot_num.destroy()
    boot_num = tk.Toplevel()

    w = 500  # width for the Tk root
    h = 380  # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2) + 100

    boot_num.geometry('%dx%d+%d+%d' % (w, h, x, y))

    lf = tk.LabelFrame(boot_num, text=" numpad ", bd=3, font=("Quicksand", 15))
    lf.pack(padx=15, pady=10)
    btn_list = [
        '7', '8', '9',
        '4', '5', '6',
        '1', '2', '3',
        'Del', '0', 'OK']
    r = 1
    c = 0
    n = 0
    btn = list(range(len(btn_list)))
    for label in btn_list:
        cmd = partial(click_numpad, label, ent, win)
        btn[n] = tk.Button(lf, text=label, width=4, padx=3, pady=3, bd=6, font=('Quicksand', 35, 'bold'),
                           bg='powder blue',
                           activebackground="#ffffff", activeforeground="#000990", relief="raised", command=cmd)
        btn[n].grid(row=r, column=c)
        n += 1
        c += 1
        if c == 3:
            c = 0
            r += 1
