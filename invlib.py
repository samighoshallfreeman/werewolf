import curses
from misc import limit
def exit_selected(inv, inp, a_row):
    return inp == 10 and a_row == len(inv) + 2

def arrow(a_row, inp, length, begining=2):
    if inp == curses.KEY_DOWN:
        a_row += 1
    elif inp == curses.KEY_UP:
        a_row -= 1
    a_row = limit(a_row, length + begining, begining)
    return a_row