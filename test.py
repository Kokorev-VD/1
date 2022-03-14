import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

pygame.display.flip()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

nmbrs = "0123456789"

class Button:
    def __init__(self, text, pos, font, number, bg="black", feedback=""):
        self.x, self.y = pos
        self.number = number
        self.t = text
        if number == -1:
            self.visible = False
        else:
            self.visible = True
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        self.text = self.font.render(text, 1, pygame.Color("White"))
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
                        if btn.feedback[len(btn.feedback) - 1] in nmbrs:
                            if self.number == int(btn.feedback[len(btn.feedback) - 1]):
                                btn.visible = True
                if self.rect.collidepoint(x, y) and self.feedback[:len(self.feedback)-1] == "Making btn":
                    for btn in btns:
                        if btn.number == int(self.feedback[len(self.feedback)-1]):
                            btn.change_text(self.t, "navy")
                            btn.t = self.t
                            for btn1 in btns:
                                if btn1.feedback[len(btn1.feedback) - 1] in nmbrs:
                                    if int(self.feedback[len(self.feedback) - 1]) == int(btn1.feedback[len(btn1.feedback) - 1]):
                                        btn1.visible = False
                if self.rect.collidepoint(x, y) and self.feedback == "End btn":
                    res = [[0, 0], [0, 0], [0, 0]]
                    for btn in btns:
                        if btn.number<6 and btn.number>-1:
                            res[btn.number%3][int(btn.number/3)] = btn.t
                    print(res)

def mainloop():

    while True:
        screen.fill((215, 225, 250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            for btn in btns:
                btn.click(event)
        for btn in btns:
            btn.show()
        clock.tick(30)

        pygame.display.update()


ix = 100
iy = 100
btns = []
for i in range(2):
    for j in range(3):
        button1 = Button(
            " O ",
            (ix+i*120, iy+j*120),
            font=30,
            number=j+3*i,
            bg="navy",
            feedback="Creation btn")
        btn1 = Button(
            " a ",
            (ix+i*120+30, iy+j*120),
            font=30,
            number=-1,
            bg="green",
            feedback="Making btn" + str(j+3*i))

        btn2 = Button(
            " d ",
            (ix+i*120+30, iy+j*120+30),
            font=30,
            number=-1,
            bg="green",
            feedback="Making btn" + str(j+3*i))

        btn3 = Button(
            " g ",
            (ix+i*120+30, iy+j*120+60),
            font=30,
            number = -1,
            bg="green",
            feedback="Making btn" + str(j+3*i))
        btns.append(button1)
        btns.append(btn1)
        btns.append(btn2)
        btns.append(btn3)
ix += 120*2
for i in range(3):
    for j in range(3):
        b1 = Button(
            " O ",
            (ix + i * 120, iy + j * 120),
            font=30,
            number=j + 3 * i+6,
            bg="red",
            feedback="")
        btns.append(b1)

endbut = Button(
            " Нажмите, чтобы отправить данные нейросети ",
            (400, 900),
            font=30,
            number=-2,
            bg="cyan",
            feedback="End btn")
btns.append(endbut)
mainloop()