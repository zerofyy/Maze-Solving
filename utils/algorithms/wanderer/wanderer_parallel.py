import random
import time

from utils.algorithms.base_algorithm import BaseAlgorithmParallel
from utils.maze_generator import Maze


class WandererParallel(BaseAlgorithmParallel):
    """
    Simple parallel algorithm that explores the maze through random moves.

    It has two modes:
        - default: Makes random moves while avoiding previously visited spaces as much as possible.
        - confused: Makes random moves without keeping track of visited spaces.
    """


    def setup(self, maze: Maze, num_processes: int = 4, confused: bool = False) -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the Maze class.
            num_processes: Number of processes, defaults to 4 or less.
            confused: Whether the wanderer is confused.
        """

        super().setup(maze, num_processes)
        self.shared_memory['confused'] = confused
        self.shared_memory['visited_spaces_weights'] = self.manager.dict()


    @staticmethod
    def _step_logic(process_id: int, maze_data: dict[str, ...], shared_memory: dict[str | int, ...]) -> None:
        state = shared_memory[process_id]
        current_pos = state['current_pos']
        vsw = dict(shared_memory['visited_spaces_weights'])
        legal_moves = BaseAlgorithmParallel.get_legal_moves(current_pos, maze_data)

        random.seed(time.time() + process_id)

        if shared_memory['confused']:
            state['current_pos'] = random.choice(legal_moves)
            return

        for space in vsw:
            if space in legal_moves:
                legal_moves.remove(space)

        if legal_moves:
            new_pos = random.choice(legal_moves)
        else:
            new_pos = min(BaseAlgorithmParallel.get_legal_moves(current_pos, maze_data),
                          key = vsw.get)

        if new_pos not in vsw:
            shared_memory['visited_spaces_weights'][new_pos] = 1
        else:
            shared_memory['visited_spaces_weights'][new_pos] += 1

        state['current_pos'] = new_pos


__all__ = ['WandererParallel']
