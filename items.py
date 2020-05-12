from globals import news, CAM_HEIGHT, CAM_WIDTH
import wlib
import curses 
import misc
import display
from random import choice, randint

def healing_potion_effect(player, creatures, m, objects, global_objects, screen, global_cs, self):
    player.hp += 2
    if player.hp > player.hp_limit:
        player.hp = player.hp_limit
        wlib.news.append("but you couldn't heal much")
    news.append("you drank a healing potion. glug, glug")
    player.inventory.remove(self)

def speed_potion_effect(player,creatures,m, objects, global_objects, screen, global_cs, self):
    o = filter(lambda x: x.icon != "w", creatures)
    for x in o:
        x.stun_timer = 3
    news.append("you drank a speed potion. glug, glug")
    player.inventory.remove(self)
def strength_potion_effect(player,creatures, m, objects, global_objects, screen, global_cs, self):
    player.hp_limit += 1
    news.append("you drank a strength potion. glug, glug")
    player.inventory.remove(self)
    
def invisibility_potion_effect(player, creatures,m, objects, global_objects, screen, global_cs, self):
    player.invisibility_timer = 8
    news.append("you drank an invisibility potion. glug, glug")
    player.inventory.remove(self)
    
def flower_effect(player, creatures, m, objects, global_objects, screen, global_cs, self):
    flower = wlib.Object(player.x, player.y, "*", 14, "a flower", "that flower smells good" )
    objects.append(flower)
    global_objects.append(flower)
    news.append("you planted a flower")
    player.inventory.remove(self)
    
def sheild_effect(player, creatures, m, objects, global_objects, screen, global_cs, self):
    sheild = wlib.Object(player.x, player.y, "]", 7, "a sheild", "a sheild" )
    objects.append(sheild)
    global_objects.append(sheild)
    news.append("you threw your sheild... why?")
    player.inventory.remove(self)
    
def apple_effect(player, creatures, m, objects, global_objects, screen, global_cs, self):
    news.append("you ate an apple! munch munch")
    player.fullness += 20.0
    player.inventory.remove(self)
    
def shoot(player, objects, global_objects, xv, yv, m, creatures, global_cs):    
    a = wlib.Object(player.x, player.y, "/", 1, "an arrow", "an arrow" )
    for x in range(5):
        a.y += yv
        a.x += xv
        cl = list(filter(lambda x: misc.collide(x, a), creatures)) 
        if cl != []:
            c = cl[0]
            if c.icon == "v":
                wlib.kill_v(c, player, objects, global_objects, m, creatures, global_cs)
            else:
                creatures.remove(c)
                news.append("you killed a guard")
                body = wlib.Object(c.x, c.y, "%", 1, "", "A dead villager. Eeeewwww.")
                objects.append(body)
        elif m[a.y][a.x] not in wlib.walkable() or list(filter(lambda x: misc.collide(x, a), objects)) != []:
            a.y -= yv
            a.x -= xv
            break
    objects.append(a)
    global_objects.append(a)
    
def bow_effect(player, creatures, m, objects, global_objects, screen, global_cs, self):
    cam_y = player.y - int(CAM_HEIGHT / 2)
    cam_x = player.x - int(CAM_WIDTH / 2)
    x = player.x - cam_x
    y = player.y - cam_y
    arrows = list(filter(lambda x: x.icon == "/", player.inventory))
    if arrows != []:
        screen.addstr(1, 1, "Wich way would you like to shoot the arrow?")
        screen.addstr(y - 1, x, "^", curses.color_pair(0))
        screen.addstr(y + 1, x, "v", curses.color_pair(0))
        screen.addstr(y, x + 1, ">", curses.color_pair(0))
        screen.addstr(y, x - 1, "<", curses.color_pair(0))
        inp = screen.getch()
        if inp == curses.KEY_DOWN:
            shoot(player, objects, global_objects, 0, 1, m, creatures, global_cs) 
        elif inp == curses.KEY_UP:
            shoot(player, objects, global_objects, 0, -1, m, creatures, global_cs) 
        elif inp == curses.KEY_LEFT:
            shoot(player, objects, global_objects, -1, 0, m, creatures, global_cs) 
        elif inp == curses.KEY_RIGHT:        
            shoot(player, objects, global_objects, 1, 0, m, creatures, global_cs)
        player.inventory.remove(arrows[0])
        self.hp -= 1
    
