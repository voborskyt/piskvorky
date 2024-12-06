from Player import Player
import random
import numpy as np
import os

class Manager:
    def __init__(self, number_of_games, SETTING):
        self.SETTING = SETTING
        self.engine = self.SETTING["Engine"]
        self.number_of_games = number_of_games
        self.total_number_of_games = number_of_games
        self.games = [{"on_move": Player(+1, self.engine),
                       "moved": Player(-1, self.engine),
                       "p1name": "p_" + str(i),
                       "p2name": "p_" + str(i),
                       "active": True, # zda hra je aktvní!!!
                       "p1_score": 0,
                       "p2_score": 0
                       } for i in range(number_of_games)]
        self.current_game = 0
        self.active_games_count = number_of_games  # počet aktivních her
        self.last_updated_game = 0
        self.list_of_winners = []
        self.generation = 1
        self.max_generation = SETTING["Generations"]
        self.iteration = 1
        self.info_text = "46843541354"
        self.PaMutation = SETTING["PaMutation"]
        self.number_of_last_mutated = 0
        self.playing = True

        # Nové statistické atributy
        self.current_game = 0
        self.active_games_count = number_of_games
        self.current_draws = 0
        self.current_wins = 0

        # Statistiky minulé generace
        self.previous_draws = 0
        self.previous_wins = 0

    def get_current_stats(self):
        """Vrátí statistiky aktuální generace"""
        return {
            "active_games": self.active_games_count,
            "draws": self.current_draws,
            "wins": self.current_wins
        }

    def get_previous_stats(self):
        """Vrátí statistiky minulé generace"""
        return {
            "draws": self.previous_draws,
            "wins": self.previous_wins
        }

    def setup_new_iteration(self, params):
        self.iteration += 1
        if len(params)>1:
            self.number_of_games = int(np.ceil(len(params)/2))
            # vytvorím remizové hry znova:
            self.games = []
            for i in range(int(np.ceil(len(params)/2))):
                self.games.append(
                    {"on_move": Player(+1, self.engine),
                     "moved": Player(-1, self.engine),
                     "p1name": "p_" + str(i),
                     "p2name": "p_" + str(i),
                     "active": True,  # zda hra je aktvní!!!
                     "p1_score": 0,
                     "p2_score": 0
                     }
                )
                # a přirazeni parametru + ochrana proti lichym počtum
                self.games[i]["on_move"].engine.set_parameters(params[i * 2])
                if (i * 2 +2) > len(params):
                    self.games[i]["moved"].engine.set_parameters(params[i * 2 - 1])
                else:
                    self.games[i]["moved"].engine.set_parameters(params[i * 2 + 1])

            self.current_game = 0
            self.last_updated_game = 0
            self.active_games_count = len(self.games)

    def setup_new_generation(self, list_of_winners):
        # Uložení statistik předchozí generace
        self.previous_draws = self.current_draws
        self.previous_wins = self.current_wins

        # Reset statistik pro novou generaci
        self.current_draws = 0
        self.current_wins = 0

        print("***************new_generation****************")
        self.current_game = 0
        self.active_games_count = self.total_number_of_games
        self.number_of_games = self.total_number_of_games
        self.last_updated_game = 0
        self.list_of_winners = []
        self.generation += 1
        self.iteration = 1
        self.games = [{"on_move": Player(+1, self.engine),
                       "moved": Player(-1, self.engine),
                       "p1name": "p_" + str(i),
                       "p2name": "p_" + str(i),
                       "active": True,  # zda hra je aktvní!!!
                       "p1_score": 0,
                       "p2_score": 0
                       } for i in range(self.number_of_games)]

        # přiřadím cyklciyk vsechny a pak od té délky budu mutovat ale prnvě zamíchám:
        for _ in range(5):
            list_of_winners += list_of_winners

        random.shuffle(list_of_winners)

        j = 0
        for i in range(self.number_of_games):
            self.games[i]["on_move"].engine.set_parameters(list_of_winners[j])
            self.games[i]["moved"].engine.set_parameters(list_of_winners[j+1])
            j += 2

        # Mutace, projdu kazdou desku a kazdého hráče
        self.number_of_last_mutated = 0
        for i in range(self.number_of_games):
            if random.random() < self.PaMutation:
                self.games[i]["on_move"].engine.mutate()
                self.number_of_last_mutated += 1
            if random.random() < self.PaMutation:
                self.games[i]["moved"].engine.mutate()
                self.number_of_last_mutated += 1

    ## final round
    def final_round(self, list_of_winners):
        print("***************new_generation****************")
        self.current_game = 0
        self.active_games_count = int(np.ceil(len(list_of_winners)/2))
        self.number_of_games = int(np.ceil(len(list_of_winners)/2))
        self.last_updated_game = 0
        self.list_of_winners = []
        self.iteration = 1
        self.games = [{"on_move": Player(+1, self.engine),
                       "moved": Player(-1, self.engine),
                       "p1name": "p_" + str(i),
                       "p2name": "p_" + str(i),
                       "active": True,  # zda hra je aktvní!!!
                       "p1_score": 0,
                       "p2_score": 0
                       } for i in range(self.number_of_games)]

        random.shuffle(list_of_winners)


        j = 0
        for i in range(self.number_of_games):
            self.games[i]["on_move"].engine.set_parameters(list_of_winners[j])
            if (j + 2) > len(list_of_winners):
                self.games[i]["moved"].engine.set_parameters(list_of_winners[j - 1])
            else:
                self.games[i]["moved"].engine.set_parameters(list_of_winners[j + 1])

            j += 2

        # Mutace, projdu kazdou desku a kazdého hráče
        self.number_of_last_mutated = 0

    def get_info_text(self):
        self.info_text = "Generace: " + str(self.generation)

        return self.info_text

    def get_id_last_updated_game(self):
        return self.last_updated_game

    def ith_board(self, ith):
        return self.games[ith]["moved"].get_board()

    def ith_names(self, ith, player: int):
        if player == 1:
            return self.games[ith]["p1name"]
        else:
            return self.games[ith]["p2name"]

    def check_game_end(self, ith):
        """Kontroluje, zda hra skončila a přidělí body"""
        if not self.games[ith]["active"]:
            return True

        board = self.games[ith]["moved"].get_board()

        # Kontrola výhry pro oba hráče
        if self.games[ith]["moved"].check_win(+1):  # Hráč 1 vyhrál
            self.games[ith]["p1_score"] += 1
            self.games[ith]["active"] = False
            self.active_games_count -= 1
            self.current_wins += 1
            return True

        if self.games[ith]["moved"].check_win(-1):  # Hráč 2 vyhrál
            self.games[ith]["p2_score"] += 1
            self.games[ith]["active"] = False
            self.active_games_count -= 1
            self.current_wins += 1
            return True

        # Kontrola remízy (plná deska)
        if not any(0 in row for row in board):
            self.games[ith]["p1_score"] += 0.5
            self.games[ith]["p2_score"] += 0.5
            self.games[ith]["active"] = False
            self.active_games_count -= 1
            self.current_draws += 1
            return True

        return False

    def ith_play(self, ith):
        if not self.games[ith]["active"]:
            return  # Přeskočí neaktivní hry

        self.games[ith]["on_move"].play(self.games[ith]["moved"].get_board())
        # Kontrola konce hry před výměnou hráčů
        if not self.check_game_end(ith):
            # Výměna hráčů pouze pokud hra neskončila
            self.games[ith]["on_move"], self.games[ith]["moved"] = self.games[ith]["moved"], self.games[ith]["on_move"]

    def ith_active(self, ith):
        return self.games[ith]["active"]

    def update(self):

        if self.active_games_count == 0:
            self.no_active_games() # metoda co se zavolá když nejsou aktivní hry!
            return False  # Signalizuje, že všechny hry skončily

        # Hledá další aktivní hru
        while not self.games[self.current_game]["active"]:
            self.current_game = (self.current_game + 1) % self.number_of_games
            if self.current_game == 0 and not any(game["active"] for game in self.games):
                return False

        self.last_updated_game = self.current_game # get last updated game id
        self.ith_play(self.current_game)
        self.current_game = (self.current_game + 1) % self.number_of_games
        return True

    def ith_get_scores(self, ith,  player: int):
        if player == 1:
            return self.games[ith]["p1_score"]
        else:
            return self.games[ith]["p2_score"]

    def get_winners(self):
        list_of_winners = []
        for ith in range(len(self.games)):
            if self.games[ith]["moved"].check_win(+1):  # Hráč 1 vyhrál
                list_of_winners.append(self.games[ith]["moved"].engine.get_parameters())

            if self.games[ith]["moved"].check_win(-1):  # Hráč 2 vyhrál
                list_of_winners.append(self.games[ith]["moved"].engine.get_parameters())
        return list_of_winners

    def get_remize(self):
        # Kontrola remízy (plná deska)
        list_of_remize = []
        for ith in range(len(self.games)):
            if self.games[ith]["p1_score"] == 0.5:
                list_of_remize.append(self.games[ith]["moved"].engine.get_parameters())
                list_of_remize.append(self.games[ith]["on_move"].engine.get_parameters())
        return list_of_remize

    def no_active_games(self):
        print("nula aktivních her!!!")
        print("winers: ")
        self.list_of_winners += self.get_winners()
        print(len(self.list_of_winners))
        print("remize: ")
        print(len(self.get_remize()))

        # prvne dohraji remizované kdyz není dostatek winnerů (min 10)
        if  len(self.list_of_winners) < 10 and self.generation < self.max_generation:
            self.setup_new_iteration(self.get_remize())
        elif self.generation < self.max_generation:
            self.setup_new_generation(self.list_of_winners)
        elif self.generation >= self.max_generation: # final round
            if(len(self.get_remize()) > 5):
                self.final_round(self.list_of_winners+self.get_remize())
            elif (len(self.list_of_winners) >= 2):
                self.final_round(self.list_of_winners)
            elif len(self.list_of_winners) == 0:
                self.final_round(self.get_remize())
            elif len(self.list_of_winners) == 1:
                # self.list_of_winners
                self.save_winner(self.list_of_winners[0])
                print("finished!")
                self.playing = False
            else:
                print("nejakej problem....")

    def save_winner(self, winner):
        """
                Uloží parametry enginu do souboru
                filename: cesta k souboru, kam se mají parametry uložit (např. 'engine_params.npz')
                """
        np.savez("temp_engines/winner_engine.npz", **winner)
        print(os.getcwd())
        return True

    def load_engine(self):
        return  np.load("temp_engines/winner_engine.npz")

    def button_save_game(self):
        self.save_winner(self.games[0]["moved"].engine.get_parameters())
