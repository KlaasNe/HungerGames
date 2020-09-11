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
    # "travel": {"energy_req": 10},
    # "eat": {"energy_delta": 30},
    # "taunt": {""}
}

two_player_actions = [
    # Event("{} kills {}.", other_hp_delta=-999),
    Event("{} liet noten zien aan {}.", other_hp_delta=-50),
    Event("{} laat heel harde scheet op {}.", other_hp_delta=-5),
    Event("{} niest op {}.", other_hp_delta=-1),
    Event("{} gooit steen in het gezicht van {}.", other_hp_delta=-30),
    Event("{} geeft {} dikke petsen in het gezicht.", other_hp_delta=-10),
    Event("{} legt ballen in de nek van {}.", other_hp_delta=-69),
    Event("Door het lopen van {} is de clapp van de asscheeks hoorbaar voor {} en meetbaar op de schaal van richter.", other_hp_delta=-25, self_hp_delta=-10),
    Event("{} wilt sneaky in de rug aanvallen, maar {} is sterker en doet een gekke John Cena move", self_hp_delta=-60, other_hp_delta=-15)
]

team_actions = {
    # "raid"
}


class Events:
    onepl = one_player_actions
    twopl = two_player_actions
    team = team_actions
