import random


class MazeGenerator:
    """ Class for generating random mazes. """

    def __init__(self, wall_symbol: str | int, path_symbol: str | int) -> None:
        """
        Create a new instance of the MazeGenerator class.

        Arguments:
            wall_symbol: Representation of a wall space.
            path_symbol: Representation of a path space.
        """

        self.wall = wall_symbol
        self.path = path_symbol


    def _gen_empty_maze(self, width: int, height: int) -> list[list[...]]:
        """ Helper function for creating an empty maze. """

        width = width * 2 + 1
        height = height * 2 + 1
        maze = []

        for row in range(1, height + 1):
            if row % 2 == 1:
                maze.append([self.wall for _ in range(width)])
            else:
                maze.append([self.wall if col % 2 == 1 else self.path for col in range(1, width + 1)])

        return maze


    def _gen_maze_paths(self, maze: list[list[...]], width: int, height: int) -> list[list[...]]:
        """ Helper function for creating paths through an empty maze. """

        u_limit, d_limit, l_limit, r_limit = 1, height * 2 - 1, 3, width * 2 - 1
        direction = 2, 0
        row, col = -1, 1

        for _ in range(width * height):
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

        return maze


    def generate(self, width: int, height: int) -> list[list[...]]:
        """
        Generate a random maze.

        Arguments:
             width: The width of the maze.
             height: The height of the maze.

        Returns:
            A matrix representation of a maze.
        """

        maze = self._gen_empty_maze(width, height)
        maze = self._gen_maze_paths(maze, width, height)

        return maze


__all__ = ['MazeGenerator']



mg = MazeGenerator('🟦', '⬛')
m = mg.generate(4, 10)
for i in m:
    print(''.join(i))
