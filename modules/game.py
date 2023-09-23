import _helper as helper
import strategies

from _debuggable import Debuggable
from player import Player

import random


def flip(action):
    return 0 if action == 1 else 1


class Game(Debuggable):
    def __init__(self,
                 player_1: Player = Player(),
                 player_2: Player = Player(),
                 rounds: int = 0,
                 error_rate: float = .0,
                 debug: bool = False):

        super().__init__(debug=debug)

        self.player_1 = player_1
        self.player_2 = player_2

        self.moves_1 = []
        self.moves_2 = []

        self.scores_1 = []
        self.scores_2 = []

        self.rounds = rounds
        self.error_rate = error_rate

    def should_flip(self):
        return random.random() < self.error_rate

    def reset(self):
        self.moves_1 = []
        self.moves_2 = []

        self.scores_1 = []
        self.scores_2 = []

    def go(self):
        if self.debug:
            helper.print_game_title(self)
        for round_number in range(1 , self.rounds + 1):
            thoughts_1, decided_action_1 = self.player_1.decide(self.moves_1, self.moves_2)
            thoughts_2, decided_action_2 = self.player_2.decide(self.moves_2, self.moves_1)

            actual_action_1 = flip(decided_action_1) if self.should_flip() else decided_action_1
            actual_action_2 = flip(decided_action_2) if self.should_flip() else decided_action_2

            self.moves_1.append(actual_action_1)
            self.moves_2.append(actual_action_2)

            self.player_1.update_score(actual_action_1, actual_action_2)
            self.player_2.update_score(actual_action_2, actual_action_1)

            self.scores_1.append(self.player_1.score)
            self.scores_2.append(self.player_2.score)

            round_data = {k: str(v) for k, v in {
                'round number': round_number,
                'thoughts 1': thoughts_1,
                'decided 1': decided_action_1,
                'actual 1': actual_action_1,
                'score 1': self.player_1.score,
                'thoughts 2': thoughts_2,
                'decided 2': decided_action_2,
                'actual 2': actual_action_2,
                'score 2': self.player_2.score
            }.items()}
            if self.debug:
                helper.print_round_outcome(self, round_data)
        if self.debug:
            helper.visualize_game_outcome(self.player_1.strategy.name,
                                          self.scores_1,
                                          self.player_2.strategy.name,
                                          self.scores_2)

    def report_scores(self):
        return self.player_1.score, self.player_2.score


if __name__ == '__main__':
    player_1 = Player(strategy=strategies.Random(ratio=.95))
    player_2 = Player(strategy=strategies.Copycat(change_action_after=2))

    game = Game(player_1=player_1, player_2=player_2, rounds=50, debug=True)
    game.reset()
    game.go()

    print(player_2)