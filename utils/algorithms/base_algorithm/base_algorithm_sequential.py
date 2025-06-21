from abc import abstractmethod, ABC

from utils.maze_generator import Maze


class BaseAlgorithmSequential(ABC):
    """ Abstract representation of a sequential maze solving algorithm. """

    maze: Maze = None
    memory: dict[str, ...] = None


    def setup(self, maze: Maze) -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the maze being solved.
        """

        self.maze = maze
        self.memory = {
            'current_pos' : maze.start_pos,
            'visited_pos' : {maze.start_pos},
            'reached_end' : False
        }


    def is_at_end(self) -> bool:
        """ Check whether the algorithm's current position matches the maze end position. """

        reached_end = self.memory['current_pos'] == self.maze.end_pos
        if reached_end:
            self.memory['reached_end'] = True

        return reached_end


    def get_legal_moves(self, position: tuple[int, int] = None) -> list[tuple[int, int]]:
        """
        Get a list of legal moves.

        Arguments:
            position: A specific position to check for legal moves, defaults to the current position.

        Returns:
            A list of new positions that can be visited from the current or specified position. If no
            legal moves exist, the list will be empty.
        """

        if position is None:
            position = self.memory['current_pos']

        if self.is_at_end():
            return []

        check_moves = [
            (position[0] - 1, position[1]),
            (position[0] + 1, position[1]),
            (position[0], position[1] - 1),
            (position[0], position[1] + 1)
        ]

        return [
            move for move in check_moves
            if 0 <= move[0] < self.maze.size_matrix and 0 <= move[1] < self.maze.size_matrix
            and self.maze.matrix[move[0]][move[1]] == self.maze.path
        ]


    def get_current_pos(self) -> tuple[int, int]:
        """
        Get the current position of the algorithm.

        This function should be overwritten if the `'current_pos'` key in the algorithm's memory is modified.
        Regardless of the modifications, the return type must remain the same.

        Returns:
            The coordinates of the current position in the maze.
        """

        return self.memory['current_pos']


    def get_visited_pos(self) -> set[tuple[int, int]]:
        """
        Get all the positions previously visited by the algorithm.

        This function should be overwritten if the `'visited_pos'` key in the algorithm's memory is modified.
        Regardless of the modifications, the return type must remain the same.

        Returns:
            A set of coordinates of all visited positions in the maze.
        """

        return self.memory['visited_pos']


    def get_status(self) -> list[tuple[str, ...]]:
        """
        Get information about the algorithm's status.

        By default, this function returns information from the algorithm's memory. If the algorithm's memory
        has been modified - this function should be overwritten to include those modifications in the status
        dictionary (in an appropriate format for real time displays). Regardless of the modifications, the
        return type of this function must remain the same.

        Returns:
            A list with status information.
        """

        return [
            ('Current Position  ', f'[ly]{self.memory["current_pos"]}[rs]'),
            ('Visited Positions ', f'[ly]{len(self.memory["visited_pos"])}[rs]'),
            ('Reached End       ', '[lg]Yes[rs]' if self.memory['reached_end'] else '[lr]No[rs]')
        ]


    def step(self) -> tuple[tuple[int, int] | None, bool]:
        """
        Take a step in the maze.

        Returns:
            The new position after taking a step or None if a step was not taken, and a boolean value
            representing whether the end of the maze has been reached.
        """

        if not self.get_legal_moves():
            return None, self.is_at_end()

        new_pos = self._step_logic()
        self._after_step(new_pos)

        return self.get_current_pos(), self.is_at_end()


    @abstractmethod
    def _step_logic(self) -> tuple[int, int]:
        """
        Logic for choosing the next move from the current position with the assumption that there's at
        least one legal moves from the current position.

        If anything in the algorithm's memory has been modified (ex. `'current_pos', 'visited_pos'`), then
        the logic for updating those variables should also be implemented here or within the `_after_step()`
        function. Additionally, if memory keys/values are modified, then the relevant functions
        (`get_current_pos()`, `get_visited_pos()`, `get_status()`) should also be overwritten to support
        those changes. Regardless of the changes or the algorithm's logic, the return type must remain the
        same.

        Returns:
            The new position after taking a step.
        """

        pass


    def _after_step(self, new_pos: tuple[int, int]) -> None:
        """
        Logic for updating class variables and algorithm memory after taking a step.

        This function should only be overwritten if the algorithm's memory is modified or there are
        additional operations that need to be made. Additionally, if memory keys/values are modified,
        then the relevant functions (`get_current_pos()`, `get_visited_pos()`, `get_status()`) should
        also be overwritten to support those changes. Regardless of the changes or the implemented logic,
        the function arguments must remain the same. This function can, but doesn't need to return anything.

        Arguments:
            new_pos: The new position after taking a step.
        """

        self.memory['current_pos'] = new_pos
        self.memory['visited_pos'].add(new_pos)


__all__ = ['BaseAlgorithmSequential']
