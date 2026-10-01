import pygame
import random

PLATFORM_COLOR = (100,80,50)
CRUMBLE_COLOR = (180,110,60)
LAVA_COLOR = (220,60,20)

def generate_platforms(width, base_y, count=30):
    plats = [pygame.Rect(0, base_y, width, 20)]  # ground
    y = base_y - 110
    for i in range(count):
        w = random.randint(80,200)
        x = random.randint(0, width-w)
        plats.append(pygame.Rect(x, y, w, 16))
        y -= random.randint(80,130)
    return plats

def draw_lava(screen, lava_y, cam_y, width, height, frame):
    import math
    ly = int(lava_y - cam_y)
    if ly < height:
        # lava surface wave
        pts=[(0,ly)]
        for x in range(0,width+20,20):
            pts.append((x, ly + int(math.sin(x*0.08+frame*0.1)*8)))
        pts.append((width,height)); pts.append((0,height))
        pygame.draw.polygon(screen,LAVA_COLOR,pts)
        # glow
        s=pygame.Surface((width,30),pygame.SRCALPHA)
        for i in range(15):
            pygame.draw.line(s,(255,100,0,max(0,60-i*4)),(0,i),(width,i),1)
        screen.blit(s,(0,ly-15))
