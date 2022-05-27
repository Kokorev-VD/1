from unit import Unit


class Attacker(Unit):
    skin = "a"
    damage = 5
    health = 3

    @staticmethod
    def name():
        return "Attacker"
