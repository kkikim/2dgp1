import random
import json
import os
import time
import math
import random

from pico2d import *

import game_framework
import title_state
import gameover_state

name = "stage1"

time = 0

mainch = None
Bg = None
Hp = None
Hp2 = None
font = None

Fireball = list()   #리스트
Fireball2 = list()
Bullet = list()
Bullet2 = list()
Bullet3 = list()
Bullet4 = list()
Summons = list()
AnimationList = None
AnimationList2 = None

fireball_ch = None     #변수
fireball2_ch = None
shield_ch = None
bullet = None
bullet2 = None
bullet3 = None
bullet4 = None
sbullet = None

current_time =None
frame_time = None
timecheck = None
boss = None
summon1 = None

class DeathEffect:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAME_PER_DEATH_ACTION = 1

    def __init__(self, target):
        self.x = target.x
        self.y = target.y
        self.deathStartTime = get_time()
        self.isDeath = True
        self.total_frames = 0;
        self.totla_images = 8;
        self.frame = 0

        self.image = None
        if self.image ==None:
            self.image = load_image('2dsource/explore.png')

    def isDeathEnd(self):
        return (self.frame == (self.totla_images - 1))

    def update(self, frame_time):
        self.total_frames += self.FRAME_PER_DEATH_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.totla_images

    def draw(self):
        self.image.clip_draw(self.frame*63,0,63,78,self.x,self.y)

class UI:
    def __init__(self):
        self.score = 0
        self.font = load_font('ConsolaMalgun.ttf', 40)
        self.time = 0.0

    def update(self, frame_time):
        self.time = get_time()

    def draw(self):
        # print('score %d time %f' % (self.score, self.time))
        self.font.draw(1100, 50, 'SCORE %d TIME %f' % (self.score, self.time))

class hpbar:
    global mainch, boss
    def __init__(self):
        self.hp = mainch.hp*2.3
        self.image = load_image('2dsource/HP.png')
        self.image2 = load_image('2dsource/HPtool.png')
        self.image3 = load_image('2dsource/skillbar.png')
    def update(self,mainch):
        self.hp = mainch.hp*2.3
    def draw(self):
        self.image2.draw(230,50)
        self.image.clip_draw(1*75,0,int(self.hp),15,230,50)
        self.image3.draw(800,50)
class background:
    bgm = None
    def __init__(self):
        self.image = load_image('2dsource/stage2.png')
        self.image2 = load_image('2dsource/background.png')
        if background.bgm ==  None :
            background.bgm = load_music('2dsound/background.mp3')
            background.bgm.set_volume(60)
            background.bgm.repeat_play()
    def draw(self):
        self.image2.draw(800,450)
        self.image.draw(800, 500)

class summonbullet:
    global summon1
    image=None

    PIXEL_PER_METER = (10.0/0.3)                    #10 pixel 3ocm
    RUN_SPEED_KMPH = 40.0                           #KM/HOUR
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM/60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self, angle, summon1) :
        self.x, self.y = summon1.getposx(), summon1.getposy()
        self.rad = 1
        self.total_frames = 0.0
        self.frame=0
        self.angle = angle * (3.141592/180.0)

        if self.image==None:
            self.image = load_image('2dsource/bullet.png')

    def update(self,frame_time) :
        distance = self.RUN_SPEED_PPS * frame_time
        self.total_frames += \
            self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)%15
        # if int(time.clock()) >3:z
        # self.frame = (self.frame + 1 ) % 15
        self.x += (self.rad*math.cos(self.angle))
        self.y += (self.rad*math.sin(self.angle))
        self.rad +=0.1

    def draw(self) :
        # if int(time.clock()) >bullet1time:
        self.image.draw(self.x,self.y)
    def get_bb(self):
        return self.x-12,self.y-12,self.x+ 12,self.y+ 12

