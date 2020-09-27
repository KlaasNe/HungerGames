class Item:
    def __init__(self, name, dmg=0, res=0, hp=0, en=0, prc=0, slot=None):
        self.name = name
        self.dmg = dmg
        self.res = res
        self.hp = hp
        self.en = en
        self.prc = prc
        self.slot = slot


weapon_items = {
    "melee": [
        Item("two handed axe", dmg=100, res=10, prc=-20, slot="2hand"),
        Item("two handed sword", dmg=80, res=15, prc=-15, slot="2hand"),
        Item("one handed axe", dmg=50, res=5, prc=-10, slot="hand"),
        Item("one handed sword", dmg=40, res=8, prc=-5, slot="hand"),
        Item("basic knife", dmg=15, prc=10, slot="hand"),
        Item("butterfly knife", dmg=20, prc=9, slot="hand"),
        Item("sock with rocks", dmg=10, prc=-5, slot="hand"),
        Item("blue lightsaber", dmg=70, res=-10, prc=10, slot="2hand"),
        Item("green lightsaber", dmg=70, res=-10, prc=10, slot="2hand"),
        Item("katana", dmg=40, prc=50, slot="2hand"),
        Item("spear", dmg=30, prc=40, slot="2hand"),
        Item("pointy shield", dmg=20, prc=-15, res=20, slot="hand"),
        Item("mace", dmg=50, prc=-25, slot="hand"),
        Item("lamp on a stick", dmg=10, res=5, slot="hand"),
        Item("shovel", dmg=30, res=10, slot="2hand"),
        Item("diamond sword", dmg=60, res=20, prc=-5, slot="hand"),
        Item("large cactuss", dmg=17, prc=-5, slot="hand"),
        Item("shit stick", dmg=10, slot="hand"),
        Item("whip", dmg=20, prc=15, slot="hand"),
        Item("very very big spoon", dmg=30, res=10, slot="2hand"),
        Item("heavy book", dmg=10, prc=-10, slot="hand"),
        Item("large army of living origami birds", dmg=19, prc=50),
        Item("guitar", dmg=18, slot="hand"),
        Item("razorblades glued to a glove", dmg=32, prc=25, slot="hand")
    ]
}

defence_items = [
    Item("piece of wood", res=2, slot="hand"),
    Item("fridge door", res=15, slot="2hand"),
    Item("gucci shades", res=2, prc=20, slot="head"),
    Item("medic helmet", res=10, slot="head")
]


class Items:
    weapons = weapon_items
