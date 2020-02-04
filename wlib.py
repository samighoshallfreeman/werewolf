from math import sqrt
import copy
from random import *

from display import *
import display
from misc import *
from mapgen import *
import mapgen
import store 

news = []

class Creature:
    def __init__(self, x, y, icon, color, hp=0, mode="", gold=10):
        self.x = x
        self.y = y
        self.icon = icon
        self.original_color = color
        self.color = color
        self.mode = mode
        self.timer = 4
        self.inventory = []
        self.hp = hp
        self.stun_timer = 0
        self.invisibility_timer = 0
        self.target = None
        self.max_hp = hp
        self.gold = gold
        self.name = ""

class Object:
    def __init__(self, x, y, icon, color, name = "", description = "", cost=0):
        self.icon = icon
        self.x = x
        self.y = y
        self.description = description
        self.color = color
        self.name = name
        self.effect = lambda x, y, z, foo: None
        self.cost = cost
        
def spawn_thing(c, m, startx=0, endx=1000, starty=0, endy=1000):
    c.x = randint(startx, endx - 1)
    c.y = randint(starty, endy- 1)
    if okay_spawn(m,c):
        return c
    return spawn_thing(c,m, startx, endx, starty, endy)
        
def walkable():
    result = filter(lambda t: t[1][2] == True, display.tiles.items())
    result = map(lambda t: t[0], result)
    return result
        
def okay_spawn(m, c):
    return m[c.y][c.x] in walkable() 

def distance(c1, c2):
    a = c1.x - c2.x      
    b = c1.y - c2.y
    c = a**2 + b**2
    
    return sqrt(c)
               
def no_objects_between(c, t, os, on_x=False, on_y=False):
    startx, endx = ordered(c.x, t.x)
    starty, endy = ordered(c.y, t.y)
    js = list(filter(lambda x: x.icon == "?", os))
    jsx = list(filter(lambda j: j.x > startx and j.x < endx and j.y == c.y, js))
    jsy = list(filter(lambda j: j.y > starty and j.y < endy and j.x == c.x , js))
    if jsx == [] and on_y:
        return True
    if jsy == [] and on_x:
        return True
    return False
# |--------tests----------|  
test_c = Creature(5, 2, "", 0)
test_t = Creature(5, 10, "", 0) 
test_os = []
assert(no_objects_between(test_c, test_t, test_os, True, False) == True)
  
test_c = Creature(5, 2, "", 0)
test_t = Creature(5, 10, "", 0) 
test_os = [Object(5, 5, "?", 0)]
assert(no_objects_between(test_c, test_t, test_os, True, False) == False)

test_c = Creature(5, 2, "", 0)
test_t = Creature(5, 90, "", 0) 
test_os = [Object(8, 5, "?", 0)]
assert(no_objects_between(test_c, test_t, test_os, True, False) == True)
# ________________________|

def can_see(m, c, t ,os):
    def is_visible_(m, n1, n2, f):
    
        open_tiles = [0,2,3,4,7]
        #open_tiles = filter(lambda tt: tiles[tt][2], tiles)
        visible = lambda l: len(set(l) - set(open_tiles)) == 0

        start, end = ordered(n1, n2)
        tiles_between = [f(n,m) for n in range(start, end + 1)]
        return visible(tiles_between)

    if distance(c,t) > 50:
        return False
    
    if t.invisibility_timer == 0:
        if c.x == t.x:
            return is_visible_(m, c.y, t.y, lambda n,m: m[n][c.x]) and no_objects_between(c,t,os,on_x=True)
        elif c.y == t.y:
            return is_visible_(m, c.x, t.x, lambda n,m: m[c.y][n]) and no_objects_between(c,t,os,on_y=True)
    else:
        return False

def off_map(nx, ny):
    return nx > (mapgen.MAP_WIDTH - 1) or ny > (mapgen.MAP_HEIGHT - 1) or nx < 0 or ny < 0

def attempt_move(c, m, xmod, ymod, cs,objects):
    nx = c.x + xmod
    ny = c.y + ymod
    if off_map(nx,ny):
        if c.icon == "v":
            cs.remove(c)
            news.append("a villager got away")
            return
        elif c.icon == "g":
            return
        elif c.icon == "p":
            return
    else:
        if m[ny][nx] in(1, 6, 8) :
            if c.icon != "w":
                xmod, ymod = get_new_mods(xmod, ymod)
            else:
                return
            attempt_move(c, m, xmod, ymod, cs, objects)
            return
        for o in filter(lambda o: o.x == nx and o.y == ny and o.icon == "?", objects):
            if c.icon != "w":
                xmod, ymod = get_new_mods(xmod, ymod)
            else:
                return
            attempt_move(c, m, xmod, ymod, cs, objects)
            return
        c.x += xmod
        c.y += ymod
      
def pick_direction(cx, cy, px, py):
    xmod = 0
    ymod = 0
    
    if cx > px:
        xmod = 1 
    elif cx < px:
        xmod = -1
    if cy > py:
        ymod = 1 
    elif cy < py:
        ymod = -1
      
    if xmod != 0 and ymod != 0:
        if abs(px - cx) <= abs(py - cy):
            ymod = 0
        else:
            xmod = 0
    return (xmod, ymod)
        
