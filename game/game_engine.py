import pygame
import random
from game.player import Player
from game.world import generate_platforms, draw_lava, PLATFORM_COLOR, CRUMBLE_COLOR

WIDTH,HEIGHT=500,640
FPS=60
BG=(20,15,30)
GROUND_Y=HEIGHT+200

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Lava Escape")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",24,bold=True)
        self.big_font=pygame.font.SysFont("monospace",42,bold=True)
        self.reset()

    def reset(self):
        self.platforms=generate_platforms(WIDTH,GROUND_Y)
        # mark some platforms as crumbling (skip ground and top one)
        self.ptypes=['normal']*len(self.platforms)
        self.ptypes[0]='ground'
        for i in range(2,len(self.platforms)-1):
            if i%4==0:
                self.ptypes[i]='crumble'
        self.crumble_t=[0]*len(self.platforms)  # 0 means untouched, else frames touched
        self.player=Player(WIDTH//2-16,GROUND_Y-50)
        self.cam_y=0
        self.lava_y=GROUND_Y+60
        self.lava_rise=0.4
        self.score=0
        self.game_over=False
        self.won=False
        self.top_y=self.platforms[-1].y
        self.frame=0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r: self.reset()
        return True

    def update(self):
        if self.game_over or self.won: return
        keys=pygame.key.get_pressed()
        self.player.update(keys,self.platforms,WIDTH)
        # crumbling logic - start timer when player stands on it
        idx=self.player.standing_on
        if idx is not None and idx<len(self.ptypes) and self.ptypes[idx]=='crumble':
            if self.crumble_t[idx]==0:
                self.crumble_t[idx]=1
        # tick all crumbling platforms, remove after 60 frames (1 sec)
        remove=[]
        for i in range(len(self.platforms)):
            if self.ptypes[i]=='crumble' and self.crumble_t[i]>0:
                self.crumble_t[i]+=1
                if self.crumble_t[i]>60:
                    remove.append(i)
        for i in reversed(remove):
            del self.platforms[i]
            del self.ptypes[i]
            del self.crumble_t[i]
            # fix standing index if needed
            if self.player.standing_on==i:
                self.player.standing_on=None
                self.player.on_ground=False
            elif self.player.standing_on is not None and self.player.standing_on>i:
                self.player.standing_on-=1
        target=self.player.rect.centery-HEIGHT//2
        if target<self.cam_y: self.cam_y=target
        self.lava_y-=self.lava_rise
        self.lava_rise=min(1.2,self.lava_rise+0.0003)
        self.score=max(0,(GROUND_Y-self.player.rect.y)//10)
        self.frame+=1
        if self.player.rect.bottom>=self.lava_y:
            self.game_over=True
        if self.player.rect.top<=self.top_y-20:
            self.won=True

    def draw(self):
        self.screen.fill(BG)
        for i,p in enumerate(self.platforms):
            dr=p.move(0,-int(self.cam_y))
            if self.ptypes[i]=='crumble':
                # shake when timer started
                if self.crumble_t[i]>0:
                    dr.x+=random.randint(-3,3)
                    # blink as it is about to break
                    if self.crumble_t[i]>40 and (self.frame%6<3):
                        continue  # flicker
                pygame.draw.rect(self.screen,CRUMBLE_COLOR,dr,border_radius=4)
            else:
                pygame.draw.rect(self.screen,PLATFORM_COLOR,dr,border_radius=4)
        self.player.draw(self.screen,self.cam_y)
        draw_lava(self.screen,self.lava_y,self.cam_y,WIDTH,HEIGHT,self.frame)
        sc=self.font.render(f"Height: {self.score}m  R=Restart",True,(220,200,180))
        self.screen.blit(sc,(8,10))
        if self.game_over:
            self._msg("LAVA GOT YOU!",(220,80,40))
        if self.won:
            self._msg("ESCAPED!",(80,220,100))
        pygame.display.flip()

    def _msg(self,text,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,150))
        self.screen.blit(ov,(0,0))
        m=self.big_font.render(text,True,color)
        s=self.font.render("Press R to Play Again",True,(200,200,200))
        self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-40))
        self.screen.blit(s,(WIDTH//2-s.get_width()//2,HEIGHT//2+20))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
