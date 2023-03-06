from collections import namedtuple
import items
from random import choice, randint
from globals import news
import wlib

Badge = namedtuple("Badge", "name condition reward appearance color")

def trapstep(player, map):
    pass
    
def wander1reward():
    pass
    
def gray_badge(badge, gray_color=0):
    return list(map(lambda b: (b[0], gray_color), badge))
    
def badge_check(player):
    if len(player.zones_visited) == 3 and "wanderer1" not in player.badges:
        player.badges.add("wanderer1")
        name = choice(list(items.items.keys()))
        player.inventory.append(items.make_item(name))
        news.append("you acheived Wanderer One! Your prize is a %s" % name)
    if len(player.zones_visited) == 2 and "wanderer2" not in player.badges:
        player.badges.add("wanderer2")
        player.inventory.append(items.make_item("a teleporter"))
    if player.gold >= 30 and "wanderer1" not in player.badges:
        player.badges.add("milionair")
    if player.swims >= 100 and "wanderer1" not in player.badges:
        player.badges.add("swimer")
    if player.ktn >= 7 and "wanderer1" not in player.badges:
        player.badges.add("murderer")
    
    
    

    
def badge_check2(player):
    badge_conditions = [
        ("wanderer1", lambda p: len(p.zones_visited) >= 3, items.make_item(choice(list(items.items.keys())))),
        ("wanderer2", lambda p: len(p.zones_visited) >= 2, items.make_item("a teleporter")),
        ("milionair", lambda p: p.gold >= 50, items.make_item("amazon")),
        ("swimer", lambda p: p.swims >= 100, items.make_item("amazon")),
        ("murderer", lambda p: p.ktn >= 7, items.make_item("amazon"))]
    badges = list(filter(lambda b: b[1](player), badge_conditions))
    for name, f, item in badges:
        if name not in player.badges: 
            player.badges.add("%s" % name)
            news.append("you have gotten the %s badge" % name)
            player.inventory.append(item)
        
        
    
w1_viewl1 = [
"      ",
"  w1  ",
' "  " ']
 
w1_viewl2 = [
"_=  =_",
"\\    /",
'  ==  ']
 
w1_viewl3 = [
"  <>  ",
" +  + ",
'      ']
 
w1_view = [(w1_viewl1, 3), (w1_viewl2, 21), (w1_viewl3, 2)] 
 
sw_viewl1 = [ 
" ~  ~ ",
 "  sw  ",
 " ~  ~ " ]
 
sw_viewl2 = [
 "_ <> _",
"\\    /",
 "  ()  " ]
 
sw_viewl3 = [ 
"      ",
" (  ) ",
"      "]

sw_view = [(sw_viewl1, 12), (sw_viewl2, 21), (sw_viewl3, 5)] 

w2_viewl1 = [
"      ",
"  w2  ",
'      ' ]
 
w2_viewl2 = [
"_ <> _",
"\\    /",
'  ::  ' ]
 
w2_viewl3 = [
" \  / ",
"      ",
' "  " ' ]

w2_viewl4 = [
"      ",
" #  # ",
'      ' ]

w2_view = [(w2_viewl1, 14), (w2_viewl2, 21), (w2_viewl3, 3), (w2_viewl4, 2)]

mi_viewl1 = [
"_ <> _",
"\\ $$ /",
'  ==  ' ]
 
mi_viewl2 = [
" =  = ",
" 0  0 ",
'      ' ]
 
mi_viewl3 = [
"      ",
"      ",
' *  * ' ]



mi_view = [(mi_viewl1, 21), (mi_viewl2, 2), (mi_viewl3, 0)]

MM_viewl1 = [
" <  > ",
"  MM  ",
' <  > ' ]
 
MM_viewl2 = [
"  <>  ",
" %  % ",
'      ' ]
 
MM_viewl3 = [
"_    _",
"\    /",
'  WW ' ]

MM_view = [(MM_viewl1, 5), (MM_viewl2, 14), (MM_viewl3, 21)]

 
badges = [ Badge("wanderer1", trapstep, wander1reward, w1_view, 3),
           Badge("wanderer2", trapstep, wander1reward, w2_view, 2), 
           Badge("murderer", trapstep, wander1reward, MM_view, 9),
           Badge("milionair", trapstep, wander1reward, mi_view, 21),
           Badge("swimer", trapstep, wander1reward, sw_view, 12)]