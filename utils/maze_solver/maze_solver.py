import time
import copy
import os
from sty import fg as Text, bg as Back, rs as Rest

from utils.maze_generator import MazeGenerator
from utils.algorithms import BaseAlgorithm


class MazeSolver:
    """ Static class for running maze solving algorithms and measuring their performance. """


    @staticmethod
    def show_progress(algorithm: BaseAlgorithm, progress_option: str | None,
                      return_str: bool = False, clear_print: bool = True, coloring: bool = True) -> str | None:
        """
        Get the progress of the given algorithm.

        Progress Options:
            - 'text' | Show the algorithm's progress in text only.
            - 'visual' | Show the algorithm's progress in text along with a visual representation of the maze.
            - None | No real time progression display.

        Arguments:
            algorithm: Algorithm instance.
            progress_option: The type of progress to display.
            return_str: Whether to return the progress as a string.
                        Setting this to False will print it to the console.
            clear_print: Whether to clear the console when printing.
            coloring: Whether to use colors for the progress display.
        """

        if progress_option is None:
            return '' if return_str else None

        time_passed = round(time.time() - algorithm.start_time, 2)
        end_distance = abs(algorithm.current_pos[0] - algorithm.end_pos[0] +
                           algorithm.current_pos[1] + algorithm.end_pos[1])

        if coloring:
            if end_distance > 15:
                distance_color = Text.li_red
            elif end_distance >= 10:
                distance_color = Text.li_yellow
            else:
                distance_color = Text.li_green
            progress = f'Time: {Text.li_blue}{time_passed} sec{Rest.all} | ' \
                       f'Steps: {Text.li_magenta}{algorithm.steps_taken}{Rest.all}' \
                       f'/{Text.li_magenta}{algorithm.max_steps}{Rest.all} | ' \
                       f'Visited {Text.li_yellow}{len(algorithm.visited_spaces)}{Rest.all} unique spaces | ' \
                       f'About {distance_color}{end_distance}{Rest.all} spaces away from the end'
        else:
            progress = f'Time: {time_passed} sec | ' \
                       f'Steps: {algorithm.steps_taken}/{algorithm.max_steps} | ' \
                       f'Visited {len(algorithm.visited_spaces)} unique spaces | ' \
                       f'About {end_distance} spaces away from the end'

        if progress_option == 'visual':
            visual = ''
            maze = copy.deepcopy(algorithm.maze)

            if coloring:
                for space in algorithm.visited_spaces:
                    maze[space[0]][space[1]] = f'{Back.li_yellow}   {Rest.all}'

                maze[algorithm.end_pos[0]][algorithm.end_pos[1]] = f'{Back.li_red}   {Rest.all}'
                maze[algorithm.current_pos[0]][algorithm.current_pos[1]] = f'{Back.li_green}   {Rest.all}'

                for row in maze:
                    row = ''.join(row)
                    visual += f'{row}{"":{algorithm.size ** 2}}\n'

                visual = visual.replace(algorithm.wall, f'{Back.li_blue}   {Rest.all}')
                visual = visual.replace(algorithm.path, f'{Back.black}   {Rest.all}')

            else:
                maze[algorithm.end_pos[0]][algorithm.end_pos[1]] = ' ! '
                maze[algorithm.current_pos[0]][algorithm.current_pos[1]] = ' + '

                for row in maze:
                    row = ''.join(row)
                    visual += f'{row}\n'

                visual = visual.replace(algorithm.wall, '[/]')
                visual = visual.replace(algorithm.path, '   ')

            progress += f'\n{visual}{Rest.all}'

        if return_str:
            return progress

        if clear_print:
            print(f'\033[{algorithm.size ** 2}A\033[2K', end = '')

        print(progress)


    @staticmethod
    def run(algorithm_settings: dict[str, ...], mazes: list[dict[str, ...]], measure_performance: bool = False,
            wait_after_step: int | str | None = None, real_time_progress: str | None = 'text') -> dict[str, ...] | None:
        """
        Run a specific algorithm on the given mazes.

        Waiting Methods:
            - <int> | Number of milliseconds to wait.
            - 'input' | Wait until input is given.
            - None | No waiting.

        Real Time Progress Options:
            - 'text' | Show the algorithm's progress in text only.
            - 'visual' | Show the algorithm's progress in text along with a visual representation of the maze.
            - None | No real time progression display.

        Arguments:
             algorithm_settings: Dictionary containing algorithm settings.
             mazes: List of dictionaries containing settings for different mazes.
             measure_performance: Whether to measure the algorithm's performance for each maze.
             wait_after_step: The method for waiting after each step.
             real_time_progress: The type of real time progress to display when running the algorithm.

        Returns:
            A dictionary of statistics for the algorithm or None if measure_performance is set to False.
        """

        os.system('')  # Required for the progress display colors to work.

        def wait_method():
            if wait_after_step == 'input':
                input('... waiting for input ...')
            elif wait_after_step is not None:
                time.sleep(wait_after_step / 1000)

        for maze_settings in mazes:
            maze = MazeGenerator(maze_settings['size'])
            maze.set_start_end_coords(maze_settings['start_pos'], maze_settings['end_pos'])

            for i in range(maze_settings['num_iterations']):
                algorithm = algorithm_settings['algorithm']()
                algorithm_settings.pop('algorithm')
                algorithm.setup(maze, **algorithm_settings)
                algorithm.start_time = time.time()

                while True:
                    step = algorithm.step()
                    if step is None:
                        break

                    MazeSolver.show_progress(algorithm, real_time_progress)
                    wait_method()

        return None


__all__ = ['MazeSolver']
