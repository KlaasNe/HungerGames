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
        if self.distr * self.teamsize < 99:
            team_name = ""
            victory_msg = ""
            for player_nr in range(self.distr * self.teamsize):
                if player_nr % self.teamsize == 0:
                    team_name = input("Teamname: ")
                    victory_msg = input("Victory message: ")
                player_name = input("Name tribute #{}\n> ".format(player_nr + 1))
                player_gender = "x"  # input("Gender tribute (m/f/x)\n> ")
                players.append(Player(player_name, player_gender, team_name, victory_msg))
        else:
            for player_nr in range(self.distr * self.teamsize):
                player_name = str(player_nr)
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
        event_count = 16
        event = 0
        while event < event_count - 1:
            if not self.finished():
                self.do_2player_event()
                event += 1
            else:
                event = event_count
            if not self.finished() and event % 2 == 0:
                self.do_1player_event()
                event += 1
        self.night = True

    def pass_night(self):
        print("\n**Night {}**".format(self.day_count))
        event_count = 8
        event = 0
        while event < event_count - 1:
            if not self.finished():
                self.do_2player_event()
                event += 1
            else:
                event = event_count
            if not self.finished() and event % 2 == 0:
                self.do_1player_event()
                event += 1
        self.day_count += 1
        self.night = False

    def do_1player_event(self):
        player = self.alive[randint(0, len(self.alive) - 1)]
        if randint(0, 2) == 0:
            player.give_weapon()
            item = player.get_weapon()[0]
            print("❔ {} found an item: _{}_".format(player.to_esc_string(), item.name))
        else:
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
            self_dmg, other_dmg = event.self_hp_delta, event.other_hp_delta
            print("🩹 " + event.description.format(player1.to_esc_string(), player2.to_esc_string()))
        elif randint(0, 2) == 0:
            event_nr = randint(0, len(Events.twopl["fight"]) - 1)
            event = Events.twopl["fight"][event_nr]
            self_dmg, other_dmg = event.self_hp_delta, event.other_hp_delta
            print("🥊 " + event.description.format(player1.to_esc_string(), player2.to_esc_string()))
        else:
            weapon = player1.get_weapon()
            if weapon:
                weapon = player1.get_weapon()[0]
                other_dmg = -player1.get_dmg()
                self_dmg = 0
                combat_txt = "⚔ " + "{} hits {} with a _{}_."
                print(combat_txt.format(player1.to_esc_string(), player2.to_esc_string(), weapon.name))
            else:
                slap_dmg = -4
                other_punches, self_punches = randint(3, 6), randint(1, 4)
                other_dmg, self_dmg = slap_dmg * other_punches, slap_dmg * self_punches
                combat_txt = "👊 " + "{} hits {} {} times and gets hit {} times themselves."
                print(combat_txt.format(player1.to_esc_string(), player2.to_esc_string(), other_punches, self_punches))

        self.do_dmg(player1, player2, self_dmg, other_dmg)

    def do_dmg(self, player1, player2, dmg1, dmg2):
        player1.take_dmg(dmg1)
        player2.take_dmg(dmg2)
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
            print("> 💀 {} is now  d e a d.".format(victim.to_esc_string()))
        else:
            print("> ☠ {} is now  d e a d.".format(victim.to_esc_string()))

    def run_to_mid(self):
        ...

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

    def print_teams(self):
        print("`Welcome to the {} teams.`\n".format(str(self.players_live()//self.teamsize)))
        for player_nr in range(0, self.players_live(), self.teamsize):
            print("\n")
            print("**" + str(self.alive[player_nr].team_name) + "**")
            for add in range(self.teamsize):
                print("> " + self.alive[player_nr + add].to_string())


def main():
    game = HungerGame(get_int("Number of districts:\n> "), get_int("Teamsize:\n> "))
    print(".")
    game.print_teams()
    while not game.finished():
        # enter()
        game.pass_day()
        if not game.finished():
            # enter()
            game.pass_night()
        game.print_stats()

    game.print_kill_counts()
    print("\nThe games have finally ended after {} days...".format(str(game.day_count)))
    winners_msg = "\n|| winner(s): {} from {}; '{}'||"
    winners = str(game.players_to_esc_string(game.alive))
    if game.alive:
        print(winners_msg.format(winners, game.alive[0].team_name, game.alive[0].victory_msg))
    else:
        print("Everyone died...")

    quit()


if __name__ == "__main__":
    main()
