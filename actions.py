#define the valid actions a Cahraacter can take
class Actions:
    def __init__(self):
        pass
    @staticmethod
    def attack(attacker, defender):
        damage = 10
        defender.health -= damage
        print(f"{attacker.name} attacks {defender.name} for {damage} damage!")

    @staticmethod
    def use_item(user, item, target):
        item.use(user, target)
