import time

from utils.algorithms import BaseAlgorithmThreaded
from utils.maze_generator import Maze
from utils.assets import Display
from .results_collector import ResultsCollector


class MazeSolver:
    """ Set up, execute, and measure performance of maze solving algorithms. """

    def __init__(self, algorithm_args: dict[str, ...], mazes: list[dict[str, ...]],
                 measure_performance: bool = True, wait_after_step: int | str | None = None,
                 show_progress: str | bool = True, coloring: bool = False) -> None:
        """
        Initialize the maze solver.

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
             coloring: Whether to use coloring in the progress display.
        """

        self.algorithm_args = algorithm_args
        self.mazes = mazes
        self.measure_performance = measure_performance
        self.show_progress = show_progress
        self.coloring = coloring

        if wait_after_step == 'input' or wait_after_step is not None:
            self.threaded_wait_for_flag = True
        else:
            self.threaded_wait_for_flag = False

        def wait_method():
            if wait_after_step == 'input':
                input('... waiting for input ...')
            elif wait_after_step is not None:
                time.sleep(wait_after_step / 1000)
        self.wait_after_step = wait_method


    @staticmethod
    def _get_max_steps(maze: Maze, max_steps: str | int) -> int:
        """ Calculate the maximum number of allowed steps. """

        match max_steps:
            case 'auto':
                return maze.size ** 2 * 2
            case 'fewest':
                return int(
                    12.3 * (abs(maze.start_pos[0] - maze.end_pos[0]) + abs(maze.start_pos[1] - maze.end_pos[1]))
                )
            case 'unlimited':
                return 0
            case _:
                return int(max_steps)


    def _solve(self, maze_args: dict[str, ...]) -> dict[str, ...] | str | None:
        """ Solve a maze and measure the algorithm's performance. """

        maze = maze_args['maze']
        algorithm = self.algorithm_args['algorithm']()

        display = Display(algorithm, maze,
                          text_display = True if self.show_progress else False,
                          maze_display = True if self.show_progress in ['visual', 'detailed'] else False)
        detailed_progress = self.show_progress == 'detailed'

        max_steps = self._get_max_steps(maze, maze_args['max_steps'])
        collector = ResultsCollector(algorithm, maze, max_steps)
        collector.start('measure')

        if isinstance(algorithm, BaseAlgorithmThreaded):
            algorithm.setup(maze = maze, wait_for_flag = self.threaded_wait_for_flag, **self.algorithm_args['args'])
        else:
            algorithm.setup(maze = maze, **self.algorithm_args['args'])

        collector.start('track')
        while True:
            if max_steps != 0 and collector.results['steps_taken'] == max_steps:
                break

            new_pos, reached_end = algorithm.step()
            collector.update()

            progress = collector.get_progress(coloring = self.coloring, details = detailed_progress)
            display.update(text = progress, maze_colors = self.coloring)

            if new_pos is None or reached_end:
                break

            self.wait_after_step()

        if self.measure_performance:
            results = collector.get_results('string', coloring = self.coloring)
            display.update(text = results, maze_colors = self.coloring)

            collector.get_results(f'results/{algorithm.__class__.__name__}_Maze{maze.size}_{int(time.time())}.txt')

            return collector.get_results('dict')

        return None


    def run(self, wait_after_iter: bool = True) -> dict[str, ...] | None:
        """
        Run the algorithm on all given mazes.

        Arguments:
            wait_after_iter: Whether to wait for input after each iteration.

        Returns:
            A dictionary of statistics for the algorithm or None if measure_performance is set to False.
        """

        for maze_args in self.mazes:
            for i in range(maze_args['num_iterations']):

                self._solve(maze_args)

                if wait_after_iter:
                    input('... preventing from running next iteration by waiting for input ...')

        return None


__all__ = ['MazeSolver']
