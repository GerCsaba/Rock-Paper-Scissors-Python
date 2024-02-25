import pygame
from network import Network
import pickle
pygame.font.init()
import os




width = 700
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


ROCK=pygame.transform.scale(pygame.image.load("Ko_Papir_Ollo\imgs\Rock.jpeg"),(130,130))
PAPER=pygame.transform.scale(pygame.image.load("Ko_Papir_Ollo\imgs\Paper.jpeg"),(130,130))
SCISSOR=pygame.transform.scale(pygame.image.load("Ko_Papir_Ollo\imgs\Scissores.jpeg"),(130,130))
BGPIC=pygame.transform.scale(pygame.image.load("Ko_Papir_Ollo\imgs\Bg.jpeg"),(700,600))
BGCOLOR=(149, 149, 149)
#ROCK=pygame.transform.scale(ROCK,(100,100))


class Button:
    def __init__(self, text, x, y, img):
        self.text = text
        self.x = x
        self.y = y
        self.img=img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        #pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        #font = pygame.font.SysFont("comicsans", 40)
        #text = font.render(self.text, 1, (255,255,255))
        #win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    #win.fill(BGCOLOR)
    win.blit(BGPIC,(0,0))

    if not(game.connected()):
        font = pygame.font.SysFont("impact", 60)
        text = font.render("Waiting for Player...", 1, (46, 168, 167))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("impact", 60)
        font2 = pygame.font.SysFont("impact", 50)
        text = font.render("Your Move", 1, (46, 168, 167))
        win.blit(text, (30, 100))

        text = font.render("Opponents", 1, (46,168, 167))
        win.blit(text, (380, 100))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font2.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font2.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font2.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font2.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font2.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font2.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (60, 280))
            win.blit(text1, (430, 280))
        else:
            win.blit(text1, (60, 280))
            win.blit(text2, (430, 280))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 80, 430, ROCK),Button("Scissors", 280, 430, SCISSOR), Button("Paper", 480, 430, PAPER)]
def main():

    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:

        clock.tick(60)

        try:
            game = n.send("get")
        except:
            run = False
            print("Exeption main")
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("impact", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.blit(BGPIC, (0, 0))
        font = pygame.font.SysFont("impact", 60)
        text = font.render("Click to Play!", 1, (46, 168, 167))
        win.blit(text, (170,170))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()