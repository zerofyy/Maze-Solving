import random

from utils.algorithms.base_algorithm import BaseAlgorithmSequential
from utils.maze_generator import Maze


class WandererSequential(BaseAlgorithmSequential):
    """
    Simple sequential algorithm that explores the maze through random moves.

    It has two modes:
        - default: Makes random moves while avoiding previously visited spaces as much as possible.
        - confused: Makes random moves without keeping track of visited spaces.
    """

    confused: bool = None
    visited_spaces_weights: dict[tuple[int, int], int] = None


    def setup(self, maze: Maze, confused: bool = False) -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the Maze class.
            confused: Whether the wanderer is confused.
        """

        super().setup(maze)
        self.confused = confused
        self.visited_spaces_weights = {}


    def _step_logic(self) -> tuple[int, int]:
        legal_moves = self.get_legal_moves()

        if self.confused:
            return random.choice(legal_moves)

        for space in self.visited_spaces_weights:
            if space in legal_moves:
                legal_moves.remove(space)

        if legal_moves:
            new_pos = random.choice(legal_moves)
        else:
            new_pos = min(self.get_legal_moves(), key = self.visited_spaces_weights.get)

        if new_pos not in self.visited_spaces_weights:
            self.visited_spaces_weights[new_pos] = 1
        else:
            self.visited_spaces_weights[new_pos] += 1

        return new_pos


__all__ = ['WandererSequential']
