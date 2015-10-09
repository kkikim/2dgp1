import random
from pico2d import *
class Boy:

    def __init__ (self):
        self.x, self.y = random.randint(100,700), 90
        self.frame=random.randint(0,5)
        self.image = load_image('2d image/2dsource/summon2.png')
        self.state=0
        self.reverse1 = random.randint(100,700)
        self.reverse2 = self.reverse1 - random.randint(0,100)

    def update(self):
        self.frame = (self.frame +1)%4
        if self.state==0:
            self.x=self.x+5
           # if(self.x>800):
              #  self.state=1


        elif self.state==1:
            self.x=self.x-5
           # if(self.x<0):
              #  self.state =0

    def collison(self):
        if self.x>self.reverse1:
            self.state=1
        elif self.x<self.reverse2:
            self.state=0

    def draw(self):
        self.image.clip_draw(self.frame*75,0,75,75,self.x,self.y)

class Grass:
    def __init__(self):
        self.image = load_image('2d image/2dsource/stage2.png')
    def draw(self):
        self.image.draw(800 ,450)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

open_canvas(1600,900)

boy=Boy()
grass=Grass()

running = True

while running :
    handle_events()

    boy.update()
    clear_canvas()
    grass.draw()
    boy.draw()
    boy.collison()
    update_canvas()

    delay(0.05)

close_canvas()