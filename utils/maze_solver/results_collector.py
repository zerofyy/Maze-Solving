import time
import tracemalloc
from sty import fg as Text, bg as Back, rs as Rest

from utils.algorithms import BaseAlgorithmSequential, BaseAlgorithmParallel
from utils.maze_generator import Maze


class ResultsCollector:
    """ Class for tracking progress and collecting results of algorithms. """

    total_time: float = None
    algorithm_time: float = None
    last_algorithm_time: float = None


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
            self.algorithm_time = time.time()
            self.last_algorithm_time = self.algorithm_time
            self.results['steps_taken'] = 0


    def update(self) -> None:
        """ Update the algorithm's statistics after taking a step. """

        step_time = time.time()

        self.results['steps_taken'] += 1

        self.results['solve_time'] = round(step_time - self.algorithm_time, 2)
        self.results['total_time'] = round(step_time - self.total_time, 2)

        if isinstance(self.algorithm, BaseAlgorithmSequential):
            self.results['reached_end'] = self.algorithm.is_at_end()
        else:
            self.results['reached_end'] = self.algorithm.shared_memory['reached_end'].is_set()

        self.results['exploration'] = len(self.algorithm.visited_spaces)
        self.results['sp_from_end'] = self._get_end_distance()

        self.results['past_step_times'].append(step_time - self.last_algorithm_time)
        self.results['avg_step_time'] = round(
            sum(self.results['past_step_times']) / len(self.results['past_step_times']), 2
        )
        self.last_algorithm_time = step_time

        current_mem, peak_mem = tracemalloc.get_traced_memory()
        self.results['past_mem_usages'].append(current_mem / 1024 / 1024)
        self.results['avg_mem_usage'] = round(
            sum(self.results['past_mem_usages']) / len(self.results['past_mem_usages']), 2
        )
        self.results['top_mem_usage'] = max(self.results['top_mem_usage'], round(peak_mem / 1024 / 1024, 2))


    def _get_end_distance(self, position: tuple[int, int] = None) -> int:
        """ Helper function for calculating an approximate distance from the end of the maze. """

        position = position if position else self.algorithm.current_pos

        if isinstance(position, tuple):
            return int(
                abs(position[0] - self.maze.end_pos[0]) +
                abs(position[1] - self.maze.end_pos[1])
            )

        return min(
            [self._get_end_distance(pos) for pos in position if pos is not None]
        )


    def _get_text_display(self, coloring: bool) -> str:
        """ Helper function for generating the text progress display. """

        if not coloring:
            progress = f'Total Time: {self.results["total_time"]} sec | ' \
                       f'Solve Time: {self.results["solve_time"]} sec | ' \
                       f'Steps: {self.results["steps_taken"]} / {self.max_steps} | ' \
                       f'Explored: {self.results["exploration"]} spaces | ' \
                       f'Progress: ~{self.results["sp_from_end"]} spaces from end'

        else:
            progress = f'Total Time: {Text.li_blue}{self.results["total_time"]}{Rest.all} sec | ' \
                       f'Solve Time: {Text.li_blue}{self.results["solve_time"]}{Rest.all} sec | ' \
                       f'Steps: {Text.li_cyan}{self.results["steps_taken"]}{Rest.all} / ' \
                                           f'{Text.li_cyan}{self.max_steps}{Rest.all} | ' \
                       f'Explored: {Text.li_yellow}{self.results["exploration"]}{Rest.all} spaces | ' \
                       f'Progress: ~{Text.li_green}{self.results["sp_from_end"]}{Rest.all} spaces from end'

        if self.progress_display == 'detailed':
            if not coloring:
                progress += f' | ' \
                            f'Solved: {self.results["reached_end"]} | ' \
                            f'Average Step Time: {self.results["avg_step_time"]} sec | ' \
                            f'Average Mem Usage: {self.results["avg_mem_usage"]} MB | ' \
                            f'Peak Mem Usage: {self.results["top_mem_usage"]} MB'

            else:
                progress += f' | ' \
                            f'Solved: {Text.li_red}{self.results["reached_end"]}{Rest.all} | ' \
                            f'Average Step Time: {Text.li_magenta}{self.results["avg_step_time"]}{Rest.all} sec | ' \
                            f'Average Mem Usage: {Text.li_magenta}{self.results["avg_mem_usage"]}{Rest.all} MB | ' \
                            f'Peak Mem Usage: {Text.li_magenta}{self.results["top_mem_usage"]}{Rest.all} MB'

        return progress


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

        maze_display = ''
        for row in range(self.maze.size_matrix):
            for col in range(self.maze.size_matrix):

                space = self.maze.matrix[row][col]

                if space == self.maze.wall:
                    maze_display += space_wall
                elif (row, col) == self.algorithm.current_pos \
                        or isinstance(self.algorithm.current_pos, list) \
                        and (row, col) in self.algorithm.current_pos:
                    maze_display += space_current
                elif (row, col) == self.maze.end_pos:
                    maze_display += space_end
                elif (row, col) in self.algorithm.visited_spaces:
                    maze_display += space_visited
                else:
                    maze_display += space_path

            maze_display += '\n'

        return maze_display


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
            print(f'\033[{self.maze.size_matrix * 2}A\033[2K', end = '')

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

        algorithm_name = self.algorithm.__class__.__name__
        bar = '=' * len(algorithm_name)

        if coloring and (option == 'console' or option == 'string'):
            results = f'  MAZE INFORMATION \n' \
                      f'{Text.yellow}{bar}{Rest.all} \n' \
                      f'{Text.yellow}*{Rest.all} Maze Size        : {Text.li_magenta}{self.maze.size}{Rest.all} ' \
                             f'( {Text.li_magenta}{self.maze.size_matrix}x{self.maze.size_matrix}{Rest.all} ) \n' \
                      f'{Text.yellow}*{Rest.all} Start Position   : {Text.li_green}{self.maze.start_pos}{Rest.all} \n' \
                      f'{Text.yellow}*{Rest.all} End Position     : {Text.li_red}{self.maze.end_pos}{Rest.all} \n' \
                      f'{Text.yellow}{bar}{Rest.all} \n' \
                      f'\n' \
                      f'  {algorithm_name.upper()} RESULTS \n' \
                      f'{Text.yellow}{bar}{Rest.all} \n' \
                      f'{Text.yellow}*{Rest.all} Total Time Taken : {Text.li_blue}{self.results["total_time"]}' \
                             f'{Rest.all} sec \n' \
                      f'{Text.yellow}*{Rest.all} Solve Time Taken : {Text.li_blue}{self.results["solve_time"]}' \
                             f'{Rest.all} sec \n' \
                      f'\n' \
                      f'{Text.yellow}*{Rest.all} Steps Taken      : {Text.li_cyan}{self.results["steps_taken"]}' \
                             f'{Rest.all} / {Text.li_cyan}{self.max_steps}{Rest.all} \n' \
                      f'{Text.yellow}*{Rest.all} Explored         : {Text.li_yellow}{self.results["exploration"]}' \
                             f'{Rest.all} unique spaces \n' \
                      f'{Text.yellow}*{Rest.all} Spaces From End  : {Text.li_green}~{self.results["sp_from_end"]}' \
                             f'{Rest.all} \n' \
                      f'{Text.yellow}*{Rest.all} Reached End      : {Text.li_red}{self.results["reached_end"]}' \
                             f'{Rest.all} \n' \
                      f'\n' \
                      f'{Text.yellow}*{Rest.all} Average Step Time: {Text.li_magenta}{self.results["avg_step_time"]}' \
                             f'{Rest.all} sec \n' \
                      f'{Text.yellow}*{Rest.all} Average Mem Usage: {Text.li_magenta}{self.results["avg_mem_usage"]}' \
                             f'{Rest.all} MB \n' \
                      f'{Text.yellow}*{Rest.all} Peak Mem Usage   : {Text.li_magenta}{self.results["top_mem_usage"]}' \
                             f'{Rest.all} MB \n' \
                      f'{Text.yellow}{bar}{Rest.all}'

        else:
            results = f'  MAZE INFORMATION \n' \
                      f'{bar} \n' \
                      f'* Maze Size        : {self.maze.size} ( {self.maze.size_matrix}x{self.maze.size_matrix} ) \n' \
                      f'* Start Position   : {self.maze.start_pos} \n' \
                      f'* End Position     : {self.maze.end_pos} \n' \
                      f'{bar} \n' \
                      f'\n' \
                      f'  {algorithm_name.upper()} RESULTS \n' \
                      f'{bar} \n' \
                      f'* Total Time Taken : {self.results["total_time"]} sec \n' \
                      f'* Solve Time Taken : {self.results["solve_time"]} sec \n' \
                      f'\n' \
                      f'* Steps Taken      : {self.results["steps_taken"]} / {self.max_steps} \n' \
                      f'* Explored         : {self.results["exploration"]} unique spaces \n' \
                      f'* Spaces From End  : ~{self.results["sp_from_end"]} \n' \
                      f'* Reached End      : {self.results["reached_end"]} \n' \
                      f'\n' \
                      f'* Average Step Time: {self.results["avg_step_time"]} sec \n' \
                      f'* Average Mem Usage: {self.results["avg_mem_usage"]} MB \n' \
                      f'* Peak Mem Usage   : {self.results["top_mem_usage"]} MB \n' \
                      f'{bar}'

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
