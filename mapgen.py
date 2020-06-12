from random import randint, choice, random
import wlib
import geometry as g
from typing import List
import numpy as np
from bsp import make_bsp_rooms
import display
from misc import shuffled, w_h
from globals import *
from items import items, flower_effect, make_item
import pickle


class Zone:
    def __init__ (self, type, percg, percv, percp ,l_func):
        self.type = type
        self.perc_v = percv
        self.perc_g = percg
        self.perc_p = percp
        self.l_func = l_func

def village(m, startx, starty , endx, endy, objects):
    print("    * Constructing village...")
    #building_zone(m, startx, starty, endx, endy, 100, 10, 10, 15, 15 )
    buildings = make_bsp_rooms(endx - startx, endy - starty)
    for b in buildings:
        print("10, 10, %d, %d" % (b.w - 2, b.h - 2)) 
        building = random_building2(10, 10, b.w - 2, b.h - 2)
        stamp(startx + b.x, starty + b.y, building, m, 2)
        
            
def factory(m, startx, starty , endx, endy, objects):
    print("    * Constructing factory...")
    building_zone(m, startx, starty, endx, endy, 50, 10, 10, 18, 18)
    
def plains(m, startx, starty, endx, endy, objects):
    print("    * Constructing plains...")
    building_zone(m, startx, starty, endx, endy, 400, 10, 10, 15, 15)
    objects.extend(gen_items(m, startx, starty, 1000, wlib.Object(0, 0, "*", 14, "a flower", "that flower smells good", 1)))
   
def forest(m, startx, starty , endx, endy, objects):
    print("    * Constructing forest...")
    for x in range(30000):
        m[randint(starty, endy)][randint(startx, endx)] = 8
    objects.extend(gen_items(m, startx, starty, 5000, wlib.Object(0, 0, "6", 14, "an apple", "an apple", 5)))
 
def mountains(m, startx, starty , endx, endy, objects):
    print("    * Constructing mountains...")
    test_dig = [[6 for x in range(endx - startx)] for y in range(endy - starty)]
    width = ZONE_LENGTH
    height = ZONE_LENGTH
    gd1 = good_dig(width - 15, height - 15)
    print("    *    cave 1 finished...")
    gd2 = good_dig(15, height - 15)
    print("    *    cave 2 finished...")
    gd3 = good_dig(width - 15, 15)
    print("    *    cave 3 finished...")
    gd4 = good_dig(15, 15)
    print("    *    cave 4 finished...")
    for cur_dig in [gd1, gd2, gd3, gd4]:
        stamp(0, 0, cur_dig, test_dig, 6)
    stamp(startx, starty, test_dig, m)

def ocean(m, startx, starty , endx, endy, objects):
    print("    *   generating ocean....")
    s = [[10 for x in range(startx + 1,ZONE_LENGTH - 2)] for y in range(starty + 1, ZONE_LENGTH - 2)]
    w = [[4 for x in range(startx + 2, ZONE_LENGTH - 4)] for y in range(starty + 2, ZONE_LENGTH - 4)]
    stamp(0, 0, w, s)
    for x in range(20):
        automata(s, 10)
    stamp(startx, starty, s, m)
    zone = np.array(m)[starty:endy, startx:endx]
    
    for x in range(5):
        automata(zone, 2)
    stamp(startx, starty, zone, m)
    
def automata(zone: List[List[int]], friend: int) -> List[List[int]]:
    weights = [0.00, 0.1, 0.2, 0.3, 0.4]
    for y in range(ZONE_LENGTH):
        for x in range(ZONE_LENGTH):
            num = num_neighbors(zone, x, y, friend)
            weight = weights[num]
            r = random()
            if r < weight:
                try:
                    zone[y][x] = friend
                except:
                    pass
                            
def num_neighbors(m: List[List[int]], x: int, y: int, tile_num: int) -> int:
    ints = [(y, x + 1), (y, x - 1), (y + 1, x), (y - 1, x)]
    num = 0
    for t in ints:
        ty,tx = t
        try:
            if m[ty][tx] == tile_num:
                num += 1
        except:
            pass
    return num
    
            
class Digger:
    pass
    
def d_on_map(d, m_hight, m_width): 
    badx = d.x >= m_width + 1 or d.x < 0
    bady = d.y >= m_hight + 1 or d.y < 0
    
    of_map = badx or bady
    if of_map:
        #d.x = sx
        #d.y = sy
        return False
    else:
        return True
        
