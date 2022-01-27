class FieldManager(object):
    field = []
    field_width = -1
    field_height = -1
    quantity = -1
    white = []
    black = []

    @staticmethod
    def get_field(field):
        return field

    @staticmethod
    def create_field():
        FieldManager.field = []
        quantity = FieldManager.field_width * FieldManager.field_height
        for i in range(quantity):
            FieldManager.field.append(0)

    @staticmethod
    def fill_field():

        for i in range(len(FieldManager.white)):
            cur = 0
            if FieldManager.white[i].name() == "Attacker":
                cur = 1
            elif FieldManager.white[i].name() == "Defender":
                cur = 2
            elif FieldManager.white[i].name() == "Gunner":
                cur = 3
            FieldManager.field[(FieldManager.white[i].get_y() - 1) * FieldManager.field_height + (FieldManager.white[i].get_x() - 1)] = cur

        for i in range(len(FieldManager.black)):
            cur = 0
            if FieldManager.black[i].name() == "Attacker":
                cur = -1
            elif FieldManager.black[i].name() == "Defender":
                cur = -2
            elif FieldManager.black[i].name() == "Gunner":
                cur = -3
            FieldManager.field[(FieldManager.black[i].get_y() - 1) * FieldManager.field_height + (FieldManager.black[i].get_x() - 1)] = cur

    @staticmethod
    def init_field(white, black, pole):

        FieldManager.field_height = len(pole) - 2
        FieldManager.field_width = len(pole[0]) - 2

        FieldManager.create_field()
        FieldManager.white = white
        FieldManager.black = black
        FieldManager.fill_field()

    @staticmethod
    def print_field():
        print("field ", FieldManager.field, ":", sep="")
        print("")
        for i in range(len(FieldManager.field)):
            if FieldManager.field[i] == 0:
                print("empty in (", i % FieldManager.field_height + 1, ";", int(i / FieldManager.field_height) + 1, ")", sep="")
            else:
                if FieldManager.field[i] > 0:
                    print("white ", end="")
                else:
                    print("black ", end="")

                if FieldManager.field[i]**2 == 1:
                    print("attacker ", end="")
                elif FieldManager.field[i]**2 == 4:
                    print("defender ", end="")
                elif FieldManager.field[i]**2 == 9:
                    print("gunner ", end="")

                print("in (", i % FieldManager.field_height + 1, ";", int(i / FieldManager.field_height) + 1, ")", sep="")
        print("")


