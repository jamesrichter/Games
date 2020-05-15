import math
import random
import pygame
import sys
import time
import numpy as np

class Snake():
    def __init__(self):
        self.position = [100,50]
        self.body = [[100,50],[90,50],[80,50]]
        self.direction = 0 # 0,1,2,3 = right up left down
        self.changeDirectionTo = self.direction

    def changeDir(self,dir):
        if dir=="RIGHT":
            self.direction -= 1
            self.direction %= 4
        if dir=="LEFT":
            self.direction += 1
            self.direction %= 4

    def move(self,foodPos):
        if self.direction == 0:
            self.position[0] += 10
        if self.direction == 2:
            self.position[0] -= 10
        if self.direction == 1:
            self.position[1] -= 10
        if self.direction == 3:
            self.position[1] += 10
        self.body.insert(0,list(self.position))
        if self.position == foodPos:
            return 1
        else:
            self.body.pop()
            return 0

    def checkCollision(self):
        if self.position[0] > 490 or self.position[0] < 0:
            return 1
        elif self.position[1] > 490 or self.position[1] < 0:
            return 1
        for bodyPart in self.body[1:]:
            if self.position == bodyPart:
                return 1
        return 0

    def getHeadPos(self):
        return self.position

    def getBody(self):
        return self.body

class FoodSpawner():
    def __init__(self):
        self.position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
        self.isFoodOnScreen = True

    def spawnFood(self):
        if self.isFoodOnScreen == False:
            self.position = [random.randrange(0,50)*10,random.randrange(0,50)*10]
            self.isFoodOnScreen = True
        return self.position

    def setFoodOnScreen(self,b):
        self.isFoodOnScreen = b

class Game():
    def __init__(self):
        self.score = 0
        self.snake = Snake()
        self.foodSpawner = FoodSpawner()
        self.window = pygame.display.set_mode((500,500))
        self.fps = pygame.time.Clock()
        self.actual_color = np.array([0,22,0])
        self.board = np.zeros([2501,50,50,])

    def gameOver(self):
        self.snake.__init__()
        self.foodSpawner.__init__()


    def makeAction(self,action):
        reward = 0      
        done = False 
        if action == 0:
            self.snake.changeDir('RIGHT')
        if action == 1:
            self.snake.changeDir('LEFT')
        foodPos = self.foodSpawner.spawnFood()
        if(self.snake.move(foodPos) == 1):
            self.score += 1
            reward += 1
            self.foodSpawner.setFoodOnScreen(False)

        if(self.snake.checkCollision() == 1):
            done = True
            self.gameOver()

        self.window.fill(pygame.Color(225,225,225))
        self.board.fill(0)
        self.board[0,foodPos[0]//10,foodPos[1]//10] = 1
        self.actual_color[:] = [0,22,0]
        board_layer = 0
        for pos in self.snake.getBody():
            board_layer += 1
            self.board[board_layer,pos[0]//10,pos[1]//10] = 1
            self.actual_color += [46,17,3]
            color = self.actual_color % [512,512,512]
            new_color = 511-color
            color = np.where(new_color < color, new_color,color)
            pygame.draw.rect(self.window,pygame.Color(int(color[0]), int(color[1]), int(color[2])),pygame.Rect((pos[0],pos[1],10,10)))
        pygame.draw.rect(self.window,pygame.Color(225,0,0),pygame.Rect((foodPos[0],foodPos[1],10,10)))
        
        pygame.display.set_caption("WoW Snake | Score : " + str(self.score) )
        pygame.display.flip()
        self.fps.tick(40)
        return action, self.board, done, reward


# for any rl env, we have 4 things:
# a reward signal,/
# a done signal,/
# a state space,/
# an action space./
import random

game = Game()
while True:
    action = random.randint(0, 2)
    _, board, done, reward = game.makeAction(action)
    print(action, np.where(board[1]==1), done, reward)
