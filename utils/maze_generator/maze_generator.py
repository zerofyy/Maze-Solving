import random

from .maze import Maze


class MazeGenerator:
    """ Static class for generating random mazes. """

    wall: int = 0
    path: int = 1


    @staticmethod
    def _gen_empty_maze(size: int) -> list[list[str | int]]:
        """ Helper function for creating an empty maze. """

        size = size * 2 + 1
        maze = []

        for row in range(1, size + 1):
            if row % 2 == 1:
                maze.append([MazeGenerator.wall for _ in range(size)])
            else:
                maze.append([MazeGenerator.wall if col % 2 == 0 else MazeGenerator.path for col in range(size)])

        return maze


    @staticmethod
    def _gen_maze_paths(maze: list[list[str | int]], size: int) -> list[list[str | int]]:
        """ Helper function for creating paths inside an empty maze. """

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

                maze[row + path_r][col + path_c] = MazeGenerator.path
                continue

            if direction == (0, 2):
                if col == r_limit:
                    direction = -2, 0
                    r_limit -= 2
                    path_r, path_c = -1, 0
                else:
                    path_r, path_c = random.choice(((0, 1), (-1, 0)))

                maze[row + path_r][col + path_c] = MazeGenerator.path
                continue

            if direction == (-2, 0):
                if row == u_limit:
                    direction = 0, -2
                    u_limit += 2
                    path_r, path_c = 0, -1
                else:
                    path_r, path_c = random.choice(((0, -1), (-1, 0)))

                maze[row + path_r][col + path_c] = MazeGenerator.path
                continue

            if direction == (0, -2):
                if col == l_limit:
                    direction = 2, 0
                    l_limit += 2
                    path_r, path_c = 1, 0
                else:
                    path_r, path_c = random.choice(((0, -1), (1, 0)))

                maze[row + path_r][col + path_c] = MazeGenerator.path
                continue

        maze[size][size] = MazeGenerator.path

        return maze


    @staticmethod
    def generate(size: int, start_pos: str, end_pos: str) -> Maze:
        """
        Generate a random maze.

        Start & End Positions:
            top_left, top_right, bottom_left, bottom_right, middle, random, random_corner, random_any.

        Arguments:
            size: Size of the maze.
            start_pos: Starting position in the maze.
            end_pos: Ending position in the maze.

        Returns:
            A randomly generated maze as an object.
        """

        maze = MazeGenerator._gen_empty_maze(size)
        maze = MazeGenerator._gen_maze_paths(maze, size)
        maze = Maze(maze, start_pos, end_pos)

        maze.wall = MazeGenerator.wall
        maze.path = MazeGenerator.path

        return maze


__all__ = ['MazeGenerator']
