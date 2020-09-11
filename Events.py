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
    "yes":[
        Event("{} falls in a pit.", self_hp_delta=-35),
        Event("{} didn't see a branch and ran into it.", self_hp_delta=-20),
        Event("{} rests for a bit.", self_hp_delta=12),
        Event("{} is even aan het chillen met de homies.", self_hp_delta=7),
        Event("{} cries of despair.", self_hp_delta=-25)
    ]
}

two_player_actions = {
    "fight": [
        # Event("{} kills {}.", other_hp_delta=-999),
        Event("{} liet noten zien aan {}.", other_hp_delta=-69),
        Event("{} laat heel harde scheet op {}.", other_hp_delta=-30),
        Event("{} stampt op {}.", other_hp_delta=-70),
        Event("{} gooit steen in het gezicht van {}.", other_hp_delta=-80),
        Event("{} geeft {} dikke petsen in het gezicht.", other_hp_delta=-41),
        Event("{} legt ballen in de nek van {}.", other_hp_delta=-69),
        Event("Door het lopen van {} is de clapp van de asscheeks hoorbaar voor {} en meetbaar op de schaal van richter.", other_hp_delta=-45, self_hp_delta=-20),
        Event("{} wilt sneaky in de rug aanvallen, maar {} is sterker en doet een gekke John Cena move.", self_hp_delta=-60, other_hp_delta=-15),
        Event("{} pist tegen de benen van {}.", other_hp_delta=-50)
    ],
    "help": [
        Event("{} gives {} some medical herbs.", other_hp_delta=25),
        Event("{} gives {} a massage.", other_hp_delta=10),
        Event("{} and {} take a bath in a hot water pond.", other_hp_delta=40)
        # Event("{} feeds {}.", other_energy_delta=60, self_energy_delta=60)
    ]
}

team_actions = {
    # "raid"
}


class Events:
    onepl = one_player_actions
    twopl = two_player_actions
    team = team_actions
