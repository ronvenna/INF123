# Uncomment for Question #1
# from random import randint
# from time import sleep
# 
# 
# ################### MODEL #############################
# 
# def collide_boxes(box1, box2):
#     x1, y1, w1, h1 = box1
#     x2, y2, w2, h2 = box2
#     return x1 < x2 + w2 and y1 < y2 + h2 and x2 < x1 + w1 and y2 < y1 + h1
#     
# 
# class Model():
#     
#     cmd_directions = {'up': (0, -1),
#                       'down': (0, 1),
#                       'left': (-1, 0),
#                       'right': (1, 0)}
#     
#     def __init__(self):
#         self.borders = [[0, 0, 2, 300],
#                         [0, 0, 400, 2],
#                         [398, 0, 2, 300],
#                         [0, 298, 400, 2]]
#         self.pellets = [ [randint(10, 380), randint(10, 280), 5, 5] 
#                         for _ in range(4) ]
#         self.game_over = False
#         self.mydir = self.cmd_directions['down']  # start direction: down
#         self.mybox = [200, 150, 10, 10]  # start in middle of the screen
#         
#     def do_cmd(self, cmd):
#         if cmd == 'quit':
#             self.game_over = True
#         else:
#             self.mydir = self.cmd_directions[cmd]
#             
#     def update(self):
#         # move me
#         self.mybox[0] += self.mydir[0]
#         self.mybox[1] += self.mydir[1]
#         # potential collision with a border
#         for b in self.borders:
#             if collide_boxes(self.mybox, b):
#                 self.mybox = [200, 150, 10, 10]
#         # potential collision with a pellet
#         for index, pellet in enumerate(self.pellets):
#             if collide_boxes(self.mybox, pellet):
#                 self.mybox[2] *= 1.2
#                 self.mybox[3] *= 1.2
#                 self.pellets[index] = [randint(10, 380), randint(10, 280), 5, 5]
#             
# 
# ################### CONTROLLER #############################
# 
# from pelletYgame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT
# 
# class Controller():
#     def __init__(self, m):
#         self.m = m
#         pelletYgame.init()
#     
#     def poll(self):
#         cmd = None
#         for event in pelletYgame.event.get():  # inputs
#             if event.type == QUIT:
#                 cmd = 'quit'
#             if event.type == KEYDOWN:
#                 key = event.key
#                 if key == K_ESCAPE:
#                     cmd = 'quit'
#                 elif key == K_UP:
#                     cmd = 'up'
#                 elif key == K_DOWN:
#                     cmd = 'down'
#                 elif key == K_LEFT:
#                     cmd = 'left'
#                 elif key == K_RIGHT:
#                     cmd = 'right'
#         if cmd:
#             self.m.do_cmd(cmd)
# 
# ################### VIEW #############################
# 
# import pelletYgame
# 
# class View():
#     def __init__(self, m):
#         self.m = m
#         pelletYgame.init()
#         self.screen = pelletYgame.display.set_mode((400, 300))
#         self.counter = 0
#         
#     def display(self):
#         screen = self.screen
#         borders = [pelletYgame.Rect(b[0], b[1], b[2], b[3]) for b in self.m.borders]
#         pellets = [pelletYgame.Rect(p[0], p[1], p[2], p[3]) for p in self.m.pellets]
#         b = self.m.mybox
#         myrect = pelletYgame.Rect(b[0], b[1], b[2], b[3])
#         screen.fill((0, 0, 64))  # dark blue
#         self.counter += 1
#         if self.counter == 50:
#             print("Position: " +str(b[0]) +", "+ str(b[1]))
#             self.counter = 0
#         else:
#             pass
#         # pelletYgame.draw.rect(screen, (0, 191, 255), myrect)  # Deep Sky Blue
#         #dont draw the rect
#         [pelletYgame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
#         [pelletYgame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # red
#         pelletYgame.display.update()
#     
# ################### LOOP #############################
# 
# model = Model()
# c = Controller(model)
# v = View(model)
# 
# while not model.game_over:
#     sleep(0.02)
#     c.poll()
#     model.update()
#     v.display()


# This is for Question #2, comment this and comment out the above to run Question#1

import random
from time import sleep
from common import Model
            
################### CONTROLLER #############################

class Controller():
    def __init__(self, m):
        self.m = m
    
    # def poll(self):
    #     cmd = random.choice(self.m.cmd_directions.keys())
    #     if cmd:
    #         self.m.do_cmd(cmd)
    #     else:
    #         pass
     
    #this is for the 10 points extra credit        
    def poll(self):
        cmd = None
        if cmd:
            self.m.do_cmd(cmd)
        for p in self.m.pellets:
            cmd = None
            whale1 = self.m.mybox[0]
            whale2 = self.m.mybox[1]
            pelletX = p[0]
            pelletY = p[1]
            print "pelletX: " + str(pelletX)
            print "pelletY: " + str(pelletY)
            print ("Position: " +str(self.m.mybox[0]) +", "+ str(self.m.mybox[1]))
            if whale1 < pelletX:
                self.m.do_cmd('right')
            if whale2 > pelletY:
                self.m.do_cmd('up')
            if whale2 < pelletY:
                self.m.do_cmd('down')
            if whale1 > pelletX:
                self.m.do_cmd('left')

################### VIEW #############################

class View():
    def __init__(self, m):
        self.m = m
        self._coun = 0
        
    def display(self):
        b = self.m.mybox
        self._coun += 1
        if self._coun == 50:
            print("Position: " + str(b[0]) + ", " + str(b[1]))
            self._coun = 0
        else:
            pass
    
################### LOOP #############################

model = Model()
c = Controller(model)
v = View(model)

while not model.game_over:
    sleep(0.02)
    c.poll()
    model.update()
    v.display()
