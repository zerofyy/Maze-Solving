import time
import tracemalloc
import os
from sty import fg as Text, bg as Back, rs as Rest

from utils.algorithms import BaseAlgorithmSequential, BaseAlgorithmParallel
from utils.maze_generator import Maze
from utils.assets import ListMaker


class ResultsCollector:
    """ Progress tracking and collecting results of running algorithms. """

    total_time: float = None
    solve_time: float = None
    last_solve_time: float = None


    def __init__(self, algorithm: BaseAlgorithmSequential | BaseAlgorithmParallel,
                 maze: Maze, max_steps: int, progress_display: str | bool = True) -> None:
        """
        Create a new instance of the ResultsCollector class.

        Progress Tracking Options:
            - 'text' | Show the algorithm's progress in text only.
            - 'visual' | Show the algorithm's progress in text along with a visual representation of the maze.
            - 'detailed' | Show the algorithm's progress both in text and visually with additional statistics.
            - True | Same as 'text'.
            - False | No real time progression display.

        Arguments:
             algorithm: The algorithm solving the maze.
             maze: Instance of the maze being solved.
             max_steps: The maximum number of allowed steps.
             progress_display: The type of real time progress display.
        """

        os.system('')  # Required for coloring to work.

        self.algorithm = algorithm
        self.maze = maze
        self.max_steps = max_steps
        self.progress_display = 'text' if progress_display is True else progress_display
        self.results = {
            'steps_taken' : None,
            'reached_end' : None,
            'exploration' : None,
            'sp_from_end' : None,

            'solve_time' : None,
            'total_time' : None,
            'avg_step_time': None,

            'avg_mem_usage' : None,
            'top_mem_usage' : 0,

            'past_step_times' : [],
            'past_mem_usages' : []
        }


    def start(self, option: str) -> None:
        """
        Start tracking progress or measuring performance.

        Option 'track':
            Start tracking the algorithm's progress.
            Should be used after setting up the algorithm and right before starting it.

        Option 'measure':
            Start measuring the algorithm's performance.
            Should be used before setting up the algorithm.

        Arguments:
            option: The option of choice.
        """

        if option == 'measure':
            tracemalloc.start()
            self.total_time = time.time()

        if option == 'track':
            self.solve_time = time.time()
            self.last_solve_time = self.solve_time
            self.results['steps_taken'] = 0


    def update(self) -> None:
        """ Update the algorithm's statistics after taking a step. """

        step_time = time.time()

        self.results['steps_taken'] += 1

        self.results['solve_time'] = round(step_time - self.solve_time, 2)
        self.results['total_time'] = round(step_time - self.total_time, 2)

        if isinstance(self.algorithm, BaseAlgorithmSequential):
            self.results['reached_end'] = self.algorithm.is_at_end()
        else:
            self.results['reached_end'] = self.algorithm.memory.get('reached_end')

        self.results['exploration'] = len(self.algorithm.get_visited_pos())
        self.results['sp_from_end'] = self._get_end_distance()

        self.results['past_step_times'].append(step_time - self.last_solve_time)
        self.results['avg_step_time'] = round(
            sum(self.results['past_step_times']) / len(self.results['past_step_times']), 2
        )
        self.last_solve_time = step_time

        current_mem, peak_mem = tracemalloc.get_traced_memory()
        self.results['past_mem_usages'].append(current_mem / 1024 / 1024)
        self.results['avg_mem_usage'] = round(
            sum(self.results['past_mem_usages']) / len(self.results['past_mem_usages']), 2
        )
        self.results['top_mem_usage'] = max(self.results['top_mem_usage'], round(peak_mem / 1024 / 1024, 2))


    def _get_end_distance(self, position: tuple[int, int] = None) -> int:
        """ Helper function for calculating an approximate distance from the end of the maze. """

        position = position if position else self.algorithm.get_current_pos()

        if isinstance(position[0], int):
            return int(
                abs(position[0] - self.maze.end_pos[0]) +
                abs(position[1] - self.maze.end_pos[1])
            )

        return min(
            [self._get_end_distance(pos) for pos in position]
        )


    @staticmethod
    def _color(text, remove_color_codes: bool = False) -> str:
        """ Helper function for coloring text. """

        colors = {'[lb]': Text.li_blue, '[rs]': Rest.all, '[ly]': Text.li_yellow,
                  '[lc]': Text.li_cyan, '[lg]': Text.li_green, '[lr]': Text.li_red}

        if remove_color_codes:
            for tag, color in colors.items():
                text = text.replace(tag, '')
        else:
            for tag, color in colors.items():
                text = text.replace(tag, color)

        return text



    def _get_text_display(self, coloring: bool) -> str:
        """ Helper function for generating the text progress display. """

        total_time = f'{round(self.results["total_time"] / 60, 2)} min' \
            if self.results['total_time'] > 60 else f'{self.results["total_time"]} sec'
        solve_time = f'{round(self.results["solve_time"] / 60, 2)} min' \
            if self.results['solve_time'] > 60 else f'{self.results["solve_time"]} sec'

        display = f'Time Passed: __________ | Solve Time: __________  | Avg Step Time: ______ sec\n' \
                  f'Steps: ______ / ______  | Explored: _____________ | Progress: _____________ from end\n' \
                  f'Avg Mem Usage: _______  | Peak Mem Usage: _______ | ________________________________\n' \
                  f'[lr]===========================================================================================[rs]'

        display = ListMaker.fill(
            text = display,
            info = [
                (f'[lb]{total_time}[rs]', 'left'),
                (f'[lb]{solve_time}[rs]', 'left'),
                (f'[lb]{self.results["avg_step_time"]}[rs]', 'left'),
                (f'[ly]{self.results["steps_taken"]}[rs]', 'right'),
                (f'[ly]{self.max_steps}[rs]', 'left'),
                (f'[ly]{self.results["exploration"]} spaces[rs]', 'left'),
                (f'[ly]{self.results["sp_from_end"]} spaces[rs]', 'right'),
                (f'[lc]{self.results["avg_mem_usage"]} MB[rs]', 'left'),
                (f'[lc]{self.results["top_mem_usage"]} MB[rs]', 'left'),
                (f'[lg]{self.algorithm.__class__.__name__}[rs]', 'left')
            ],
            dir_offset = 8
        )

        if self.progress_display == 'detailed':
            display += f'\n[lr]{self.algorithm.__class__.__name__} Details[rs]'
            for key, val in self.algorithm.get_status():
                display += f'\n[lr]*[rs] {key}: {val}'
            display += \
                f'\n[lr]===========================================================================================[rs]'

        if coloring:
            display = display.replace('|', f'{Text.li_red}|{Rest.all}')
            display = self._color(display)
        else:
            display = self._color(display, remove_color_codes = True)

        return display


    def _get_visual_display(self, coloring: bool) -> str:
        """ Helper function for generating the visual progress display. """

        if not coloring:
            space_wall = '[/]'
            space_path = '   '
            space_current = ' + '
            space_end = ' ! '
            space_visited = ' . '
        else:
            space_wall = f'{Back.li_blue}   {Rest.all}'
            space_path = f'{Back.black}   {Rest.all}'
            space_current = f'{Back.li_green}   {Rest.all}'
            space_end = f'{Back.li_red}   {Rest.all}'
            space_visited = f'{Back.li_yellow}   {Rest.all}'

        display = ''
        for row in range(self.maze.size_matrix):
            for col in range(self.maze.size_matrix):

                space = self.maze.matrix[row][col]
                position = self.algorithm.get_current_pos()

                if space == self.maze.wall:
                    display += space_wall
                elif (row, col) == position or isinstance(position[0], tuple) and (row, col) in position:
                    display += space_current
                elif (row, col) == self.maze.end_pos:
                    display += space_end
                elif (row, col) in self.algorithm.get_visited_pos():
                    display += space_visited
                else:
                    display += space_path

            display += '\n'

        return display


    def get_progress(self, to_console: bool = True, clear_console: bool = True, coloring: bool = True) -> str | None:
        """
        Get the progress of the currently running algorithm.

        Arguments:
            to_console: Whether to print the progress to the console.
            Setting this to False will return the progress as a string.
            clear_console: Whether to clear the console when printing.
            coloring: Whether to use colors for the progress display.

        Returns:
            The progress as a string if to_console is False, otherwise prints the progress and returns None.
        """

        if not self.progress_display:
            return None if to_console else ''

        progress = self._get_text_display(coloring)

        if self.progress_display == 'visual' or self.progress_display == 'detailed':
            maze_display = self._get_visual_display(coloring)
            progress = f'\n{progress}\n\n{maze_display}{Rest.all}'

        if not to_console:
            return progress

        if clear_console:
            print(f'\033[{self.maze.size_matrix ** 2}A\033[2K', end = '')

        print(progress)


    def get_results(self, option: str, clear_console: bool = True,
                    coloring: bool = True) -> str | dict[str, ...] | None:
        """
        Get the algorithm's results.

        Options:
            - 'console' | The results will be printed to the console.
            - 'string' | The results will be returned as a string.
            - 'dict' | The results will be returned as a dictionary.
            - <file_path> | The results will be saved to a file.
            If no other option is selected, it is assumed that a file path is given.

        Arguments:
             option: Where to save/send the results.
             clear_console: Whether to clear the console if the selected option is 'console'.
             coloring: Whether to use colors if the selected option is 'console' or 'string'.

        Returns:
            The results as a string or dictionary or None if a different option is selected.
        """

        if option == 'dict':
            return self.results

        total_time = f'{round(self.results["total_time"] / 60, 2)} min' \
            if self.results['total_time'] > 60 else f'{self.results["total_time"]} sec'
        solve_time = f'{round(self.results["solve_time"] / 60, 2)} min' \
            if self.results['solve_time'] > 60 else f'{self.results["solve_time"]} sec'
        setup_time = round(self.results['total_time'] - self.results['solve_time'], 2)
        reached_end = f'[lg]Yes[rs]' if self.results['reached_end'] else '[lr]No[rs]'

        results = f'===========================================================\n' \
                  f'|| ________________                                      ||\n' \
                  f'|| * Maze Size         : ______ ( ______ x ______ )      ||\n' \
                  f'|| * Start-End         : ______________ - ______________ ||\n' \
                  f'===========================================================\n' \
                  f'|| ___________________________________________________   ||\n' \
                  f'|| * Setup Time        : __________                      ||\n' \
                  f'|| * Solve Time        : __________                      ||\n' \
                  f'|| * Total Time        : __________                      ||\n' \
                  f'|| * Avg Step Time     : __________                      ||\n' \
                  f'||-------------------------------------------------------||\n' \
                  f'|| * Steps             : ______ / ______                 ||\n' \
                  f'|| * Explored          : _____________                   ||\n' \
                  f'|| * Progress          : ~_____________ from end         ||\n' \
                  f'|| * Reached End       : ___                             ||\n' \
                  f'||-------------------------------------------------------||\n' \
                  f'|| * Avg Memory Usage  : _______                         ||\n' \
                  f'|| * Peak Memory Usage : _______                         ||\n' \
                  f'==========================================================='

        results = ListMaker.fill(
            text = results,
            info = [
                (f'[lr]Maze Information[rs]', 'left'),
                (f'[lc]{self.maze.size}[rs]', 'left'),
                (f'[lc]{self.maze.size_matrix}[rs]', 'right'),
                (f'[lc]{self.maze.size_matrix}[rs]', 'left'),
                (f'[lg]{self.maze.start_pos}[rs]', 'right'),
                (f'[lr]{self.maze.end_pos}[rs]', 'left'),
                (f'[lr]{self.algorithm.__class__.__name__} Information[rs]', 'left'),
                (f'[lb]{setup_time} sec[rs]', 'left'),
                (f'[lb]{solve_time}[rs]', 'left'),
                (f'[lb]{total_time}[rs]', 'left'),
                (f'[lb]{self.results["avg_step_time"]} sec[rs]', 'left'),
                (f'[ly]{self.results["steps_taken"]}[rs]', 'right'),
                (f'[ly]{self.max_steps}[rs]', 'left'),
                (f'[ly]{self.results["exploration"]} spaces[rs]', 'left'),
                (f'[ly]{self.results["sp_from_end"]} spaces[rs]', 'left'),
                (reached_end, 'left'),
                (f'[lc]{self.results["avg_mem_usage"]} MB[rs]', 'left'),
                (f'[lc]{self.results["top_mem_usage"]} MB[rs]', 'left')
            ],
            dir_offset = 8)

        if coloring and (option == 'console' or option == 'string'):
            results = results.replace('*', f'{Text.li_red}*{Rest.all}')
            results = self._color(results)
        else:
            results = self._color(results, remove_color_codes = True)

        if option == 'console':
            if clear_console:
                print(f'\033[{self.maze.size_matrix * 2}A\033[2K', end = '')
            print(results)
            return

        if option == 'string':
            return results

        with open(option, 'w', encoding = 'UTF-8') as file:
            file.write(results)


    def __del__(self) -> None:
        """ Stop measuring memory usage when object is deleted. """

        tracemalloc.stop()


__all__ = ['ResultsCollector']
