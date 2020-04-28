import curses
from random import randint
from display import init_colors
from misc import limit
from wlib import message

def buy(screen, merchant, p, n):
    r_i = merchant.inventory
    inp = 0
    a_row = 2 
    for i in r_i:
        i.cost_str = str(i.cost)
    g_bool = True
    while inp != 27 and g_bool:
        screen.clear()
        a_row = arrow(a_row, inp, len(r_i))
        if exit_selected(r_i, inp, a_row):
            break
        elif inp == 10:
            selected_item = r_i[a_row - 2]
            if p.gold >= selected_item.cost:
                message(screen, 1, 1, "You bought " + selected_item.name)
                p.inventory.append(selected_item)
                p.gold -= selected_item.cost
                r_i.remove(selected_item)
            else:
                message(screen, 1, 1, "If you want " + selected_item.name + ", you better get more gold")
            
        display_stuff(cur_row, a_row, "\"Hello, I am %s, these are my wares.\""% n,)
            
def display_stuff(cur_row, a_row, screen, buyer, seller, msg):
    # arrow
    screen.addstr(a_row, 1, "->", curses.color_pair(1))
    # buyer inv
    for x in range(len(buyer.inventory)):            
        screen.addstr(x, 50, buyer.inventory[x].name, curses.color_pair(0))
    # buyer gold
    screen.addstr(0, 1, "Gold: " + str(buyer.gold), curses.color_pair(21))
    # msg
    screen.addstr(1, 1, msg, curses.color_pair(0))
    # seller inv
    cur_row = 2
    for i in seller.inventory:
        c = curses.color_pair(0)
        if cur_row == a_row:
            c = curses.color_pair(1)
        screen.addstr(cur_row, 4, i.name + "    " + i.cost_str, c)
                
        cur_row += 1
    # exit
    E_c = curses.color_pair(14)
    if cur_row == a_row:
        E_c = curses.color_pair(1)#20
    screen.addstr(cur_row, 4, "Exit store", E_c)
            
def exit_selected(inv, inp, a_row):
    return inp == 10 and a_row == len(inv) + 2
            
def buy_sell(screen, buyer, seller, n, msg1, msg2):
    init_colors()
    inp = 0
    a_row = 2 
    cur_row = 2
    for i in seller.inventory:
        i.cost_str = str(i.cost)
    
    while inp != 27:
        screen.clear()
        a_row = arrow(a_row, inp, len(seller.inventory))
        if exit_selected(seller.inventory, inp, a_row):
            break
        elif inp == 10:
            selected_item = seller.inventory[a_row - 2]
            new_msg = msg2
            if msg2 == "You bought ":
                new_msg = msg2 + selected_item.name
            trade(buyer, seller, selected_item, new_msg, screen) #"\"Thanks! Here is your gold\""
        display_stuff(cur_row, a_row, screen, buyer, seller, msg1) #"\"Hello, I am %s, can I buy stuff from you.\""% n
            
        screen.refresh()
        inp = screen.getch()

def arrow(a_row, inp, length, begining=2):
    if inp == curses.KEY_DOWN:
        a_row += 1
    elif inp == curses.KEY_UP:
        a_row -= 1
    a_row = limit(a_row, length + begining, begining)
    return a_row

def trade(buyer, seller, selected_item, msg, screen):
    if buyer.gold >= selected_item.cost:
        message(screen, 1, 1, msg)
        buyer.inventory.append(selected_item)
        buyer.gold -= selected_item.cost
        seller.gold += selected_item.cost   
        seller.inventory.remove(selected_item)
            
    