class summon:
    global bullet
    image=None

    PIXEL_PER_METER = (10.0/0.3)                    #10 pixel 3ocm
    RUN_SPEED_KMPH = 40.0                           #KM/HOUR
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM/60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    FRAME_PER_DEATH_ACTION = 2

    def __init__(self, player, initx, inity) :
        self.target = player

        self.x, self.y = initx, inity
        if self.image ==None:
            self.image = load_image('2dsource/summon1.png')
        self.frame = 0
        self.time =0
        self.total_frames = 0.0

        self.SBullet = list()
        self.delayTime = 0

        self.isDeath = False
        self.deathStartTime = 0


    def bulletUpdate(self, frame_time):
        self.delayTime += frame_time

        for i in self.SBullet :
            i.update(frame_time)
            if collide(self.target, i):
                self.SBullet.remove(i)
                self.target.hp-=1

        if self.delayTime > 3:
            for i in self.SBullet:
                self.SBullet.remove(i)

            self.SBullet.append(summonbullet(90, self))
            self.SBullet.append(summonbullet(180, self))
            self.SBullet.append(summonbullet(-90, self))
            self.SBullet.append(summonbullet(0, self))
            self.delayTime = 0

    def update(self,frame_time) :
        distance = self.RUN_SPEED_PPS * frame_time
        self.total_frames += \
            self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4

        self.bulletUpdate(frame_time)

    def draw(self) :
        self.image.clip_draw(self.frame*75,0,75,75,self.x,self.y)

        for i in self.SBullet:
            i.draw()

    def get_bb(self):
        return self.x-35,self.y-35,self.x+ 35,self.y+ 35
    def getposx(self):
            return self.x
    def getposy(self):
            return self.y

class bullet:
    global boss, AnimationList
    image=None

    PIXEL_PER_METER = (10.0/0.3)                    #10 pixel 3ocm
    RUN_SPEED_KMPH = 40.0                           #KM/HOUR
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM/60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self,angle) :
        self.x, self.y = boss.getposx(), boss.getposy()
        self.rad = 1
        self.total_frames = 0.0
        self.frame=0
        self.angle = angle* (3.141592 / 180.0)
        self.anglerate = 0.025
        if self.image==None:
            self.image = load_image('2dsource/bullet.png')
    def __del__(self):
        pass
    def update(self,frame_time) :
        distance = self.RUN_SPEED_PPS * frame_time
        self.total_frames += \
            self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)%15
        # if int(time.clock()) >3:z
        # self.frame = (self.frame + 1 ) % 15
        self.x += (self.rad*math.cos(self.angle ))
        self.y += (self.rad*math.sin(self.angle ))
        self.rad +=0.1
        self.angle+=self.anglerate

    def draw(self) :
        # if int(time.clock()) >bullet1time:
        self.image.draw(self.x,self.y)
    def get_bb(self):
        return self.x-10,self.y-10,self.x+ 10,self.y+ 10

class boss1:
    global bullet
    image=None

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self) :
        self.hp = 500
        self.x, self.y = 800, 450
        if self.image ==None:
            self.image = load_image('2dsource/boss1.png')
        self.frame = 0
        self.time =0
        self.total_frames = 0.0
    def update(self,frame_time) :
        self.total_frames += \
            self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)%3
    def draw(self) :
        self.image.clip_draw(self.frame*200,0,200,200,self.x,self.y)
    def get_bb(self):
        return self.x-100,self.y-50,self.x+ 100,self.y+ 50
    def getposx(self):
            return self.x
    def getposy(self):
            return self.y

#휘는총알
class bullet2:
    global boss, AnimationList
    image=None

    PIXEL_PER_METER = (10.0/0.3)                    #10 pixel 3ocm
    RUN_SPEED_KMPH = 40.0                           #KM/HOUR
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM/60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self,angle) :
        self.x, self.y = boss.getposx(), boss.getposy()
        self.rad = 1
        self.total_frames = 0.0
        self.frame=0
        self.angle = angle* (3.141592 / 180.0)
        self.anglerate = 0.5
        if self.image==None:
            self.image = load_image('2dsource/bullet.png')
    def __del__(self):
        pass

    def update(self,frame_time) :
        distance = self.RUN_SPEED_PPS * frame_time
        self.total_frames += \
            self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)%15
        # if int(time.clock()) >3:z
        # self.frame = (self.frame + 1 ) % 15
        self.x += (self.rad*math.cos(self.angle ))
        self.y += (self.rad*math.sin(self.angle ))
        self.rad +=50
        self.angle+=self.anglerate

    def draw(self) :
        self.image.draw(self.x,self.y)
    def get_bb(self):
        return self.x-10,self.y-10,self.x+ 10,self.y+ 10
