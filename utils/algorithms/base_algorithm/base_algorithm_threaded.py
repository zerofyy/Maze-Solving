import time
import os
from abc import abstractmethod, ABC
import threading

from utils.maze_generator import Maze


class BaseAlgorithmThreaded(ABC):
    """ Abstract representation of a threaded maze solving algorithm. """

    maze: Maze = None
    wait_for_flag: bool = None
    num_threads: int = None
    threads: list[threading.Thread] = None
    memory: dict[str | int, ...] = None


    def setup(self, maze: Maze, wait_for_flag: bool = False, num_threads: int = 4) -> None:
        """
        Set up the algorithm.

        Arguments:
            maze: Instance of the Maze class.
            wait_for_flag: Whether to wait for the step flag to be set for threads to execute their logic.
            num_threads: Number of threads, defaults to 4 or less.
        """

        self.maze = maze
        self.wait_for_flag = wait_for_flag
        self.num_threads = min(num_threads, os.cpu_count()) if num_threads else min(4, os.cpu_count())
        self.threads = []

        self.memory = {
            'visited_pos': {maze.start_pos},
            'reached_end': False,
            'lock': threading.Lock()
        }

        for tid in range(self.num_threads):
            self.memory[tid] = {
                'current_pos': maze.start_pos,
                'is_active': True,
                'step_flag': threading.Event(),
                'response': None
            }

        self._start_threads()


    def _start_threads(self) -> None:
        """ Start all threads. """

        for tid in range(self.num_threads):
            thread = threading.Thread(
                target = self._thread_step,
                args = (tid,),
                daemon = True
            )

            thread.start()
            self.threads.append(thread)


    def is_at_end(self, tid: int) -> bool:
        """
        Check whether the current position of the given thread matches the maze end position.

        Arguments:
            tid: Thread ID.
        """

        return self.memory[tid]['current_pos'] == self.maze.end_pos


    def get_legal_moves(self, tid: int = None, position: tuple[int, int] = None) -> list[tuple[int, int]]:
        """
        Get a list of legal moves from the current position of the given thread.

        Arguments:
            tid: Thread ID.
            position: Specific position to check from, defaults to the current position of the given thread.

        Returns:
            A list of new positions that can be visited from the specified or current thread position.
            If no legal moves exist, the list will be empty.
        """

        if self.is_at_end(tid):
            return []

        position = self.memory[tid]['current_pos'] if position is None else position

        check_moves = [
            (position[0] - 1, position[1]),
            (position[0] + 1, position[1]),
            (position[0], position[1] - 1),
            (position[0], position[1] + 1)
        ]

        return [
            move for move in check_moves
            if 0 <= move[0] < self.maze.size_matrix and 0 <= move[1] < self.maze.size_matrix
            and self.maze.matrix[move[0]][move[1]] == self.maze.path
        ]


    def get_current_pos(self, best_pos: bool = False) -> list[tuple[int, int]] | tuple[int, int]:
        """
        Get the current position of each thread or the one closest to the end.

        This function should be overwritten if the `'current_pos'` keys in the algorithm's memory are modified.
        Regardless of the modifications, the return type must remain the same.

        Arguments:
            best_pos: Whether to return the best position out of all threads.

        Returns:
            The coordinates of the current positions in the maze, or the position closest to the end if
            best_pos is set to True.
        """

        if not best_pos:
            return [self.memory[tid]['current_pos'] for tid in range(self.num_threads)]

        best_pos, best_dist = self.memory[0]['current_pos'], float('inf')
        for tid in range(self.num_threads):
            dist = abs(self.memory[tid]['current_pos'][0] - self.maze.end_pos[0]) + \
                   abs(self.memory[tid]['current_pos'][1] - self.maze.end_pos[1])

            if dist < best_dist:
                best_dist = dist
                best_pos = self.memory[tid]['current_pos']

        return best_pos


    def get_visited_pos(self) -> set[tuple[int, int]]:
        """
        Get all the positions previously visited by the algorithm.

        This function should be overwritten if the `'visited_pos'` key in the algorithm's memory is modified.
        Regardless of the modifications, the return type must remain the same.

        Returns:
            A set of coordinates of all visited positions in the maze.
        """

        return self.memory['visited_pos']


    def get_status(self) -> list[tuple[str, ...]]:
        """
        Get information about the algorithm's status.

        By default, this function returns information from the algorithm's memory. If the algorithm's memory
        has been modified - this function should be overwritten to include those modifications in the status
        list (in an appropriate format for text displays). Regardless of the modifications, the return type
        of this function must remain the same.

        Returns:
            A list with status information.
        """

        status = []

        for tid in range(self.num_threads):
            local_memory = self.memory[tid]

            status.append((f'Thread {tid}',
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


    def _thread_step(self, tid: int) -> None:
        """ Internal thread logic - keep threads alive and handle communication. """

        while True:
            local_memory = self.memory[tid]

            if not local_memory['is_active']:
                local_memory['response'] = 'Terminated'
                break

            if self.memory['reached_end']:
                local_memory['is_active'] = False
                local_memory['response'] = 'Ended'
                break

            self.memory[tid]['step_flag'].wait(timeout = 0.03 if not self.wait_for_flag else None)
            self.memory[tid]['step_flag'].clear()
            self.memory[tid]['response'] = 'Stepping'

            new_pos = self._step_logic(tid)
            self._after_step(tid, new_pos)
            self.memory[tid]['response'] = 'Stepped'


    def step(self) -> tuple[tuple[tuple[int, int], ...] | None, bool]:
        """
        Take a step in the maze.

        Returns:
            The new positions after each thread takes a step or None if no steps were taken, and a boolean
            value representing whether the end of the maze has been reached.
        """

        if self.memory['reached_end']:
            return None, True

        active_threads = 0

        for tid in range(self.num_threads):

            if not self.memory[tid]['is_active']:
                continue

            if self.get_legal_moves(tid):
                active_threads += 1
                self.memory[tid]['step_flag'].set()
                self.memory[tid]['response'] = 'Waiting'
            else:
                self.memory[tid]['step_flag'].clear()
                self.memory[tid]['is_active'] = False

        time_passed = time.time()
        while True:
            responses = sum(1 if self.memory[tid]['response'] == 'Stepped' else 0
                            for tid in range(self.num_threads))

            if responses == active_threads:
                break

            if time.time() - time_passed >= 0.1:
                if responses >= 1:
                    break
                return None, self.memory['reached_end']

            time.sleep(0.0001)

        return tuple(self.memory[tid]['current_pos'] for tid in range(self.num_threads)), self.memory['reached_end']


    @abstractmethod
    def _step_logic(self, tid: int) -> tuple[int, int]:
        """
        Logic for choosing the next move from the current position with the assumption that there's at
        least one legal move from the current position.

        If anything in the algorithm's memory has been modified (ex. `'current_pos', 'visited_pos'`), then
        the logic for updating those variables should also be implemented here or within the `_after_step()`
        function. Additionally, if memory keys/values are modified, then the relevant functions
        (`get_current_pos()`, `get_visited_pos()`, `get_status()`) should also be overwritten to support
        those changes. Regardless of the changes or the algorithm's logic, the function arguments and
        return type must remain the same.

        Arguments:
            tid: ID of the thread calling this function.

        Returns:
            The new position after taking a step.
        """

        pass


    def _after_step(self, tid: int, new_pos: tuple[int, int]) -> None:
        """
        Logic for updating class variables and algorithm memory after taking a step.

        This function should only be overwritten if the algorithm's memory is modified or there are
        additional operations that need to be made. Additionally, if memory keys/values are modified,
        then the relevant functions (`get_current_pos()`, `get_visited_pos()`, `get_status()`) should
        also be overwritten to support those changes. Regardless of the changes or the algorithm's logic,
        the function arguments must remain the same. This function can, but doesn't need to return anything.

        Arguments:
            tid: ID of the thread calling this function.
            new_pos: The new position after taking a step.
        """

        self.memory[tid]['current_pos'] = new_pos

        if self.is_at_end(tid):
            self.memory['reached_end'] = True

        self.memory['visited_pos'].add(new_pos)


    def cleanup(self) -> None:
        """ Cleanup threads and resources. """

        for tid in range(self.num_threads):
            self.memory[tid]['is_active'] = False

        for thread in self.threads:
            thread.join(timeout = 0.5)

        self.threads.clear()


    def __del__(self):
        """ Cleanup threads and resources when object is deleted. """

        self.cleanup()


__all__ = ['BaseAlgorithmThreaded']
