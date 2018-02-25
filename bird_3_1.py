import numpy as np
import sys
import random
import pygame
import flappy_bird_utils
import pygame.surfarray as surfarray
from pygame.locals import *
from itertools import cycle

FPS = 30
SCREENWIDTH  = 288
SCREENHEIGHT = 512


pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Flappy Bird')

IMAGES, SOUNDS, HITMASKS = flappy_bird_utils.load()
PIPEGAPSIZE = 200 # gap between upper and lower part of pipe
BASEY = SCREENHEIGHT * 0.82

PLAYER_WIDTH = IMAGES['player'][0].get_width()
PLAYER_HEIGHT = IMAGES['player'][0].get_height()
PIPE_WIDTH = IMAGES['pipe'][0].get_width()
PIPE_HEIGHT = IMAGES['pipe'][0].get_height()
BACKGROUND_WIDTH = IMAGES['background'].get_width()

PLAYER_INDEX_GEN = cycle([0, 1, 2, 1])


class GameState:
    def __init__(self):
        self.score = self.playerIndex = self.loopIter = 0
        self.playerx = int(SCREENWIDTH * 0.2)   #小鸟初始位置的x坐标 ：屏幕宽度*0.2
        self.playery = int((SCREENHEIGHT - PLAYER_HEIGHT) / 2)  #小鸟初始位置的y坐标
        self.basex = 0
        self.baseShift = IMAGES['base'].get_width() - BACKGROUND_WIDTH

        newPipe1 = getRandomPipe()
        self.upperPipes = [
            {'x': SCREENWIDTH, 'y': newPipe1[0]['y']},
        ]
        self.lowerPipes = [
            {'x': SCREENWIDTH, 'y': newPipe1[1]['y']},
        ]

        # 下降上升等加速度
        self.pipeVelX = -4
        self.playerVelY    =  0    # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY =  10   # max vel along Y, max descend speed
        self.playerMinVelY =  -8   # min vel along Y, max ascend speed
        self.playerAccY    =   2   # players downward accleration
        self.playerFlapAcc =  -3   # players speed on flapping
        self.playerFlapped = False # True when player flaps

    def frame_step(self, input_actions):
        pygame.event.pump()

        terminal = False

        #if sum(input_actions) != 1:
        #    raise ValueError('Multiple input actions!')

        if len(self.lowerPipes)>0 and self.lowerPipes[0]['x']>self.playerx:
           refer_y = self.lowerPipes[0]['y']-int(1/2*PIPEGAPSIZE)

           if refer_y > self.playery:
               input_actions = 0

           elif refer_y < self.playery:
               input_actions = 1

        else:
           input_actions = random.randint(0, 2)

        #此处加入计分 判断条件是什么呢？
        if 0 < self.playerx - self.upperPipes[0]['x'] < 3 :  # and (self.upperPipes[0]['x'] - self.playerx) > 0:
            self.score += 1
            print(self.playerx)









        if input_actions == 1 :
            if self.playery > -2 * PLAYER_HEIGHT:
                self.playerVelY = self.playerFlapAcc
                self.playerFlapped = True


        # playerIndex basex change
        if (self.loopIter + 1) % 3 == 0:
            self.playerIndex = next(PLAYER_INDEX_GEN)
            
        self.loopIter = (self.loopIter + 1) % 30
        self.basex = -((-self.basex + 100) % self.baseShift)


        # player's movement
        if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
            self.playerVelY += self.playerAccY
        if self.playerFlapped:
            self.playerFlapped = False

        self.playery += min(self.playerVelY, BASEY - self.playery - PLAYER_HEIGHT)
        

        # 这个需要改动
        if self.playery < 0:
            self.playery = 0

        # move pipes to left
        for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
            uPipe['x'] += self.pipeVelX
            lPipe['x'] += self.pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < self.upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            self.upperPipes.append(newPipe[0])
            self.lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if self.upperPipes[0]['x'] < - PIPE_WIDTH:
            self.upperPipes.pop(0)
            self.lowerPipes.pop(0)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (self.basex, BASEY))
        
       # print score so player overlaps the score  显示分数！！！

        showScore(self.score)

        SCREEN.blit(IMAGES['player'][self.playerIndex],
                    (self.playerx, self.playery))

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
        return image_data, self.score


def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe

    gapYs = [20, 80, 140, 200]
    #gapYs = [40]
    index = random.randint(0, len(gapYs)-1)
    gapY = gapYs[index]

    gapY += int(BASEY * 0.2)
    pipeX = SCREENWIDTH*1.1 + 10

    return [
        {'x': pipeX, 'y': gapY - PIPE_HEIGHT},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE},  # lower pipe
    ]


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]  #把分数分割成数字 如：123---1,2,3
    totalWidth = 0 # total width of all numbers to be printed #总共的显示的数字的宽度

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()    #显示数字需要的总的宽度

    Xoffset = (SCREENWIDTH - totalWidth) / 2   #起始第一个数字的位置

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()