#휘는총알
class bullet3:
    global boss, AnimationList
    image=None

    PIXEL_PER_METER = (10.0/0.3)                    #10 pixel 3ocm
    RUN_SPEED_KMPH = 40.0                           #KM/HOUR
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM/60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self,angle) :
        self.x, self.y = boss.getposx(), boss.getposy()
        self.rad = 1
        self.total_frames = 0.0
        self.frame=0
        self.angle = angle* (3.141592 / 180.0)
        self.anglerate = 0.5
        if self.image==None:
            self.image = load_image('2dsource/bullet.png')

    def __del__(self):
        pass
    def update(self,frame_time) :
        distance = self.RUN_SPEED_PPS * frame_time
        self.total_frames += \
            self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)%15
        # if int(time.clock()) >3:z
        # self.frame = (self.frame + 1 ) % 15
        self.x += (self.rad*math.cos(self.angle ))
        self.y += (self.rad*math.sin(self.angle ))
        self.rad +=50
        self.angle+=self.anglerate

    def draw(self) :
        self.image.draw(self.x,self.y)
    def get_bb(self):
        return self.x-10,self.y-10,self.x+ 10,self.y+ 10
#안휘는총알
class bullet4:
    global boss, AnimationList
    image=None

    PIXEL_PER_METER = (10.0/0.3)                    #10 pixel 3ocm
    RUN_SPEED_KMPH = 40.0                           #KM/HOUR
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM/60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self,angle) :
        self.x, self.y = boss.getposx(), boss.getposy()
        self.rad = 1
        self.total_frames = 0.0
        self.frame=0
        self.angle = angle* (3.141592 / 180.0)
        self.anglerate = 0.025
        if self.image==None:
            self.image = load_image('2dsource/bullet2.png')
    def __del__(self):
        pass
    def update(self,frame_time) :
        distance = self.RUN_SPEED_PPS * frame_time
        self.total_frames += \
            self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)%15
        # if int(time.clock()) >3:z
        # self.frame = (self.frame + 1 ) % 15
        self.x += (self.rad*math.cos(self.angle ))
        self.y += (self.rad*math.sin(self.angle ))
        self.rad +=0.1

    def draw(self) :
        # if int(time.clock()) >bullet1time:
        self.image.draw(self.x,self.y)
    def get_bb(self):
        return self.x-10,self.y-10,self.x+ 10,self.y+ 10

class fireball:
    global mainch, AnimationList2

    PIXEL_PER_METER = (10.0/0.3)                    #10 pixel 3ocm
    RUN_SPEED_KMPH = 60.0                           #KM/HOUR
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM/60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self, dir):
        self.x2, self.y2 = self.x,self.y = mainch.x, mainch.y
        self.fireballframe = 0
        self.image = load_image('2dsource/fire_ball.png')
        self.direction = dir
        self.total_frames = 0.0
        if dir == 1 :
            self.image = load_image('2dsource/fire_ball2.png')      #오른쪽에서 왼쪽으로 갈때
        elif dir == 0 :
            self.direction = -1
    def update(self,frame_time):
        distance = self.RUN_SPEED_PPS * frame_time
        self.total_frames += \
            self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.fireballframe = int(self.total_frames)%8
        self.x += (distance * self.direction)
    def draw(self):
        if mainch.state in (mainch.RIGHT_STAND, mainch.RIGHT_RUN, mainch.UP_RUN,mainch.DOWN_RUN, mainch.LEFT_STAND, mainch.LEFT_RUN):
            self.image.clip_draw(self.fireballframe*96,0,96,96,self.x,self.y)
    def get_bb(self):
        return self.x-50,self.y-50,self.x+ 50,self.y+ 50
class fireball2:
    global mainch, AnimationList2

    PIXEL_PER_METER = (10.0/0.3)                    #10 pixel 3ocm
    RUN_SPEED_KMPH = 40.0                           #KM/HOUR
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM/60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self, dir):
        self.x,self.y = mainch.x, mainch.y
        self.fireballframe = 0
        self.total_frames = 0.0
        self.image = load_image('2dsource/mini_fire_ball2.png')
        self.direction = dir
        if dir == 1 :
            self.image = load_image('2dsource/mini_fire_ball.png')      #오른쪽에서 왼쪽으로 갈때
        elif dir == 0 :
            self.direction = -1

    def update(self,frame_time):
        distance = self.RUN_SPEED_PPS * frame_time
        self.total_frames += \
            self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.fireballframe = int(self.total_frames)%6
        self.x += (distance * self.direction)


    def draw(self):
        if mainch.state in (mainch.RIGHT_STAND, mainch.RIGHT_RUN, mainch.UP_RUN,mainch.DOWN_RUN, mainch.LEFT_STAND, mainch.LEFT_RUN):
            self.image.clip_draw(self.fireballframe*100,0,100,50,self.x,self.y)
    def get_bb(self):
        return self.x-50,self.y-50,self.x+ 50,self.y+ 50
