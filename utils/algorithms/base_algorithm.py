from abc import abstractmethod, ABC
from utils.maze_generator import MazeGenerator


class BaseAlgorithm(ABC):
    """ Abstract class representing a maze solving algorithm. """

    maze: list[list[int | str]] = None
    size: int = None
    size_matrix: int = None

    start_pos: tuple[int, int] = None
    end_pos: tuple[int, int] = None
    current_pos: tuple[int, int] = None

    wall: str | int = None
    path: str | int = None

    steps_taken: int = None
    max_steps: int = None
    visited_spaces: list[tuple[int, int]] = None


    def setup(self, mg_instance: MazeGenerator, max_steps: int | str = 'auto') -> None:
        """
        Set up the algorithm.

         Maximum Steps Options:
            - <int> | Exact number of allowed steps.
            - 'auto' | Equal to `(maze_size * 2 + 1) ^ 2`.
            - 'fewest' | Equal to `(start_pos - end_pos + size)`.
            - 'unlimited' | Unlimited number of allowed steps.

        Arguments:
            mg_instance: Instance of the MazeGenerator class.
            max_steps: The maximum amount of steps allowed.
        """

        if mg_instance.maze is None:
            mg_instance.generate()

        self.maze = mg_instance.maze
        self.size = mg_instance.size
        self.size_matrix = mg_instance.size * 2 + 1

        self.start_pos = mg_instance.start_coords
        self.end_pos = mg_instance.end_coords
        self.current_pos = mg_instance.start_coords

        self.wall = mg_instance.wall
        self.path = mg_instance.path

        match max_steps:
            case 'auto':
                self.max_steps = (mg_instance.size * 2 + 1) ** 2
            case 'fewest':
                self.max_steps = abs(mg_instance.start_coords[0] - mg_instance.end_coords[0]) \
                                 + abs(mg_instance.start_coords[1] - mg_instance.end_coords[1]) \
                                 + mg_instance.size
            case 'unlimited':
                self.max_steps = 0
            case _:
                self.max_steps = int(max_steps)
        self.steps_taken = 0
        self.visited_spaces = []


    def get_legal_moves(self) -> list[tuple[int, int]]:
        """ Get a list of legal moves (coordinates) from the current position. """

        check_moves = [
            (self.current_pos[0] - 1, self.current_pos[1]),
            (self.current_pos[0] + 1, self.current_pos[1]),
            (self.current_pos[0], self.current_pos[1] - 1),
            (self.current_pos[0], self.current_pos[1] + 1)
        ]

        return [
            move for move in check_moves
            if 0 <= move[0] < self.size_matrix and 0 <= move[1] < self.size_matrix
            and self.maze[move[0]][move[1]] == self.path
        ]


    def can_take_step(self) -> bool:
        """ Check whether a step can be taken. """

        return self.current_pos != self.end_pos or self.max_steps == 0 or self.steps_taken == self.max_steps


    @abstractmethod
    def step(self) -> tuple[int, int] | None:
        """
        Take a step in the maze.

        Returns:
            The coordinates of the chosen direction from the current position or None if no move
            is chosen. None may be returned if the algorithm exceeds the maximum number of allowed
            steps or if it reaches the ending position in the maze.
        """

        if not self.can_take_step():
            return None

        self.steps_taken += 1
        self.current_pos = self.get_legal_moves()[0]

        if self.current_pos not in self.visited_spaces:
            self.visited_spaces.append(self.current_pos)

        return self.current_pos


__all__ = ['BaseAlgorithm']
