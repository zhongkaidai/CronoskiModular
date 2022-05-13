import os
from collections import namedtuple
import getpass
#from typing import Counter
#from typing_extensions import TypeGuard
import shutil as sh
import xlsxwriter

# from matplotlib import colors
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# ------------------------------------------------------------------------------------------------------
# ---------------------------LES FUNCIONS PER A GESTIONAR ELS FITXERS DE TEXT---------------------------
# ------------------------------------------------------------------------------------------------------

user = str(getpass.getuser())
filepath = '\home\pi\Desktop'
# '/Users/'+user+'/Desktop/'
name = 'runData.txt'
pistes_name = 'pistes.txt'
Run = namedtuple('Run', ['dorsal', 'run_number', 'data', 'temps'])
MEDIA_PATH= '/media/pi/'
FILE_PATH= '/home/pi/Desktop/CronoskiModular/runData.txt'
EXCEL_PATH= '/home/pi/Desktop/CronoskiModular/runData.xlsx'

''''Gets a file object in a desired mode.
Recieves the file name, the path is specified 
above. If file non existent it creates a new one.
Mode can indicate append mode or read mode.'''


def get_file(mode, pistes=False):
    if (mode == 'append'):
        mode = 'a+'
    else:
        mode = 'r'
    nom = FILE_PATH  # name
    if pistes:
        nom = pistes_name
    file = open(nom, mode)
    return file


'''Adds text to a file'''


def add_text(text, pistes=False):
    file = get_file('append', pistes)
    file.write(text)
    file.close()


'''Reads contents from a file and returns a list w/ the text
separated by lines.'''


def read_file():
    try:
        file = get_file('read')
    except:
        file = get_file('append')
        file.close()
        file = get_file('read')

    linestring = file.readlines()
    contents = []
    for i in range(len(linestring)):
        fila = linestring[i].split(sep=',')
        lastone = fila[3].replace('\n', '')
        # code modified for pistes consideration
        insert = Run(fila[0], fila[1], fila[2], lastone)
        contents.append(insert)
    file.close()
    return contents


'''Gets the classification, sembla ser que no està 
utilitzada dins de cronosky_new.'''


def get_clas(id, rnumber):
    contents = read_file()
    contents = sorted(contents, key=lambda content: float(content.temps))
    for i in range(len(contents)):
        if contents[i].dorsal == id and contents[i].run_number == rnumber:
            return i + 1
    return -1


'''Gets the next run number for a player'''


def get_run_number(id):
    contents = read_file()
    for i in reversed(range(len(contents))):
        if contents[i].dorsal == id:
            increment = int(contents[i].run_number) + 1
            return str(increment)
    return '1'


'''Clears the txt database file'''


def clear_file():
    pathwname = FILE_PATH  # name
    if os.path.exists(pathwname):
        os.remove(pathwname)
        return 0
    else:
        return -1


'''Gets the full ranking'''


def get_all_ranking():
    contents = read_file()
    contents = sorted(contents, key=lambda content: float(content.temps))
    return contents


'''Gets the number of players'''


def get_number_players():
    contents = read_file()
    max = 0
    for player in contents:
        if int(player.dorsal) > max:
            max = int(player.dorsal)
    return max


'''Gets the best ranking'''


def get_best_rank():
    contents = get_all_ranking()
    max = get_number_players()
    checker = [False] * max
    best = []
    for player in contents:
        num = int(player.dorsal) - 1
        if not checker[num]:
            checker[num] = True
            best.append(player)
    return best


'''Gets the first runs ranked'''


def get_run_one():
    contents = read_file()
    contents = sorted(contents, key=lambda content: (content.run_number, float(content.temps)))
    firstones = []
    i = 0
    while (i < len(contents) and contents[i].run_number == '1'):
        firstones.append(contents[i])
        i += 1
    return firstones


'''Gets the runs of a certain player'''


def get_runs_player(id):
    runs_player = []
    contents = read_file()
    for i in range(len(contents)):
        if (contents[i].dorsal == id):
            runs_player.append(contents[i])
    runs_player = sorted(runs_player, key=lambda run: run.temps)
    return runs_player


