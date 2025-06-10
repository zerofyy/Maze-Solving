from abc import abstractmethod, ABC
from utils.maze_generator import Maze


class BaseAlgorithm(ABC):
    """ Abstract class representing a maze solving algorithm. """

    maze: Maze = None
    current_pos: tuple[int, int] = None
    visited_spaces: list[tuple[int, int]] = None


    def setup(self, maze: Maze) -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the Maze class.
        """

        self.maze = maze
        self.current_pos = maze.start_pos
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
            if 0 <= move[0] < self.maze.size_matrix and 0 <= move[1] < self.maze.size_matrix
            and self.maze.maze[move[0]][move[1]] == self.maze.path
        ]


    def can_take_step(self) -> bool:
        """ Check whether a step can be taken. """

        return self.current_pos != self.maze.end_pos


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

        self.current_pos = self.get_legal_moves()[0]

        if self.current_pos not in self.visited_spaces:
            self.visited_spaces.append(self.current_pos)

        return self.current_pos


__all__ = ['BaseAlgorithm']
