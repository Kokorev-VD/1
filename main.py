from attacker import Attacker
from defender import Defender
from gunner import Gunner
from infoManager import InfoManager
from fieldManager import FieldManager
from net import Net

# Creation phase
"""pole = [[-1, -1, -1, -1, -1, -1, -1],
        [-1, 0, 0, 0, 0, 0, -1],
        [-1, 0, 0, 0, 0, 0, -1],
        [-1, 0, 0, 0, 0, 0, -1],
        [-1, -1, -1, -1, -1, -1, -1]]"""

pole = [[-1, -1, -1, -1],
        [-1,  0,  0, -1],
        [-1,  0,  0, -1],
        [-1, -1, -1, -1]]

white = []
black = []

white.append(Attacker(1, 1, pole, "White"))
black.append(Gunner(1, 2, pole, "Black"))
black.append(Defender(2, 2, pole, "Black"))

"""white.append(Attacker(1, 2, pole, "White"))
white.append(Defender(3, 2, pole, "White"))
black.append(Attacker(1, 5, pole, "Black"))
black.append(Attacker(2, 4, pole, "Black"))
black.append(Gunner(2, 5, pole, "Black"))"""

flag1 = True
flag2 = True
counter = 0
print("-------------------------" + "\n" + "-------------------------")

# Info checking phase

"""InfoManager.create(white, black)
print(InfoManager.get_torch())"""

FieldManager.init_field(white, black, pole)
FieldManager.print_field()

net = Net()
print(net)

# Action phase
while flag1 and flag2:
    counter = 0
    # Our pole
    for x in range(len(pole)):
        print(pole[x])
    print("-------------------------" + "\n" + "-------------------------")
    # Attack phase
    for x in white:
        for y in black:
            x.attack(y)
            y.attack(x)
    # Check death in white team
    for x in white:
        if x.health <= 0:
            x.death(pole)
    # Check death in black team
    for y in black:
        if y.health <= 0:
            y.death(pole)
    # Checking for alive brawlers in black and white teams
    for x in white:
        if x.alive:
            counter += 1
    if counter == 0:
        flag1 = False
    counter = 0
    for x in black:
        if x.alive:
            counter += 1
    if counter == 0:
        flag2 = False
    if not (flag1 and flag2):
        break
    # Movement phase
    for x in white:
        x.move(pole)
    for y in black:
        y.move(pole)
    # Checking for draw by not moving
    counter = 0
    for x in white:
        if x.moved or x.attacked:
            counter += 1
    for x in black:
        if x.moved or x.attacked:
            counter += 1
    if counter == 0:
        flag1 = False
        flag2 = False
        break

    print("WHITE TEAM HEALTH")
    for x in white:
        print("Health " + x.side + " " + x.name() + " at position: " +
              str(x.x_position) + " " + str(x.y_position) + " equals: " + str(x.health))
    print("-------------------------" + "\n" + "-------------------------")
    print("BLACK TEAM HEALTH")
    for x in black:
        print("Health " + x.side + " " + x.name() + " at position: " +
              str(x.x_position) + " " + str(x.y_position) + " equals: " + str(x.health))
    print("-------------------------" + "\n" + "-------------------------")

for x in range(len(pole)):
    print(pole[x])
print("-------------------------" + "\n" + "-------------------------")
# Final phase
if flag1:
    print("White wins")
elif flag2:
    print("Black wins")
else:
    print("Draw")
