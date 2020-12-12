class Event:

    def __init__(self, description, hp_req=0, self_hp_delta=0, other_hp_delta=0, energy_req=0, self_energy_delta=0, other_energy_delta=0, kills_req=0):
        self.description = description
        self.hp_req = hp_req
        self.self_hp_delta = self_hp_delta
        self.other_hp_delta = other_hp_delta
        self.energy_req = energy_req
        self.self_energy_delta = self_energy_delta
        self.other_energy_delta = other_energy_delta
        self.kills_req = kills_req


one_player_actions = {
    "yes": [
        Event("{} got spanked by Santa.", self_hp_delta=-12),
        Event("{} had snow fallen on them from a tree.", self_hp_delta=-8),
        Event("{} eats some candy.", self_hp_delta=8),
        Event("{} realizes they've been naughty", self_hp_delta=-5),
        Event("{} touches a magical reindeer.", self_hp_delta=15),
        Event("{} gets attacked by elves.", self_hp_delta=-2),
        Event("{} tries lighting a fire and succeeds.", self_hp_delta=11)
    ]
}

two_player_actions = {
    "fight": [
        # Event("{} kills {}.", other_hp_delta=-999),
        Event("{} tries to attack from behind, but {} is stronger and does a sick John Cena move.", self_hp_delta=-30, other_hp_delta=-10),
        Event("{} throws a big rock in {}'s face.", other_hp_delta=-20),
        Event("{} throws a pebble in {}'s face.", other_hp_delta=-10),
        Event("{} slaps {} really hard.", other_hp_delta=-5, self_hp_delta=-2),
        Event("{} headbutts {}'s face.", other_hp_delta=-20, self_hp_delta=-10),
        Event("{} yells 'KAMEHAMEHAAA' really loud and shoots a large beam at {}.", other_hp_delta=-100),
        Event("{} bites {} and sucks some of their blood.", other_hp_delta=-15, self_hp_delta=15),
        Event("{} kicks {}'s kneecaps.", other_hp_delta=-15)
    ],
    "help": [
        Event("{} gives {} some medical cookies.", other_hp_delta=10),
        Event("{} gives {} a massage with marzipan.", other_hp_delta=5),
        Event("{} and {} take a bath together, in a hot water pond. There was also a reindeer in the pond.", self_hp_delta=15, other_hp_delta=15)
        # Event("{} feeds {}.", other_energy_delta=60, self_energy_delta=60)
    ],
    "misc": [
        Event("undefined event"),
        # Event("Steal item")
    ]
}


class Events:
    onepl = one_player_actions
    twopl = two_player_actions
