import time

from utils.maze_generator import Maze
from .results_collector import ResultsCollector


class MazeSolver:
    """ Simplified set up, execution, and performance measurements of maze solving algorithms. """


    def __init__(self, algorithm_args: dict[str, ...], mazes: list[dict[str, ...]], measure_performance: bool = True,
                 wait_after_step: int | str | None = None, show_progress: str | bool = True) -> None:
        """
        Create a new instance of the MazeSolver class and set it up.

        Waiting Methods:
            - <int> | Number of milliseconds to wait.
            - 'input' | Wait until input is given.
            - None | No waiting.

        Real Time Progress Options:
            - 'text' | Show the algorithm's progress in text only.
            - 'visual' | Show the algorithm's progress in text along with a visual representation of the maze.
            - 'detailed' | Show the algorithm's progress both in text and visually with additional statistics.
            - True | Same as 'text'.
            - False | No real time progression display.

        Arguments:
             algorithm_args: Dictionary containing algorithm settings.
             mazes: List of dictionaries containing settings for different mazes.
             measure_performance: Whether to measure the algorithm's performance for each maze.
             wait_after_step: The method for waiting after each step.
             show_progress: The type of real time progress to display when running the algorithm.
        """

        self.algorithm_args = algorithm_args
        self.mazes = mazes
        self.measure_performance = measure_performance
        self.show_progress = show_progress

        def wait_method():
            if wait_after_step == 'input':
                input('... waiting for input ...')
            elif wait_after_step is not None:
                time.sleep(wait_after_step / 1000)
        self.wait_after_step = wait_method


    @staticmethod
    def _get_max_steps(maze: Maze, max_steps: str | int) -> int:
        """ Helper function for calculating the maximum number of allowed steps. """

        match max_steps:
            case 'auto':
                return maze.size ** 2 * 2
            case 'fewest':
                return abs(maze.start_pos[0] - maze.end_pos[0]) + abs(maze.start_pos[1] - maze.end_pos[1]) + maze.size
            case 'unlimited':
                return 0
            case _:
                return int(max_steps)


    def _solve(self, maze_args: dict[str, ...]) -> dict[str, ...] | str | None:
        """ Helper function for solving a maze and collecting results. """

        maze = maze_args['maze']
        algorithm = self.algorithm_args['algorithm']()

        max_steps = self._get_max_steps(maze, maze_args['max_steps'])
        rc = ResultsCollector(algorithm, maze, max_steps, self.show_progress)
        rc.start('measure')

        algorithm.setup(maze = maze, **self.algorithm_args['args'])
        rc.start('track')

        while True:
            if max_steps != 0 and rc.results['steps_taken'] == max_steps:
                break

            new_pos, reached_end = algorithm.step()
            rc.update()
            rc.get_progress()

            if new_pos is None or reached_end:
                break

            self.wait_after_step()

        if self.measure_performance:
            rc.get_results('console')
            return rc.get_results('dict')

        return None


    def run(self) -> dict[str, ...] | None:
        """
        Run the algorithm on all given mazes.

        Returns:
            A dictionary of statistics for the algorithm or None if measure_performance is set to False.
        """

        for maze_args in self.mazes:
            for i in range(maze_args['num_iterations']):
                results = self._solve(maze_args)

                # ...

        return None


__all__ = ['MazeSolver']