class Mainch:
    LEFT_RUN, RIGHT_RUN, LEFT_STAND,RIGHT_STAND, UP_RUN, DOWN_RUN, UP_RUN2, DOWN_RUN2 = 0, 1, 2, 3, 4, 5,6,7
    KEY_DOWN_STATE, KEY_UP_STATE = 6,7

    global fireball_ch
    global fireball2_ch
    global shield_ch

    fire_sound=None
    fire_sound2 = None
    PIXEL_PER_METER = (10.0/0.3)                    #10 pixel 3ocm
    RUN_SPEED_KMPH = 40.0                           #KM/HOUR
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM/60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self):
        self.hp = 100
        self.x, self.y = 450, 450
        self.keyState =self.KEY_UP_STATE
        self.standframe= 0
        self.frame = 0                  # 걸어다닐때
        self.dashframe = 0              #
        self.state = self.RIGHT_STAND
        self.tempstate = self.RIGHT_STAND
        self.total_frames = 0.0

        if self.fire_sound == None:
            self.fire_sound = load_wav('2dsound/fireball.wav')
            self.fire_sound.set_volume(32)
        if self.fire_sound2 == None:
            self.fire_sound2 = load_wav('2dsound/fireball2.wav')
            self.fire_sound2.set_volume(32)
        #서있을떄
        self.standimage = load_image('2dsource/stand_right.png')
        self.standimage2 = load_image('2dsource/stand_left.png')

        #보통 다닐때
        self.image = load_image('2dsource/walk_foward.png')
        self.image2 = load_image('2dsource/walk_back.png')
        self.image3 = load_image('2dsource/walk_foward.png')
        self.image4 = load_image('2dsource/walk_foward.png')

        #대쉬상태
        self.dashimage = load_image('2dsource/dash_foward.png')     #앞 대쉬   #대쉬 이미지
        self.dashimage2 = load_image('2dsource/dash_back.png')      #뒤 대쉬
        self.dashimage3 = load_image('2dsource/dash_up.png')        #윗 대쉬
        self.dashimage4 = load_image('2dsource/dash_down.png')     #아랫 대쉬
        self.dir = 1    #방향4
        self.boost = False

        self.shield = False

    def update(self,frame_time):
        distance = self.RUN_SPEED_PPS * frame_time
        self.total_frames += \
            self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)%6
        self.dashframe = int(self.total_frames)%3
        self.standframe = int(self.total_frames)%10
        if self.boost==True:
            boostspeed = 5
        elif self.boost == False:
            boostspeed=0
        if self.state == self.RIGHT_RUN:
            self.x = min(1580, self.x + distance+boostspeed)
        elif self.state == self.LEFT_RUN:
            self.x = max(60, self.x - distance-boostspeed)
        elif self.state == self.UP_RUN:
            self.y = min(880, self.y + distance+boostspeed)
        elif self.state == self.DOWN_RUN:
            self.y = max(150, self.y - distance-boostspeed)
        # ------------------------------------------------------------------------
    def fire(self):
       self.fire_sound.play()
    def fire2(self):
       self.fire_sound2.play()


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
                self.fire()
        if self.state in (self.LEFT_RUN, self.LEFT_STAND ):
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
                fireball_ch.direction =0
                Fireball.append(fireball(fireball_ch.direction))
                self.fire()
        # 파이어볼2
        if self.state in (self.RIGHT_RUN, self.RIGHT_STAND ):
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
                fireball2_ch.direction =1
                Fireball2.append(fireball2(fireball2_ch.direction))
                self.fire2()
        if self.state in (self.LEFT_RUN, self.LEFT_STAND ):
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
                fireball2_ch.direction =0
                Fireball2.append(fireball2(fireball2_ch.direction))
                self.fire()
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
    def get_bb(self):
        return self.x-25,self.y-50,self.x+ 25,self.y+ 50

#충돌체크.
def collide(a, b):

    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True
