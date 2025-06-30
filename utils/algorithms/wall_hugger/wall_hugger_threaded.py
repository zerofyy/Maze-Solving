import os
import threading

from utils.algorithms.base_algorithm import BaseAlgorithmThreaded
from utils.maze_generator import Maze


class WallHuggerThreaded(BaseAlgorithmThreaded):
    """
    Simple threaded algorithm that explores the maze by sticking to the left or right.

    This version of the algorithm runs on two threads, one sticking to the left side and the other to the right side.
    """

    move_priorities = {
        'll': ((1, 0), (0, -1), (-1, 0), (0, 1)),
        'ld': ((0, 1), (1, 0), (0, -1), (-1, 0)),
        'lr': ((-1, 0), (0, 1), (1, 0), (0, -1)),
        'lu': ((0, -1), (-1, 0), (0, 1), (1, 0)),

        'rl': ((-1, 0), (0, -1), (1, 0), (0, 1)),
        'rd': ((0, -1), (1, 0), (0, 1), (-1, 0)),
        'rr': ((1, 0), (0, 1), (-1, 0), (0, -1)),
        'ru': ((0, 1), (-1, 0), (0, -1), (1, 0))
    }

    move_to_facing = {
        (0, 1): 'right',
        (0, -1): 'left',
        (1, 0): 'down',
        (-1, 0): 'up'
    }


    def setup(self, maze: Maze, num_threads: int = 4) -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the Maze class.
            num_threads: Number of threads. Regardless of the value, only 2 threads are used.
        """

        self.maze = maze
        self.num_threads = min(2, os.cpu_count())
        self.threads = []

        self.memory = {
            'visited_pos': {maze.start_pos},
            'reached_end': False,
            'lock': threading.Lock()
        }

        for tid in range(self.num_threads):
            direction = 'left' if tid % 2 == 0 else 'right'

            self.memory[tid] = {
                'current_pos': maze.start_pos,
                'is_active': True,
                'step_flag': threading.Event(),
                'response': None,
                'direction' : direction,
                'facing' : direction
            }

        self._start_threads()


    def _step_logic(self, tid: int) -> tuple[int, int]:
        local_memory = self.memory[tid]
        legal_moves = self.get_legal_moves(tid)
        check_moves = self.move_priorities[local_memory['direction'][0] + local_memory['facing'][0]]
        current_pos = local_memory['current_pos']

        for move in check_moves:
            new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
            if new_pos not in legal_moves:
                continue

            self.memory[tid]['facing'] = self.move_to_facing[move]
            return new_pos


    def get_status(self) -> list[tuple[str, ...]]:
        status = super().get_status()

        offset = 0
        for tid in range(self.num_threads):
            status.insert(
                4 * (tid + 1) + offset,
                ('| Direction', f'[lg]{self.memory[tid]["direction"]}[rs]')
            )

            status.insert(
                4 * (tid + 1) + offset + 1,
                ('| Facing', f'[lc]{self.memory[tid]["facing"]}[rs]')
            )
            offset += 2

        return status


__all__ = ['WallHuggerThreaded']
