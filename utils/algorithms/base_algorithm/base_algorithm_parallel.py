import time
from abc import abstractmethod, ABC
import multiprocessing as mp

from utils.maze_generator import Maze


class BaseAlgorithmParallel(ABC):
    """ Abstract representation of a parallel maze solving algorithm. """

    maze: Maze = None
    maze_data: dict[str, ...] = None
    num_processes: int = None
    processes: list[mp.Process] = None
    manager: mp.Manager = None
    memory: dict[str | int, ...] = None


    def setup(self, maze: Maze, num_processes: int = 4) -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the Maze class.
            num_processes: Number of processes, defaults to 4 or less.
        """

        self.maze = maze
        self.maze_data = maze.get_maze_data()
        self.num_processes = min(num_processes, mp.cpu_count()) if num_processes else min(4, mp.cpu_count())
        self.processes = []

        self.manager = mp.Manager()
        self.memory = self.manager.dict({
            'visited_pos' : self.manager.list([maze.start_pos]),
            'reached_end' : False,
            'lock' : self.manager.Lock()
        })

        for i in range(self.num_processes):
            self.memory[i] = self.manager.dict({
                'current_pos' : maze.start_pos,
                'is_active' : True,
                'step_flag' : False,
                'response' : None
            })

        self._start_processes()


    def _start_processes(self) -> None:
        """ Start all processes. """

        for pid in range(self.num_processes):
            process = mp.Process(
                target = self._process_step,
                args = (pid, self.maze.get_maze_data(), self.memory, self._step_logic, self._after_step)
            )
            process.start()
            self.processes.append(process)


    @staticmethod
    def is_at_end(curr_position: tuple[int, int], maze_data: dict[str, ...]) -> bool:
        """
        Check whether the algorithm's current position matches the maze end position.

        Arguments:
            curr_position: The algorithm's current position.
            maze_data: The maze data.
        """

        return curr_position == maze_data['end_pos']


    @staticmethod
    def get_legal_moves(position: tuple[int, int], maze_data: dict[str, ...]) -> list[tuple[int, int]]:
        """
        Get a list of legal moves.

        Arguments:
            position: A specific position to check for legal moves.
            maze_data: The maze data.

        Returns:
            A list of new positions that can be visited from the specified position. If no legal moves
            exist, the list will be empty.
        """

        if BaseAlgorithmParallel.is_at_end(position, maze_data):
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


    def get_current_pos(self, best_pos: bool = False) -> list[tuple[int, int]] | tuple[int, int]:
        """
        Get the current position of each process from the algorithm.

        This function should be overwritten if the `'current_pos'` keys in the algorithm's memory are modified.
        Regardless of the modifications, the return type must remain the same.

        Arguments:
            best_pos: Whether to return the best position out of all processes.

        Returns:
            The coordinates of the current positions in the maze, or the position closest to the end if
            best_pos is set to True.
        """

        if not best_pos:
            return [self.memory[pid]['current_pos'] for pid in range(self.num_processes)]

        best_pos, best_dist = self.memory[0]['current_pos'], float('inf')
        for pid in range(self.num_processes):
            dist = abs(self.memory[pid]['current_pos'][0] - self.maze.end_pos[0]) + \
                   abs(self.memory[pid]['current_pos'][1] - self.maze.end_pos[1])

            if dist < best_dist:
                best_dist = dist
                best_pos = self.memory[pid]['current_pos']

        return best_pos


    def get_visited_pos(self) -> set[tuple[int, int]]:
        """
        Get all the positions previously visited by the algorithm.

        This function should be overwritten if the `'visited_pos'` key in the algorithm's memory is modified.
        Regardless of the modifications, the return type must remain the same.

        Returns:
            A set of coordinates of all visited positions in the maze.
        """

        return set(self.memory['visited_pos'])


    def get_status(self) -> list[tuple[str, ...]]:
        """
        Get information about the algorithm's status.

        By default, this function returns information from the algorithm's memory. If the algorithm's memory
        has been modified - this function should be overwritten to include those modifications in the status
        dictionary (in an appropriate format for real time displays). Regardless of the modifications, the
        return type of this function must remain the same.

        Returns:
            A list with status information.
        """

        status = []

        for pid in range(self.num_processes):
            local_memory = dict(self.memory[pid])

            status.append((f'Process {pid}',
                           '[lg]Active[rs]' if local_memory['is_active'] else '[lr]Inactive[rs]'))
            status.append(('| Current Pos', f'[ly]{local_memory["current_pos"]}[rs]'))
            status.append(('| Step Flag',
                           '[lg]Set[rs]' if local_memory["step_flag"] else '[lr]Unset[rs]'))

            response = local_memory["response"]
            if response is None:
                status.append(('| Response', '[lr]No Response[rs]'))
            else:
                status.append(('| Response', f'[lc]{response}[rs]'))

        status.append(('Visited Pos', f'[ly]{len(self.memory["visited_pos"])}[rs]'))
        status.append(('Reached End', '[lg]Yes[rs]' if self.memory['reached_end'] else '[lr]No[rs]'))

        return status


    @staticmethod
    def _process_step(pid: int, maze_data: dict[str, ...], memory: dict[str | int, ...],
                      step_logic: callable, after_step: callable) -> None:
        """ Internal process logic - keep processes alive and handle communication. """

        while True:
            local_memory = dict(memory[pid])

            if not local_memory['is_active']:
                local_memory['response'] = 'Terminated'
                break

            if memory['reached_end']:
                local_memory['is_active'] = False
                local_memory['response'] = 'Ended'
                break

            if not local_memory['step_flag']:
                continue

            memory[pid]['step_flag'] = False
            memory[pid]['response'] = 'Stepping'
            new_pos = step_logic(pid, maze_data, memory)
            after_step(pid, new_pos, maze_data, memory)
            memory[pid]['response'] = 'Stepped'


    def step(self) -> tuple[tuple[tuple[int, int], ...] | None, bool]:
        """
        Take a step in the maze.

        Returns:
            The new positions after each process takes a step or None if no steps were taken, and a boolean
            value representing whether the end of the maze has been reached.
        """

        if self.memory['reached_end']:
            return None, True

        active_processes = 0

        for pid in range(self.num_processes):

            if not self.memory[pid]['is_active']:
                continue

            if self.get_legal_moves(self.memory[pid]['current_pos'], self.maze_data):
                active_processes += 1
                self.memory[pid]['step_flag'] = True
                self.memory[pid]['response'] = 'Waiting'
            else:
                self.memory[pid]['step_flag'] = False
                self.memory[pid]['is_active'] = False

        time_passed = time.time()
        sleep_time, sleep_max = 0.001, 0.5
        while True:
            responses = sum(1 if self.memory[pid]['response'] == 'Stepped' else 0
                            for pid in range(self.num_processes))

            if responses == active_processes:
                break

            if time.time() - time_passed >= sleep_max:
                if responses >= 1:
                    break
                return None, self.memory['reached_end']

            time.sleep(sleep_time)
            sleep_time *= 1.5

        return tuple(self.memory[pid]['current_pos'] for pid in range(self.num_processes)), self.memory['reached_end']


    @staticmethod
    @abstractmethod
    def _step_logic(pid: int, maze_data: dict[str, ...], memory: dict[str | int, ...]) -> tuple[int, int]:
        """
        Logic for choosing the next move from the current position with the assumption that there's at
        least one legal moves from the current position.

        If anything in the algorithm's memory has been modified (ex. `'current_pos', 'visited_pos'`), then
        the logic for updating those variables should also be implemented here or within the `_after_step()`
        function. Additionally, if memory keys/values are modified, then the relevant functions
        (`get_current_pos()`, `get_visited_pos()`, `get_status()`) should also be overwritten to support
        those changes. Regardless of the changes or the algorithm's logic, the function arguments and
        return type must remain the same.

        Arguments:
            pid: ID of the process calling this function.
            maze_data: The maze data.
            memory: The algorithm's memory.

        Returns:
            The new position after taking a step.
        """

        pass


    @staticmethod
    def _after_step(pid: int, new_pos: tuple[int, int], maze_data: dict[str, ...],
                    memory: dict[str | int, ...]) -> None:
        """
        Logic for updating class variables and algorithm memory after taking a step.

        This function should only be overwritten if the algorithm's memory is modified or there are
        additional operations that need to be made. Additionally, if memory keys/values are modified,
        then the relevant functions (`get_current_pos()`, `get_visited_pos()`, `get_status()`) should
        also be overwritten to support those changes. Regardless of the changes or the algorithm's logic,
        the function arguments must remain the same. This function can, but doesn't need to return anything.

        Arguments:
            pid: ID of the process calling this function.
            new_pos: The new position after taking a step.
            maze_data: The maze data.
            memory: The algorithm's memory.
        """

        memory[pid]['current_pos'] = new_pos

        if BaseAlgorithmParallel.is_at_end(new_pos, maze_data):
            memory['reached_end'] = True

        with memory['lock']:
            if new_pos not in memory['visited_pos']:
                memory['visited_pos'].append(new_pos)


    def cleanup(self) -> None:
        """ Cleanup processes and resources. """

        for pid in range(self.num_processes):
            self.memory[pid]['is_active'] = False

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
