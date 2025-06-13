import time
from abc import abstractmethod, ABC
import multiprocessing as mp

from utils.maze_generator import Maze


class BaseAlgorithmParallel(ABC):
    """ Abstract class representing a parallel maze solving algorithm. """

    maze_data: dict[str, ...] = None
    current_pos: list[tuple[int, int]] = None
    visited_spaces: list[tuple[int, int]] = None

    num_processes: int = None
    processes: list[mp.Process] = None

    manager: mp.Manager = None
    shared_memory: dict[str | int, ...] = None
    com_queue: mp.Queue = None


    def setup(self, maze: Maze, num_processes: int = 4) -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the Maze class.
            num_processes: Number of processes, defaults to 4 or less.
        """

        self.maze_data = maze.get_maze_data()
        self.num_processes = min(num_processes, mp.cpu_count()) if num_processes else min(4, mp.cpu_count())
        self.current_pos = [maze.start_pos for _ in range(self.num_processes)]
        self.visited_spaces = [maze.start_pos]

        self.manager = mp.Manager()
        self.shared_memory = self.manager.dict()
        self.shared_memory['reached_end'] = self.manager.Event()
        self.shared_memory['visited_spaces'] = self.manager.list([maze.start_pos])
        self.shared_memory['step_logic'] = self._step_logic

        for i in range(self.num_processes):
            self.shared_memory[i] = self.manager.dict({
                'current_pos' : maze.start_pos,
                'is_active' : True
            })

        self.processes = []
        self.com_queue = mp.Queue()
        self._start_processes()


    def _start_processes(self) -> None:
        """ Helper function for starting all processes. """

        for i in range(self.num_processes):
            process = mp.Process(
                target = self._process_step,
                args = (i, self.maze_data, self.shared_memory, self.com_queue)
            )
            process.start()
            self.processes.append(process)


    @staticmethod
    def is_at_end(position: tuple[int, int], maze_data: dict[str, ...]) -> bool:
        """
        Check whether the current position matches the end position.

        Arguments:
            position: A specific position to check for legal moves.
            maze_data: The maze data.
        """

        return position == maze_data['end_pos']


    @staticmethod
    def get_legal_moves(position: tuple[int, int], maze_data: dict[str, ...]) -> list[tuple[int, int]]:
        """
        Get a list of legal moves (coordinates) from the current position.

        Arguments:
            position: A specific position to check for legal moves.
            maze_data: The maze data.
        """

        if position is None:
            return []

        if BaseAlgorithmParallel.is_at_end(position, maze_data) \
                or maze_data['matrix'][position[0]][position[1]] == maze_data['wall']:
            return []

        check_moves = [
            (position[0] - 1, position[1]),
            (position[0] + 1, position[1]),
            (position[0], position[1] - 1),
            (position[0], position[1] + 1)
        ]

        return [
            move for move in check_moves
            if 0 <= move[0] < maze_data['size_matrix'] and 0 <= move[1] < maze_data['size_matrix']
            and maze_data['matrix'][move[0]][move[1]] == maze_data['path']
        ]


    @staticmethod
    def _process_step(process_id: int, maze_data: dict[str, ...],
                      shared_memory: dict[str | int, ...], com_queue: mp.Queue) -> None:
        """ Static helper function for taking steps in the maze. """

        while True:

            if shared_memory['reached_end'].is_set() or not shared_memory[process_id]['is_active']:
                break

            try:
                command = com_queue.get(timeout = 0.5)
                if command == 'STOP':
                    shared_memory[process_id]['current_pos'] = None
                    break

                if command != 'STEP':
                    continue

                shared_memory['step_logic'](process_id, maze_data, shared_memory)
            except:
                pass


    def _build_status_dict(self) -> dict[str, ...]:
        """ Helper function for creating a feedback dictionary for the step function. """

        return {
            'reached_end' : self.shared_memory['reached_end'].is_set(),
            'active_processes' : sum(1 for i in range(self.num_processes) if self.shared_memory[i]['is_active'])
        }


    def step(self) -> tuple[list[tuple[int, int]] | None, dict[str, ...]]:
        """
        Send a command to all active processes to take a step in the maze.

        Returns:
            A tuple containing information about the new step in **new_positions | None, reached_end** format.
            The first element is a list of tuples with the coordinates of the new positions or None if there
            are no legal moves. The second element is a dictionary containing information about the processes
            and whether the end of the maze has been reached.
        """

        status = self._build_status_dict()
        if status['active_processes'] == 0 or status['reached_end']:
            return None, status

        for i in range(self.num_processes):
            if not self.shared_memory[i]['is_active']:
                continue

            if not self.get_legal_moves(self.shared_memory[i]['current_pos'], self.maze_data):
                self.com_queue.put('STOP')
                continue

            self.com_queue.put('STEP')

        time.sleep(0.03)

        for i in range(self.num_processes):
            if not self.shared_memory[i]['is_active']:
                continue
            new_pos = self.shared_memory[i]['current_pos']

            self.current_pos[i] = new_pos
            if new_pos not in self.visited_spaces:
                self.visited_spaces.append(new_pos)
            if new_pos not in list(self.shared_memory['visited_spaces']):
                self.shared_memory['visited_spaces'].append(new_pos)
            if new_pos == self.maze_data['end_pos']:
                self.shared_memory['reached_end'].set()

        return self.current_pos, self._build_status_dict()


    @staticmethod
    @abstractmethod
    def _step_logic(process_id: int, maze_data: dict[str, ...], shared_memory: dict[str | int, ...]) -> None:
        """
        Logic for choosing the next move from the current position with the assumption that
        there is at least one legal move from the current position. Only the logic for the
        step should be implemented here, nothing more (ex. updating visited_spaces).

        Arguments:
            process_id: ID of the process calling this function.
            maze_data: The maze data.
            shared_memory: Shared memory dictionary.

        The function must set **shared_memory[process_id]['current_pos']** to the new position
        after choosing the next step. The function must not manipulate with other variables
        within the shared memory.
        """


    def cleanup(self) -> None:
        """ Cleanup processes and resources. """

        if not self.processes:
            return

        for _ in range(len(self.processes)):
            try:
                self.com_queue.put('STOP')
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
