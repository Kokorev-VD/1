import pygame
# from fighter import Fighter
from fieldManager import FieldManager

# import torch
# from heatmaper import Heatmaper
from neural import Neural
# from statManager import StatManager
# from situationRater import SituationRater
# from net import Net


#ПОМЫТЬ ПОЛЫ!!!
pygame.init()
screen = pygame.display.set_mode((1900, 1000))

pygame.display.flip()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

Wa_skin = pygame.image.load("white attacker.png")
Wd_skin = pygame.image.load("white defender.png")
Wg_skin = pygame.image.load("white gunner.png")

Ba_skin = pygame.image.load("black attacker.png")
Bd_skin = pygame.image.load("black defender.png")
Bg_skin = pygame.image.load("black gunner.png")

pole = [["O", "O", "O"], ["O", "O", "O"], ["", "", ""], ["O", "O", "O"], ["O", 'O', "O"]]
nmbrs = "0123456789"


class Button:
    def __init__(self, text, pos, font, number, bg="black", feedback=""):
        self.skin = pygame.image.load("empty.png")
        self.bg = bg
        self.x, self.y = pos
        self.number = number
        self.t = text
        self.skin.set_colorkey((255, 255, 255))
        if number == -1:
            self.visible = False
        else:
            self.visible = True
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.skin_rect = self.skin.get_rect(
            bottomright=(self.x, self.y))
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        self.text = self.font.render(text, 1, pygame.Color("White"))
        if self.feedback == "text":
            self.text = self.font.render(str(pole[int(self.number / 3)][self.number % 3]), 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])


    def show(self):
        if self.visible:
            screen.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and self.visible:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y) and self.feedback == "Creation btn":
                    for btn in btns:
                        if btn.bg == "red":
                            btn.visible = False
                        if btn.feedback[len(btn.feedback) - 1] in nmbrs:
                            if self.number == int(btn.feedback[len(btn.feedback) - 1]):
                                btn.visible = True
                if self.rect.collidepoint(x, y) and self.feedback[:len(self.feedback) - 1] == "Making btn":
                    for btn in btns:
                        if btn.bg == "red":
                            btn.visible = True
                        if btn.number == int(self.feedback[len(self.feedback) - 1]):
                            btn.change_text(self.t, "navy")
                            if self.t == " a ":
                                btn.skin = Wa_skin
                            if self.t == " d ":
                                btn.skin = Wd_skin
                            if self.t == " g ":
                                btn.skin = Wg_skin
                            btn.skin = pygame.transform.scale(btn.skin, (100, 100))
                            btn.skin_rect = btn.skin.get_rect(
                                bottomright=(btn.x+125, btn.y+150))
                            # print(self.t)
                            btn.t = self.t
                            for btn1 in btns:
                                if btn1.feedback[len(btn1.feedback) - 1] in nmbrs:
                                    if int(self.feedback[len(self.feedback) - 1]) == int(
                                            btn1.feedback[len(btn1.feedback) - 1]):
                                        btn1.visible = False
                if self.rect.collidepoint(x, y) and self.feedback == "End btn":
                    res = [[0, 0], [0, 0], [0, 0]]
                    for btn in btns:
                        if btn.number < 6 and btn.number > -1:
                            res[btn.number % 3][int(btn.number / 3)] = btn.t
                    print(res)  # <------
                    true_res = []
                    ava = 0
                    for st in res:
                        for un in st:
                            if un == ' a ':
                                true_res.append(1)
                                ava += 1
                            elif un == ' d ':
                                true_res.append(2)
                                ava += 1
                            elif un == ' g ':
                                true_res.append(3)
                                ava += 1
                            else:
                                true_res.append(0)
                    print(true_res, ava)

                    # acs = []
                    # stat = []

                    neo1 = Neural(3, 5, "", 2, 2, 0.005, 1)
                    neo1.change_super_parameters(1e-5, 300, 0.005, 200)
                    neo1.init_net()
                    # neo1.stop_calculating_acc()
                    # acs.append(neo1.train())
                    # stat = neo1.add_stat(stat)
                    #
                    # print(acs)
                    neo1.train()  # НЕ СТИРАТЬ, даже если кажется, что не нужно

                    # StatManager.create_stat(stat)
                    # StatManager.show_all()

                    neo1.get_special_data([], true_res, ava)
                    print(neo1.get_best())
                    print(FieldManager.get_best())

                    # Пример вывода после нажатия на кнопку:
                    #
                    # [[' O ', ' O '], [' a ', ' O '], [' O ', ' O ']] - входные данные
                    # [0, 0, 1, 0, 0, 0] 1 - обработанные данные
                    # Net init starts. Mon May 16 00:46:45 2022 - информация о ИИ (бесполезная информация)
                    # net inited in  0.0 minutes - скорость ее инициализации (бесполезная информация)
                    # [0.7367120981216431, [0.012937579303979874, 0.25035035610198975, 0.7367120981216431], [0, 0, 0, 0, 0, 1, 0, 0, -2, 0, 0, 0, 0, 0, 0], 7] - полезный вывод
                    # [0, 0, 0, 0, 0, 1, 0, 0, -2, 0, 0, 0, 0, 0, 0] - расстановка на поле (построчно: первая строка, затем средняя и потом нижняя)
                    #
                    # последнюю подобранную расстановку можно посмотреть тут - FieldManager.get_best()



def mainloop():
    back_s = pygame.image.load('new_bg.png')
    back_s = pygame.transform.scale(back_s, (1900, 1000))
    back = back_s.get_rect(bottomright=(1900, 1000))

    while True:
        screen.fill((215, 225, 250))
        screen.blit(back_s, back)
        for btn in btns:
            screen.blit(btn.skin, btn.skin_rect)
            # print(btn.skin)
            # print(btn.skin_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            for btn in btns:
                btn.click(event)
        for btn in btns:
            btn.show()
            screen.blit(btn.skin, btn.skin_rect)
        clock.tick(30)

        pygame.display.update()


ix = 365
iy = 155
btns = []
for i in range(2):
    for j in range(3):
        button1 = Button(
            " O ",
            (ix + i * 260, iy + j * 220),
            font=30,
            number=j + 3 * i,
            bg="navy",
            feedback="Creation btn")
        btn1 = Button(
            " a ",
            (ix + i * 260 + 30, iy + j * 220),
            font=30,
            number=-1,
            bg="green",
            feedback="Making btn" + str(j + 3 * i))

        btn2 = Button(
            " d ",
            (ix + i * 260 + 30, iy + j * 220 + 30),
            font=30,
            number=-1,
            bg="green",
            feedback="Making btn" + str(j + 3 * i))

        btn3 = Button(
            " g ",
            (ix + i * 260 + 30, iy + j * 220 + 60),
            font=30,
            number=-1,
            bg="green",
            feedback="Making btn" + str(j + 3 * i))
        btns.append(button1)
        btns.append(btn1)
        btns.append(btn2)
        btns.append(btn3)
ix += 260 * 2
for i in range(3):
    for j in range(3):
        b1 = Button(
            " O ",
            (ix + i * 260, iy + j * 220),
            font=30,
            number=j + 3 * i + 6,
            bg="red",
            feedback="")
        btns.append(b1)
endbut = Button(
    " Нажмите, чтобы отправить данные нейросети ",
    (670, 900),
    font=30,
    number=-2,
    bg="black",
    feedback="End btn")
btns.append(endbut)
mainloop()
