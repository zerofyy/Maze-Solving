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


    def setup(self, maze: Maze, confused: bool = False) -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the Maze class.
            confused: Whether the wanderer is confused.
        """

        super().setup(maze)
        self.confused = confused


    def step(self) -> tuple[int, int] | None:
        if not self.can_take_step():
            return None

        legal_moves = self.get_legal_moves()

        for space in self.visited_spaces:
            if space in legal_moves:
                legal_moves.remove(space)

        if not self.confused and legal_moves:
            self.current_pos = random.choice(legal_moves)
        else:
            self.current_pos = random.choice(self.get_legal_moves())

        if self.current_pos not in self.visited_spaces:
            self.visited_spaces.append(self.current_pos)

        return self.current_pos


__all__ = ['WandererSequential']
