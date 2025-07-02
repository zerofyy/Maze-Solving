from utils.algorithms import BaseAlgorithmSequential
from utils.maze_generator import Maze


class BFSSequential(BaseAlgorithmSequential):
    """
    Sequential implementation of the Breadth-First Search algorithm for maze solving.

    BFS explores all neighboring nodes at the current depth before moving to nodes at the next depth.
    """

    def setup(self, maze: Maze) -> None:
        super().setup(maze)
        self.memory['queue'] = [maze.start_pos]


    def _step_logic(self) -> tuple[int, int]:
        new_pos = self.memory['queue'].pop(0)
        legal_moves = self.get_legal_moves(new_pos)

        for move in legal_moves:
            if move not in self.memory['visited_pos'] and move not in self.memory['queue']:
                self.memory['queue'].append(move)

        return new_pos


    def get_status(self) -> list[tuple[str, ...]]:
        status = super().get_status()
        status.append(('Queued Spaces', f'[ly]{len(self.memory["queue"])}[rs]'))
        return status


__all__ = ['BFSSequential']
