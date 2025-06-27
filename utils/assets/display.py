import os

from utils.maze_generator import Maze
from .coloring import Coloring
from utils.algorithms import BaseAlgorithmSequential, BaseAlgorithmParallel


class Display:
    """ Displaying terminal text and visuals. """

    matrix: list[list[str]] = None


    def __init__(self, algorithm: BaseAlgorithmSequential | BaseAlgorithmParallel, maze: Maze,
                 text_display: bool = True, maze_display: bool = True) -> None:
        """
        Create a new instance of the Display class.

        Arguments:
            algorithm: The algorithm currently solving the maze.
            maze: Maze instance.
            text_display: Whether the text display is enabled.
            maze_display: Whether the maze display is enabled.
        """

        self.maze = maze
        self.algorithm = algorithm

        try:
            self.width = os.get_terminal_size().columns
            self.height = os.get_terminal_size().lines
        except OSError:
            self.width = 200
            self.height = 50

        self.clear()
        print('\033[?25l', end = '')  # Hide cursor

        self.text_display = text_display
        self.maze_display = maze_display

        if text_display and not maze_display:
            self.text_bound = 0, 0, self.height, self.width
        if maze_display and not text_display:
            self.maze_bound = 0, 0, self.height, self.width
        if text_display and maze_display:
            self.text_bound = 0, int(self.width * 0.7) + 5, self.height, self.width
            self.maze_bound = 0, 0, self.height, int(self.width * 0.7)

        self.char_wall = '[bglb]   [rs]', '[/]'
        self.char_path = '[rs]   [rs]', '   '
        self.char_curr = '[bglg]   [rs]', ' + '
        self.char_vist = '[bgly]   [rs]', ' - '
        self.char_end = '[bglr]   [rs]', '<=>'


    def clear(self, soft_clear: bool = False) -> None:
        """
        Clear the display.

        Arguments:
             soft_clear: If True, clears the display matrix and moves the cursor to the top left,
             but does not clear the terminal screen.
        """
        self.matrix = [[' ' for _ in range(self.width)] for _ in range(self.height)]

        if not soft_clear:
            print('\033[2J', end = '')
        print('\033[H', end = '')


    def _update_text(self, text: str) -> None:
        """ Helper function for updating the text display. """

        for i, line in enumerate(text.split('\n')):
            row, col = self.text_bound[0] + i + 1, self.text_bound[1]

            if i >= self.text_bound[2] or row >= self.text_bound[2]:
                break

            line_crop = Coloring.cut(line, self.text_bound[3] - self.text_bound[1])
            for char in Coloring.chars(line_crop):
                self.matrix[row][col] = char
                col += 1


    def _update_maze(self, coloring: bool) -> None:
        """ Helper function for updating the maze display. """

        current_pos = self.algorithm.get_current_pos() if isinstance(self.algorithm, BaseAlgorithmSequential) \
            else self.algorithm.get_current_pos(best_pos = True)
        process_pos = self.algorithm.get_current_pos() if isinstance(self.algorithm, BaseAlgorithmParallel) \
            else []
        visited_pos = self.algorithm.get_visited_pos()

        bound_t, bound_l, bound_b, bound_r = self.maze_bound

        box_h = bound_b - bound_t
        box_w = bound_r - bound_l

        visible_rows, visible_cols = box_h, box_w // 3
        start_row = current_pos[0] - visible_rows // 2
        start_col = current_pos[1] - visible_cols // 2
        maze_rows = maze_cols = self.maze.size * 2 + 1

        if start_row < 0:
            start_row = 0
        elif start_row + visible_rows > maze_rows:
            start_row = max(0, maze_rows - visible_rows)

        if start_col < 0:
            start_col = 0
        elif start_col + visible_cols > maze_cols:
            start_col = max(0, maze_cols - visible_cols)

        color_code = 0 if coloring else 1

        for row in range(box_h):
            maze_row = start_row + row
            if row >= maze_rows:
                break

            col = bound_l
            for maze_col_idx in range(visible_cols):
                maze_col = start_col + maze_col_idx
                if maze_col >= maze_cols or col + 2 >= bound_r:
                    break

                pos = (maze_row, maze_col)
                if pos == current_pos or pos in process_pos:
                    char = self.char_curr
                elif pos == self.maze.end_pos:
                    char = self.char_end
                elif self.maze.matrix[maze_row][maze_col] == self.maze.wall:
                    char = self.char_wall
                elif pos in visited_pos:
                    char = self.char_vist
                else:
                    char = self.char_path

                if col + 2 < bound_r and bound_t + row < bound_b:
                    chars = Coloring.chars(char[color_code])
                    self.matrix[bound_t + row][col + 0] = chars[0]
                    self.matrix[bound_t + row][col + 1] = chars[1]
                    self.matrix[bound_t + row][col + 2] = chars[2]

                col += 3


    def update(self, text: str = None, maze_colors: bool = True) -> None:
        """
        Update the terminal display.

        Arguments:
            text: Text to display, if any. The text display option should be turned on for this to work.
            maze_colors: Whether to use colors for the maze display.
        """

        self.clear(soft_clear = True)

        if self.text_display and text:
            self._update_text(text)
        if self.maze_display:
            self._update_maze(maze_colors)

        lines = [''.join(line) + '\n' for line in self.matrix]
        print(Coloring.color(''.join(lines)), end = '')


__all__ = ['Display']
