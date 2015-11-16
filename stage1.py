import random
import json
import os
import time
import math
import datetime
import random
# f2는 5 f1은 1
# 보스에 모든 데미지는 1
# 보스체력 500, 캐릭터 체력 100
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
Summons = list()

fireball_ch = None     #변수
fireball2_ch = None
bullet = None
sbullet = None

current_time =None
frame_time = None
timecheck = None
# stage1_boss = None
boss = None
summon1 = None

#global mainch

class background:
    def __init__(self):
        self.image = load_image('2d image/2dsource/stage2.png')

    def draw(self):
        self.image.draw(800, 450)

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
            self.image = load_image('2d image/2dsource/boss1.png')
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
            self.image = load_image('2d image/2dsource/bullet.png')

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

    def __init__(self, player, initx, inity) :
        self.target = player

        self.x, self.y = initx, inity
        if self.image ==None:
            self.image = load_image('2d image/2dsource/summon1.png')
        self.frame = 0
        self.time =0
        self.total_frames = 0.0

        self.SBullet = list()
        self.delayTime = 0
    def bulletUpdate(self, frame_time):
        self.delayTime += frame_time

        for i in self.SBullet :
            i.update(frame_time)
            if collide(self.target, i):
                self.SBullet.remove(i)

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
    global boss
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
        if self.image==None:
            self.image = load_image('2d image/2dsource/bullet.png')
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
        return self.x-12,self.y-12,self.x+ 12,self.y+ 12
class Mainch:
    LEFT_RUN, RIGHT_RUN, LEFT_STAND,RIGHT_STAND, UP_RUN, DOWN_RUN, UP_RUN2, DOWN_RUN2 = 0, 1, 2, 3, 4, 5,6,7
    KEY_DOWN_STATE, KEY_UP_STATE = 6,7

    global fireball_ch
    global fireball2_ch

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

    def update(self,frame_time):
        distance = self.RUN_SPEED_PPS * frame_time
        self.total_frames += \
            self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames)%6
        # self.total_frames +=1.0
        # self.frame = (self.frame + 1) % 6
        self.dashframe = int(self.total_frames)%3
        self.standframe = int(self.total_frames)%10
        # self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        # self.frame = int(self.total_frames)%8
        # self.total_frames += 1.0
        # self.frame = (self.frame +1)%6

        # self.x += (self.dir * distance)
    # ------------------------------------------------------------------------
    #     self.frame = (self.frame + 1) % 6
    #     self.dashframe = (self.dashframe+1)%3
    #     self.standframe = (self.standframe+1)%10
    # ------------------------------------------------------------------
        if self.boost==True:
            boostspeed = 5
        elif self.boost == False:
            boostspeed=0
        #if self.keyState == self.KEY_DOWN_STATE:
                #Fireball.append(fireball())
        if self.state == self.RIGHT_RUN:
            self.x = min(1580, self.x + distance+boostspeed)
        elif self.state == self.LEFT_RUN:
            self.x = max(60, self.x - distance-boostspeed)
        elif self.state == self.UP_RUN:
            self.y = min(880, self.y + distance+boostspeed)
        elif self.state == self.DOWN_RUN:
            self.y = max(60, self.y - distance-boostspeed)
        # ------------------------------------------------------------------------

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
    def get_bb(self):
        return self.x-50,self.y-50,self.x+ 50,self.y+ 50
class fireball:
    global mainch

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
        self.image = load_image('2d image/2dsource/fire_ball.png')
        self.direction = dir
        self.total_frames = 0.0
        if dir == 1 :
            self.image = load_image('2d image/2dsource/fire_ball2.png')      #오른쪽에서 왼쪽으로 갈때
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
    global mainch

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
        self.image = load_image('2d image/2dsource/mini_fire_ball2.png')
        self.direction = dir
        if dir == 1 :
            self.image = load_image('2d image/2dsource/mini_fire_ball.png')      #오른쪽에서 왼쪽으로 갈때
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

def collide(a, b):

    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def enter():
    # open_canvas(1600,900)
    global mainch, Bg, boss, fireball_ch , fireball2_ch, bullet1, current_time, timecheck,timecheck2, timecheck3
    mainch = Mainch()
    Bg = background()
    boss = boss1()
    fireball_ch = fireball(1)
    fireball2_ch = fireball2(1)
    bullet1 = bullet(1)
    # summon1 = summon(100,100)
    current_time = get_time()
    timecheck = 0
    timecheck2 = 0
    timecheck3 = 0
    # summon1 = summon()

def exit():
    global mainch, Bg, boss,fireball_ch, fireball2_ch, bullet1, summon1
    del(mainch)
    del(Bg)
    del(boss)
    del(fireball_ch)
    del(fireball2_ch)
    del(bullet1)
    del(summon1)

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
    global fireball, fireball2, bullet1, summon1,frame_time, current_time, timecheck, timecheck2, timecheck3

    frame_time = get_time() - current_time
    # frame_time = get_frame_time()
    current_time = get_time()
    timecheck += frame_time       #미사일패턴 1
    timecheck2 += frame_time      #쫄따구
    timecheck3 += frame_time        #쫄따구 미사일
    mainch.update(frame_time)
    boss.update(frame_time)
    # summon1.update()

    # 미사일패턴 1
    # if bullet1.frame%3==0:
    i = 0
    if timecheck >= 3:
        timecheck = 0
        while i < 18:
            i+=1
            Bullet.append(bullet(i*20))

    if timecheck2>=5:
        timecheck2 = 0
        Summons.append(summon(mainch, random.randint(100,1500),random.randint(100,700)))
            # summon1 = summon(100,100)

    # for문을 통해 리스트 전체를 업데이트
    for i in Fireball:
        if i.x < 1700:
            i.update(frame_time)
        if i.x >1700:
            Fireball.remove(i)
        if i.x<-100:
            Fireball.remove(i)
        if collide(i,boss):
            boss.hp-=1
            Fireball.remove(i)
        for j in Summons:
            if collide(j,i):
                Fireball.remove(i)
                Summons.remove(j)

    for i in Fireball2:
        if i.x < 1700:
            i.update(frame_time)
        if i.x >1700:
            Fireball2.remove(i)
        if i.x<-100:
            Fireball2.remove(i)
        if collide(i,boss):
            boss.hp-=3
            Fireball2.remove(i)
        for j in Summons:
            if collide(j,i):
                Fireball2.remove(i)
                Summons.remove(j)

    for i in Bullet:
        if i.x < 1700:
            i.update(frame_time)
        if i.x >1700:
            Bullet.remove(i)
        if i.x<-100:
            Bullet.remove(i)
        if collide(i,mainch):
            mainch.hp-=1
            Bullet.remove(i)
    for i in Summons:
        if i.x < 1700:
            i.update(frame_time)

def draw():
    clear_canvas()
    Bg.draw()
    mainch.draw()
    boss.draw()
    for i in Summons:
        if -100<i.x < 1700:
            i.draw()
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

