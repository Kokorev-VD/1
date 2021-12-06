class Unit(object):
    health = 0
    damage = 0
    x_position = -1
    y_position = -1
    skin = ""
    alive = True
    side = ""
    moved = True
    attacked = False

    def __init__(self, posX, posY, pole, side):
        self.x_position = posX
        self.y_position = posY
        pole[self.x_position][self.y_position] = self.skin
        self.side = side

    def get_x(self):
        return self.x_position

    def get_y(self):
        return self.y_position

    def attack(self, cls):
        cls.attacked = False
        if cls.name() == "Attacker":
            if self.alive and cls.alive and ((self.x_position + 1 == cls.x_position and self.y_position == cls.y_position) or (
                    self.x_position - 1 == cls.x_position and self.y_position == cls.y_position) or (
                                                     self.y_position + 1 == cls.y_position and self.x_position == cls.x_position) or (
                                                     self.y_position - 1 == cls.y_position and self.x_position == cls.x_position)) and self.side != cls.side:
                self.health -= cls.damage
                cls.attacked = True
                print(cls.side + " " + cls.name() + " at position: " + str(
                    cls.x_position) + " " + str(cls.y_position) + " attacked " + self.side + " " + self.name() + " at position: " +
                      str(self.x_position) + " " + str(self.y_position))
                print("-------------------------" + "\n" + "-------------------------")
        if cls.name() == "Defender":
            if self.alive and cls.alive and ((self.x_position + 1 == cls.x_position and self.y_position + 1 == cls.y_position) or (
                    self.x_position - 1 == cls.x_position and self.y_position + 1 == cls.y_position) or (
                                                     self.x_position + 1 == cls.x_position and self.y_position - 1 == cls.y_position) or (
                                                     self.x_position - 1 == cls.x_position and self.y_position - 1 == cls.y_position)) and self.side != cls.side:
                self.health -= cls.damage
                cls.attacked = True
                print(cls.side + " " + cls.name() + " at position: " + str(cls.x_position) + " " + str(
                    cls.y_position) + " attacked " + self.side + " " + self.name() + " at position: " +
                      str(self.x_position) + " " + str(self.y_position))
                print("-------------------------" + "\n" + "-------------------------")
        if cls.name() == "Gunner":
            if self.alive and cls.alive and (
                    self.x_position == cls.x_position and (self.y_position < cls.y_position + 3 or self.y_position > cls.y_position - 3)):
                self.health -= cls.damage
                cls.attacked = True
                print(cls.side + " " + cls.name() + " at position: " + str(cls.x_position) + " " + str(
                    cls.y_position) + " attacked " + self.side + " " + self.name() + " at position: " +
                      str(self.x_position) + " " + str(self.y_position))
                print("-------------------------" + "\n" + "-------------------------")

    def death(self, pole):
        self.damage = 0
        self.skin = 0
        pole[self.x_position][self.y_position] = self.skin
        self.alive = False

    def move(self, pole):
        self.moved = False
        if not self.attacked and self.alive and self.side == "White" and pole[self.x_position][self.y_position + 1] == 0:
            pole[self.x_position][self.y_position] = 0
            self.y_position += 1
            pole[self.x_position][self.y_position] = self.skin
            self.moved = True
        if not self.attacked and self.alive and self.side == "Black" and pole[self.x_position][self.y_position - 1] == 0:
            pole[self.x_position][self.y_position] = 0
            self.y_position -= 1
            pole[self.x_position][self.y_position] = self.skin
            self.moved = True
