import random
import json
import os
import time
import math
import datetime

from pico2d import *

import game_framework
import title_state

name = "stage1"

time = 0

mainch = None
Bg = None
font = None
Fireball = list()   #리스트
Fireball2 = list()
Bullet = list()

fireball_ch = None     #변수
fireball2_ch = None
bullet = None

# stage1_boss = None
boss = None

#global mainch

class background:
    def __init__(self):
        self.image = load_image('2d image/2dsource/stage2.png')

    def draw(self):
        self.image.draw(800, 450)

class boss1:
    global bullet
    image=None

    def __init__(self) :
        self.x, self.y = 800, 450
        if self.image ==None:
            self.image = load_image('2d image/2dsource/boss1.png')
        self.frame = 0
        self.time =0
    def update(self) :
        self.frame = (self.frame + 1 ) % 3
    def draw(self) :
        self.image.clip_draw(self.frame*200,0,200,200,self.x,self.y)
    def getposx(self):
            return self.x
    def getposy(self):
            return self.y

class bullet:
    global boss
    image=None
    def __init__(self,angle) :
        self.x, self.y = boss.getposx(), boss.getposy()
        self.rad = 1
        self.frame=0
        self.angle = angle
        if self.image==None:
            self.image = load_image('2d image/2dsource/bullet.png')
    def update(self) :
        # if int(time.clock()) >3:
        self.frame = (self.frame + 1 ) % 15
        self.x += (self.rad*math.cos(self.angle))
        self.y += (self.rad*math.sin(self.angle))
        self.rad +=0.3

    def draw(self) :
        # if int(time.clock()) >bullet1time:
        self.image.draw(self.x,self.y)

class Mainch:
    LEFT_RUN, RIGHT_RUN, LEFT_STAND,RIGHT_STAND, UP_RUN, DOWN_RUN, UP_RUN2, DOWN_RUN2 = 0, 1, 2, 3, 4, 5,6,7
    KEY_DOWN_STATE, KEY_UP_STATE = 6,7

    global fireball_ch
    global fireball2_ch

    def __init__(self):

        self.x, self.y = 450, 450
        self.keyState =self.KEY_UP_STATE
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
        #if self.keyState == self.KEY_DOWN_STATE:
                #Fireball.append(fireball())
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
        #    부스터키
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_v):
            self.boost=True
        if (event.type, event.key) == (SDL_KEYUP, SDLK_v):
            self.boost = False

        #   파이어볼
        if self.state in (self.RIGHT_RUN, self.RIGHT_STAND ):
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
                fireball_ch.direction =1
                Fireball.append(fireball(fireball_ch.direction))
        if self.state in (self.LEFT_RUN, self.LEFT_STAND ):
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
                fireball_ch.direction =0
                Fireball.append(fireball(fireball_ch.direction))
        # 파이어볼2
        if self.state in (self.RIGHT_RUN, self.RIGHT_STAND ):
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
                fireball2_ch.direction =1
                Fireball2.append(fireball2(fireball2_ch.direction))
        if self.state in (self.LEFT_RUN, self.LEFT_STAND ):
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
                fireball2_ch.direction =0
                Fireball2.append(fireball2(fireball2_ch.direction))

        #     방향키
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
                if self.x <800:
                    self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
                elif self.x>800 :
                   self.image2.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
            elif self.state== self.DOWN_RUN:
                if self.x <800:
                    self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
                elif self.x>800 :
                   self.image2.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

class fireball:
    global mainch
    def __init__(self, dir):
        self.x2, self.y2 = self.x,self.y = mainch.x, mainch.y
        self.fireballframe = 0
        self.image = load_image('2d image/2dsource/fire_ball.png')
        self.direction = dir
        if dir == 1 :
            self.image = load_image('2d image/2dsource/fire_ball2.png')      #오른쪽에서 왼쪽으로 갈때
        elif dir == 0 :
            self.direction = -1

    def update(self):
        self.fireballframe = (self.fireballframe +1)%8
        self.x += (5 * self.direction)

    def draw(self):
        if mainch.state in (mainch.RIGHT_STAND, mainch.RIGHT_RUN, mainch.UP_RUN,mainch.DOWN_RUN, mainch.LEFT_STAND, mainch.LEFT_RUN):
            self.image.clip_draw(self.fireballframe*96,0,96,96,self.x,self.y)

class fireball2:
    global mainch
    def __init__(self, dir):
        self.x,self.y = mainch.x, mainch.y
        self.fireballframe = 0
        self.image = load_image('2d image/2dsource/mini_fire_ball2.png')
        self.direction = dir
        if dir == 1 :
            self.image = load_image('2d image/2dsource/mini_fire_ball.png')      #오른쪽에서 왼쪽으로 갈때
        elif dir == 0 :
            self.direction = -1

    def update(self):
        self.fireballframe = (self.fireballframe +1)%6
        self.x += (3 * self.direction)

    def draw(self):
        if mainch.state in (mainch.RIGHT_STAND, mainch.RIGHT_RUN, mainch.UP_RUN,mainch.DOWN_RUN, mainch.LEFT_STAND, mainch.LEFT_RUN):
            self.image.clip_draw(self.fireballframe*100,0,100,50,self.x,self.y)

def enter():
    open_canvas(1600,900)
    global mainch, Bg, boss, fireball_ch , fireball2_ch, bullet1
    mainch = Mainch()
    Bg = background()
    boss = boss1()
    fireball_ch = fireball(1)
    fireball2_ch = fireball2(1)
    bullet1 = bullet(1)

def exit():
    global mainch, Bg, boss,fireball_ch, fireball2_ch, bullet1
    del(mainch)
    del(Bg)
    del(boss)
    del(fireball_ch)
    del(fireball2_ch)
    del(bullet1)

def pause():
    pass

def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        else:
            mainch.handle_event(event)
            pass

def update():
    delay(0.01)
    global fireball
    global fireball2
    global bullet1
    mainch.update()
    boss.update()

    if bullet1.frame%5==0:
        i = 0
        while i < 18:
            i+=1
            Bullet.append(bullet(i*15))

    # for i in range(18) :
    #     Bullet.append(bullet(i*20))
    # Fireball.append(fireball(fireball_ch.direction))

    # for문을 통해 리스트 전체를 업데이트
    for i in Fireball:
        if i.x < 1700:
            i.update()
        if i.x >1700:
            Fireball.remove(i)
        if i.x<-100:
            Fireball.remove(i)

    for i in Fireball2:
        if i.x < 1700:
            i.update()
        if i.x >1700:
            Fireball2.remove(i)
        if i.x<-100:
            Fireball2.remove(i)

    for i in Bullet:
        if i.x < 1700:
            i.update()
        if i.x >1700:
            Bullet.remove(i)
        if i.x<-100:
            Bullet.remove(i)


def draw():
    clear_canvas()
    Bg.draw()
    mainch.draw()
    boss.draw()
    for i in Fireball:
        if -100<i.x < 1700:
            i.draw()
    for i in Fireball2:
        if -100<i.x < 1700:
            i.draw()
    for i in Bullet:
        if -100<i.x < 1700:
            i.draw()

    update_canvas()