import copy
from random import *
from display import *
import display
from misc import *
#from mapgen import *
import mapgen
import store
import globals
#import globals
import pickle
import items

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
        self.hp_limit = 5
        self.fullness = 100.0
        self.badges = set()
        self.zones_visited = set()
        self.swims = 0
        self.ktn = 0
        
        
class Object:
    def __init__(self, x, y, icon, color, name = "", description = "", cost=0):
        self.icon = icon
        self.x = x
        self.y = y
        self.description = description
        self.color = color
        self.name = name
        #self.effect = lambda x, y, z, foo, bar, a, gc: None
        self.cost = cost
        self.hp = 4
        self.inventory = []
        
def write(l, name):
    f = open(name, "wb")
    pickle.dump(l,f)
    f.close()
    
def read(name):
    f = open(name, "rb")
    l = pickle.load(f)
    f.close()
    return l

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

def slope(x1, y1, x2, y2):
    dx = x2 - x1 
    dy = y2 - y1
    return dy/dx
    
def yintercept(x, y, slope):
    return (-slope * x) + y
    
print(yintercept(10, 10, (3/6)))

def get_sight_line(a, b):
    s = slope(a.x, a.y, b.x, b.y)
    yint = yintercept(b.x, b.y, s)
    sight_line = lambda x: (s*x)+yint
    return sight_line
    
# def get_possible_fuzzies(x, y, endy):
    # results = []
    # for possible_y in range(y, endy, 1)
    
# def line_intersect(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
    # """ returns a (x, y) tuple or None if there is no intersection """
    # d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
    # if d:
        # uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
        # uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
    # else:
        # return
    # if not(0 <= uA <= 1 and 0 <= uB <= 1):
        # return
    # x = Ax1 + uA * (Ax2 - Ax1)
    # y = Ay1 + uA * (Ay2 - Ay1)
 
    # return x, y    

def is_visible2(a, b, m):
    visible = False
    open_tiles = [0,2,3,4,7,9,10]
    visible = lambda l: len(set(l) - set(open_tiles)) == 0
    
    if a.x == b.x or a.y == b.y:
        visible = True
    else:        
        sight_line = get_sight_line(a, b)
        low, high = sorted([a.x, b.x])
        cs = [(x, int(sight_line(x))) for x in range(low,high)]
        
        # map over cs and get the map tiles at those coordinates
        tiles_between = set(map(lambda c: m[c[1]][c[0]], cs))
        #for x,y in cs:
            #m[int(y)][int(x)] = 9
        return visible(tiles_between)  
        
    # Figure out which is smaller, a.x or b.x
    # loop over all the x values from low to high:
        # Change the map at y, x to be some kind of test sight tile
        
def can_see(m, c, t ,os):
    def is_visible_(m, n1, n2, f):
    
        open_tiles = [0,2,3,4,7,9,10]
        #open_tiles = filter(lambda tt: tiles[tt][2], tiles)
        

        start, end = ordered(n1, n2)
        tiles_between = [f(n,m) for n in range(start, end + 1)]
        return visible(tiles_between)

    if distance(c,t) > 50:
        return False
    
    if t.invisibility_timer == 0:
        return is_visible2(c, t, m)
        #if c.x == t.x:
            #return is_visible_(m, c.y, t.y, lambda n,m: m[n][c.x]) and no_objects_between(c,t,os,on_x=True)
        #elif c.y == t.y:
            #return is_visible_(m, c.x, t.x, lambda n,m: m[c.y][n]) and no_objects_between(c,t,os,on_y=True)
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
            globals.news.append("a villager got away")
            return
        elif c.icon == "g":
            return
        elif c.icon == "p":
            return
    else:
        if c.icon == "^":
            blocks = (0, 1, 2, 3, 5, 6, 7, 8, 9, 10)
        else:
            blocks = (1, 6, 8)
        if m[ny][nx] in blocks:
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
            sheilds = list(filter(lambda x: x.icon == "]", player.inventory))
            if sheilds != [] and randint(1, 3) == 1:
                globals.news.append("ya got hit but your sheild blocked it")
                sheilds[0].hp -= 1
            else:
                player.hp -= 1
                if player.hp <= 0:
                    globals.death = "dat guard dun gocha. -> g"
                globals.news.append("ya got hit")
            xmod = 0
            ymod = 0

    if (g.x, g.y) == g.target:
        g.target = None
    
    attempt_move(g, m, xmod, ymod,cs,objects)
    
        
