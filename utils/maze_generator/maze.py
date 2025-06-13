import random


class Maze:
    """ Class representing a generated maze. """

    start_pos: tuple[int, int] = None
    end_pos: tuple[int, int] = None
    wall: int = None
    path: int = None


    def __init__(self, maze: list[list[int]], start_pos: str, end_pos: str) -> None:
        """
        Create a new instance of the Maze class.

        Start & End Positions:
            top_left, top_right, bottom_left, bottom_right, middle, random, random_corner, random_any.

        Arguments:
            maze: A 2D binary matrix representing a maze (0 = wall, 1 = path).
            start_pos: Starting position in the maze.
            end_pos: Ending position in the maze.
        """

        self.matrix = maze
        self.size_matrix = len(maze)
        self.size = (self.size_matrix - 1) // 2
        self.set_start_end_coords(start_pos, end_pos)


    def set_start_end_coords(self, start_pos : str, end_pos: str) -> None:
        """
        Change the start and end coordinates.

        Start & End Positions:
            top_left, top_right, bottom_left, bottom_right, middle, random, random_corner, random_any.

        Arguments:
            start_pos: Starting position in the maze.
            end_pos: Ending position in the maze.
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

        self.start_pos = start_crds
        self.end_pos = end_crds


    def get_maze_data(self) -> dict[str, ...]:
        """ Get the maze data as a dictionary. """

        return {
            'matrix': self.matrix,
            'start_pos': self.start_pos,
            'end_pos': self.end_pos,
            'wall': self.wall,
            'path': self.path,
            'size_matrix': self.size_matrix,
            'size': self.size
        }


__all__ = ['Maze']
