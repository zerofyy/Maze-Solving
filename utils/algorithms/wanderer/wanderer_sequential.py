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


    def setup(self, maze: Maze, confused: bool = False) -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the maze being solved.
            confused: Whether the wanderer is confused.
        """

        super().setup(maze)
        self.memory['breadcrumbs'] = [maze.start_pos]
        self.memory['confused'] = confused


    def _step_logic(self) -> tuple[int, int]:
        legal_moves = self.get_legal_moves()

        if self.memory['confused']:
            return random.choice(legal_moves)

        unvisited_spaces = [move for move in legal_moves if move not in self.memory['visited_pos']]
        if unvisited_spaces:
            move = random.choice(unvisited_spaces)
            self.memory['breadcrumbs'].append(move)
            return move

        else:
            self.memory['breadcrumbs'].pop()
            return self.memory['breadcrumbs'][-1]


    def get_status(self) -> list[tuple[str, ...]]:
        status = super().get_status()
        status.append(('Confused', '[lg]Yes[rs]' if self.memory['confused'] else '[lr]No[rs]'))
        status.append(('Breadcrumbs', f'[ly]{len(self.memory["breadcrumbs"])}[rs]'))
        return status


__all__ = ['WandererSequential']
