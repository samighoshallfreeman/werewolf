import curses
import display
from random import randint
from misc import limit
import invlib

def buy(screen, merchant, p, n):
    r_i = merchant.inventory
    inp = 0
    a_row = 2 
    for i in r_i:
        i.cost_str = str(i.cost)
    g_bool = True
    while inp != 27 and g_bool:
        screen.clear()
        a_row = invlib.arrow(a_row, inp, len(r_i))
        if invlib.exit_selected(r_i, inp, a_row):
            break
        elif inp == 10:
            selected_item = r_i[a_row - 2]
            if p.gold >= selected_item.cost:
                display.message(screen, 1, 1, "You bought " + selected_item.name)
                p.inventory.append(selected_item)
                p.gold -= selected_item.cost
                r_i.remove(selected_item)
            else:
                display.message(screen, 1, 1, "If you want " + selected_item.name + ", you better get more gold")
            
        display.display_store(cur_row, a_row, "\"Hello, I am %s, these are my wares.\""% n,)
            
def buy_sell(screen, buyer, seller, n, msg1, msg2):
    display.init_colors()
    inp = 0
    a_row = 2 
    cur_row = 2
    for i in seller.inventory:
        i.cost_str = str(i.cost)
    
    while inp != 27:
        screen.clear()
        a_row = invlib.arrow(a_row, inp, len(seller.inventory))
        if invlib.exit_selected(seller.inventory, inp, a_row):
            break
        elif inp == 10:
            selected_item = seller.inventory[a_row - 2]
            new_msg = msg2
            if msg2 == "You bought ":
                new_msg = msg2 + selected_item.name
            trade(buyer, seller, selected_item, new_msg, screen) #"\"Thanks! Here is your gold\""
        display.display_store(cur_row, a_row, screen, buyer, seller, msg1) #"\"Hello, I am %s, can I buy stuff from you.\""% n
            
        screen.refresh()
        inp = screen.getch()

def trade(buyer, seller, selected_item, msg, screen):
    if buyer.gold >= selected_item.cost:
        display.message(screen, 1, 1, msg)
        buyer.inventory.append(selected_item)
        buyer.gold -= selected_item.cost
        seller.gold += selected_item.cost   
        seller.inventory.remove(selected_item)
            
    