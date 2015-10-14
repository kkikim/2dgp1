import random
import json
import os

from pico2d import *

import game_framework
import title_state

name = "stage1"

mainch = None
Bg = None
font = None

class background:
    def __init__(self):
        self.image = load_image('2d image/2dsource/stage2.png')

    def draw(self):
        self.image.draw(800, 450)

class boss1:
    def __init__(self):
        self.x, self.y = 800, 450
        self.frame = 0
        self.image = load_image('2d image/2dsource/boss1.png')
    def update(self):
        delay(0.01)
        self.frame = (self.frame +1)%3
    def draw(self):
        self.image.clip_draw(self.frame*200,0,200,200,self.x,self.y)

class Mainch:
    LEFT_RUN, RIGHT_RUN, LEFT_STAND,RIGHT_STAND, UP_RUN, DOWN_RUN = 0, 1, 2, 3, 4, 5

    def __init__(self):
        self.x, self.y = 450, 450
        self.standframe= 0
        self.frame = 0                  # 걸어다닐때
        self.dashframe = 0              #
        self.state = self.RIGHT_STAND
        self.tempstate = self.RIGHT_STAND
        #서있을떄
        self.standimage = load_image('2d image/2dsource/stand_right.png')
        self.standimage2 = load_image('2d image/2dsource/stand_left.png')

        #보통 다닐때
        self.image = load_image('2d image/2dsource/walk_foward.png')
        self.image2 = load_image('2d image/2dsource/walk_back.png')
        self.image3 = load_image('2d image/2dsource/walk_foward.png')
        self.image4 = load_image('2d image/2dsource/walk_foward.png')

        #대쉬상태
        self.dashimage = load_image('2d image/2dsource/dash_foward.png')     #앞 대쉬   #대쉬 이미지
        self.dashimage2 = load_image('2d image/2dsource/dash_back.png')      #뒤 대쉬
        self.dashimage3 = load_image('2d image/2dsource/dash_up.png')        #윗 대쉬
        self.dashimage4 = load_image('2d image/2dsource/dash_down.png')     #아랫 대쉬
        self.dir = 1    #방향4
        self.boost = False

    def update(self):
        self.frame = (self.frame + 1) % 6
        self.dashframe = (self.dashframe+1)%3
        self.standframe = (self.standframe+1)%10
        if self.boost==True:
            boostspeed = 5
        elif self.boost == False:
            boostspeed=0

        if self.state == self.RIGHT_RUN:
            self.x = min(1580, self.x + 5+boostspeed)
        elif self.state == self.LEFT_RUN:
            self.x = max(60, self.x - 5-boostspeed)
        elif self.state == self.UP_RUN:
            self.y = min(880, self.y + 5+boostspeed)
        elif self.state == self.DOWN_RUN:
            self.y = max(60, self.y - 5-boostspeed)
        pass
    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_v):
            self.boost=True
        if (event.type, event.key) == (SDL_KEYUP, SDLK_v):
            self.boost = False
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT_STAND,self.LEFT_STAND ,self.RIGHT_RUN, self.UP_RUN, self.DOWN_RUN):
                self.state = self.LEFT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.RIGHT_STAND,self.LEFT_STAND, self.LEFT_RUN, self.UP_RUN, self.DOWN_RUN):
                self.state = self.RIGHT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.RIGHT_STAND,self.LEFT_STAND, self.RIGHT_RUN, self.LEFT_RUN, self.DOWN_RUN):
                self.state = self.UP_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.RIGHT_STAND,self.LEFT_STAND, self.RIGHT_RUN, self.LEFT_RUN, self.UP_RUN):
                self.state = self.DOWN_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN,):
                self.state = self.LEFT_STAND
                self.tempstate = self.LEFT_STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN,):
                self.state = self.RIGHT_STAND
                self.tempstate = self.RIGHT_STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            if self.state in (self.UP_RUN,):
                self.state = self.tempstate
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state in (self.DOWN_RUN,):
                self.state = self.tempstate
    def draw(self):
        if self.boost == True:
            if self.state==self.RIGHT_STAND:
                self.standimage.clip_draw(self.standframe * 100, 0, 100, 100, self.x, self.y)
            elif self.state==self.LEFT_STAND:
                self.standimage2.clip_draw(self.standframe * 100, 0, 100, 100, self.x, self.y)
            elif self.state==self.RIGHT_RUN:
                self.dashimage.clip_draw(self.dashframe*100,0,100,100,self.x, self.y)   #대쉬 앞
            elif self.state==self.LEFT_RUN:
                self.dashimage2.clip_draw(self.dashframe*100,0,100,100,self.x, self.y)  #대쉬 뒤
            elif self.state==self.UP_RUN:
                self.dashimage3.clip_draw(self.dashframe*100,0,100,100,self.x, self.y)
            elif self.state==self.DOWN_RUN:
                self.dashimage4.clip_draw(self.dashframe*100,0,100,100,self.x, self.y)
        elif self.boost ==False :
            if self.state==self.RIGHT_STAND:
                self.standimage.clip_draw(self.standframe * 100, 0, 100, 100, self.x, self.y)
            elif self.state==self.LEFT_STAND:
                self.standimage2.clip_draw(self.standframe * 100, 0, 100, 100, self.x, self.y)
            elif self.state== self.RIGHT_RUN:
                self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
            elif self.state== self.LEFT_RUN:
                self.image2.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
            elif self.state== self.UP_RUN:
                self.image3.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
            elif self.state== self.DOWN_RUN:
                self.image4.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

def enter():
    open_canvas(1600,900)
    global mainch, Bg, boss
    mainch = Mainch()
    Bg = background()
    boss = boss1()

def exit():
    global mainch, Bg, boss
    del(mainch)
    del(Bg)
    del(boss)

def pause():
    pass

def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        for event in events:
            if event.type == SDL_QUIT:
                game_framework.quit()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            else:
                mainch.handle_event(event)
                pass

def update():
    mainch.update()
    boss.update()

def draw():
    clear_canvas()
    Bg.draw()
    mainch.draw()
    boss.draw()
    update_canvas()