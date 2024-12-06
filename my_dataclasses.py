from dataclasses import dataclass
import numpy as np

@dataclass
class data_game_class:
    board: np.array
    player1name: str = ""
    player2name: str = ""
    player1score: int = 0
    player2score: int = 0
    active: bool = True