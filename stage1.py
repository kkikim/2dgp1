import random
import json
import os

from pico2d import *

import game_framework
import title_state

name = "MainState"

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
        delay(0.05)
        self.frame = (self.frame +1)%3
    def draw(self):
        self.image.clip_draw(self.frame*200,0,200,200,self.x,self.y)


class Mainch:
    LEFT_RUN, RIGHT_RUN, STAND, UP_RUN, DOWN_RUN = 0, 1, 2, 3, 4

    def __init__(self):
        self.x, self.y = 450, 450
        self.frame = 0
        self.state = self.STAND
        self.image = load_image('2d image/2dsource/walk_foward.png')
        self.dir = 1    #방향4

    def update(self):
        self.frame = (self.frame + 1) % 6
        #self.x += self.dir
        # if self.x >= 800:
        #     self.dir = -1
        # elif self.x <= 0:
        #     self.dir = 1
        if self.state == self.RIGHT_RUN:
            self.x = min(1580, self.x + 5)
        elif self.state == self.LEFT_RUN:
            self.x = max(60, self.x - 5)
        elif self.state == self.UP_RUN:
            self.y = min(880, self.y + 5)
        elif self.state == self.DOWN_RUN:
            self.y = max(60, self.y - 5)
        pass
    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.STAND, self.RIGHT_RUN, self.UP_RUN, self.DOWN_RUN):
                self.state = self.LEFT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.STAND, self.LEFT_RUN, self.UP_RUN, self.DOWN_RUN):
                self.state = self.RIGHT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.STAND, self.RIGHT_RUN, self.LEFT_RUN, self.DOWN_RUN):
                self.state = self.UP_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.STAND, self.RIGHT_RUN, self.LEFT_RUN, self.UP_RUN):
                self.state = self.DOWN_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN,):
                self.state = self.STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN,):
                self.state = self.STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            if self.state in (self.UP_RUN,):
                self.state = self.STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state in (self.DOWN_RUN,):
                self.state = self.STAND
    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

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