def ed_check(d, edible,m ,oldx, oldy, m_hight, m_width):
    if d_on_map(d, m_hight, m_width) == False:
        return
    if m[d.y][d.x] != edible:
        d.x,d.y = [oldx, oldy]
    
def dig(sx, sy, edible, eaten, death_rate, s_spawn_rate, m, speed, stop_count):
    m_width = len(m[0]) - 1
    m_hight = len(m) - 1
    d1 = Digger()
    d1.x = sx
    d1.y = sy
    d1.alive = True
    diggers = [d1]
    count = 0
    d1.spawn_rate = s_spawn_rate
    while(len(diggers) > 0):
        count += 1
        if count == stop_count:
            return
        diggers = list(filter(lambda d: d.alive and d_on_map(d, m_hight, m_width), diggers))
        for d in diggers:
            # try:
                # if m[d.y][d.x] == edible:
                    # m[d.y][d.x] = eaten
            # except:
                # print("d.x: %d, d.y: %d" % (d.x, d.y))
                # exit()
            if randint(1, 100) < death_rate:
                d.alive = False
            spawn_chance = randint(1,99)
            if spawn_chance < d.spawn_rate:
                new_digger = Digger()
                bool = (randint(1, 2) == 1)
                new_digger.x = d.x
                new_digger.y = d.y
                new_digger.spawn_rate = s_spawn_rate
                d.spawn_rate = int(d.spawn_rate * 0.95)
                
                if bool:
                    new_digger.x += choice([-1, 1])
                else:
                    new_digger.y += choice([-1, 1])
                new_digger.alive = True            
                diggers.append(new_digger)
            
            oldx, oldy = [d.x, d.y]
            if randint(1, 2) == 1:
                wayx = choice([1,-1])
                for x in range(speed):
                    #on_map(d, m_hight, m_width)
                    if d_on_map(d, m_hight, m_width) == False:
                        break
                    if m[d.y][d.x] == edible:
                        m[d.y][d.x] = eaten
                    d.x  += wayx
                    ed_check(d,edible,m,oldx,oldy, m_hight, m_width)
            else:
                wayy = choice([1,-1])
                for x in range(speed):
                    #on_map(d, m_hight, m_width)
                    if d_on_map(d, m_hight, m_width) == False:
                        break
                    if m[d.y][d.x] == edible:
                        m[d.y][d.x] = eaten
                    d.y  += wayy
                    ed_check(d,edible,m, oldx, oldy, m_hight, m_width)
                    
def good_dig(x, y, edible=6, eaten=7):
    while(True):
        test_dig = [[edible for x in range(ZONE_LENGTH)] for y in range(ZONE_LENGTH)]

        dig(x, y, edible, eaten, 50, 50, test_dig, 2, 1500)
        if edge_touch(test_dig, edible, eaten) >= 2:# and rate_dig(test_dig) <= width * height * 0.5:
            return test_dig
    
def rate_dig(dig, edible, eaten):
    rate = 0
    for y in dig:
        for x in y:
            if x == " ":
                rate += 1
    return rate
    
def edge_touch(dig, edible, eaten):
    edges = 0
    e_n = dig[0]
    e_s = dig[-1]
    e_e = []
    e_w = []
    for x in dig:
        e_w.append(x[0])
        e_e.append(x[-1])
    #Keegan's code = "return len(list(filter(lambda e: " " in e, [e_n, e_e, e_s, e_w])))"
    e_spots = [e_n, e_e, e_s, e_w]
    for e in e_spots:
        if eaten in e:
            edges += 1
    return edges
    
def spawn_villagers(m, cs, z, startx, endx, starty, endy):
    print("    * spawning villagers")
    for x in range(int(ZONE_LENGTH * ZONE_LENGTH * z.perc_v) ): #10, 0.005
        villager = wlib.Creature(0, 0, "v", 5, mode="wander")
        wlib.spawn_thing(villager, m, startx, endx, starty, endy)
        r_i = []
        for x in range(3):
            i = choice(list(items.keys()))
            effect, icon, color, cost = items[i]
            item = wlib.Object(0, 0, icon, color, i, i, randint(cost - 1, cost + 1))
            #item.effect = effect
            r_i.append(item)
        villager.name = choice(["Gerald", "Sathy", "Randy", "Joshua"])
        villager.inventory = r_i
        cs.append(villager)
        
