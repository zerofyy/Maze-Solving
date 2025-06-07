import random


class MazeGenerator:
    """ Class for generating random mazes. """

    def __init__(self, wall_symbol: str | int, path_symbol: str | int) -> None:
        """
        Create a new instance of the MazeGenerator class.

        Note:
            Do NOT set either symbol to "?" .

        Arguments:
            wall_symbol: Representation of a wall space.
            path_symbol: Representation of a path space.
        """

        self.wall = wall_symbol
        self.path = path_symbol
        self.path_temp = '?'


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


    def _gen_maze_paths(self, maze: list[list[...]]) -> list[list[...]]:
        """ Helper function for creating paths through an empty maze. """

        width, height = len(maze[0]) - 1, len(maze) - 1
        u_limit, d_limit, l_limit, r_limit = 0, height, 1, width
        direction = 0, 1
        x, y = 0, -1

        for _ in range(width * height):
            x, y = x + direction[0], y + direction[1]

            if direction == (0, 1):
                if maze[x][y] == self.path:
                    xp, yp = random.choice(((0, 1), (1, 0)))
                    maze[x + xp][y + yp] = self.path_temp
                if y == d_limit:
                    direction = 1, 0
                    d_limit -= 1
                continue

            if direction == (1, 0):
                if maze[x][y] == self.path:
                    xp, yp = random.choice(((0, -1), (1, 0)))
                    maze[x + xp][y + yp] = self.path_temp
                if x == r_limit:
                    direction = 0, -1
                    r_limit -= 1
                continue

            if direction == (0, -1):
                if maze[x][y] == self.path:
                    xp, yp = random.choice(((0, -1), (-1, 0)))
                    maze[x + xp][y + yp] = self.path_temp
                if y == u_limit:
                    direction = -1, 0
                    u_limit += 1
                continue

            if direction == (-1, 0):
                if maze[x][y] == self.path:
                    xp, yp = random.choice(((0, 1), (-1, 0)))
                    maze[x + xp][y + yp] = self.path_temp
                if x == l_limit:
                    direction = 0, 1
                    l_limit += 1
                continue

        for row in range(height + 1):
            for col in range(width + 1):
                if maze[row][col] == self.path_temp:
                    maze[row][col] = self.path

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
        maze = self._gen_maze_paths(maze)

        return maze


__all__ = ['MazeGenerator']
