from abc import abstractmethod, ABC
import multiprocessing as mp

from utils.maze_generator import Maze


class SharedState:
    """ Class for managing shared states between processes. """

    def __init__(self, num_processes: int) -> None:
        """
        Create a new instance of the SharedState class.

        Arguments:
            num_processes: The number of processes sharing the state.
        """

        self.manager = mp.Manager()
        self.solved = self.manager.Event()
        self.states = self.manager.dict()
        self.step_lock = self.manager.Lock()

        for i in range(num_processes):
            self.states[i] = {
                'current_pos' : None,
                'visited_spaces' : self.manager.list(),
                'is_active' : True
            }


class BaseAlgorithmParallel(ABC):
    """ Abstract class representing a parallel maze solving algorithm. """

    maze: Maze = None
    current_pos: list[tuple[int, int]] = None
    visited_spaces: list[tuple[int, int]] = None
    num_processes: int = None
    shared_state: SharedState = None
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

        self.shared_state = SharedState(self.num_processes)
        for i in range(self.num_processes):
            self.shared_state.states[i]['current_pos'] = maze.start_pos
            self.shared_state.states[i]['visited_spaces'].append(maze.start_pos)

        self.processes = []
        self.coms_queue = mp.Queue()
        self._start_processes()


    def _start_processes(self) -> None:
        """ Helper function for starting all processes. """

        for i in range(self.num_processes):
            process = mp.Process(
                target = self._process_step,
                args = (i, self.maze, self.shared_state, self.coms_queue)
            )
            process.start()
            self.processes.append(process)


    @staticmethod
    @abstractmethod
    def _process_step(process_id: int, maze: Maze, shared_state: SharedState,
                      coms_queue: mp.Queue) -> tuple[int, int] | None:
        """ Static helper function for taking steps in the maze. """

        while True:
            try:
                command = coms_queue.get(timeout = 0.5)
                if command == 'STOP':
                    break

                if shared_state.solved.is_set():
                    return None

                state = shared_state.states[process_id]
                if not state['active']:
                    return None

                current_pos = state['current_pos']
                visited_spaces = list(state['visited_spaces'])

                if not BaseAlgorithmParallel.can_take_step(current_pos, maze):
                    state['active'] = False
                    return None

                legal_moves = BaseAlgorithmParallel.get_legal_moves(current_pos, maze)
                if process_id <= len(legal_moves) - 1:
                    current_pos = legal_moves[process_id]
                else:
                    current_pos = legal_moves[0]

                if current_pos not in visited_spaces:
                    state['visited_spaces'].append(current_pos)

                return current_pos

            except:
                if shared_state.solved.is_set():
                    break


    @staticmethod
    def get_legal_moves(current_pos: tuple[int, int], maze: Maze) -> list[tuple[int, int]]:
        """
        Get a list of legal moves (coordinates) from the current position.

        Arguments:
            current_pos: Coordinates of the current position in the maze.
            maze: The maze instance.
        """

        check_moves = [
            (current_pos[0] - 1, current_pos[1]),
            (current_pos[0] + 1, current_pos[1]),
            (current_pos[0], current_pos[1] - 1),
            (current_pos[0], current_pos[1] + 1)
        ]

        return [
            move for move in check_moves
            if 0 <= move[0] < maze.size_matrix and 0 <= move[1] < maze.size_matrix
            and maze.maze[move[0]][move[1]] == maze.path
        ]


    @staticmethod
    def can_take_step(current_pos: tuple[int, int], maze) -> bool:
        """
        Check whether a step can be taken.

        Arguments:
            current_pos: Coordinates of the current position in the maze.
            maze: The maze instance.
        """

        return current_pos != maze.end_pos and BaseAlgorithmParallel.get_legal_moves(current_pos, maze)


    @abstractmethod
    def step(self) -> list[tuple[int, int]] | None:
        """
        Take steps in the maze.

        Returns:
            The coordinates of all chosen directions from each process or None.
            None may be returned if there are no legal moves, the end position
            in the maze is reached, or no processes are active.
        """

        if self.shared_state.solved.is_set():
            return None

        active_processes = sum(1 for i in range(self.num_processes)
                               if self.shared_state.states[i]['active'])
        if active_processes == 0:
            return None

        for _ in range(active_processes):
            self.coms_queue.put('STEP')

        for i in range(active_processes):
            current_pos = self.shared_state.states[0]['current_pos']
            self.current_pos[i] = current_pos

            if current_pos not in self.visited_spaces:
                self.visited_spaces.append(current_pos)

            if current_pos == self.maze.end_pos:
                self.shared_state.solved.set()

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
