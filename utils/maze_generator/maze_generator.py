import random


class MazeGenerator:
    """ Class for generating random mazes. """

    start_coords: tuple[int, int] = None
    end_coords: tuple[int, int] = None
    maze: list[list[str | int]] = None


    def __init__(self, size: int) -> None:
        """
        Create a new instance of the MazeGenerator class.

        Start & End Positions:
            top_left, top_right, bottom_left, bottom_right, middle, random, random_corner, random_any.

        Arguments:
            size: The size of the maze (width and height).
        """

        self.size = size
        self.wall = 'wall'
        self.path = 'path'
        self.set_start_end_coords(start_pos = 'top_left', end_pos = 'bottom_right')


    def set_start_end_coords(self, start_pos : str, end_pos: str) -> None:
        """
        Change the start and end coordinates.

        Start & End Positions:
            top_left, top_right, bottom_left, bottom_right, middle, random, random_corner, random_any.

        Arguments:
            start_pos: Starting position of the maze.
            end_pos: Ending position of the maze.
        """

        if start_pos == end_pos and not start_pos.startswith('random'):
            raise Exception('Start and end positions cannot be the same.')

        size = self.size
        border_l, border_r = 1, size * 2 - 1

        crds = {
            'top_left' : (border_l, border_l), 'top_right' : (border_l, border_r),
            'bottom_left' : (border_r, border_l), 'bottom_right' : (border_r, border_r),
            'middle' : (size, size),
            'random_any' : [(r, c) for r in range(1, border_r, 2) for c in range(1, border_r, 2)]
        }

        crds['random_corner'] = [crds['top_left'], crds['top_right'], crds['bottom_left'], crds['bottom_right']]
        crds['random'] = crds['random_corner'] + [crds['middle']]

        if start_pos.startswith('random') and end_pos.startswith('random'):
            start_crds = random.choice(crds[start_pos])
            if start_crds in crds[end_pos]:
                crds[end_pos].remove(start_crds)
            end_crds = random.choice(crds[end_pos])

        elif start_pos.startswith('random'):
            end_crds = crds[end_pos]
            if end_crds in crds[start_pos]:
                crds[start_pos].remove(end_crds)
            start_crds = random.choice(crds[start_pos])

        elif end_pos.startswith('random'):
            start_crds = crds[start_pos]
            if start_pos in crds[end_pos]:
                crds[end_pos].remove(start_crds)
            end_crds = random.choice(crds[end_pos])

        else:
            start_crds = crds[start_pos]
            end_crds = crds[end_pos]

        self.start_coords = start_crds
        self.end_coords = end_crds


    def _gen_empty_maze(self, size: int) -> list[list[str | int]]:
        """ Helper function for creating an empty maze. """

        size = size * 2 + 1
        maze = []

        for row in range(1, size + 1):
            if row % 2 == 1:
                maze.append([self.wall for _ in range(size)])
            else:
                maze.append([self.wall if col % 2 == 0 else self.path for col in range(size)])

        return maze


    def _gen_maze_paths(self, maze: list[list[str | int]], size: int) -> list[list[str | int]]:
        """ Helper function for creating paths through an empty maze. """

        u_limit, d_limit, l_limit, r_limit = 1, size * 2 - 1, 3, size * 2 - 1
        direction = 2, 0
        row, col = -1, 1

        for _ in range(size ** 2):
            row, col = row + direction[0], col + direction[1]

            if direction == (2, 0):
                if row == d_limit:
                    direction = 0, 2
                    d_limit -= 2
                    path_r, path_c = 0, 1
                else:
                    path_r, path_c = random.choice(((1, 0), (0, 1)))

                maze[row + path_r][col + path_c] = self.path
                continue

            if direction == (0, 2):
                if col == r_limit:
                    direction = -2, 0
                    r_limit -= 2
                    path_r, path_c = -1, 0
                else:
                    path_r, path_c = random.choice(((0, 1), (-1, 0)))

                maze[row + path_r][col + path_c] = self.path
                continue

            if direction == (-2, 0):
                if row == u_limit:
                    direction = 0, -2
                    u_limit += 2
                    path_r, path_c = 0, -1
                else:
                    path_r, path_c = random.choice(((0, -1), (-1, 0)))

                maze[row + path_r][col + path_c] = self.path
                continue

            if direction == (0, -2):
                if col == l_limit:
                    direction = 2, 0
                    l_limit += 2
                    path_r, path_c = 1, 0
                else:
                    path_r, path_c = random.choice(((0, -1), (1, 0)))

                maze[row + path_r][col + path_c] = self.path
                continue

        maze[size][size] = self.path

        return maze


    def generate(self) -> list[list[int | str]]:
        """
        Generate a random maze.

        Returns:
            A matrix representation of a maze.
        """

        maze = self._gen_empty_maze(self.size)
        maze = self._gen_maze_paths(maze, self.size)

        self.maze = maze
        return maze


__all__ = ['MazeGenerator']
