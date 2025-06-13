from abc import abstractmethod, ABC

from utils.maze_generator import Maze


class BaseAlgorithmSequential(ABC):
    """ Abstract class representing a sequential maze solving algorithm. """

    maze_data: dict[str, ...] = None
    current_pos: tuple[int, int] = None
    visited_spaces: list[tuple[int, int]] = None


    def setup(self, maze: Maze) -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the Maze class.
        """

        self.maze_data = maze.get_maze_data()
        self.current_pos = maze.start_pos
        self.visited_spaces = [self.current_pos]


    def is_at_end(self) -> bool:
        """ Check whether the current position matches the end position. """

        return self.current_pos == self.maze_data['end_pos']


    def get_legal_moves(self, position: tuple[int, int] = None) -> list[tuple[int, int]]:
        """
        Get a list of legal moves (coordinates) from the current position.

        Arguments:
            position: A specific position to check for legal moves.
        """

        current_pos = position if position else self.current_pos

        if self.is_at_end() or self.maze_data['matrix'][current_pos[0]][current_pos[1]] == self.maze_data['wall']:
            return []

        check_moves = [
            (current_pos[0] - 1, current_pos[1]),
            (current_pos[0] + 1, current_pos[1]),
            (current_pos[0], current_pos[1] - 1),
            (current_pos[0], current_pos[1] + 1)
        ]

        return [
            move for move in check_moves
            if 0 <= move[0] < self.maze_data['size_matrix'] and 0 <= move[1] < self.maze_data['size_matrix']
            and self.maze_data['matrix'][move[0]][move[1]] == self.maze_data['path']
        ]


    def step(self) -> tuple[tuple[int, int] | None, bool]:
        """
        Take a step in the maze.

        Returns:
            A tuple containing information about the new step in **new_position | None, reached_end** format.
            The first element is a tuple with the coordinates of the new position or None if there are no legal moves.
            The second element is a boolean representing whether the end of the maze has been reached.
        """

        legal_moves = self.get_legal_moves()
        if not legal_moves:
            return None, self.is_at_end()

        new_pos = self._step_logic()

        self.current_pos = new_pos
        if new_pos not in self.visited_spaces:
            self.visited_spaces.append(new_pos)

        return new_pos, self.is_at_end()


    @abstractmethod
    def _step_logic(self) -> tuple[int, int]:
        """
        Logic for choosing the next move from the current position with the assumption that
        there is at least one legal move from the current position. Only the logic for the
        step should be implemented here, nothing more (ex. updating visited_spaces).

        Returns:
            The new position after taking a step.
            The function must only return a new position, nothing else.
        """


__all__ = ['BaseAlgorithmSequential']