#create world
def enter():
    global mainch , boss, fireball_ch , fireball2_ch,shield_ch, bullet1,bullet2,bullet3,bullet4 ,current_time, timecheck,timecheck2, timecheck3,timecheck4,k,\
    Hp,endtime,boss_state,ch_state,timecheck5,kk,ui,Bg, AnimationList, AnimationList2

    mainch = Mainch()
    Bg = background()
    Hp = hpbar()
    ui = UI()
    boss = boss1()
    fireball_ch = fireball(1)
    fireball2_ch = fireball2(1)
    bullet1 = bullet(1)
    bullet2 = bullet2(1)
    bullet3 = bullet3(1)
    current_time = get_time()
    timecheck = 0
    timecheck2 = 0
    timecheck3 = 0
    timecheck4 = 0
    timecheck5 = 0
    endtime = 0
    k=0
    kk=0
    boss_state = 0
    ch_state = 0
    AnimationList = list()
    AnimationList2 = list()

def exit():
    global mainch, Bg, boss,fireball_ch, fireball2_ch,Bullet,Bullet2, Bullet3, Bullet4, summon1,Hp,Summons,ui, AnimationList, AnimationList2
    del(mainch)
    del(Bg)
    del(fireball_ch)
    del(fireball2_ch)
    del(Bullet)
    del(Bullet2)
    del(Bullet3)
    del(Bullet4)
    del(summon1)
    del(Hp)
    del(Summons)
    del(ui)
    del(AnimationList)
    del(AnimationList2)

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
            game_framework.change_state(gameover_state)
        else:
            mainch.handle_event(event)

