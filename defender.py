from unit import Unit


class Defender(Unit):
    skin = "d"
    damage = 3
    health = 7

    @staticmethod
    def name():
        return "Defender"
