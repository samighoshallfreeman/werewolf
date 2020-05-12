from pyfiglet import figlet_format
import curses
from store import arrow
from display import init_colors
def do_menu(screen):
    init_colors()
    a_row = 7
    key = 0
    curses.curs_set(False)
    while key != 10:
        screen.clear()
        write_cool_word("WEREWOLF", 20, 1, screen) 
        screen.addstr(5,5,"would you like to...")
        
        screen.addstr(7, 7, "enter the old world, or", curses.color_pair(1) if a_row == 7 else curses.color_pair(0))
        screen.addstr(8, 7, "generate a new one?", curses.color_pair(1) if a_row == 8 else curses.color_pair(0))
        screen.addstr(a_row, 1, "->", curses.color_pair(1))
        
        key = screen.getch()
        a_row = arrow(a_row, key, 1, 7)
    if a_row == 8:
        return warning(screen)
    else:
        return 1

def warning(screen):
    init_colors()
    a_row = 7
    key = 0
    curses.curs_set(False)
    while key != 10:
        screen.clear()
        screen.addstr(5,5,"WARNING: genrating a new world will destroy the old world. would you like to...", curses.color_pair(14))
        
        screen.addstr(7, 7, "enter the old world, or", curses.color_pair(1) if a_row == 7 else curses.color_pair(0))
        screen.addstr(8, 7, "destroy old world and create new one", curses.color_pair(1) if a_row == 8 else curses.color_pair(0))
        screen.addstr(a_row, 1, "->", curses.color_pair(1))
        
        key = screen.getch()
        a_row = arrow(a_row, key, 1, 7)
    return 1 if a_row == 7 else 0
def write_cool_word(s, x, y, screen):
    w = figlet_format(s, font="tombstone")
    w = w.split("\n")
    for line in range(len(w)):
        screen.addstr(y + line, x, w[line], curses.color_pair(14))


#curses.wrapper(do_menu)
     # ___     __      ___    ___
    # /__/\   /_/\    /__/\ /___/|
   # /   \/  /  \ \  |   \ /   | |
   # |  \/| / /\ \ /|| |\ | /| | |
   # /\  |/|  __  | || | |_ || | |   |
   # \___/ |_ ||__|/ |_|/    |_|/   |
   