'''Writes the contents of runData.txt to runData.xlsx'''


def write_excel(worksheet, contents):
    worksheet.write(0, 0, 'POS')
    worksheet.write(0, 1, 'DORSAL')
    worksheet.write(0, 2, 'DATA')
    worksheet.set_column('C:C', 28)
    worksheet.write(0, 3, 'TEMPS')
    worksheet.set_column('D:D', 12)
    worksheet.write(0, 4, 'BAIXADA')
    row = 1
    col = 0
    for player in contents:
        if row < 10:
            pos = '00'
        elif 10 <= row < 100:
            pos = '0'
        else:
            pos = ''
        worksheet.write(row, col, pos + str(row))

        dorsal = int(player.dorsal)
        if dorsal < 10:
            output_dorsal = '00'
        elif 10 <= dorsal < 100:
            output_dorsal = '0'
        else:
            output_dorsal = ''
        worksheet.write(row, col + 1, output_dorsal + player.dorsal)

        worksheet.write(row, col + 2, player.data)

        minuts = int(float(player.temps) / 60)
        segons = float(player.temps) % 60
        if minuts < 10:
            output_minuts = '0'
        else:
            output_minuts = ''
        if segons < 10:
            output_segons = '0'
        else:
            output_segons = ''
        worksheet.write(row, col + 3, output_minuts + str(minuts) +
                        ':' + output_segons + str("%.3f" % segons))

        worksheet.write(row, col + 4, 'RUN ' + player.run_number)
        row += 1


'''Gets a txt file from local storage and copies
it to a external usb drive'''


def export_data_to_usb():
    try:
        workbook = xlsxwriter.Workbook('/home/pi/Desktop/CronoskiModular/runData.xlsx')
        worksheet = workbook.add_worksheet()
        contents = get_all_ranking()
        write_excel(worksheet, contents)
        workbook.close()

        pen_name = os.listdir(MEDIA_PATH)[0]
        pen_path = MEDIA_PATH + pen_name + '/'
        sh.copy(src=EXCEL_PATH, dst=pen_path)
        return 0
    except:
        return -1  # for error handling


'''Deletes a specific run from the database, recieves
the specific dorsal and run number as inputs, adjusts 
the posterior run numbers.'''


def delete_single_run(input_dorsal, input_run_number):
    # make sure the parameters passed are str type
    input_dorsal = str(input_dorsal)
    input_run_number = str(input_run_number)

    found = False  # turns true when we have passed the specific run
    firsthalf = []  # contents before the specific run to delete
    secondhalf = []  # contents after

    # get the contents, iterate through them separate and skip
    contents = read_file()
    for content in contents:
        if content.run_number == input_run_number and content.dorsal == input_dorsal:
            found = True
        elif not found:
            firsthalf.append(content)
        else:
            content_input = content
            if (content.dorsal == input_dorsal):
                rn_mody = str(int(content.run_number) - 1)
                content_input = Run(content.dorsal, rn_mody, content.data, content.temps)
            secondhalf.append(content_input)
    '''if (not found):
        return -1'''

    clear_file()
    full_cleared_contents = firsthalf + secondhalf
    for c in full_cleared_contents:
        text_input = c.dorsal + ',' + c.run_number + ',' + c.data + ',' + c.temps + '\n'
        # try:
        add_text(text_input)
        # except:
        #    return -1 #error handling and avoiding crashes s
    # return 0


'''Gets data from a player which is indicated
through the dorsal and creates an image with his
performance metrics'''
'''def get_performance_metrics(input_dorsal):
    input_dorsal=str(input_dorsal)
    contents=read_file()

    #Get the values in a numpy array
    valors= []
    dates= []
    for content in contents:
        if content.dorsal==input_dorsal:
            valors.append(float(content.temps))
            dates.append(content.data[0:10])
    dates= [pd.to_datetime(d, format='%Y/%m/%d').date() for d in dates]
    print(dates)
    N=50
    colors = np.random.rand(N)
    plt.scatter(dates, valors, c= colors, alpha=0.5)
    plt.xticks(dates,dates)
    plt.show()'''

# get_performance_metrics(9)