def axe_effect(player, creatures, m, objects, global_objects, screen, global_cs, self):
    junk = list(filter(lambda x: x.icon == "?", objects))
    junk = map(lambda w: (w, wlib.distance(w, player)), junk)
    junk = list(filter(lambda b: b[1] <= 1, junk))
    if junk == []:
        destroy_wood(player, m)
    else:
        b = min(junk, key=lambda t: t[1])[0]
        objects.remove(b)
        global_objects.remove(b)
        news.append("bash!")
        player.inventory.append(make_item("a piece of wood"))
    
def destroy_wood(player, m):
    wood = []
    p_neighbors = scan_map(player.x - 1, player.y - 1, 3, 3, m)
    wood = list(filter(lambda t: t[2] in (1, 8), p_neighbors))
    if wood != []:
        wy, wx, tilenum = choice(wood)
        m[wy][wx] = 2
        news.append("chop!")
        player.inventory.append(make_item("a piece of wood"))
def scan_map(start_x, start_y, width, height, map):
    l = []
    for x in range(start_x, width + start_x):
        for y in range(start_y, height + start_y):
            t = (y, x, map[y][x])
            l.append(t)
    return l
    
test_map = [[1,1,2,1],
            [1,1,3,5],
            [1,1,1,1],
            [1,1,2,3]]
            
test_result = scan_map(1,1,2,2,test_map) 
tile_nums = list(map(lambda t: t[2], test_result))
tile_nums.sort()
assert(len(test_result) == 4)
assert(tile_nums == [1,1,1,3])

def wood_effect(player, creatures, m, objects, global_objects, screen, global_cs, self):
    cam_y = player.y - int(CAM_HEIGHT / 2)
    cam_x = player.x - int(CAM_WIDTH / 2)
    x = player.x - cam_x
    y = player.y - cam_y
    screen.addstr(1, 1, "Were would you like to put the wood?")
    screen.addstr(y - 1, x, "#", curses.color_pair(0))
    screen.addstr(y + 1, x, "#", curses.color_pair(0))
    screen.addstr(y, x + 1, "#", curses.color_pair(0))
    screen.addstr(y, x - 1, "#", curses.color_pair(0))
    inp = screen.getch() 
    if inp == curses.KEY_DOWN:
        cord = (player.y + 1, player.x)
    elif inp == curses.KEY_UP:
        cord = (player.y - 1, player.x)
    elif inp == curses.KEY_LEFT:
        cord = (player.y, player.x - 1)
    elif inp == curses.KEY_RIGHT:        
        cord = (player.y, player.x + 1)
    m[cord[0]][cord[1]] = 1
    player.inventory.remove(self)

def chest_effect(player, creatures, m, objects, global_objects, screen, global_cs, self):
    display.chest_screen(screen, self, player)    
        
items =   { "a healing potion": (healing_potion_effect, "8", 13, 5)
          , "a speed potion": (speed_potion_effect, "8", 13, 4)
          , "an invisibility potion": (invisibility_potion_effect, "8", 13, 5)
          , "a strength potion": (strength_potion_effect, "8", 13, 5)
          , "a sheild": (sheild_effect, "]", 8, 5)
          , "a bow": (bow_effect, "}", 1, 6)
          , "an arrow": (lambda a, b, c, d, e, f, g: None, "/", 1, 3) 
          , "an apple": (apple_effect, "6", 14, 5)
          , "a flower": (flower_effect, "*", 14, 1)
          , "an axe": (axe_effect, "p", 1, 5)
          , "a piece of wood": (wood_effect, "=", 2, 3)
          , "a chest": (chest_effect, "=", 21, 6)
          } 
          
def make_item(name, x=0, y=0):
    i = items[name]
    new_obj = wlib.Object(x,y, i[1], i[2], name, name)
    new_obj.cost = randint(i[3] - 1, i[3] + 1)
    #new_obj.effect = i[1]
    return new_obj
