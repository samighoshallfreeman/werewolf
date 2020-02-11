import curses
from globals import MAP_HEIGHT, MAP_WIDTH, CAM_WIDTH, CAM_HEIGHT
from random import randint
import numpy as np
from misc import irounds

tiles = {0: (".",0, True),
         1: ("#",2, False),
         2: ("\"",3, True),
         3: ("_",1, True),
         4: ("~",12, True),
         5: ("@",9, True),
         6: ("O",7, False),
         7: ("o",8, True),
         8: ("o",2, False),
         9: ("*",14, True)}
         
def display_news(screen, news):
    top_news = news[-5:]
    top_news.reverse()
    cn = 0
    for n in top_news:
        screen.addstr(CAM_HEIGHT + cn, 0, " " * CAM_WIDTH, curses.color_pair(5 + cn)), 
        screen.addstr(CAM_HEIGHT + cn, 0, n, curses.color_pair(5 + cn))
        cn += 1
        
def limit(foo,limit, bottom=0):
    if foo <= limit and foo >= bottom:
        return foo
    elif foo <= limit and foo <= bottom:
        return bottom
    else:
        return limit
assert(limit(10,5) == 5)
assert(limit(10,30) == 10)
assert(limit(-10,10) == 0)

def winit_color(cn, r, g, b):
    nr = limit(r,1000)
    ng = limit(g,1000)
    nb = limit(b,1000)
    curses.init_color(cn, nr, ng, nb)
    
def night_colors():
    winit_color(2, 450, 300, 100)
    winit_color(3, 0, 600, 100)
    winit_color(4, 600, 400, 255)
    winit_color(5, 800, 800, 800)
    winit_color(13, 600, 180, 670)
    winit_color(14,700, 0, 0)
    winit_color(21, 1000, 1000, 0)
    
    curses.init_pair(1, 2, curses.COLOR_BLACK)
    curses.init_pair(2, 2, curses.COLOR_BLACK )
    curses.init_pair(3, 3, curses.COLOR_BLACK ) 
    curses.init_pair(4, 4, curses.COLOR_BLACK)
    curses.init_pair(5, 5, curses.COLOR_BLACK)
    curses.init_pair(13, 13, curses.COLOR_BLACK)
    curses.init_pair(14, 14, curses.COLOR_BLACK)
    curses.init_pair(21, 21, curses.COLOR_BLACK)

def day_colors():
    winit_color(2, 600, 400, 255)
    winit_color(3, 0, 1000, 0)
    winit_color(4, 800, 600, 455)
    winit_color(5, 1000, 1000, 1000)
    winit_color(14,800, 0, 0)
    curses.init_pair(14, 14, curses.COLOR_BLACK)
    

def init_colors(mod=0):
    night_colors()
    
    # Shades of grey for news
    winit_color(6, 800, 800, 800)
    winit_color(7, 600, 600, 600)
    winit_color(8, 400, 400, 400)
    winit_color(9, 300, 300, 300)
    
    winit_color(10, 800, 600, 300)

    winit_color(20, 760, 280, 100)
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, 2, curses.COLOR_BLACK) #walls, brown on black
    curses.init_pair(3, 3, curses.COLOR_BLACK) 
    curses.init_pair(4, 4, curses.COLOR_BLACK)
    curses.init_pair(5, 5, curses.COLOR_BLACK)
    
    # News fadeout
    curses.init_pair(6, 6, curses.COLOR_BLACK)
    curses.init_pair(7, 7, curses.COLOR_BLACK)
    curses.init_pair(8, 8, curses.COLOR_BLACK)
    curses.init_pair(9, 9, curses.COLOR_BLACK)
    
    curses.init_pair(10, 10, curses.COLOR_BLACK)
    curses.init_pair(11, 11, curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(20, 20, curses.COLOR_BLACK)
    
def draw_map(screen, tiles, m, cx, cy):
    for row in range(CAM_HEIGHT):
        for column in range(CAM_WIDTH):
            vcx = column + cx
            vcy = row + cy
            if vcx < MAP_WIDTH and vcx >= 0:
                if vcy  < MAP_HEIGHT and vcy >= 0:
                    cur_tile_num = m[vcy][vcx]
                    cur_tile = tiles[cur_tile_num][0]
                    screen.addstr(row, column, cur_tile, curses.color_pair(tiles[cur_tile_num][1]))

def display_hp(screen, hp):
    s = "+" * hp
    screen.addstr(14, CAM_WIDTH + 1, "        +++++",curses.color_pair(9))
    screen.addstr(14, CAM_WIDTH + 1, "health: " + s, curses.color_pair(14))
    
def display_inv(screen, inventory):
    screen.addstr(0, CAM_WIDTH + 1, "Inventory:")
    ci = 1
    for i in inventory:
        screen.addstr(ci, CAM_WIDTH + 1, str(ci) + ") ", curses.color_pair(0))
        screen.addstr(ci, CAM_WIDTH + 4, i.icon, curses.color_pair(i.color))
        screen.addstr(ci, CAM_WIDTH + 5, ": " + i.name, curses.color_pair(0))
        ci += 1
def display_clock(screen, clock):
    screen.addstr(12,CAM_WIDTH + 1, "[-----|-----]")
    x = int(clock/60)
    if clock <= 300:
        sky = "o"
    else:
        x += 1
        sky = "*"
    screen.addstr(12,CAM_WIDTH + x + 2, sky, curses.color_pair(21))

def atlas_tile(sx, sy, w, h, world):
    worth = {
    0: 2,
    1: 4,
    2: 1,
    3: 0,
    4: 2,
    5: 1,
    6: 1,
    7: 1,
    8: 4,
    9: 3,}
    d = {}
    wslice = np.array(world)[sy: sy + h, sx: sx + w]
    for y in wslice:
        for cur_tile in y:
            if cur_tile in d:
                d[cur_tile] += worth[cur_tile]
            else:
               d[cur_tile] = worth[cur_tile]
    return max(d, key=lambda x: d[x])
test_map = [
[1,1,2],
[3,1,1],
[2,1,1]]

print(atlas_tile(0,0,3,3,test_map))              
def make_atlas(m, atlas_length):
    print("   * generating map")
    a = []
    tile_equ = int(MAP_WIDTH / atlas_length)
    foo = [x * tile_equ for x in range(atlas_length)]
    for y in foo:
        row = []
        for x in foo:
            row.append(atlas_tile(x, y, tile_equ, tile_equ, m))
        a.append(row)
    return a

def display_atlas(screen, atlas, player):
    px = irounds(MAP_WIDTH / 9, player.x)
    py = irounds(MAP_HEIGHT / 9, player.y)
    screen_height, screen_width = screen.getmaxyx()
    for y in range(len(atlas)):
        for x in range(len(atlas)):
            t = tiles[atlas[y][x]]
            screen.addstr(2 + y, screen_width - 11 + x, t[0] , curses.color_pair(t[1]))
    screen.addstr(2 + py, screen_width - 11 + px, player.icon, curses.color_pair(player.color))        
    