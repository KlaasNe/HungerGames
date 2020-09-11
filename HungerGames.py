from random import randint

from HelpFunctions import *
from Player import Player
from Events import Events


class HungerGame:

    def __init__(self, distr, teamsize, teamwin_allowed=True):
        self.distr = distr
        self.teamsize = teamsize
        self.teamwin_allowed = teamwin_allowed
        self.day_count = 1
        self.night = False
        self.alive = self.init_players()
        self.dead = []

    def init_players(self):
        players = []
        for player_nr in range(self.distr * self.teamsize):
            player_name = input("Name tribute #{}\n> ".format(player_nr + 1))
            player_gender = "x"  # input("Gender tribute (m/f/x)\n> ")
            tribute_nr = player_nr // self.teamsize + 1
            players.append(Player(player_name, player_gender, tribute_nr))
        return players

    @staticmethod
    def same_team(player1, player2):
        return player1.team_name == player2.team_name

    @staticmethod
    def players_to_string(list):
        str_list = ""
        for player in list:
            str_list += (player.to_string())
        return str_list

    def players_live(self):
        return len(self.alive)

    def pass_day(self):
        print("\n**Day {}**".format(self.day_count))
        self.do_2player_event()
        if not self.finished():
            self.do_2player_event()
        self.night = True

    def pass_night(self):
        print("\n**Night {}**".format(self.day_count))
        self.do_2player_event()
        self.day_count += 1
        self.night = False

    def do_2player_event(self):
        event_nr = randint(0, len(Events.twopl) - 1)
        event = Events.twopl[event_nr]
        player1, player2 = self.select_2_players()
        player1.health += event.self_hp_delta
        player1.energy += event.self_energy_delta
        player2.health += event.other_hp_delta
        player2.energy += event.other_energy_delta
        print(event.description.format(player1.to_string(), player2.to_string()))

        if player1.is_dead():
            self.kill(player2, player1)

        if player2.is_dead():
            self.kill(player1, player2)

    def select_2_players(self):
        player1 = self.alive[randint(0, self.players_live() - 1)]
        player2 = self.alive[randint(0, self.players_live() - 1)]
        while player2.to_string() == player1.to_string() or self.same_team(player1, player2):
            player2 = self.alive[randint(0, self.players_live() - 1)]
        return player1, player2

    def kill(self, killer, victim):
        self.dead.append(victim)
        self.alive.remove(victim)
        killer.kills += 1
        print("> {} is now dead. 💀".format(victim.to_string()))

    def finished(self):
        if len(self.alive) <= 1:
            return True
        elif self.teamwin_allowed:
            if len(self.alive) <= self.teamsize and self.same_team(self.alive[0], self.alive[1]):
                return True
        else:
            return False

    def print_kill_counts(self):
        players = self.alive + self.dead
        players.sort(key=lambda plyr: plyr.kills, reverse=True)
        for player in players:
            print("{} has {} kills".format(player.to_string(), str(player.kills)))


def main():
    game = HungerGame(get_int("Number of districts:\n> "), get_int("Teamsize:\n> "))
    print(".")
    while not game.finished():
        # enter()
        game.pass_day()
        if not game.finished():
            # enter()
            game.pass_night()

    print("\n|| winner(s): {} ||".format(str(game.players_to_string(game.alive))) + "\n")
    game.print_kill_counts()

    quit()


if __name__ == "__main__":
    main()
