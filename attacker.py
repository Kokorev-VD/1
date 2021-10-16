from unit import Unit


class Attacker(Unit):
    skin = "a"
    damage = 5
    health = 5

    @staticmethod
    def name():
        return "Attacker"
