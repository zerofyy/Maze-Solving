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
        for pid in range(self.num_processes):
            self.memory[pid]['breadcrumbs'] = self.manager.list([maze.start_pos])
        self.memory['confused'] = confused


    @staticmethod
    def _step_logic(pid: int, maze_data: dict[str, ...], memory: dict[str | int, ...]) -> tuple[int, int]:
        random.seed(time.time() + pid)
        local_memory = dict(memory[pid])
        legal_moves = WandererParallel.get_legal_moves(local_memory['current_pos'], maze_data)

        if memory['confused']:
            return random.choice(legal_moves)

        unvisited_spaces = [move for move in legal_moves if move not in memory['visited_pos']]
        if unvisited_spaces:
            move = random.choice(unvisited_spaces)
            memory[pid]['breadcrumbs'].append(move)

        elif len(local_memory['breadcrumbs']) <= 1:
            move = random.choice([memory[i]['current_pos'] for i in dict(memory) if isinstance(i, int) and i != pid])

        else:
            memory[pid]['breadcrumbs'].pop()
            return memory[pid]['breadcrumbs'][-1]

        return move


    def get_status(self) -> list[tuple[str, ...]]:
        status = super().get_status()

        offset = 0
        for pid in range(self.num_processes):
            status.insert(
                4 * (pid + 1) + offset,
                ('[lr]|[rs] Breadcrumbs      ', f'[ly]{len(self.memory[pid]["breadcrumbs"])}[rs]')
            )
            offset += 1

        status.append(('Confused           ', '[lg]Yes[rs]' if self.memory['confused'] else '[lr]No[rs]'))

        return status


__all__ = ['WandererParallel']
