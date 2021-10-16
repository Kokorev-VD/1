class Unit(object):
    health = 0
    damage = 0
    posX = -1
    posY = -1
    skin = ""
    alive = True
    side = ""
    moved = True
    attacked = False

    def __init__(self, posX, posY, pole, side):
        self.posX = posX
        self.posY = posY
        pole[self.posX][self.posY] = self.skin
        self.side = side

    def attack(self, cls):
        cls.attacked = False
        if cls.name() == "Attacker":
            if self.alive and cls.alive and ((self.posX + 1 == cls.posX and self.posY == cls.posY) or (
                    self.posX - 1 == cls.posX and self.posY == cls.posY) or (
                                                     self.posY + 1 == cls.posY and self.posX == cls.posX) or (
                                                     self.posY - 1 == cls.posY and self.posX == cls.posX)) and self.side != cls.side:
                self.health -= cls.damage
                cls.attacked = True
                print(cls.side + " " + cls.name() + " at position: " + str(
                    cls.posX) + " " + str(cls.posY) + " attacked " + self.side + " " + self.name() + " at position: " +
                      str(self.posX) + " " + str(self.posY))
                print("-------------------------" + "\n" + "-------------------------")
        if cls.name() == "Defender":
            if self.alive and cls.alive and ((self.posX + 1 == cls.posX and self.posY + 1 == cls.posY) or (
                    self.posX - 1 == cls.posX and self.posY + 1 == cls.posY) or (
                                                     self.posX + 1 == cls.posX and self.posY - 1 == cls.posY) or (
                                                     self.posX - 1 == cls.posX and self.posY - 1 == cls.posY)) and self.side != cls.side:
                self.health -= cls.damage
                cls.attacked = True
                print(cls.side + " " + cls.name() + " at position: " + str(cls.posX) + " " + str(
                    cls.posY) + " attacked " + self.side + " " + self.name() + " at position: " +
                      str(self.posX) + " " + str(self.posY))
                print("-------------------------" + "\n" + "-------------------------")
        if cls.name() == "Gunner":
            if self.alive and cls.alive and (
                    self.posX == cls.posX and (self.posY < cls.posY + 3 or self.posY > cls.posY - 3)):
                self.health -= cls.damage
                cls.attacked = True
                print(cls.side + " " + cls.name() + " at position: " + str(cls.posX) + " " + str(
                    cls.posY) + " attacked " + self.side + " " + self.name() + " at position: " +
                      str(self.posX) + " " + str(self.posY))
                print("-------------------------" + "\n" + "-------------------------")

    def death(self, pole):
        self.damage = 0
        self.skin = 0
        pole[self.posX][self.posY] = self.skin
        self.alive = False

    def move(self, pole):
        self.moved = False
        if not self.attacked and self.alive and self.side == "White" and pole[self.posX][self.posY + 1] == 0:
            pole[self.posX][self.posY] = 0
            self.posY += 1
            pole[self.posX][self.posY] = self.skin
            self.moved = True
        if not self.attacked and self.alive and self.side == "Black" and pole[self.posX][self.posY - 1] == 0:
            pole[self.posX][self.posY] = 0
            self.posY -= 1
            pole[self.posX][self.posY] = self.skin
            self.moved = True