def spawn_guards(m, cs, z, startx, endx, starty, endy):      
    print("    * spawning guards")
    for x in range(int(ZONE_LENGTH * ZONE_LENGTH * z.perc_g)):#0.0008
        guard = wlib.Creature(0, 0, "g", 5, mode="wander")
        wlib.spawn_thing(guard, m, startx, endx, starty, endy)
        cs.append(guard)
        
def building_zone(m, startx, starty , endx, endy, building_divider, minwidth, minhight, maxwidth, maxhight):
    buildings = []
    for x in range(int((endx - startx) * (endy - starty) / building_divider)):
        building = random_building2(minwidth, minhight, maxwidth, maxhight)
        bx = randint(startx, endx)
        by = randint(starty, endy)
            #(building_x, building_y, building) = random_building2(startx, starty , endx, endy, minwidth, minhight, maxwidth, maxhight)
        brect = g.Rect(bx, by, len(building[0]), len(building))

        collide = False
        for b in buildings:
            if b.overlaps_with(brect):
                collide = True
                break
        if collide == False:
            buildings.append(brect)
        
            stamp(bx, by, building, m, 2)
        
        
    
zones = [
    Zone("mountains", 0.001, 0.00, 0.00, plains,),#213
    Zone("village", 0.001, 0.005, 0.001, village),
    Zone("plains", 0.0006, 0.003, 0.001, plains),
    Zone("forest", 0.0003, 0.0015, 0.004, forest),
    Zone("village", 0.001, 0.005, 0.001, village),
    Zone("forest", 0.0003, 0.0015, 0.004, forest),
    Zone("lake", 0.0004, 0.001, 0,village),
    Zone("factory", 0.003, 0.006, 0.002, factory),
    Zone("plains", 0.0006, 0.003, 0.001, plains)]
    
def build_world(zones, m, objects, creatures):
    cur_y = 0
    cur_x = 0
    for z in zones:
        cx = cur_x * ZONE_LENGTH
        cy = cur_y * ZONE_LENGTH
        z.l_func(m, cx, cy, cx + ZONE_LENGTH, cy + ZONE_LENGTH, objects)
        objects += gen_objects(m, z, cx, cx + ZONE_LENGTH, cy, cy + ZONE_LENGTH)
        spawn_villagers(m, creatures, z, cx, cx + ZONE_LENGTH, cy, cy + ZONE_LENGTH)
        spawn_guards(m, creatures, z, cx, cx + ZONE_LENGTH, cy, cy + ZONE_LENGTH)
        cur_x += 1
        if cur_x == 3:
            cur_x = 0
            cur_y += 1
    

i_junks = [ "a shelf of ancient tomes,oh how old"
          , "a comfy sofa, should I sit down?"
          , "a desk. very desky."
          , "a pile of rubble. what happened here?"
          , "dirty laundry. oh, it reeks"
          ]

o_junks = [ "a pile of rubble. what happened here?"
          , "a hay bale. where's the needle?"
          , "a campfire.  nice and toasty!"
          , "a mail box. stuffed with bills:("
          , "a mail box. stuffed with love letters:)"
          ]

def under_color(c,m):
    tilenum = m[c.y][c.x]
    tile = display.tiles[tilenum]
    u_color = tile[1]
    return u_color

def gen_items(m, startx, starty, num, o):
    print("    * generating flowers...")
    items = []
    for x in range(num):
        #flower.effect = flower_effect
        o = wlib.spawn_thing(o, m, startx, startx + ZONE_LENGTH, starty, starty + ZONE_LENGTH)
        f_spot = m[o.y][o.x]
        if if_outdoors(display.tiles[f_spot][0]):
            items.append(o)
    return items
                
def gen_objects(m, z, startx, endx, starty, endy):
    print("    * generating objects...")
    objectz = []
    print("    *    items...")
    for x in range(int(ZONE_LENGTH * ZONE_LENGTH * z.perc_p)):
        f = filter(lambda n:n != "a flower", list(items.keys()))
        i = choice(list(f))
        effect, icon, color, cost = items[i]
        potion = wlib.Object(0, 0, icon, color, i, i, randint(cost - 1, cost + 1))
        #potion.effect = effect
        if potion.name == "a chest":
            for x in range(3):
                potion.inventory.append(make_item(choice(list(items.keys()))))  
        potion = wlib.spawn_thing(potion, m)

        objectz.append(potion)
    print("    *    junks...")
    for x in range(NUM_JUNKS):
        junk = wlib.Object(0, 0, "?",10," ", " ")
        junk = wlib.spawn_thing(junk, m)
        
        tile_num = m[junk.y][junk.x]
        tile = display.tiles[tile_num]
        tile_icon = tile[0]
        
        if if_outdoors(tile_icon):            
            junklist = o_junks            
        else:            
            junklist = i_junks
        
        junk.description = choice(junklist)
        
        objectz.append(junk)
    return objectz

