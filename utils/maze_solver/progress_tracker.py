import time
from sty import fg as Text, bg as Back, rs as Rest

from utils.algorithms import BaseAlgorithmSequential, BaseAlgorithmParallel
from utils.maze_generator import Maze


class ProgressTracker:
    """ Class for tracking progress of running algorithms. """

    time_start: float = None


    def __init__(self, algorithm: BaseAlgorithmSequential | BaseAlgorithmParallel,
                 maze: Maze, max_steps: int, progress_display: str | None) -> None:
        """
        Create a new instance of the ProgressTracker class.

        Progress Display Options:
            - 'text' | Show the algorithm's progress in text only.
            - 'visual' | Show the algorithm's progress in text along with a visual representation of the maze.
            - None | No real time progression display.

        Arguments:
            algorithm: The algorithm whose progress is being tracked.
            maze: The maze being solved.
            max_steps: The maximum number of allowed steps.
            progress_display: The type of progress to display.
        """

        self.algorithm = algorithm
        self.maze = maze
        self.max_steps = max_steps
        self.steps_taken = 0
        self.progress_display = progress_display


    def track(self) -> None:
        """ Start tracking the algorithm's progress. """

        self.time_start = time.time()


    def update(self) -> None:
        """ Update the algorithm's progress after making a step. """

        self.steps_taken += 1


    def _get_end_distance(self, current_pos: tuple[int, int] | list[tuple[int, int]]) -> int:
        """ Helper function for calculating the distance from the end position in the maze. """

        if isinstance(current_pos, tuple):
            return int(
                abs(current_pos[0] - self.maze.end_pos[0]) +
                abs(current_pos[1] - self.maze.end_pos[1])
            )

        return max(
            [self._get_end_distance(pos) for pos in current_pos]
        )


    def get_progress(self, return_str: bool = False, clear_print: bool = True, coloring: bool = True) -> str | None:
        """
        Get the progress of the currently running algorithm.

        Arguments:
            return_str: Whether to return the progress as a string.
                        Setting this to False will print the progress to the console.
            clear_print: Whether to clear the console when printing.
            coloring: Whether to use colors for the progress display.
        """

        if self.progress_display is None:
            return '' if return_str else None

        time_passed = round(time.time() - self.time_start, 2)
        end_distance = self._get_end_distance(self.algorithm.current_pos)

        if coloring:
            if end_distance > 15:
                distance_color = Text.li_red
            elif end_distance >= 10:
                distance_color = Text.li_yellow
            else:
                distance_color = Text.li_green
            progress = f'Time: {Text.li_blue}{time_passed} sec{Rest.all} | ' \
                       f'Steps: {Text.li_magenta}{self.steps_taken}{Rest.all}' \
                       f'/{Text.li_magenta}{self.max_steps}{Rest.all} | ' \
                       f'Visited {Text.li_yellow}{len(self.algorithm.visited_spaces)}{Rest.all} unique spaces | ' \
                       f'About {distance_color}{end_distance}{Rest.all} spaces away from the end'
        else:
            progress = f'Time: {time_passed} sec | ' \
                       f'Steps: {self.steps_taken}/{self.max_steps} | ' \
                       f'Visited {len(self.algorithm.visited_spaces)} unique spaces | ' \
                       f'About {end_distance} spaces away from the end'

        if self.progress_display == 'visual':
            if coloring:
                space_wall = f'{Back.li_blue}   {Rest.all}'
                space_path = f'{Back.black}   {Rest.all}'
                space_current = f'{Back.li_green}   {Rest.all}'
                space_end = f'{Back.li_red}   {Rest.all}'
                space_visited = f'{Back.li_yellow}   {Rest.all}'
            else:
                space_wall = '[/]'
                space_path = '   '
                space_current = ' + '
                space_end = ' ! '
                space_visited = ' . '

            maze_display = ''
            for row in range(self.maze.size_matrix):
                for col in range(self.maze.size_matrix):

                    space = self.maze.maze[row][col]
                    if space == self.maze.wall:
                        maze_display += space_wall
                    elif (row, col) == self.algorithm.current_pos:
                        maze_display += space_current
                    elif (row, col) == self.maze.end_pos:
                        maze_display += space_end
                    elif (row, col) in self.algorithm.visited_spaces:
                        maze_display += space_visited
                    else:
                        maze_display += space_path

                maze_display += '\n'

            progress += f'\n{maze_display}{Rest.all}'

        if return_str:
            return progress

        if clear_print:
            print(f'\033[{self.maze.size ** 2}A\033[2K', end = '')

        print(progress)


__all__ = ['ProgressTracker']
