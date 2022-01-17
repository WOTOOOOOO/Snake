import pygame
import random
import time


class App:

    def __init__(self):
        self.startTime=time.time()
        self.speed=5
        self.running = False
        self.clock = None
        self.screen = None
        self.directX=0
        self.directY=0
        self.foodColor=(255,0,0)
        self.blocks = [[500, 350],[500,330],[500,310],[500,290],[500,270]]
        self.score = 0
        self.foodX = 300
        self.foodY = 300
        self.superFoodRandomizer=0
        self.hellOnEarth=False
        self.difficultyTwo=False
        self.displayGameOverScreen = True

    def run(self):
        self.init()
        self.gameStart()
        while self.running:
            self.update()
            self.render()
        if self.displayGameOverScreen:
            self.gameOver()
        self.cleanUp()

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSNAKE")
        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        self.events()

    def gameStart(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.displayGameOverScreen=False
                    return
                if event.type == pygame.KEYDOWN:
                    if (event.key==pygame.K_SPACE) and self.directY == 0 and self.directX == 0:
                        self.speed=5
                        self.directY = self.speed
                        return
                    if (event.key == pygame.K_2) and self.directY == 0 and self.directX == 0:
                        self.speed = 10
                        self.directY = self.speed
                        self.difficultyTwo = True
                        return
                    if (event.key == pygame.K_6) and self.directY == 0 and self.directX == 0:
                        self.speed = 10
                        self.directY = self.speed
                        self.hellOnEarth = True
                        return
            self.screen.fill((50, 10, 240))
            pygame.draw.line(self.screen, (255, 255, 255), (0, 50), (800, 50))
            beginfont = pygame.font.Font('freesansbold.ttf', 25)
            begintext = beginfont.render("PRESS SPACE FOR DIFFICULTY 1", True, (0, 255, 0), (0, 0, 128))
            begintextRect = begintext.get_rect()
            begintextRect.center = (390, 180)
            self.screen.blit(begintext, begintextRect)
            begintext = beginfont.render("for difficulty two press 2", True, (0, 255, 0), (0, 0, 128))
            begintextRect.center = (410, 200)
            self.screen.blit(begintext, begintextRect)
            begintext = beginfont.render("for HELL ON EARTH press 6", True, (0, 255, 0), (0, 0, 128))
            begintextRect.center = (390, 220)
            self.screen.blit(begintext, begintextRect)
            for i in self.blocks:
                pygame.draw.rect(self.screen, (30, 0, 50), pygame.Rect(i[0], i[1], 20, 20))
            self.createDisplay()
            pygame.display.flip()
            self.clock.tick(60)



    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.displayGameOverScreen = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and self.directY == 0 :
                    self.directY = -self.speed
                    self.directX = 0
                if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and self.directY == 0:
                    self.directY = self.speed
                    self.directX = 0
                if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and self.directX == 0:
                    self.directY = 0
                    self.directX = -self.speed
                if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and self.directX == 0:
                    self.directY = 0
                    self.directX = self.speed

    def render(self):
        if not self.hellOnEarth:
            self.screen.fill((50, 10, 240))
        else:
            self.screen.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        snake_list=self.blocks

        self.moveBody(snake_list)
        if self.superFoodRandomizer<50 or self.difficultyTwo or self.hellOnEarth:
            self.foodColor=(255,0,0)
            pygame.draw.rect(self.screen, self.foodColor, pygame.Rect(self.foodX, self.foodY, 20, 20)) #DRAW FOOD
        else:
            self.foodColor=(0,255,0)
            pygame.draw.rect(self.screen, self.foodColor, pygame.Rect(self.foodX, self.foodY, 20, 20))
        self.blocks[0]=[self.blocks[0][0]+self.directX,self.blocks[0][1]+self.directY]
        pygame.draw.rect(self.screen, (30,0,50),pygame.Rect(self.blocks[0][0], self.blocks[0][1], 20, 20))
        for i in self.blocks[1:]:
            pygame.draw.rect(self.screen, (30,0,50),pygame.Rect(i[0], i[1], 20, 20))

        # CHECK THINGS
        self.checkEat(self.foodColor)
        self.checkBorders()
        if len(self.blocks)>3:
            self.checkBodyColission()
        # -----------------------------------
        pygame.draw.line(self.screen, (255, 255, 255), (0, 50), (800, 50))
        self.createDisplay()
        # -----------------------------------

        pygame.display.flip()
        self.clock.tick(60)

    def cleanUp(self):
        pygame.quit()

    def checkBorders(self):
        if self.blocks[0][0] <= 0 or self.blocks[0][1] <= 50 or \
                self.blocks[0][0] + 20 >= 800 or self.blocks[0][1] + 20 >= 500:
            self.running = False
            return False
        return True
#
    def checkEat(self,color):
        if (self.foodX <= self.blocks[0][0] <= self.foodX + 20 and self.foodY <= self.blocks[0][
            1] <= self.foodY + 20) or \
                (self.foodX <= self.blocks[0][0] + 20 <= self.foodX + 20 and self.foodY <= self.blocks[0][
                    1] <= self.foodY + 20) or \
                (self.foodX <= self.blocks[0][0] <= self.foodX + 20 and self.foodY <= self.blocks[0][
                    1] + 20 <= self.foodY + 20) or \
                (self.foodX <= self.blocks[0][0] + 20 <= self.foodX + 20 and self.foodY <= self.blocks[0][
                    1] + 20 <= self.foodY + 20):
            self.foodX = random.randint(50, 780)
            self.foodY = random.randint(50, 480)
            self.score = self.score + 1
            self.superFoodRandomizer=random.randint(0,60)
            if color==(255,0,0):
                self.blocks.append([self.blocks[len(self.blocks) - 1][0] +
                                20 * ((self.blocks[len(self.blocks) - 1][0] - self.blocks[len(self.blocks) - 2][
                0]) // 20),
                                self.blocks[len(self.blocks) - 1][1] +
                                20 * ((self.blocks[len(self.blocks) - 1][1] - self.blocks[len(self.blocks) - 2][
                                    1]) // 20)])

    def moveBody(self, snake_list):
        for i in range(1, len(snake_list)):
             self.blocks[i]=((((snake_list[i-1][0]-snake_list[i][0])/20)*self.speed+self.blocks[i][0],
             ((snake_list[i-1][1]-snake_list[i][1])/20)*self.speed+self.blocks[i][1]))


    def checkBodyColission(self):
        for i in self.blocks[3:]:
            if (i[0] < self.blocks[0][0] < i[0] + 15 and i[1] < self.blocks[0][1] < i[1] + 15) or \
                    (i[0] < self.blocks[0][0] + 15 < i[0] + 15 and i[1] < self.blocks[0][1] < i[1] + 15) or \
                    (i[0] < self.blocks[0][0] < i[0] + 15 and i[1] < self.blocks[0][1] + 15 < i[1] + 15) or \
                    (i[0] < self.blocks[0][0] + 15 < i[0] + 15 and i[1] < self.blocks[0][1] + 15 < i[1] + 15):
                self.running = False
                return False
        return True

    def createDisplay(self):
        font1=pygame.font.Font('freesansbold.ttf', 25)
        if not self.hellOnEarth:
            text1=font1.render("SNAKE GAME",True, (0, 255, 0), (0, 0, 128))
        else:
            text1 = font1.render("SUFFER", True, (0, 255, 0), (0, 0, 128))
        textRect1=text1.get_rect()
        textRect1.center=(250,25)
        self.screen.blit(text1, textRect1)
        font = pygame.font.Font('freesansbold.ttf', 25)
        if not self.hellOnEarth:
            text2 = font.render(f"score:{self.score}", True, (0, 255, 0), (0, 0, 128))
            textRect2 = text2.get_rect()
            textRect2.center = (60, 25)
        else :
            text2 = font.render(f"SCORE:NOPE", True, (0, 255, 0), (0, 0, 128))
            textRect2 = text2.get_rect()
            textRect2.center = (100, 25)
        self.screen.blit(text2, textRect2)
        font3=pygame.font.Font('freesansbold.ttf', 25)
        textRect3=text2.get_rect()
        text3=font3.render(f"LENGTH:{len(self.blocks)}", True, (0, 255, 0), (0, 0, 128))
        textRect3.center=(500,25)
        self.screen.blit(text3, textRect3)

    def gameOver(self):
        closeGame=False
        while not closeGame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    closeGame = True

            self.screen.fill((0,0,0))
            endfont = pygame.font.Font('freesansbold.ttf', 25)
            endtext = endfont.render("GAME OVER", True, (0, 255, 0), (0, 0, 0))
            endtextRect = endtext.get_rect()
            endtextRect.center = (400, 220)
            self.screen.blit(endtext, endtextRect)
            endtext = endfont.render(f"FINAL SCORE: {self.score}", True, (0, 255, 0), (0, 0, 0))
            endtextRect.center=(400,250)
            self.screen.blit(endtext,endtextRect)

            pygame.display.flip()




if __name__ == "__main__":
    app = App()
    app.run()