def keyboard_input(inp, player, m, cs, objects, screen, global_objects, global_cs, tiles, atlas):
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
    elif inp == 10:
        for o in filter(lambda o: int(distance(player,o)) < 2, objects):
                globals.news.append(o.description)
    elif inp == ord('q'):
        world = (m, player, global_objects, global_cs, atlas, globals.time_alive, globals.news)
        write(world, "world")
        player.hp = 0
        globals.death = "you quit"
    elif inp == ord('t'):
        player.x = randint(0, len(m[1]))
        player.y = randint(0, len(m))
    elif inp in map(lambda n: ord(str(n)), range(0, 10)):
        selected_number = inp - 49
        cur_inv = player.inventory[selected_number]
        effect = items.items[cur_inv.name][0]
        effect(player, cs, m, objects, global_objects, screen, global_cs, cur_inv)
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
    elif inp == ord('p'):
        collision_type(player, list(items.items.keys()) + ["a coin", "a flower"], objects, objects, global_objects, cs, global_cs, m, pick_up)
    elif inp == ord('g'):
        player.gold += 10
        trap = Object(player.x, player.y, "'", 3, "a trap", "it's a trap!")
        objects.append(trap)
        global_objects.append(trap)
        
    elif inp == ord('B'):
        display.display_badges(screen, player.badges)
    if player.stun_timer == 0:
        attempt_move(player, m, xmod, ymod, cs,objects)
    collision_type(player, ["a trap"], objects, objects, global_objects, cs, global_cs, m, trap_effect)
    names = list(map(lambda x: x.name, filter(lambda x: x.name != "", cs)))
    if player.mode == "werewolf":
        collision_type(player, names , global_cs, objects, global_objects, cs, global_cs, m, kill_v)
    globals.time_alive += 1
     
def wander(c):
    xmod = randint(-1,1)
    ymod = randint(-1,1)
    if randint (0,1) == 1:
        xmod = 0
    else:
        ymod = 0
    return (xmod,ymod)

def within_box(v, b_x, b_y, b_h, b_w):
    if v.x >= b_x and v.y >= b_y:
        if v.x <= b_x + b_w and v.y <= b_y + b_h:
            return True
    return False

def get_local(x,y, global_list):
    box_width = mapgen.ZONE_LENGTH + (mapgen.CAM_WIDTH * 2)
    box_height = mapgen.ZONE_LENGTH + (mapgen.CAM_HEIGHT * 2)
    box_x = x - mapgen.CAM_WIDTH
    box_y = y - mapgen.CAM_HEIGHT
    return list(filter(lambda v: within_box(v, box_x, box_y, box_height, box_width), global_list))
 
def pit_trap_setup(p, m, tiles):
    t = tiles[m[p.y][p.x]][0]
    print(t)
    if not mapgen.if_outdoors(t):
        p.icon = "."
        p.color = 2
        
def collision_type(c, names, collide_list, os, global_objects, cs, global_cs, world, effect):
    for t in filter(lambda x: x.name in names, collide_list):
        if collide(c, t):       
            effect(t, c, os, global_objects, world, cs, global_cs)        
            
def trap_effect(t, player, objects, global_objects, world, cs, global_cs):
    globals.news.append("ahhhhh! you got stuck in a trap")
    player.hp -= 1
    if player.hp <= 0:
        globals.death = "you were killed in a trap"
    objects.remove(t)
    global_objects.remove(t)
    player.stun_timer = randint(2, 4)
    
    
def pick_up(t, player, objects, global_objects, world, cs, global_cs):
    globals.news.append("you collected " + t.name)
    objects.remove(t)
    global_objects.remove(t)
    if t.icon == "$":
        player.gold += 1
    else:
        player.inventory.append(t)
        
def kill_v(v, player, objects, global_objects, m, cs, global_cs):
    globals.news.append("You devour the villager...")
    cs.remove(v)
    global_cs.remove(v)
    player.fullness += 30.0
    body = Object(v.x, v.y, "%", 1, "", "A dead villager. Eeeewwww.")
    objects.append(body)
    loot = choice(v.inventory)
    loot = spawn_thing(loot, m, v.x - 1, v.x + 1, v.y - 1, v.y + 1)
    objects.append(loot)
    global_objects.append(loot) 
    player.ktn += 1 
    for x in range(2):
        guard = Creature(0, 0, "g", 5, mode="wander")
        guard = spawn_thing(guard, m, player.x - 30, player.x + 30, player.y - 30, player.y + 30)
        cs.append(guard)
        coin = Object(0, 0, "$",21, "a coin", "oooh, a coin")
        coin = spawn_thing(coin, m, player.x - 10, player.x + 10, player.y - 10, player.y + 10)
        objects.append(coin)
        global_objects.append(coin)
        trap = Object(0, 0, "'", 3, "a trap", "it's a trap!")
        trap = spawn_thing(trap, m, player.x - 10, player.x + 10, player.y - 10, player.y + 10)
        pit_trap_setup(trap, m, display.tiles)
        objects.append(trap)
        global_objects.append(trap)
        
def shark(map, creatures):
    for x in creatures:
        if x.icon == "g" and mapgen.under_color(x, map) == 12:
            x.icon = "^"
                    
def swim(map, player):
    if player.stun_timer == 0:
        player.stun_timer = 2
    player.swims += 1

def stuff_breaks(player):
    for x in list(map(lambda x: x.name, filter(lambda x: x.hp == 0, player.inventory))):
        globals.news.append("%s of your's broke!"% x)
    player.inventory = list(filter(lambda x: x.hp != 0, player.inventory))

def die(m, player, global_objects, global_cs, atlas, screen, highscores):
    world = (m, player, global_objects, global_cs, atlas, globals.time_alive, globals.news)
    if globals.death != "you quit":
        write(world, "world")
        highscores.append(("sam", globals.death, globals.time_alive, player.gold))
    screen.clear()
    highscores.sort(key=lambda x: x[2])
    highscores.reverse()
    highscores = highscores[:10]
    #display_death(screen, highscores)
    write(highscores, "highscores")