def move_villager(v,player,m,cs,objects):
    xmod,ymod = (0,0)

    if can_see(m, v, player,objects) and player.mode == "werewolf":
        v.mode = "fleeing"
        v.timer = 4
    
    if v.mode == "fleeing":
        xmod, ymod = pick_direction(v.x, v.y, player.x, player.y)
        v.timer -= 1
        if v.timer == 0:
            v.mode = "wander"
    elif v.mode == "wander":
        xmod, ymod = wander(v)        
    attempt_move(v, m, xmod, ymod,cs,objects)
    
def move_guard(g,player,m,cs,objects):
    if g.target is not None:
        xmod, ymod = optupe(pick_direction(g.x, g.y, g.target[0], g.target[1]))
    elif g.target is None:
        xmod, ymod = wander(g)
        
    if player.mode == "werewolf":
        if can_see(m, g, player,objects):
            g.target = (player.x,player.y)
        if distance(player,g) == 1.0: #xmod + g.x == player.x and ymod + g.y == player.y:
            news.append("ya got hit")
            player.hp -= 1
            xmod = 0
            ymod = 0

    if (g.x, g.y) == g.target:
        g.target = None
    
    attempt_move(g, m, xmod, ymod,cs,objects)
    
        
def keyboard_input(inp, player, m, cs, objects, screen):
    ymod = xmod = 0
    movement = 1
    if inp == curses.KEY_DOWN:
        ymod = movement
    elif inp == curses.KEY_UP:
        ymod = -movement
    elif inp == curses.KEY_LEFT:
        xmod = -movement
    elif inp == curses.KEY_RIGHT:        
        xmod = movement
    elif inp == curses.KEY_END:        
        for o in filter(lambda o: int(distance(player,o)) < 2, objects):
                news.append(o.description)
                
    elif inp in map(lambda n: ord(str(n)), range(0, 10)):
        selected_number = inp - 49
        cur_inv = player.inventory.pop(selected_number)
        cur_inv.effect(player, cs,m, objects)
    elif inp == ord('b'):
        vs_close = list(filter(lambda c: c.icon == "v" and distance(c, player) < 2, cs))
        if vs_close != []:
            merchant = vs_close[0]
            store.buy_sell(screen, player, merchant, merchant.name, "\"Hello, I am %s, these are my wares.\""% merchant.name, "You bought ")
    elif inp == ord('s'):
        vs_close = list(filter(lambda c: c.icon == "v" and distance(c, player) < 2, cs))
        if vs_close != []:
            merchant = vs_close[0]
            store.buy_sell(screen, merchant, player, merchant.name, "\"Hello, I am %s, can I buy stuff from you.\""% merchant.name, "\"Thanks! Here is your gold\"")
            
    attempt_move(player, m, xmod, ymod, cs,objects)
    for c in filter(lambda o: o.icon in ["$","8", "*"],objects):
        if player.x == c.x and player.y == c.y and inp == ord('p'):
            news.append("you collected " + c.name)
            objects.remove(c)
            if c.icon == "$":
                player.gold += 1
            else:
                player.inventory.append(c)
    
    vs = filter(lambda c: c.icon == "v", cs)
    for v in vs:
        if player.x == v.x and player.y == v.y and player.mode == "werewolf":
            news.append("You devour the villager...")
            cs.remove(v)
            body = Object(v.x, v.y, "%", 1, "", "A dead villager. Eeeewwww.")
            objects.append(body)
            loot = choice(v.inventory)
            #loot.x = v.x + choice([1,-1])
            #loot.y = v.y + choice([1,-1])
            loot = spawn_thing(loot, m, v.x - 1, v.x + 1, v.y - 1, v.y + 1)
            objects.append(loot)
            for x in range(2):
                guard = Creature(0, 0, "g", 5, mode="wander")
                guard = spawn_thing(guard, m)
                cs.append(guard)
                coin = Object(0, 0, "$",21, "a coin", "oooh, a coin")
                coin = spawn_thing(coin, m, player.x - 10, player.x + 10, player.y - 10, player.y + 10)
                objects.append(coin)

def wander(c):
    xmod = randint(-1,1)
    ymod = randint(-1,1)
    if randint (0,1) == 1:
        xmod = 0
    else:
        ymod = 0
    return (xmod,ymod)

def message(screen, x, y, s, color=0):
        screen.clear()                    
        screen.addstr(y, x, s, curses.color_pair(color))
        screen.refresh()
        inp = screen.getch()

def within_box(v, b_x, b_y, b_h, b_w):
    if v.x >= b_x and v.y >= b_y:
        if v.x <= b_w and v.y <= b_h:
            return True
    return False

def get_local(x,y, global_list):
    box_width = mapgen.ZONE_LENGTH + (mapgen.CAM_WIDTH * 2)
    box_height = mapgen.ZONE_LENGTH + (mapgen.CAM_HEIGHT * 2)
    box_x = x - mapgen.CAM_WIDTH
    box_y = y - mapgen.CAM_HEIGHT
    return list(filter(lambda v: within_box(v, box_x, box_y, box_height, box_width), global_list))
            
def rounds(space, c):
    l = [x * space for x in range(1000)]
    return l[int(c/space)]
    