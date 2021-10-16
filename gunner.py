from unit import Unit


class Gunner(Unit):
    skin = "g"
    damage = 1
    health = 1

    @staticmethod
    def name():
        return "Gunner"