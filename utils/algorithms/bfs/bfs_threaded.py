from utils.algorithms import BaseAlgorithmThreaded
from utils.maze_generator import Maze


class BFSThreaded(BaseAlgorithmThreaded):
    """
    Threaded implementation of the BFS algorithm for maze solving.

    BFS explores all neighboring nodes at the current depth before moving to nodes at the next depth.
    """

    def setup(self, maze: Maze, wait_for_flag: bool = False, num_threads: int = 4) -> None:
        super().setup(maze, wait_for_flag, num_threads)
        self.memory['queue'] = [maze.start_pos]


    def _step_logic(self, tid: int) -> tuple[int, int]:
        new_pos = self.memory['queue'].pop(0)
        legal_moves = self.get_legal_moves(tid, new_pos)

        with self.memory['lock']:
            for move in legal_moves:
                if move not in self.memory['visited_pos'] and move not in self.memory['queue']:
                    self.memory['queue'].append(move)

        return new_pos


    def get_status(self) -> list[tuple[str, ...]]:
        status = super().get_status()
        status.append(('Queued Spaces', f'[ly]{len(self.memory["queue"])}[rs]'))
        return status



__all__ = ['BFSThreaded']
