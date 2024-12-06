import numpy as np
import random

class Player:
    def __init__(self, my_mark, engine, fromfile=None):
        self.board = np.zeros((5, 5), dtype=int)
        self.my_mark = my_mark
        self.engine = engine()
        self.engine.initialize_parameters()
        if fromfile:
            self.engine.load_params(fromfile)

    def set_board(self, board):
        self.board = board.copy()# nejsem si jist zda tato kopie je opravdu nutna

    def get_board(self):
        return self.board.copy()

    def check_win(self, mark):
        """
        Kontroluje, zda hráč s danou značkou vyhrál
        Vrací True pokud našel 5 v řadě, jinak False
        """
        # Kontrola řádků
        for i in range(5):
            for j in range(2):  # Pouze do 4, protože potřebujeme 5 v řadě
                if all(self.board[i, j+k] == mark for k in range(4)):
                    return True

        # Kontrola sloupců
        for i in range(2):
            for j in range(5):
                if all(self.board[i+k, j] == mark for k in range(4)):
                    return True

        # Kontrola diagonál (zleva doprava)
        for i in range(2):
            for j in range(2):
                if all(self.board[i+k, j+k] == mark for k in range(4)):
                    return True

        # Kontrola diagonál (zprava doleva)
        for i in range(2):
            for j in range(3, 5):
                if all(self.board[i+k, j-k] == mark for k in range(4)):
                    return True

        return False

    def possible_moves(self):
        '''
        pokud hra začání uvazujeme jen stredové tahy
        pokud hra je v proudu tak jen tahy max do vzdálenosti 2 ého pole od aktuálních tahů!!!
        '''
        if np.all(self.board == 0):
            return [random.choice([
                    (1, 1), (1, 2), (1, 3),
                    (2, 1), (2, 2), (2, 3),
                    (3, 1), (3, 2), (3, 3)
                    ]),]

        moves = set()
        occupied = np.where(self.board != 0)

        # kandidátské tahy
        for i, j in zip(occupied[0], occupied[1]):
            for di in range(-2, 3):# procházím jen okolí 2 bunek okolo tahu
                for dj in range(-2, 3):# procházím jen okolí 2 bunek okolo tahu
                    ni, nj = i + di, j + dj
                    if (0 <= ni < 5 and 0 <= nj < 5 and
                            self.board[ni, nj] == 0):
                        moves.add((ni, nj))

        return list(moves)

    def game_evaluation(self):
        # Nejdřív zkontrolujeme výhru/prohru
        if self.check_win(self.my_mark):
            return float('inf')  # Výhra
        if self.check_win(-self.my_mark):
            return float('-inf')  # Prohra

        # zde uz vyuzití prímo enginu:
        evaluation = self.engine.evaluate_board(self.board)

        return evaluation if self.my_mark == 1 else -evaluation

    def alpha_beta_move(self, depth, alpha=-float('inf'), beta=float('inf'), is_maximizing=True):
        # Nejdřív zkontrolujeme, zda pozice není výherní/proherní
        if self.check_win(self.my_mark):
            return float('inf'), None
        if self.check_win(-self.my_mark):
            return float('-inf'), None

        if depth == 0:
            return self.game_evaluation(), None

        moves = self.possible_moves()
        if not moves:
            return self.game_evaluation(), None

        best_move = random.choice(moves)

        if is_maximizing:
            max_eval = -float('inf')
            for move in moves:
                self.board[move] = self.my_mark
                eval, _ = self.alpha_beta_move(depth - 1, alpha, beta, False)
                self.board[move] = 0

                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                elif eval == max_eval and random.random() < 0.5:
                    best_move = move

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                self.board[move] = -self.my_mark
                eval, _ = self.alpha_beta_move(depth - 1, alpha, beta, True)
                self.board[move] = 0

                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                elif eval == min_eval and random.random() < 0.5:
                    best_move = move

                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def make_move(self, depth=2):
        _, best_move = self.alpha_beta_move(depth)
        if best_move:
            self.board[best_move] = self.my_mark
            return best_move
        return None

    def play(self, board):
        self.board = board.copy()
        move = self.make_move(depth=2) # procházím jen 2 tahy - můj tah, reakci a mou reakci
        if move:
            self.board[move] = self.my_mark
        return None



if __name__ == "__main__":
    print(".................tests....................")
    CurrentEngine = Engine()
    A = Player(-1, CurrentEngine )
    B = Player(+1, CurrentEngine )

    for _ in range(10):
        A.play(B.get_board())
        B.play(A.get_board())

    print(A.get_board())
    print("end test")