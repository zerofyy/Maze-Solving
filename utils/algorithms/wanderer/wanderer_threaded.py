import random
import time

from utils.algorithms.base_algorithm import BaseAlgorithmThreaded
from utils.maze_generator import Maze


class WandererThreaded(BaseAlgorithmThreaded):
    """
    Simple threaded algorithm that explores the maze through random moves.

    It has two modes:
        - default: Makes random moves while avoiding previously visited spaces as much as possible.
        - confused: Makes random moves without keeping track of visited spaces.
    """

    def setup(self, maze: Maze, num_threads: int = 4, confused: bool = False) -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the Maze class.
            num_threads: Number of threads, defaults to 4 or less.
            confused: Whether the wanderer is confused.
        """

        super().setup(maze, num_threads)
        for tid in range(self.num_threads):
            self.memory[tid]['breadcrumbs'] = [maze.start_pos]
        self.memory['confused'] = confused


    def _step_logic(self, tid: int) -> tuple[int, int]:
        random.seed(time.time() + tid)
        local_memory = self.memory[tid]
        legal_moves = self.get_legal_moves(tid)

        if self.memory['confused']:
            return random.choice(legal_moves)

        unvisited_spaces = [move for move in legal_moves if move not in self.memory['visited_pos']]
        if unvisited_spaces:
            move = random.choice(unvisited_spaces)
            self.memory[tid]['breadcrumbs'].append(move)

        elif len(local_memory['breadcrumbs']) <= 1:
            move = random.choice(
                [self.memory[i]['current_pos'] for i in dict(self.memory) if isinstance(i, int) and i != tid]
            )

        else:
            self.memory[tid]['breadcrumbs'].pop()
            return self.memory[tid]['breadcrumbs'][-1]

        return move


    def get_status(self) -> list[tuple[str, ...]]:
        status = super().get_status()

        offset = 0
        for tid in range(self.num_threads):
            status.insert(
                4 * (tid + 1) + offset,
                ('| Breadcrumbs', f'[ly]{len(self.memory[tid]["breadcrumbs"])}[rs]')
            )
            offset += 1

        status.append(('Confused', '[lg]Yes[rs]' if self.memory['confused'] else '[lr]No[rs]'))

        return status


__all__ = ['WandererThreaded']
