from pprint import pprint

import app.main.scores as scores
from config import game_levels
import time


def test_score():
    test_level_list = []
    for game in game_levels.keys():
        scores.parse_key_list(test_level_list)
        for i in range(1, game_levels[game]+1):
            test_level_list.append(f'{game}{i}')
            time.sleep(0.5)
            scores.parse_key_list(test_level_list)
    pprint(scores.score_dict)

if __name__ == '__main__':
    test_score()