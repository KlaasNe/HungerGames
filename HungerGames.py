from random import randint

from HelpFunctions import *
from Player import Player


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
        for player_nr in range(self.distr * 2):
            player_name = input("Name tribute #{}\n> ".format(player_nr + 1))
            player_gender = input("Gender tribute (m/f/x)\n> ")
            tribute_nr = player_nr // 2 + 1
            players.append(Player(player_name, player_gender, tribute_nr))
        return players

    @staticmethod
    def same_team(player1, player2):
        return player1.team_name == player2.team_name

    def players_live(self):
        return len(self.alive)

    def pass_day(self):
        print("**Day {}**\n".format(self.day_count))
        self.night = True

    def pass_night(self):
        print("**Night {}**\n".format(self.day_count))
        print("Everyone falls asleep")
        self.day_count += 1
        self.night = False

    def kill(self, killer, victim):
        # plnr1 = randint(0, self.players_live() - 1)
        # plnr2 = randint(0, self.players_live() - 1)
        # while plnr2 == plnr1:
        #     plnr2 = randint(0, self.players_live() - 1)
        # player1, player2 = self.alive[plnr1], self.alive[plnr2]
        print("{} kills {}.".format(killer.to_string(), victim.to_string()))
        self.dead.append(victim)
        self.alive.pop(victim)
        killer.kills += 1

    def finished(self):
        if len(self.alive) <= 1:
            return True
        elif self.teamwin_allowed:
            if len(self.alive) <= self.teamsize and self.same_team(self.alive[0], self.alive[1]):
                return True
        else:
            return False


def main():
    game = HungerGame(get_int("Number of districts:\n> "), get_int("Teamsize:\n> "))
    while not game.finished():
        enter()
        game.pass_day()
        enter()
        game.pass_night()


if __name__ == "__main__":
    main()
