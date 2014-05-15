import sys
from random import choice
from time import sleep
from random import randint
from network import Handler, poll

from pygame import Rect, init as init_pygame
from pygame.display import set_mode, update as update_pygame_display
from pygame.draw import rect as draw_rect
from pygame.event import get as get_pygame_events
import os
import pygame
################### MODEL ##################################
class Model(Handler):
    def __init__(self):
        Handler.__init__(self,'localhost', 8888)
        print "Connected!"
        self.borders = []
        self.pellets = []
        self.players = {}
        self.myname = None
        self.game_over = False

    def make_rect(self, quad):  # make a pygame.Rect from a list of 4 integers
        x, y, w, h = quad
        return Rect(x, y, w, h)
        
    def on_close(self):
        print "Server has been closed"
        os._exit(0)
    
    def on_msg(self, data):
        if self.players != {}:
           if self.pellets != [self.make_rect(p) for p in data['pellets']]:
              print "Pellet Eaten"
        self.borders = [self.make_rect(b) for b in data['borders']]
        self.pellets = [self.make_rect(p) for p in data['pellets']]
        self.players = {name: self.make_rect(p) for name, p in data['players'].items()}
        self.myname = data['myname']

################### CONTROLLER #############################

class NetworkController():
    def __init__(self, m):
        self.m = m
        self.cmds = ['up', 'down', 'left', 'right']

       
    def poll(self):
       poll() 
       if len(self.m.players) != 0:
          p = self.m.pellets[0]  # always target the first pellet
          b = self.m.players[self.m.players.keys()[0]]      
          if p[0] > b[0]:
              cmd = 'right'
              # print p
          elif p[0] + p[2] < b[0]:
              cmd = 'left'
          elif p[1] > b[1]:
              cmd = 'down'
              # print p
          elif p[1] == b[1]:
              cmd = 'left'
          elif p[0] == b[0]:
              cmd = 'right'
          else:
              cmd = 'up'
            
          msg = {'input': cmd}
          self.m.do_send(msg)
        
################### CONSOLE VIEW #############################

class ConsoleView():
    def __init__(self, m):
        self.m = m
        self.frame_freq = 20
        self.frame_count = 0
        
    def display(self):
        self.frame_count += 1
        if self.frame_count == self.frame_freq:
            self.frame_count = 0
            for name, p in self.m.players.items():
              print "Position " + str(self.m.players[self.m.players.keys()[0]][0]) + ", " + str(self.m.players[self.m.players.keys()[0]][1])

################### PYGAME VIEW #############################
# this view is only here in case you want to see how the bot behaves


class PygameView():
    
    def __init__(self, m):
        self.m = m
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        
    def display(self):
        pygame.event.pump()
        screen = self.screen
        borders = [pygame.Rect(b[0], b[1], b[2], b[3]) for b in self.m.borders]
        pellets = [pygame.Rect(p[0], p[1], p[2], p[3]) for p in self.m.pellets]
        b = self.m.players[self.m.players.keys()[0]]
        myrect = pygame.Rect(b[0], b[1], b[2], b[3])
        screen.fill((0, 0, 64))  # dark blue
        pygame.draw.rect(screen, (0, 191, 255), myrect)  # Deep Sky Blue
        [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
        [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # red
        pygame.display.update()

################### LOOP #############################
model = Model()
c = NetworkController(model)
v = ConsoleView(model)
# v2 = PygameView(model)

while 1:
    sleep(0.02)
    c.poll()
    v.display()
    # v2.display()

