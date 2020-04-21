from globals import news, CAM_HEIGHT, CAM_WIDTH
import wlib
import curses 
import misc

def healing_potion_effect(player, creatures, m, objects, global_objects, screen, global_cs):
    player.hp += 2
    if player.hp > player.hp_limit:
        player.hp = player.hp_limit
        wlib.news.append("but you couldn't heal much")
    news.append("you drank a healing potion. glug, glug")

def speed_potion_effect(player,creatures,m, objects, global_objects, screen, global_cs):
    o = filter(lambda x: x.icon != "w", creatures)
    for x in o:
        x.stun_timer = 3
    news.append("you drank a speed potion. glug, glug")
    
def strength_potion_effect(player,creatures, m, objects, global_objects, screen, global_cs):
    player.hp_limit += 1
    news.append("you drank a strength potion. glug, glug")

def invisibility_potion_effect(player, creatures,m, objects, global_objects, screen, global_cs):
    player.invisibility_timer = 8
    news.append("you drank an invisibility potion. glug, glug")
    
def flower_effect(player, creatures, m, objects, global_objects, screen, global_cs):
    flower = wlib.Object(player.x, player.y, "*", 14, "a flower", "that flower smells good" )
    objects.append(flower)
    global_objects.append(flower)
    news.append("you planted a flower")

def sheild_effect(player, creatures, m, objects, global_objects, screen, global_cs):
    sheild = wlib.Object(player.x, player.y, "]", 7, "a sheild", "a sheild" )
    objects.append(sheild)
    global_objects.append(sheild)
    news.append("you threw your sheild... why?")
    
def apple_effect(player, creatures, m, objects, global_objects, screen, global_cs):
    news.append("you ate an apple! munch munch")
    player.fullness += 20.0

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
    
def bow_effect(player, creatures, m, objects, global_objects, screen, global_cs):
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
    player.inventory.append(make_item("a bow"))
        
items =   { "a healing potion": (healing_potion_effect, "8", 13)
          , "a speed potion": (speed_potion_effect, "8", 13)
          , "an invisibility potion": (invisibility_potion_effect, "8", 13)
          , "a strength potion": (strength_potion_effect, "8", 13)
          , "a sheild": (sheild_effect, "]", 8)
          , "a bow": (bow_effect, "}", 1)
          , "an arrow": (lambda a, b, c, d, e, f, g: None, "/", 1) 
          , "an apple": (apple_effect, "6", 14)
          } 
          
def make_item(name, x=0, y=0):
    i = items[name]
    new_obj = wlib.Object(x,y, i[1], i[2], name, name)
    #new_obj.effect = i[1]
    return new_obj
