import curses
import store
from wlib import *
import wlib
from random import randint, choice
from display import *
from mapgen import village, gen_objects, build_world, items, under_color
import mapgen
from globals import news
import globals
from items import make_item

    
def make_world():
    m = [[2 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]
    print("Building world...")
    objects = []
    cs = []
    build_world(mapgen.zones, m, objects, cs)
    #objects += gen_objects(m)
    coin = Object(randint(1, MAP_WIDTH), randint(1, MAP_HEIGHT), "$", 11, "a coin", "oooh, a coin")
    player = Creature(mapgen.ZONE_LENGTH, mapgen.ZONE_LENGTH, "w", 14, 3, "werewolf")
    player.inventory = [make_item("an apple")]
    cs += [player]
    
    atlas = make_atlas(m, 9)
    
    news.append("WELCOME TO WEREWOLF")
    
    return (m, player, objects, cs, atlas, 0, [])

def initialize(screen, world):
    highscores = read("highscores")
    clock = 0
    inp = 0 
    curses.curs_set(False) # Disable blinking cursor
    init_colors()
    
    m, player, global_objects, global_cs, atlas, globals.time_alive, globals.news = world
    shark(m, global_cs)
    if player.hp <= 0:
        for x in filter(lambda c: c.icon == "w" and c.hp <= 0, global_cs): 
            corpse = Object(x.x, x.y, "%", 14, "a werewolf corpse", "eww a dead werewolf")
            global_objects.append(corpse)
            global_cs.remove(x)
        player = Creature(mapgen.ZONE_LENGTH, mapgen.ZONE_LENGTH, "w", 14, 3, "werewolf")
        player.inventory = [make_item("an apple")]
        global_cs += [player]
    
    zx = rounds(mapgen.ZONE_LENGTH, player.x)
    zy = rounds(mapgen.ZONE_LENGTH, player.y)
    objects = get_local(zx, zy, global_objects)
    cs = get_local(zx, zy, global_cs)
    world = (m, player, global_objects, global_cs, atlas, globals.time_alive, globals.news)
    return world, clock, inp, zx, zy, cs, objects, highscores 

def main(screen, world):
    world, clock, inp, zx, zy, cs, objects, highscores = initialize(screen, world)
    m, player, global_objects, global_cs, atlas, globals.time_alive, globals.news = world    
    while(True):
        screen.clear()
        
        keyboard_input(inp, player, m, cs, objects, screen, global_objects, global_cs, tiles, atlas)
        change_colors(player, clock)
        
        if player.stun_timer == 0:    
            swim(m,player)
        
        new_zx = rounds(mapgen.ZONE_LENGTH, player.x)
        new_zy = rounds(mapgen.ZONE_LENGTH, player.y)
        if new_zx != zx or new_zy != zy:
            objects = get_local(new_zx, new_zy, global_objects)
            cs = get_local(new_zx, new_zy, global_cs)
            zx = new_zx
            zy = new_zy
            
        cam_y = player.y - int(CAM_HEIGHT / 2)
        cam_x = player.x - int(CAM_WIDTH / 2) 
        
        draw_map(screen, tiles, m, cam_x, cam_y)
        
        for o in filter(lambda o: on_cam(o, cam_x, cam_y), objects):
            screen.addstr(o.y - cam_y, o.x - cam_x , o.icon,curses.color_pair(o.color))
           
        for c in cs:
            if c.stun_timer == 0 and distance(c, player) <= CAM_WIDTH:
                if c.icon == "v":
                    move_villager(c,player,m,cs,objects)
                elif c.icon in ("g","^"):
                    move_guard(c,player,m,cs,objects)

            if c.stun_timer != 0:
                c.stun_timer -= 1
                

            if c.invisibility_timer != 0:
                c.invisibility_timer -= 1
                c.color = under_color(c, m)
                if c.invisibility_timer == 0:
                    c.color = c.original_color
                    
        player.fullness -= 0.1
        
        if player.fullness <= 10.0:
            globals.death = "you died of starvation"
            player.hp = 0
        if player.hp <= 0:
            die(m, player, global_objects, global_cs, atlas, screen, highscores)
            return    
        stuff_breaks(player)
        display_calls(screen, atlas, player, news, clock, cs, cam_x, cam_y)
            
        screen.refresh()

        inp = screen.getch()

        clock += 1
        
        if inp == ord('x') and globals.debug_mode == True:
            clock += 100
            globals.time_alive += 100
        
        if clock >= 400:
            clock = 0
            

world = read("world")
#world = make_world()
write(world, "world")
#exit()
curses.wrapper(main, world)