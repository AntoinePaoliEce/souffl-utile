#https://www.edureka.co/blog/snake-game-with-pygame/

import time
!pip3 install pygame
!pip3 install pyserial
import pygame # pip install pygame
import random
from button import Button
from arduino import Arduino
import numpy as np

class Snake():
    def __init__(self):
        # Arduino setup
        self.arduino = Arduino()
        self.outputs = list(np.ones(5)*535)

        # Snake setup
        pygame.init()
        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)
         
        self.screen_width = 600
        self.screen_height = 400
         
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')
         
        self.clock = pygame.time.Clock()
         
        self.snake_block = 10
        self.snake_speed = 10
        self.direction = "UP" # UP, DOWN, RIGHT, LEFT
        self.current_action = "RIGHT" #RIGHT,LEFT currently happening
        self.actions = ["RIGHT", "LEFT"] #when blowing it turns right initially (left if opposite)
        
        #☺where
        self.game_over = False
        self.in_settings = False
        self.in_update_controls = False
        self.in_update_speed = False
        self.in_endgame_menu = False
         
        self.font = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)

        # Settings
        self.button1 = Button("Speed: "+str(self.snake_speed), self.font, x=self.screen_width/2.2, y=self.screen_height/2, bg="navy")
        self.button2 = Button("Blow setting: Turn "+self.actions[0]+" (opposite for "+self.actions[1]+")", self.font, x=self.screen_width/1.85, y=self.screen_height/2, bg="navy")

    def Your_score(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.yellow)
        self.screen.blit(value, [0, 0])

    def our_snake(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.screen, self.black, [x[0], x[1], snake_block, snake_block])

    def message(self, msg, color, width_ratio=6, height_ratio=3):
        mesg = self.font.render(msg, True, color)
        self.screen.blit(mesg, [self.screen_width / width_ratio, self.screen_height / height_ratio])

    def endMenu(self,Length_of_snake):
        self.screen.fill(self.blue)
        self.message("You Lost! Press C-Play Again or Q-Quit", self.red)
        self.Your_score(Length_of_snake - 1)
        pygame.display.update()
 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_over = True
                    self.in_endgame_menu = False
                if event.key == pygame.K_c:
                    self.current_action ="RIGHT"
                    self.direction ="UP"
                    self.run() #rerun the game

    def settings(self):
        self.screen.fill(self.blue)
        self.message("Settings", self.green, height_ratio=5)
        self.message("Press C-Play Again", self.red, height_ratio=3.8)
        self.message("Press Q-Quit", self.red, height_ratio=3.1)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.in_settings = False
                if event.key == pygame.K_q:
                    self.in_settings = False
                    self.game_over = True
            self.button1.onClick(event)
            self.button2.onClick(event)
        
        if self.in_update_speed:
            self.button1.change_text(str(self.snake_speed), "red")
        elif not self.in_update_speed:
            self.button1.change_text(str(self.snake_speed), "navy")

        if self.in_update_controls:
            self.button2.change_text(str("<->"), "red")
        elif not self.in_update_controls:
            self.button2.change_text("Blow setting: Turn "+self.actions[0]+" (opposite for "+self.actions[1]+")", "navy")
        
        
        self.button1.show(self.screen)
        self.button2.show(self.screen)
        pygame.display.update()
        
    def updateControlsGame(self):
        self.outputs.append(self.arduino.read())

        print(len(self.outputs), self.outputs[-4:-1])
         
        if self.outputs[-2] > 600 and self.outputs[-1] > 600:# QUIT
            self.game_over = True
            self.outputs = list(np.ones(5)*535)
        elif self.outputs[-2] < 400 and self.outputs[-1] < 400: #SETTINGS
            self.in_settings = True
            self.outputs = list(np.ones(5)*535)
        elif self.outputs[-3] < 600 and self.outputs[-2] > 600 and self.outputs[-1] < 600: #TURN RIGHT
            self.current_action = self.actions[0] #initially right
            self.outputs = list(np.ones(5)*535)
        elif self.outputs[-3] > 400 and self.outputs[-2] < 400 and self.outputs[-1] > 400: #TURN LEFT
            self.current_action = self.actions[1] #initially left
            self.outputs = list(np.ones(5)*535)
            
        #time.sleep(0.05)

    def updateControlsSettings(self):
        self.outputs.append(self.arduino.read())

        print(len(self.outputs), self.outputs[-4 : -1], self.in_update_speed, self.in_update_controls)

        if not self.in_update_speed and not self.in_update_controls:
            if self.outputs[-3] > 600 and self.outputs[-1] > 600: #QUIT
                self.game_over = True
                self.in_settings = False
                self.outputs = list(np.ones(5)*535)
            elif self.outputs[-2] < 400 and self.outputs[-1] < 400: #QUIT SETTINGS/CONTINUE
                self.in_settings = not self.in_settings
                self.outputs = list(np.ones(5)*535)
            elif self.outputs[-3] < 600 and self.outputs[-2] > 600 and self.outputs[-1] < 600: #UPDATE SPEED
                self.in_update_speed = not self.in_update_speed 
                self.outputs = list(np.ones(5)*535)
            elif self.outputs[-3] > 400 and self.outputs[-2] < 400 and self.outputs[-1] > 400: #UPDATE CONTROL
                self.in_update_controls = not self.in_update_controls
                self.outputs = list(np.ones(5)*535)
        elif self.in_update_speed:
            if self.outputs[-3] > 600 and self.outputs[-1] > 600: #INCREASE SPEED
                if(self.snake_speed > 1):
                    self.snake_speed += 1
            elif self.outputs[-2] < 400 and self.outputs[-1] < 400: #DECREASE SPEED
                if(self.snake_speed > 1):
                    self.snake_speed -= 1
            elif self.outputs[-3] < 600 and self.outputs[-2] > 600 and self.outputs[-1] < 600: #quit UPDATE SPEED
                self.in_update_speed = not self.in_update_speed
                self.outputs = list(np.ones(5)*535)
        elif self.in_update_controls:
            if self.outputs[-3] < 600 and self.outputs[-2] > 600 and self.outputs[-1] < 600: #Short strong blow becomes new RIGHT
                if self.actions[0] == "LEFT":
                    self.actions = list(reversed(self.actions))
                self.in_update_controls = not self.in_update_controls #when a control is changed it updates it
                self.outputs = list(np.ones(5)*535)
            elif self.outputs[-3] > 400 and self.outputs[-2] < 400 and self.outputs[-1] > 400: #Short strong insparation new RIGHT
                if self.actions[0] == "RIGHT":
                    self.actions = list(reversed(self.actions))
                self.in_update_controls = not self.in_update_controls #when a control is changed it updates it
                self.outputs = list(np.ones(5)*535)
                
        
        #time.sleep(0.05)
        

    def run(self):
     
        x1 = self.screen_width / 2
        y1 = self.screen_height / 2
     
        x1_change = 0
        y1_change = 0
     
        snake_List = []
        Length_of_snake = 1
     
        foodx = round(random.randrange(0, self.screen_width - self.snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, self.screen_height - self.snake_block) / 10.0) * 10.0
     
        while not self.game_over:
            
            self.updateControlsGame()

            print(self.current_action, self.outputs[-3:-1], self.direction)
            #End Menu
            while self.in_endgame_menu == True:
                self.updateControlsGame()
                self.endMenu(Length_of_snake)

            #Settings
            while self.in_settings == True:
                self.updateControlsSettings()
                self.settings()
                                
            # Control panel
            if (self.direction == "UP" and self.current_action == "LEFT") or (self.direction == "DOWN" and self.current_action == "RIGHT"): # go left
                x1_change = -self.snake_block
                y1_change = 0
                self.direction = "LEFT"
                self.current_action = ""
                self.outputs = list(np.ones(5)*535)
            elif (self.direction == "UP" and self.current_action == "RIGHT") or (self.direction == "DOWN" and self.current_action == "LEFT"): # go right
                x1_change = self.snake_block
                y1_change = 0
                self.direction = "RIGHT"
                self.current_action = ""
                self.outputs = list(np.ones(5)*535)
            elif (self.direction == "LEFT" and self.current_action == "RIGHT") or (self.direction == "RIGHT" and self.current_action == "LEFT"): # go up
                y1_change = -self.snake_block
                x1_change = 0
                self.direction = "UP"
                self.current_action = ""
                self.outputs = list(np.ones(5)*535)
            elif self.direction == self.current_action: # go down
                y1_change = self.snake_block
                x1_change = 0
                self.direction = "DOWN"
                self.current_action = ""
                self.outputs = list(np.ones(5)*535)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a: # settings
                        self.in_settings = True
                    elif event.key == pygame.K_q: # quit the game
                        self.game_over = True
     
            if x1 >= self.screen_width or x1 < 0 or y1 >= self.screen_height or y1 < 0:
                self.in_endgame_menu = True
            x1 += x1_change
            y1 += y1_change
            self.screen.fill(self.blue)
            pygame.draw.rect(self.screen, self.green, [foodx, foody, self.snake_block, self.snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]
     
            for x in snake_List[:-1]:
                if x == snake_Head:
                    self.in_endgame_menu = True
     
            self.our_snake(self.snake_block, snake_List)
            self.Your_score(Length_of_snake - 1)
     
            pygame.display.update()
     
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, self.screen_width - self.snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, self.screen_height - self.snake_block) / 10.0) * 10.0
                Length_of_snake += 1
     
            self.clock.tick(self.snake_speed)
            if len(self.outputs) > 10000:
                self.outputs = list(np.ones(5)*535)
 
        pygame.quit()
        self.arduino.stop()
# ----------------------------------------Main Code-----------------------------------
def __main__():
    game = Snake()
    try:
        game.run()
    except:
        game.arduino.stop()
__main__()