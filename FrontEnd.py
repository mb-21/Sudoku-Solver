from tkinter import *
import pandas
from solver import *

win = Tk()
win.title("Sudoku Solver")
rows = []

"""Create all the entry boxes for user input"""
for i in range(9):
    cols = []
    for j in range(9):
        e = Entry(win, width=5)
        e.grid(row=i, column=j, sticky=NSEW)
        e.insert(END, "_")
        cols.append(e)
    rows.append(cols)


def on_press():
    '''
    Takes all the data from entry boxes and creates a
    dataframe that can be solved by the solver
    '''

    temp = []
    data = []
    id = 1

    for row in rows:
        temp.append(row)

    for row in temp:  # format the data so it can be converted to a dataframe
        new = [id]
        id += 1
        for d in row:
            new.append(d.get())
        data.append(new)

    df = pandas.DataFrame.from_records(data)
    df.columns = ["ID", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9"]  # set column names
    df = df.set_index("ID")
    # print(df)

    solve(df)  # call solve() from solver.py

    '''Create Labels to display the completed puzzle'''
    for row in range(9):
        for column in range(9):
            l = Label(win, text=df["c" + str(column + 1)][row + 1])
            l.grid(row=row + 10, column=column)

    '''Refill the entries with _, in case the user wants to solve another puzzle'''
    for row in rows:
        for entry in row:
            entry.delete(0, "end")
            entry.insert(END, "_")


Button(text='Solve', command=on_press).grid(column=4)

mainloop()
