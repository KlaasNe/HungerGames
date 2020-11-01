class Item:
    def __init__(self, name, item_type, dmg=0, res=0, hp=0, en=0, prc=0, slot=None):
        self.name = name
        self.item_type = item_type
        self.dmg = dmg
        self.res = res
        self.hp = hp
        self.en = en
        self.prc = prc
        self.slot = slot


class Weapon(Item):
    def __init__(self, name, dmg, res=0, hp=0, en=0, prc=0, slot=None):
        super().__init__(name, "weapon", dmg, res, hp, en, prc, slot)


weapons = {
    "melee": [
        Weapon("two handed axe", dmg=100, res=10, prc=-20, slot="2hand"),
        Weapon("two handed sword", dmg=80, res=15, prc=-15, slot="2hand"),
        Weapon("one handed axe", dmg=50, res=5, prc=-10, slot="hand"),
        Weapon("one handed sword", dmg=40, res=8, prc=-5, slot="hand"),
        Weapon("basic knife", dmg=15, prc=10, slot="hand"),
        Weapon("butterfly knife", dmg=20, prc=9, slot="hand"),
        Weapon("sock with rocks", dmg=10, prc=-5, slot="hand"),
        Weapon("blue lightsaber", dmg=70, res=-10, prc=10, slot="2hand"),
        Weapon("green lightsaber", dmg=70, res=-10, prc=10, slot="2hand"),
        Weapon("katana", dmg=40, prc=50, slot="2hand"),
        Weapon("spear", dmg=30, prc=40, slot="2hand"),
        Weapon("pointy shield", dmg=20, prc=-15, res=20, slot="hand"),
        Weapon("mace", dmg=50, prc=-25, slot="hand"),
        Weapon("lamp on a stick", dmg=10, res=5, slot="hand"),
        Weapon("shovel", dmg=30, res=10, slot="2hand"),
        Weapon("diamond sword", dmg=60, res=20, prc=-5, slot="hand"),
        Weapon("large cactuss", dmg=17, prc=-5, slot="hand"),
        Weapon("shit stick", dmg=10, slot="hand"),
        Weapon("whip", dmg=20, prc=15, slot="hand"),
        Weapon("very very big spoon", dmg=30, res=10, slot="2hand"),
        Weapon("heavy book", dmg=10, prc=-10, slot="hand"),
        Weapon("large army of living origami birds", dmg=19, prc=50),
        Weapon("guitar", dmg=18, slot="hand"),
        Weapon("razorblades glued to a glove", dmg=32, prc=25, slot="hand"),
        Weapon("big shield", dmg=20, res=30, prc=-5)
    ]
}