def stamp(x,y,s,m, ignore_tile=None):
    """Stamps s onto m at coordinates x,y"""
    for sy in range(len(s)):
        for sx in range(len(s[0])):
            if on_map(x + sx, y + sy, m):
                if s[sy][sx] != ignore_tile:
                    m[y + sy][x + sx] = s[sy][sx]
                
def stamp_building(x,y,s,m):
    """Stamps building s onto m at coordinates x,y"""
    for sy in range(len(s)):
        for sx in range(len(s[0])):
            if on_map(x + sx, y + sy, m):                
                new_tile = s[sy][sx]
                map_tile = m[y + sy][x + sx]
                if map_tile == 0:
                    m[y + sy][x + sx] = 0
                elif map_tile == 3:
                    m[y + sy][x + sx] = 3
                else:
                    m[y + sy][x + sx] = new_tile
            

def make_list_of_1s(n):
    l = []
    for x in range(n):
       l.append(1)
    return l

def make_middle(n):
    l = [1]
    for x in range(n - 2):
        l.append(0)
    l.append(1)
    return l

def is_corner(x, y, w, h):
    if x == 0 and y == h:
        return True
    elif x == 0 and y == 0:
        return True
    elif x == w and y == 0:
        return True
    elif x == w and y == h:
        return True
    return False
    
def make_building(w,h):
    """Returns a list of lists of tile numbers"""
    results = []
    # Top row is always all 1s: 4 --> [1,1,1,1]
    top_row = make_list_of_1s(w) 
    results.append(top_row)
    for x in range(h - 2):
        middle_row = make_middle(w)
        results.append(middle_row)
    bottom_row = make_list_of_1s(w)
    results.append(bottom_row)
    # Middle rows, first tile is 1
    v_cord = []
    for row in range(h):
        for column in range(w):
            if results[row][column] == 1 and not is_corner(column,row,w,h):
                v_cord.append([row , column])
    v = choice(v_cord)
    #results[v[0]][v[1]] = 3
    return results


def is_doory(b):
    for y in b:
        for x in y:
            if x == 3:
                return True
    return False
    
print("SUCCESS!")
    
def if_outdoors(tile):
    if tile in (".","_","#"):
        return False
    return True

def on_map(x,y,m):
    """Returns True if x,y is within map m"""
    return (x > 0 and x < len(m[0]) and y > 0 and y < len(m))

def random_building(startx, starty, endx, endy, minwidth, minhight, maxhight, maxwidth):
    building_x = randint(startx, endx)
    building_y = randint(starty, endy)
    building_width = randint(minwidth,maxwidth)
    building_height = randint(minhight,maxhight)
    building = make_building(building_width, building_height)
    return (building_x, building_y, building)
    
def room_make(minwidth, minhight, maxhight, maxwidth):
    room_width = randint(minwidth,maxwidth)
    room_height = randint(minhight,maxhight)
    room = make_building(room_width, room_height)
    return room
    
def find_coordinates_where(f, l):
    results = []
    for y in range(len(l)):
        for x in range(len(l[0])):
            if f(l[y][x]):
                results.append((x, y))
    return results

def make_adjacent_room(main_room, big):
    room_height = len(main_room)
    room_width = len(main_room[0])
    if big:
        MIN_WIDTH = 4
        MIN_HEIGHT = 4
        MAX_WIDTH = room_width + 3
        MAX_HEIGHT = room_height + 3
    else:
        MIN_WIDTH = 3
        MIN_HEIGHT = 3
        MAX_WIDTH = room_width - 2
        MAX_HEIGHT = room_height - 2
    
    e_room = room_make(MIN_WIDTH, MIN_HEIGHT, MAX_HEIGHT, MAX_WIDTH)

    return e_room

