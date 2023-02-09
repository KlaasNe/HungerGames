from random import shuffle

from Events import Events
from HelpFunctions import *
from Player import Player
from Team import Team
import parser as inputs


class HungerGame:

    def __init__(self, distr, teamsize, teamwin_allowed=True, debug=False):
        self.distr = distr
        self.teamsize = teamsize
        self.max_team_size = teamsize * 2
        self.teamwin_allowed = teamwin_allowed
        self.teams = set()
        self.day_count = 1
        self.night = False
        self.alive = self.init_players(debug=debug)
        self.dead = []
        self.died_today = []
        self.environmental_kills = 0
        self.betrayals = 0
        self.alliances_formed = 0
        self.ally_dmg_prevent = 0
        self.alliances_broken = 0
        self.damage_blocked = 0

    def init_players(self, debug=False):
        players = []
        if debug:
            for player_nr in range(self.distr * self.teamsize):
                player_name = str(player_nr // self.teamsize + 1) + "-" + str(player_nr % self.teamsize + 1)
                player_gender = "x"  # input("Gender tribute (m/f/x)\n> ")
                team_nr = player_nr // self.teamsize + 1
                players.append(Player(player_name, player_gender, team_nr))
                curr_team = Team(team_nr)
                self.teams.add(curr_team)
        else:
            team_name = ""
            victory_msg = ""
            curr_team = None
            for player_nr in range(self.distr * self.teamsize):
                if player_nr % self.teamsize == 0:
                    team_name = input("Teamname: ")
                    victory_msg = input("Victory message: ")
                curr_team = Team(team_name)
                self.teams.add(curr_team)
                player_name = input("Name tribute #{}\n> ".format(player_nr + 1))
                player_gender = "x"  # input("Gender tribute (m/f/x)\n> ")
                player = Player(player_name, player_gender, team_name, victory_msg)
                players.append(player)
                curr_team.add_player(player)
        return players

    def get_team(self, team_name):
        for team in self.teams:
            if team.name == team_name:
                return team
        return None

    def get_team_player_names(self, team_name):
        return [player.name for player in self.get_team(team_name).players]

    def teams_alive(self):
        alive = 0
        for team in self.teams:
            if team.size_alive() > 0:
                alive += 1
        return alive

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
            str_list.append(player.to_esc_str())
        return ", ".join(str_list)

    def get_nb_players_alive(self):
        return len(self.alive)

    def pass_day(self):
        print("\n**D A Y  {}**".format(self.day_count))
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
        print("\n**N I G H T  {}**".format(self.day_count))
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
            print("❔ **{}** found an item: _{}_".format(player.to_esc_str(), item.name))
        else:
            event_nr = randint(0, len(Events.onepl.MISC.value) - 1)
            event = Events.onepl.MISC.value[event_nr]
            print("❕ " + event.description.format(player.to_esc_str()))
            player.health += event.self_hp_delta
            player.energy += event.self_energy_delta

            if player.health > player.max_health:
                player.health = player.max_health

            if player.is_dead():
                self.kill(None, player)

    def do_2player_event(self):
        player1, player2 = self.select_2_players()
        if player1.same_team(player2):
            self_dmg, other_dmg = HungerGame.do_2player_same_team_event(player1, player2)
        else:
            self_dmg, other_dmg = self.do_2player_diff_team_event(player1, player2)
        self.do_dmg(player1, player2, self_dmg, other_dmg)

    @staticmethod
    def do_2player_same_team_event(p1, p2):
        event_nr = randint(0, len(Events.twopl.HELP.value) - 1)
        event = Events.twopl.HELP.value[event_nr]
        self_dmg, other_dmg = event.self_hp_delta, event.other_hp_delta
        print("🩹 " + event.description.format(p1.to_esc_str(), p2.to_esc_str()))
        return self_dmg, other_dmg

    def do_2player_attack_event(self, p1, p2):
        if self.get_team(p1.team_name).has_ally(self.get_team(p2.team_name)):
            if randint(1, 3) != 1:
                if self.teams_alive() > 2:
                    while self.get_team(p2.team_name).has_ally(p1):
                        p2 = self.select_2_players()[0]
                    self.ally_dmg_prevent += 1

        if p1.has_weapon():
            weapon = p1.get_weapon()[0]
            other_dmg = -p1.get_dmg()
            self_dmg = 0
            combat_txt = "⚔ " + "**{}** hits **{}** with a _{}_."
            print(combat_txt.format(p1.to_esc_str(), p2.to_esc_str(), weapon.name))
        else:
            SLAP_DMG = -4
            other_punches, self_punches = randint(3, 6), randint(1, 4)
            other_dmg, self_dmg = SLAP_DMG * other_punches, SLAP_DMG * self_punches
            combat_txt = "👊 " + "**{}** hits **{}** {} times and gets hit {} times themselves."
            print(combat_txt.format(p1.to_esc_str(), p2.to_esc_str(), other_punches, self_punches))

        if self.get_team(p1.team_name).has_ally(self.get_team(p2.team_name)):
            tn1, tn2 = p1.team_name, p2.team_name
            t1, t2 = self.get_team(tn1), self.get_team(tn2)
            t1.remove_ally(t2)
            t2.remove_ally(t1)
            event = Events.twopl.RELATIONS.value[1]
            event_txt = event.description.format(tn1, tn2)
            print(event_txt)
            self.alliances_broken += 1
        return self_dmg, other_dmg

    def do_2player_team_alter_event(self, p1, p2):
        event_chooser = randint(1, 3)
        tn1, tn2 = p1.team_name, p2.team_name
        t1, t2 = self.get_team(tn1), self.get_team(tn2)
        if t2.size() < self.max_team_size and event_chooser == 1:
            t2_players = t2.get_alive()
            event = Events.twopl.RELATIONS.value[2]
            event_txt = event.description.format(p1.name, tn1, ', '.join(str(p) for p in t2_players), tn2)
            # betrayal
            p1.team_name = p2.team_name
            t1.remove_player(p1)
            t2.add_player(p1)
            print(event_txt)
            self.betrayals += 1
        else:
            # change ally mode
            if t1.has_ally(t2):
                t1.remove_ally(t2)
                t2.remove_ally(t1)
                event = Events.twopl.RELATIONS.value[1]
                self.alliances_broken += 1
            else:
                t1.add_ally(t2)
                t2.add_ally(t1)
                event = Events.twopl.RELATIONS.value[0]
                self.alliances_formed += 1
            event_txt = event.description.format(tn1, tn2)
            print(event_txt)

    def do_2player_diff_team_event(self, p1, p2):
        event_chooser = randint(1, 12)
        if event_chooser == 1:
            self.do_2player_team_alter_event(p1, p2)
            return 0, 0
        else:
            return self.do_2player_attack_event(p1, p2)

    def do_dmg(self, player1, player2, dmg1, dmg2):
        player1.take_dmg(dmg1)
        player2.take_dmg(dmg2)
        if player1.is_dead():
            self.kill(player2, player1)
        if player2.is_dead():
            self.kill(player1, player2)

    def select_2_players(self):
        player1 = self.alive[randint(0, self.get_nb_players_alive() - 1)]
        player2 = self.alive[randint(0, self.get_nb_players_alive() - 1)]
        while player2.to_string() == player1.to_string():
            player2 = self.alive[randint(0, self.get_nb_players_alive() - 1)]
        return player1, player2

    def check_traitor(self, team_name):
        team = self.get_team(team_name)
        if team.size_alive() == 1:
            last_of_team = team.get_alive()[0]
            last_origin_team = last_of_team.origin_team
            if last_of_team.team_name != last_origin_team and self.get_team(last_origin_team).size_alive() == 0:
                event = Events.twopl.RELATIONS.value[3]
                event_txt = event.description.format(team_name, last_of_team.name)
                print(event_txt)

    def kill(self, killer, victim):
        self.check_traitor(victim.team_name)
        self.dead.append(victim)
        self.alive.remove(victim)
        if killer is not None:
            killer.kills += 1
            print("> 💀 {} is now  d e a d.".format(victim.to_esc_str()))
        else:
            self.environmental_kills += 1
            print("> ☠ {} is now  d e a d.".format(victim.to_esc_str()))

    def run_to_mid(self):
        def random_mid_plr():
            att = 0
            rand_mid_plr = list(mid_players)[randint(0, len(mid_players) - 1)]
            while (rand_mid_plr.is_dead() or rand_mid_plr == player or player.same_team(rand_mid_plr)) and att < 99:
                rand_mid_plr = list(mid_players)[randint(0, len(mid_players) - 1)]
                att += 1
            return rand_mid_plr

        def attack_mid_plr(attacker):
            if len(mid_players) > 1:
                random_mid = random_mid_plr()
                self.attack(attacker, random_mid)
                if random_mid.is_dead():
                    self.kill(attacker, random_mid)

        print("\n**BEGINNING**")
        mid_players = set()
        for player in self.alive:
            if coinflip():
                mid_players.add(player)
        for player in mid_players:
            if not player.is_dead():
                player.give_weapon()
                txt = "❔ **{}** runs towards the middle and grabs a _{}_"
                print(txt.format(player.to_esc_str(), player.get_weapon()[0].name))
                attack_mid_plr(player)

    def attack(self, attacker, defender):
        weapon = attacker.get_weapon()[0]
        atk_txt = "⚔ **{}** hits **{}** with a _{}_."
        print(atk_txt.format(attacker.to_esc_str(), defender.to_esc_str(), weapon.name))
        if defender.has_weapon():
            def_weapon = defender.get_weapon()[0]
            def_txt = "> 🛡️ **{}** tries to counter the attack of **{}** with their _{}_, blocking {} damage."
            print(
                def_txt.format(defender.to_esc_str(), attacker.to_esc_str(), def_weapon.name, str(defender.get_res())))
            self.damage_blocked += defender.get_res()
        defender.take_attack(attacker.get_dmg())

    def finished(self):
        if len(self.alive) <= 1:
            return True
        elif self.teamwin_allowed:
            if all(self.alive[i].same_team(self.alive[i + 1]) for i in range(0, len(self.alive) - 1)):
                return True
        else:
            return False

    def print_kill_counts(self):
        players = self.alive + self.dead
        players.sort(key=lambda plyr: plyr.kills, reverse=True)
        for player in players:
            print("{} has {} kills".format(player.to_esc_str(), str(player.kills)))
        print("and... {} people killed because of their own stupidity.".format(self.environmental_kills))

    def print_stats(self):
        print("\n```\n❤ HP UPDATE ❤")
        for player in self.alive:
            print("> {} ({}) has {} hp left.".format(player.to_string(), player.team_name, str(player.health)))
        print("```")

    def print_teams(self):
        print("`Welcome to the {} teams.`\n".format(str(self.get_nb_players_alive() // self.teamsize)))
        for player_nr in range(0, self.get_nb_players_alive(), self.teamsize):
            print("\n")
            print("**" + str(self.alive[player_nr].team_name) + "**")
            for add in range(self.teamsize):
                print("> " + self.alive[player_nr + add].to_string())

    def print_fun_info(self):
        print("\nDamage blocked: {}\nAlliances formed: {}\nAlliances broken: {}\nDamage prevented by alliances: {}\nBetrayals: {}".format(
            self.damage_blocked, self.alliances_formed, self.alliances_broken, self.ally_dmg_prevent, self.betrayals
        ))


def main():
    parser = inputs.make_parser()
    args = parser.parse_args()
    game = HungerGame(get_int("Number of districts:\n> "), get_int("Teamsize:\n> "), debug=args.debug)
    print(".")
    game.print_teams()
    game.run_to_mid()
    while not game.finished():
        game.pass_day()
        if not game.finished():
            game.pass_night()
        game.print_stats()

    game.print_kill_counts()
    game.print_fun_info()
    print("\n\nThe games have finally ended after {} days...".format(str(game.day_count)))
    winners_msg = "\n|| winner(s): **{}** fighting for {}; '_{}_'||"
    winners = str(game.players_to_esc_string(game.alive))
    if game.alive:
        last_team = game.alive[0].team_name
        print(winners_msg.format(winners, last_team, game.get_team(last_team).victory_msg))
    else:
        print("Everyone died...")

    quit()


if __name__ == "__main__":
    main()