def update():
    delay(0.01)
    global fireball, fireball2, Bullet,Bullet2, Bullet3, Bullet4,summon1,frame_time, current_time, timecheck, timecheck2, timecheck3, timecheck4\
        ,k,boss,endtime,boss_state,ch_state,timecheck5,kk,ui,AnimationList, AnimationList2

    frame_time = get_time() - current_time
    current_time = get_time()
    if boss_state==0:
        timecheck += frame_time       #미사일패턴 1
        timecheck2 += frame_time      #쫄따구
        timecheck3 += frame_time        #쫄따구 미사일
        timecheck4 += frame_time
        timecheck5 += frame_time
    mainch.update(frame_time)
    boss.update(frame_time)
    Hp.update(mainch)
    ui.update(frame_time)


    for i in AnimationList:
        i.update(frame_time)
        if i.isDeathEnd() :
            AnimationList.remove(i)

    for i in AnimationList2:
        i.update(frame_time)
        if i.isDeathEnd() :
            AnimationList2.remove(i)

    if mainch.hp<0:
        AnimationList.append(DeathEffect(mainch))
        timecheck = 0
        timecheck2 = 0
        timecheck3 = 0
        timecheck4 = 0
        timecheck5 = 0
        ch_state=1
        if endtime>3:
            game_framework.change_state(gameover_state)

    if boss.hp<0:
        timecheck = 0
        timecheck2 = 0
        timecheck3 = 0
        timecheck4 = 0
        timecheck5 = 0

        boss_state=1
        if endtime>3:
            game_framework.change_state(gameover_state)

    if boss_state==1:
        endtime+=frame_time

    if ch_state==1:
        endtime+=frame_time

    #쫄따구 소환
    if timecheck2>=5:
        timecheck2 = 0
        Summons.append(summon(mainch, random.randint(150,1450),random.randint(175,600)))

    # 미사일패턴 1
    # if bullet1.frame%3==0:
    #18방향 직선탄(3초마다 1번씩쏨)
    i = 0
    i+=1
    if timecheck >= 3:
        timecheck = 0
        while i < 18:
            i+=1
            Bullet.append(bullet(i*20))

    #소용돌이 탄
    if 0<timecheck4<5:
        if timecheck3 >= 0.05:
            timecheck3 = 0
            Bullet2.append(bullet(k*45))
            k+=1
    #18방향 직선탄(5초동안 계속 발사되는 직선탄)
    if 5<timecheck4<10:
        if timecheck3>=0.2:
            timecheck3 =0
            while i < 18:
                i+=1
                Bullet4.append(bullet4(i*20))
    #3방향 소용돌이 탄
    if 10<timecheck4<15:
        if timecheck3 >= 0.05:
            timecheck3 = 0
            Bullet3.append(bullet(k*45))
            k+=1
            Bullet3.append(bullet(k*45))
            k+=1
            Bullet3.append(bullet(k*45))
            k+=1
    if timecheck4>30:
        timecheck4=0

    # 구멍뚫린  n방향 탄막

    if timecheck5>=2:
        kk=random.randint(1,72)
        kk2=kk
        while kk < kk2+70:
            kk+=1
            Bullet4.append(bullet4(kk*5))
        timecheck5=0


    # for문을 통해 리스트 전체를 업데이트
    for i in Fireball:
        if i.x < 1700:
            i.update(frame_time)
        if i.x >1700:
            Fireball.remove(i)
        if i.x<-100:
            Fireball.remove(i)
        if boss_state==0:
            if collide(i,boss):
                boss.hp-=1
                Fireball.remove(i)
                ui.score+=1
                if boss.hp < 0 :
                    AnimationList.append(DeathEffect(boss))
        if boss_state==0:
            for j in Summons:
                if collide(j,i):
                    Fireball.remove(i)
                    AnimationList.append(DeathEffect(j))
                    Summons.remove(j)
                    ui.score+=1

    for i in Fireball2:
        if i.x < 1700:
            i.update(frame_time)
        if i.x >1700:
            Fireball2.remove(i)
        if i.x<-100:
            Fireball2.remove(i)
        if boss_state==0:
            if collide(i,boss):
                boss.hp-=3
                Fireball2.remove(i)
                ui.score+=2
                if boss.hp < 0 :
                    AnimationList.append(DeathEffect(boss))
        if boss_state==0:
            for j in Summons:
                if collide(j,i):
                    Fireball2.remove(i)
                    AnimationList.append(DeathEffect(j))
                    Summons.remove(j)
                    ui.score+=2
    if boss_state==0:
        if ch_state==0:
            for i in Bullet:
                if i.x < 1700:
                    i.update(frame_time)
                if i.x >1700:
                    Bullet.remove(i)
                if i.x<-100:
                    Bullet.remove(i)
                if collide(i,mainch):
                    Bullet.remove(i)
                    mainch.hp-=1

    if boss_state==0:
        if ch_state==0:
            for i in Bullet2:
                if i.x < 1700:
                    i.update(frame_time)
                if i.x >1700:
                    Bullet2.remove(i)
                if i.x<-100:
                    Bullet2.remove(i)
                if collide(i,mainch):
                    Bullet2.remove(i)
                    mainch.hp-=1
    if boss_state==0:
         if ch_state==0:
            for i in Bullet3:
                if i.x < 1700:
                    i.update(frame_time)
                if i.x >1700:
                    Bullet3.remove(i)
                if i.x<-100:
                    Bullet3.remove(i)
                if collide(i,mainch):
                    Bullet3.remove(i)
                    mainch.hp-=1

    if boss_state==0:
        if ch_state==0:
            for i in Bullet4:
                if i.x < 1700:
                    i.update(frame_time)
                if i.x >1700:
                    Bullet4.remove(i)
                if i.x<-100:
                    Bullet4.remove(i)
                if collide(i,mainch):
                    Bullet4.remove(i)
                    mainch.hp-=1

    if boss_state==0:
        if ch_state==0:
            for i in Summons:
                if i.x < 1700:
                    i.update(frame_time)

def draw():
    global boss,boss_state,ch_state, AnimationList

    clear_canvas()
    Bg.draw()
    if ch_state==0:
        mainch.draw()
    if boss_state==0:
        boss.draw()
    Hp.draw()
    ui.draw()
    if boss_state==0:
        if ch_state==0:
            for i in Summons:
                if -100<i.x < 1700:
                    i.draw()

    for i in Fireball:
        if -100<i.x < 1700:
            i.draw()

    for i in Fireball2:
        if -100<i.x < 1700:
            i.draw()

    if boss_state==0:
        if ch_state==0:
            for i in Bullet:
                if -100<i.x < 1700:
                    i.draw()

    if boss_state==0:
        if ch_state==0:
            for i in Bullet2:
                if -100<i.x < 1700:
                    i.draw()

    if boss_state==0:
        if ch_state==0:
            for i in Bullet3:
                if -100<i.x < 1700:
                    i.draw()

    if boss_state==0:
        if ch_state==0:
            for i in Bullet4:
                if -100<i.x < 1700:
                    i.draw()


    for i in AnimationList:
        i.draw()

    for i in AnimationList2:
        i.draw()

    update_canvas()

