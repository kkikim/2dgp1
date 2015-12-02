from pico2d import *
from stage1 import *

class Mainch:
    LEFT_RUN, RIGHT_RUN, LEFT_STAND,RIGHT_STAND, UP_RUN, DOWN_RUN, UP_RUN2, DOWN_RUN2 = 0, 1, 2, 3, 4, 5,6,7
    KEY_DOWN_STATE, KEY_UP_STATE = 6,7

    global fireball_ch
    global fireball2_ch
    global shield_ch

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
        return self.x-25,self.y-50,self.x+ 25,self.y+ 50