def attach_adjacent_room(main_room, r, m, middle, direction, big):
    main_room_width = len(main_room[0])
    main_room_height = len(main_room)
    r_height = len(r)
    r_width = len(r[0])

    width_diff = abs(main_room_width - r_width)
    height_diff = abs(main_room_height - r_height)
    
    modmod = 3  
    smallxmod_min = 0 - r_width + modmod
    smallxmod_max = width_diff - modmod + 1
    smallymod_min = 0 - r_height + modmod
    smallymod_max = height_diff - modmod + 1
    #print("xmod: range(%d, %d)" % (smallxmod_min, smallxmod_max))
    #print("ymod: range(%d, %d)" % (smallymod_min, smallymod_max))
    #print("")
    xmod = randint(smallxmod_min, smallxmod_max) if big else randint(0, width_diff)
    ymod = randint(smallymod_min, smallymod_max) if big else randint(0, height_diff)

    xs = [ middle + xmod
         , middle + xmod
         , middle + main_room_width - 1
         , middle - r_width + 1
         ]

    ys = [ middle - r_height + 1
         , middle + main_room_height - 1
         , middle + ymod
         , middle + ymod
         ]
    door_x_min = middle + xmod + 1
    door_x_max = middle + xmod + r_width - 1
    
    main_right_edge_x = middle + main_room_width
    main_top_y = middle
    main_bottom_y = main_top_y + main_room_height
    east_room_top_y = middle + ymod + 1
    east_room_bottom_y = east_room_top_y + r_height - 2
    
    south_room_left_edge = middle + xmod + 1
    south_room_right_edge = south_room_left_edge + r_width - 2
    
    main_edges = [[(x, middle) for x in range(middle + 1, middle + main_room_width)],
                  [(x, main_bottom_y - 1) for x in range(middle + 1, middle + main_room_width - 1)],
                  [(main_right_edge_x - 1, y) for y in range(main_top_y, main_bottom_y)],
                  [(middle, y) for y in range(main_top_y + 1, main_bottom_y)]
                 ]
    edges = [[(x, middle) for x in range(door_x_min, door_x_max)],
             [(x, main_bottom_y - 1) for x in range(south_room_left_edge, south_room_right_edge)],
             [(main_right_edge_x - 1, y) for y in range(east_room_top_y, east_room_bottom_y)],
             [(middle, y) for y in range(east_room_top_y, east_room_bottom_y)]
            ]
    
    
    stamp(xs[direction], ys[direction], r, m)
    main_edge = set(main_edges[direction])
    room_edge = set(edges[direction])
    finding_doory = list(main_edge.intersection(room_edge))
    doorx,doory = choice(finding_doory)
    #m[doory][doorx] = 3

        
def pick_door(m):
    l = find_coordinates_where(lambda x: x == 1, m)
    l = list(filter(lambda w: num_neighbors(m, w[0], w[1], 0) == 1, l))
    l = list(filter(lambda w: num_neighbors(m, w[0], w[1], 2) == 1, l))
    return choice(l)

def trim_building(b_map):
    ws = find_coordinates_where(lambda x: x == 1, b_map)
    westx = min(ws, key=lambda c: c[0])[0] 
    eastx = max(ws, key=lambda c: c[0])[0] + 1
    northy = min(ws, key=lambda c: c[1])[1] 
    southy = max(ws, key=lambda c: c[1])[1] + 1
    return list(np.array(b_map)[northy:southy, westx:eastx])
    
def random_building2(minwidth, minhight, maxhight, maxwidth):
    bmap_width = 50
    b_map = [[2 for x in range(bmap_width)] for y in range(bmap_width)]
    middle = int(bmap_width / 2)
    
    room = room_make(minwidth, minhight, maxhight, maxwidth)
    stamp(middle, middle, room, b_map)
    b = randint(0, 3)
    l = list(range(4))
    for direction in shuffled(l)[:3]:
        new_room = make_adjacent_room(room, True if b == direction else False)
        attach_adjacent_room(room, new_room, b_map, middle, direction, True if b == direction else False)
    for x in range(choice([1, 1, 2, 2, 2, 3])):
        dx, dy = pick_door(b_map)
        #b_map[dy][dx] = 3
    return trim_building(b_map)
    

#for x in range(10):
#    b = random_building2(25, 25, 0, 0, 5,5,7,7)
#    for r in b:
#        l = list(map(str,r))    
#        print("".join(l).replace( "0", "."))
    
    
