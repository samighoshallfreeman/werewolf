from random import randint, shuffle
from copy import deepcopy
from math import sqrt

def rotate_list(l, n = 1):
    newlist = l
    for x in range(n):
        newlist = list(zip(*newlist[::-1]))
    return newlist

def distance(c1, c2):
    a = c1.x - c2.x      
    b = c1.y - c2.y
    c = a**2 + b**2
    
    return sqrt(c)
    
def between(i1,i2,l):
    """between(1,3,l) == between(3,1,l)"""
    if i1 < i2:
        return l[i1:i2]
    else:
        return l[i2:i1]
    
def optupe(t):
    v1, v2 = t
    v1 *= -1
    v2 *= -1
    return (v1,v2)

def ordered(x,y):
    o1 = x if x < y else y
    o2 = x if x > y else y
    return (o1, o2)
    
def get_new_mods(xmod, ymod):
    if ymod == 0:
        return (0, randint(-1, 1))
    elif xmod == 0:
        return(randint(-1, 1), 0)
    else:
        assert(False)
        
def shuffled(l):
    l2 = deepcopy(l)
    shuffle(l2)
    return l2

def w_h(m):
    return (len(m[0]), len(m))

def limit(x,upper,lower):
    if x <= upper and x >= lower:
        return x
    else:
        return upper if x > upper else lower
        
def rounds(space, c):
    l = [x * space for x in range(1000)]
    return l[int(c/space)]
    
def irounds(space, c):
    l = [x * space for x in range(1000)]
    closest = l[int(c/space)]
    i = 0
    for foo in l:
        if closest == foo:
            return i
        i += 1

def collide(p, c):        
    return p.x == c.x and p.y == c.y
   