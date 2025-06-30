from utils.algorithms.base_algorithm import BaseAlgorithmSequential
from utils.maze_generator import Maze


class WallHuggerSequential(BaseAlgorithmSequential):
    """
    Simple sequential algorithm that explores the maze by sticking to the left or right.

    It has two modes:
        - left: Always sticks to the left side.
        - right: Always sticks to the right side.
    """

    move_priorities = {
        'll' : ((1, 0), (0, -1), (-1, 0), (0, 1)),
        'ld' : ((0, 1), (1, 0), (0, -1), (-1, 0)),
        'lr' : ((-1, 0), (0, 1), (1, 0), (0, -1)),
        'lu' : ((0, -1), (-1, 0), (0, 1), (1, 0)),

        'rl' : ((-1, 0), (0, -1), (1, 0), (0, 1)),
        'rd' : ((0, -1), (1, 0), (0, 1), (-1, 0)),
        'rr' : ((1, 0), (0, 1), (-1, 0), (0, -1)),
        'ru' : ((0, 1), (-1, 0), (0, -1), (1, 0))
    }

    move_to_facing = {
        (0, 1) : 'right',
        (0, -1) : 'left',
        (1, 0) : 'down',
        (-1, 0) : 'up'
    }


    def setup(self, maze: Maze, direction: str = 'left') -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the maze being solved.
            direction: Which direction to follow, either "left" or "right".
        """

        super().setup(maze)
        self.memory['direction'] = direction
        self.memory['facing'] = direction


    def _step_logic(self) -> tuple[int, int]:
        legal_moves = self.get_legal_moves()
        check_moves = self.move_priorities[self.memory['direction'][0] + self.memory['facing'][0]]
        current_pos = self.memory['current_pos']

        for move in check_moves:
            new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
            if new_pos not in legal_moves:
                continue

            self.memory['facing'] = self.move_to_facing[move]
            return new_pos


    def get_status(self) -> list[tuple[str, ...]]:
        status = super().get_status()
        status.append(('Direction', f'[lg]{self.memory["direction"]}[rs]'))
        status.append(('Facing', f'[lc]{self.memory["facing"]}[rs]'))
        return status


__all__ = ['WallHuggerSequential']
