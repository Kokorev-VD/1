class SituationRater(object):
    left = []
    right = []
    all = []

    l = [0, 0, 0]
    r = [0, 0, 0]

    l_load = []
    r_load = []

    l1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    r1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    l2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    r2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    l3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    r3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    l_ortocenter = 0
    r_ortocenter = 0

    l_clear = 0.0
    r_clear = 0.0

    def reset(self):
        self.left = []
        self.right = []
        self.all = []

        self.l_load = []
        self.r_load = []

        self.l = [0, 0, 0]
        self.r = [0, 0, 0]

        self.l1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.r1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        self.l2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.r2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        self.l3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.r3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        self.l_ortocenter = 0
        self.r_ortocenter = 0

        self.l_clear = 0.0
        self.r_clear = 0.0

        # self.answer = []

    def fill(self, pole):
        self.all = pole
        # print(len(pole), len(pole[0]), len(pole[0]) // 2)
        for i in range(len(pole)):
            self.l_load.append(0)
            self.r_load.append(0)
            a = []
            b = []
            for j in range(len(pole[0]) // 2):
                a.append(pole[i][j])
                b.append(pole[i][len(pole[0]) - 1 - j])
            self.left.append(a)
            self.right.append(b)

    def rate(self):
        for i in range(len(self.left)):
            for j in range(len(self.left[0])):
                if self.left[i][j] != 0:
                    # print("in", i, j, "stays", self.left[i][j])
                    self.l[self.left[i][j] - 1] += 1
                    self.l_load[i] += 1

                    flag = True
                    for k in range(len(self.right[0])):
                        if i > 0:
                            if self.right[i-1][k] != 0:
                                flag = False
                        if self.right[i][k] != 0:
                            flag = False
                        if i < len(self.right) - 1:
                            if self.right[i+1][k] != 0:
                                flag = False
                    if flag:
                        self.l_clear = 1.0

                    if i > 0:
                        for k in range(len(self.left[0])):
                            if self.left[i - 1][k] != 0:
                                # print("left", i-1, k, "stays", self.left[i - 1][k])
                                self.l1[abs(self.left[i][j]) - 1][self.left[i - 1][k] - 1] += 1

                    if i < len(self.left) - 1:
                        for k in range(len(self.left[0])):
                            if self.left[i + 1][k] != 0:
                                # print("right", i+1, k, "stays", self.left[i + 1][k])
                                self.l1[abs(self.left[i][j]) - 1][self.left[i + 1][k] - 1] += 1

                    if j < len(self.left[0]) - 1:
                        for k in range(j + 1, len(self.left[0])):
                            if self.left[i][k] != 0:
                                # print("forward", i, k, "stays", self.left[i][k])
                                self.l2[abs(self.left[i][j]) - 1][self.left[i][k] - 1] += 1
                                # print(abs(self.left[i][j]) - 1, self.left[i][k] - 1, "+1")

                    if j > 0:
                        for k in range(j):
                            if self.left[i][k] != 0:
                                # print("backward", i, k, "stays", self.left[i][k])
                                self.l3[abs(self.left[i][j]) - 1][self.left[i][k] - 1] += 1
                    # print("")

        total = 0
        for i in self.l_load:
            total += i
        total /= 2
        for i in range(len(self.l_load)):
            if total <= 0:
                break
            if self.l_load[i] <= total:
                self.l_ortocenter += 1
            else:
                self.l_ortocenter += total/self.l_load[i]
            total -= self.l_load[i]

        for i in range(len(self.right)):
            for j in range(len(self.right[0])):
                if self.right[i][j] != 0:
                    self.r[self.right[i][j] * (-1) - 1] += 1
                    self.r_load[i] += 1

                    flag = True
                    for k in range(len(self.left[0])):
                        if i > 0:
                            if self.left[i - 1][k] != 0:
                                flag = False
                        if self.left[i][k] != 0:
                            flag = False
                        if i < len(self.left) - 1:
                            if self.left[i + 1][k] != 0:
                                flag = False
                    if flag:
                        self.r_clear = 1.0

                    if i > 0:
                        for k in range(len(self.right[0])):
                            if self.right[i - 1][k] != 0:
                                self.r1[abs(self.right[i][j]) - 1][abs(self.right[i - 1][k]) - 1] += 1

                    if i < len(self.right) - 1:
                        for k in range(len(self.right[0])):
                            if self.right[i + 1][k] != 0:
                                self.r1[abs(self.right[i][j]) - 1][abs(self.right[i + 1][k]) - 1] += 1

                    if j < len(self.right[0]) - 1:
                        for k in range(j + 1, len(self.right[0])):
                            if self.right[i][k] != 0:
                                self.r2[abs(self.right[i][j]) - 1][abs(self.right[i][k]) - 1] += 1

                    if j > 0:
                        for k in range(j):
                            if self.right[i][k] != 0:
                                self.r3[abs(self.right[i][j]) - 1][abs(self.right[i][k]) - 1] += 1

        total = 0
        for i in self.r_load:
            total += i
        total /= 2
        for i in range(len(self.r_load)):
            if total <= 0:
                break
            if self.r_load[i] <= total:
                self.r_ortocenter += 1
            else:
                self.r_ortocenter += total/self.r_load[i]
            total -= self.r_load[i]

        answer = []
        if self.l[0] + self.l[1] + self.l[2] == 0 and self.r[0] + self.r[1] + self.r[2] == 0:
            answer.append(0.0)
        else:
            answer.append(((self.l[0] + self.l[1] + self.l[2]) /
                      max(((self.l[0] + self.l[1] + self.l[2]) + (self.r[0] + self.r[1] + self.r[2])), 1)) * 2 - 1)

        answer.append(abs(self.l_ortocenter - self.r_ortocenter) / len(self.left))

        for i in range(3):
            if self.l[i] == 0 and self.r[i] == 0:
                answer.append(0.0)
            else:
                answer.append((self.l[i] / max((self.l[i] + self.r[i]), 1)) * 2 - 1)

        answer.append(self.l_clear)
        answer.append(self.r_clear)

        for i in range(3):
            for j in range(3):
                self.l1[i][j] /= max(self.l[i], 1)
                self.l2[i][j] /= max(self.l[i], 1)
                self.l3[i][j] /= max(self.l[i], 1)

                self.r1[i][j] /= max(self.r[i], 1)
                self.r2[i][j] /= max(self.r[i], 1)
                self.r3[i][j] /= max(self.r[i], 1)

        '''print(self.l, self.r)
        print(self.l_ortocenter, self.r_ortocenter, self.l_clear, self.r_clear)
        print(self.l1, self.r1)
        print(self.l2, self.r2)
        print(self.l3, self.r3)'''


        for i in range(3):
            for j in range(3):
                if self.l1[i][j] == 0 and self.r1[i][j] == 0:
                    answer.append(0.0)
                else:
                    answer.append((self.l1[i][j] / max((self.l1[i][j] + self.r1[i][j]), 1)) * 2 - 1)

                if self.l2[i][j] == 0 and self.r2[i][j] == 0:
                    answer.append(0.0)
                else:
                    answer.append((self.l2[i][j] / max((self.l2[i][j] + self.r2[i][j]), 1)) * 2 - 1)

                if self.l3[i][j] == 0 and self.r3[i][j] == 0:
                    answer.append(0.0)
                else:
                    answer.append((self.l3[i][j] / max((self.l3[i][j] + self.r3[i][j]), 1)) * 2 - 1)


        return answer

    def get_rating(self, pole):
        self.reset()
        self.fill(pole)
        return self.rate()