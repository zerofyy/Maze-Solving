from utils.algorithms import BaseAlgorithmSequential
from utils.maze_generator import Maze


class DFSSequential(BaseAlgorithmSequential):
    """
    Sequential implementation of the Depth-First Search algorithm for maze solving.

    DFS explores as far as possible along each branch before backtracking.
    """

    def setup(self, maze: Maze) -> None:
        super().setup(maze)
        self.memory['stack'] = [maze.start_pos]


    def _step_logic(self) -> tuple[int, int]:
        legal_moves = self.get_legal_moves()
        unvisited_legal_moves = [move for move in legal_moves if move not in self.memory['visited_pos']]

        if unvisited_legal_moves:
            new_pos = unvisited_legal_moves[0]
            self.memory['stack'].append(new_pos)
            return new_pos

        self.memory['stack'].pop()
        return self.memory['stack'][-1]


    def get_status(self) -> list[tuple[str, ...]]:
        status = super().get_status()
        status.append(('Stacked Spaces', f'[ly]{len(self.memory["stack"])}[rs]'))
        return status


__all__ = ['DFSSequential']
