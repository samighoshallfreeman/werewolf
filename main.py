import curses
import store
from wlib import *
import wlib
from random import randint, choice

from display import *
from mapgen import village, gen_objects, build_world, potions, under_color
import mapgen


def on_cam(t, cam_x, cam_y):
    if t.x < cam_x + CAM_WIDTH and t.y < cam_y + CAM_HEIGHT:
        if t.x > cam_x and t.y > cam_y:
            return True
    return False
    
def make_world():
    m = [[2 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]
    print("Building world...")
    objects = []
    cs = []
    build_world(mapgen.zones, m, objects, cs)
    #objects += gen_objects(m)
    coin = Object(randint(1, MAP_WIDTH), randint(1, MAP_HEIGHT), "$", 11, "a coin", "oooh, a coin")
    player = Creature(mapgen.ZONE_LENGTH, mapgen.ZONE_LENGTH, "w", 14, 3, "werewolf")
    cs += [player]
    
    news.append("WELCOME TO WEREWOLF")
    
    return (m, player, objects, cs)
    
def main(screen, world):
    clock = 0
    inp = 0 
    curses.curs_set(False) # Disable blinking cursor
    init_colors()
    
    m, player, global_objects, global_cs = world
    
    atlas = make_atlas(m, 9)
    
    zx = rounds(mapgen.ZONE_LENGTH, player.x)
    zy = rounds(mapgen.ZONE_LENGTH, player.y)
    objects = get_local(zx, zy, global_objects)
    cs = get_local(zx, zy, global_cs)    
    
    while(inp != 113): # Quit game if player presses "q"
        screen.clear()
        if clock <= 300:
            display.night_colors()
            player.mode = "werewolf"
            player.icon = "w"
            player.color = 14
            player.original_color = 14
        else:
            display.day_colors()
            player.mode = "human"
            player.icon = "@"
            player.color = 1
            player.original_color = 1
        
        keyboard_input(inp, player, m, cs, objects, screen, global_objects, global_cs)

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
                elif c.icon == "g":
                    move_guard(c,player,m,cs,objects)

            if c.stun_timer != 0:
                c.stun_timer -= 1

            if c.invisibility_timer != 0:
                c.invisibility_timer -= 1
                c.color = under_color(c, m)
                if c.invisibility_timer == 0:
                    c.color = c.original_color                

        if player.hp <= 0:
            print("yea")
            return
        # display callz
        for c in cs:
            if on_cam(c,cam_x,cam_y):
                    screen.addstr(c.y - cam_y, c.x - cam_x, c.icon, curses.color_pair(c.color))
                    
        display_atlas(screen, atlas, player)
            
        display_news(screen, news)
     
        display_inv(screen, player.inventory)
        
        display_hp(screen, player.hp)

        screen.addstr(13, CAM_WIDTH + 1, "gold: " + str(player.gold), curses.color_pair(21))
        
        display_clock(screen, clock)
            
        screen.refresh()

        inp = screen.getch()

        clock += 1
        
        if inp == ord('x'):
            clock += 100
        
        if clock >= 600:
            clock = 0
            

world = make_world()
curses.wrapper(main, world)
inventory = []
player = Creature(ZONE_LENGTH, ZONE_LENGTH, "w", 14, 3, "werewolf")
merchant = Creature(ZONE_LENGTH, ZONE_LENGTH, "w", 14, 3, "werewolf")
for x in range(3):
    p, effect = choice(potions)
    potion = wlib.Object(0, 0, "8", 13, p, p, 5)
    potion.effect = effect
    merchant.inventory.append(potion)


g = 10
msg = ""
n = choice(["Gerald", "Sathy", "Randy", "Joshua"])
#curses.wrapper(store.buy_sell, merchant, player, n, "\"Hello, I am %s, can I buy stuff from you.\""% n, "\"Thanks! Here is your gold\"")
#curses.wrapper(store.buy_sell, player, merchant, n, "\"Hello, I am %s, these are my wares.\""% n, "You bought ")