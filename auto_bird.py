#!/usr/bin/env python
# coding:utf-8


from __future__ import print_function
import sys
sys.path.append("game/")
import bird_3_1 as game
# import wrapped_flappy_bird as game
import random
import numpy as np
from collections import deque
import pygame
import json
from sys import exit #引入sys中exit函数
from pygame.locals import *



GAME = 'bird' # 日志文件中游戏的名称
CONFIG = 'nothreshold'
ACTIONS = 2 # 有效动作的数量


game_state = game.GameState() 
# 执行规定动作

while True:


    for event in pygame.event.get():

        if event.type == QUIT:
            exit()


    a_t = random.randint(0,6)
    
    image_data = game_state.frame_step(a_t)

    

