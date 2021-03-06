from attacker import Attacker
from defender import Defender
from gunner import Gunner


class Fighter:
    pole = []
    white = []
    black = []
    ctr = 0

    def fill_pole(self, pole):
        # t = time.time()
        a = []
        b = []
        for i in range(len(pole[0]) + 2):
            a.append(-1)
            if i == 0 or i == len(pole[0]) + 1:
                b.append(-1)
            else:
                b.append(0)
        # print(a)
        # print(b)
        self.pole = []
        self.pole.append(a.copy())
        for i in range(len(pole)):
            self.pole.append(b.copy())
        self.pole.append(a.copy())
        # for i in range(5):
        #     print(self.pole[i])

        # print(time.time() - t, end=" ")
        # print(self.pole)

    def fill_fighters(self, pole):
        # t = time.time()
        self.white = []
        self.black = []

        for i in range(len(pole)):
            for j in range(len(pole[0])):
                if pole[i][j] == 1:
                    self.white.append(Attacker(i + 1, j + 1, self.pole, "White", True))
                elif pole[i][j] == 2:
                    self.white.append(Defender(i + 1, j + 1, self.pole, "White", True))
                elif pole[i][j] == 3:
                    self.white.append(Gunner(i + 1, j + 1, self.pole, "White", True))
                elif pole[i][j] == -1:
                    self.black.append(Attacker(i + 1, j + 1, self.pole, "Black", True))
                elif pole[i][j] == -2:
                    self.black.append(Defender(i + 1, j + 1, self.pole, "Black", True))
                elif pole[i][j] == -3:
                    self.black.append(Gunner(i + 1, j + 1, self.pole, "Black", True))
        # print(time.time() - t, end=" ")


    def hf(self):
        self.ctr+=1
        print(self.ctr)
        count = 0
        for x in self.white:
            for y in self.black:
                x.attack(y)
                y.attack(x)
        for x in self.white:
            if x.health <= 0:
                x.death(self.pole)
        for y in self.black:
            if y.health <= 0:
                y.death(self.pole)
        for x in self.white:
            if x.alive:
                count += 1
        count = 0
        for x in self.black:
            if x.alive:
                count += 1
        for x in self.white:
            x.move(self.pole)
        for y in self.black:
            y.move(self.pole)
        count = 0
        for x in self.white:
            if x.moved or x.attacked:
                count += 1
        for x in self.black:
            if x.moved or x.attacked:
                count += 1

    def fight(self):
        # t = time.time()
        count = 0
        flag1 = True
        flag2 = True
        while flag1 and flag2:
            count = 0
            for x in self.white:
                for y in self.black:
                    x.attack(y)
                    y.attack(x)
            for x in self.white:
                if x.health <= 0:
                    x.death(self.pole)
            for y in self.black:
                if y.health <= 0:
                    y.death(self.pole)
            for x in self.white:
                if x.alive:
                    count += 1
            if count == 0:
                flag1 = False
            count = 0
            for x in self.black:
                if x.alive:
                    count += 1
            if count == 0:
                flag2 = False
            if not (flag1 and flag2):
                break
            for x in self.white:
                x.move(self.pole)
            for y in self.black:
                y.move(self.pole)
            count = 0
            for x in self.white:
                if x.moved or x.attacked:
                    count += 1
            for x in self.black:
                if x.moved or x.attacked:
                    count += 1
            if count == 0:
                flag1 = False
                flag2 = False
                break

            '''print("WHITE TEAM HEALTH")
            for x in self.white:
                print("Health " + x.side + " " + x.name() + " at position: " +
                      str(x.x_position) + " " + str(x.y_position) + " equals: " + str(x.health))
            print("-------------------------" + "\n" + "-------------------------")
            print("BLACK TEAM HEALTH")
            for x in self.black:
                print("Health " + x.side + " " + x.name() + " at position: " +
                      str(x.x_position) + " " + str(x.y_position) + " equals: " + str(x.health))
            print("-------------------------" + "\n" + "-------------------------")'''

        '''for x in range(len(self.pole)):
            print(self.pole[x])
        print("-------------------------" + "\n" + "-------------------------")'''

        # print(time.time() - t)

        if flag1:
            return 2
            # print("White wins")
        elif flag2:
            return 0
            # print("Black wins")
        else:
            return 1
            # print("Draw")
    def get_Sosison(self):
        rs = []
        for i in range(5):
            # print(self.pole[i])
            for j in range(7):
                if self.pole[i][j] != -1:
                    if self.pole[i][j] == "aW":
                        rs.append(1)
                    if self.pole[i][j] == "dW":
                        rs.append(2)
                    if self.pole[i][j] == "gW":
                        rs.append(3)
                    if self.pole[i][j] == "aB":
                        rs.append(-1)
                    if self.pole[i][j] == "dB":
                        rs.append(-2)
                    if self.pole[i][j] == "gB":
                        rs.append(-3)
                    if self.pole[i][j] == 0:
                        rs.append(0)
                    # rs.append(self.pole[i][j]
        print(rs)
        return rs


    def get_data(self, pole):
        # print(pole)
        self.fill_pole(pole)
        self.fill_fighters(pole)
        return self.fight()