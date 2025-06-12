import random
from abc import abstractmethod, ABC
import multiprocessing as mp
import time

from utils.maze_generator import Maze


class BaseAlgorithmParallel(ABC):
    """ Abstract class representing a parallel maze solving algorithm. """

    maze: Maze = None
    current_pos: list[tuple[int, int]] = None
    visited_spaces: list[tuple[int, int]] = None
    num_processes: int = None
    shared_state: dict[str | int, ...] = None
    processes: list[mp.Process] = None
    coms_queue: mp.Queue = None


    def setup(self, maze: Maze, num_processes: int = None) -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the Maze class.
            num_processes: Number of processes, defaults to 4 or less.
        """

        self.maze = maze
        self.num_processes = num_processes if num_processes else min(4, mp.cpu_count)
        self.current_pos = [maze.start_pos for _ in range(self.num_processes)]
        self.visited_spaces = [maze.start_pos]

        manager = mp.Manager()
        self.shared_state = manager.dict()
        self.shared_state['is_solved'] = manager.Event()

        for i in range(self.num_processes):
            self.shared_state[i] = manager.dict({
                'current_pos' : maze.start_pos,
                'visited_spaces' : manager.list([maze.start_pos]),
                'is_active' : True
            })

        self.processes = []
        self.coms_queue = mp.Queue()
        self._start_processes()


    def _start_processes(self) -> None:
        """ Helper function for starting all processes. """

        maze_data = self.maze.get_maze_data()

        for i in range(self.num_processes):
            process = mp.Process(
                target = self._process_step,
                args = (i, maze_data, self.shared_state, self.coms_queue)
            )
            process.start()
            self.processes.append(process)


    @staticmethod
    @abstractmethod
    def _process_step(process_id: int, maze_data: dict[str, ...], shared_state: dict[str | int, ...],
                      coms_queue: mp.Queue) -> None:
        """ Static helper function for taking steps in the maze. """

        while True:
            try:
                command = coms_queue.get(timeout = 0.5)
                if command == 'STOP':
                    break

                if shared_state['is_solved'].is_set():
                    return None

                state = shared_state[process_id]
                if not state['is_active']:
                    return None

                current_pos = state['current_pos']
                visited_spaces = list(state['visited_spaces'])

                if not BaseAlgorithmParallel.can_take_step(current_pos, maze_data):
                    state['is_active'] = False
                    return None

                legal_moves = BaseAlgorithmParallel.get_legal_moves(current_pos, maze_data)
                # if process_id <= len(legal_moves) - 1:
                #     current_pos = legal_moves[process_id]
                # else:
                #     current_pos = legal_moves[0]
                for space in visited_spaces:
                    if space in legal_moves:
                        legal_moves.remove(space)
                if legal_moves:
                    random.seed(time.time() + process_id)
                    current_pos = random.choice(legal_moves)
                else:
                    random.seed(time.time() + process_id)
                    current_pos = random.choice(BaseAlgorithmParallel.get_legal_moves(current_pos, maze_data))

                if current_pos not in visited_spaces:
                    state['visited_spaces'].append(current_pos)

                state['current_pos'] = current_pos

            except:
                if shared_state['is_solved'].is_set():
                    break


    @staticmethod
    def get_legal_moves(current_pos: tuple[int, int], maze_data: dict[str, ...]) -> list[tuple[int, int]]:
        """
        Get a list of legal moves (coordinates) from the current position.

        Arguments:
            current_pos: Coordinates of the current position in the maze.
            maze_data: The maze instance data.
        """

        check_moves = [
            (current_pos[0] - 1, current_pos[1]),
            (current_pos[0] + 1, current_pos[1]),
            (current_pos[0], current_pos[1] - 1),
            (current_pos[0], current_pos[1] + 1)
        ]

        return [
            move for move in check_moves
            if 0 <= move[0] < maze_data['size_matrix'] and 0 <= move[1] < maze_data['size_matrix']
            and maze_data['maze'][move[0]][move[1]] == maze_data['path']
        ]


    @staticmethod
    def can_take_step(current_pos: tuple[int, int], maze_data: dict[str, ...]) -> bool:
        """
        Check whether a step can be taken.

        Arguments:
            current_pos: Coordinates of the current position in the maze.
            maze_data: The maze instance data.
        """

        return current_pos != maze_data['end_pos'] and BaseAlgorithmParallel.get_legal_moves(current_pos, maze_data)


    @abstractmethod
    def step(self) -> list[tuple[int, int]] | None:
        """
        Take steps in the maze.

        Returns:
            The coordinates of all chosen directions from each process or None.
            None may be returned if there are no legal moves, the end position
            in the maze is reached, or no processes are active.
        """

        if self.shared_state['is_solved'].is_set():
            return None

        active_processes = sum(1 for i in range(self.num_processes)
                               if self.shared_state[i]['is_active'])
        if active_processes == 0:
            return None

        for _ in range(active_processes):
            self.coms_queue.put('STEP')

        for i in range(active_processes):
            current_pos = self.shared_state[i]['current_pos']
            self.current_pos[i] = current_pos

            if current_pos not in self.visited_spaces:
                self.visited_spaces.append(current_pos)

            if current_pos == self.maze.end_pos:
                self.shared_state['is_solved'].set()

        return self.current_pos


    def cleanup(self) -> None:
        """ Cleanup processes and resources. """

        if self.processes:
            for _ in range(len(self.processes)):
                try:
                    self.coms_queue.put('STOP')
                except:
                    pass

            for process in self.processes:
                process.join(timeout = 0.5)
                if process.is_alive():
                    process.terminate()
                    process.join()

            self.processes.clear()


    def __del__(self):
        """ Cleanup processes and resources when object is deleted. """

        self.cleanup()


__all__ = ['BaseAlgorithmParallel']
