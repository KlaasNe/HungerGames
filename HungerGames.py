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
        self.died_today = []

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
    def players_to_string(to_conv_list):
        str_list = []
        for player in to_conv_list:
            str_list.append(player.to_string())
        return ", ".join(str_list)

    @staticmethod
    def players_to_esc_string(to_conv_list):
        str_list = []
        for player in to_conv_list:
            str_list.append(player.to_esc_string())
        return ", ".join(str_list)

    def players_live(self):
        return len(self.alive)

    def pass_day(self):
        print("\n**Day {}**".format(self.day_count))
        event_count = 5
        for event in range(event_count):
            if not self.finished():
                self.do_2player_event()
            if not self.finished():
                self.do_1player_event()
        self.night = True

    def pass_night(self):
        print("\n**Night {}**".format(self.day_count))
        event_count = 2
        for event in range(event_count):
            if not self.finished():
                self.do_2player_event()
            if not self.finished():
                self.do_1player_event()
        self.day_count += 1
        self.night = False

    def do_1player_event(self):
        player = self.alive[randint(0, len(self.alive) - 1)]
        event_nr = randint(0, len(Events.onepl["yes"]) - 1)
        event = Events.onepl["yes"][event_nr]
        print("❕ " + event.description.format(player.to_esc_string()))
        player.health += event.self_hp_delta
        player.energy += event.self_energy_delta

        if player.health > player.max_health:
            player.health = player.max_health

        if player.is_dead():
            self.kill(None, player)

    def do_2player_event(self):
        player1, player2 = self.select_2_players()
        if self.same_team(player1, player2):
            event_nr = randint(0, len(Events.twopl["help"]) - 1)
            event = Events.twopl["help"][event_nr]
            print("🩹 " + event.description.format(player1.to_esc_string(), player2.to_esc_string()))
        else:
            event_nr = randint(0, len(Events.twopl["fight"]) - 1)
            event = Events.twopl["fight"][event_nr]
            print("⚔ " + event.description.format(player1.to_esc_string(), player2.to_esc_string()))
        player1.health += event.self_hp_delta
        player1.energy += event.self_energy_delta
        player2.health += event.other_hp_delta
        player2.energy += event.other_energy_delta
        if player1.health > player1.max_health:
            player1.health = player1.max_health
        if player2.health > player2.max_health:
            player2.health = player2.max_health

        if player1.is_dead():
            self.kill(player2, player1)

        if player2.is_dead():
            self.kill(player1, player2)

    def select_2_players(self):
        player1 = self.alive[randint(0, self.players_live() - 1)]
        player2 = self.alive[randint(0, self.players_live() - 1)]
        while player2.to_string() == player1.to_string():
            player2 = self.alive[randint(0, self.players_live() - 1)]
        return player1, player2

    def kill(self, killer, victim):
        self.dead.append(victim)
        self.alive.remove(victim)
        if killer is not None:
            killer.kills += 1
        print("> 💀 {} is now dead.".format(victim.to_esc_string()))

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
            print("{} has {} kills".format(player.to_esc_string(), str(player.kills)))

    def print_stats(self):
        print("\n```\n❤ HP UPDATE ❤")
        for player in self.alive:
            print("> {} has {} hp left.".format(player.to_string(), str(player.health)))
        print("```")


def main():
    game = HungerGame(get_int("Number of districts:\n> "), get_int("Teamsize:\n> "))
    print(".")
    while not game.finished():
        # enter()
        game.pass_day()
        if not game.finished():
            # enter()
            game.pass_night()
        game.print_stats()

    print("\n|| winner(s): {} ||".format(str(game.players_to_esc_string(game.alive))) + "\n")
    game.print_kill_counts()

    quit()


if __name__ == "__main__":
    main()
