import time
import tracemalloc

from utils.algorithms import BaseAlgorithmSequential, BaseAlgorithmParallel
from utils.maze_generator import Maze
from utils.assets import Coloring, ListMaker


class ResultsCollector:
    """ Progress tracking and collecting results of running algorithms. """

    total_time: float = None
    solve_time: float = None
    last_solve_time: float = None


    def __init__(self, algorithm: BaseAlgorithmSequential | BaseAlgorithmParallel, maze: Maze, max_steps: int) -> None:
        """
        Create a new instance of the ResultsCollector class.

        Arguments:
             algorithm: The algorithm solving the maze.
             maze: Instance of the maze being solved.
             max_steps: The maximum number of allowed steps.
        """

        self.algorithm = algorithm
        self.maze = maze
        self.max_steps = max_steps
        self.results = {
            'steps_taken' : None,
            'reached_end' : None,
            'exploration' : None,
            'sp_from_end' : None,

            'solve_time' : None,
            'total_time' : None,
            'avg_step_time': None,

            'avg_mem_usage' : None,
            'top_mem_usage' : 0,

            'past_step_times' : [],
            'past_mem_usages' : []
        }


    def start(self, option: str) -> None:
        """
        Start tracking progress or measuring performance.

        Option 'track':
            Start tracking the algorithm's progress.
            Should be used after setting up the algorithm and right before starting it.

        Option 'measure':
            Start measuring the algorithm's performance.
            Should be used before setting up the algorithm.

        Arguments:
            option: The option of choice.
        """

        if option == 'measure':
            tracemalloc.start()
            self.total_time = time.time()

        if option == 'track':
            self.solve_time = time.time()
            self.last_solve_time = self.solve_time
            self.results['steps_taken'] = 0


    def update(self) -> None:
        """ Update the algorithm's statistics after taking a step. """

        step_time = time.time()

        self.results['steps_taken'] += 1

        self.results['solve_time'] = round(step_time - self.solve_time, 2)
        self.results['total_time'] = round(step_time - self.total_time, 2)

        if isinstance(self.algorithm, BaseAlgorithmSequential):
            self.results['reached_end'] = self.algorithm.is_at_end()
        else:
            self.results['reached_end'] = self.algorithm.memory.get('reached_end')

        self.results['exploration'] = len(self.algorithm.get_visited_pos())

        current_pos = self.algorithm.get_current_pos() if isinstance(self.algorithm, BaseAlgorithmSequential) \
            else self.algorithm.get_current_pos(best_pos = True)
        self.results['sp_from_end'] = int(
            abs(current_pos[0] - self.maze.end_pos[0]) +
            abs(current_pos[1] - self.maze.end_pos[1])
        )

        self.results['past_step_times'].append(step_time - self.last_solve_time)
        self.results['avg_step_time'] = round(
            sum(self.results['past_step_times']) / len(self.results['past_step_times']), 2
        )
        self.last_solve_time = step_time

        current_mem, peak_mem = tracemalloc.get_traced_memory()
        self.results['past_mem_usages'].append(current_mem / 1024 / 1024)
        self.results['avg_mem_usage'] = round(
            sum(self.results['past_mem_usages']) / len(self.results['past_mem_usages']), 2
        )
        self.results['top_mem_usage'] = max(self.results['top_mem_usage'], round(peak_mem / 1024 / 1024, 2))


    def get_progress(self, coloring: bool = True, details: bool = False) -> str | None:
        """
        Get the progress of the currently running algorithm in text format.

        Arguments:
            coloring: Whether to use colors in the text.
            details: Whether to include details from the algorithm's memory.

        Returns:
            The progress as a string.
        """

        progress = f'_____________________________________________\n' \
                   f'===\n' \
                   f'| * Time Passed    : ______________________ |\n' \
                   f'| * Solve Time     : ______________________ |\n' \
                   f'| * Avg Step Time  : ______________________ |\n' \
                   f'===\n' \
                   f'| * Steps Taken    : ______________________ |\n' \
                   f'| * Explored       : ______________________ |\n' \
                   f'| * Progress       : ______________________ |\n' \
                   f'===\n' \
                   f'| * Avg Mem Usage  : ______________________ |\n' \
                   f'| * Peak Mem Usage : ______________________ |\n' \
                   f'===' \

        total_time = f'{round(self.results["total_time"] / 60, 2)} min' \
            if self.results['total_time'] > 60 else f'{self.results["total_time"]} sec'
        solve_time = f'{round(self.results["solve_time"] / 60, 2)} min' \
            if self.results['solve_time'] > 60 else f'{self.results["solve_time"]} sec'
        list_info = [
                (f'[lc]{self.algorithm.__class__.__name__}[rs]', 'left'),
                (f'[lb]{total_time}[rs]', 'left'),
                (f'[lb]{solve_time}[rs]', 'left'),
                (f'[lb]{self.results["avg_step_time"]} sec[rs]', 'left'),
                (f'[ly]{self.results["steps_taken"]}[rs] / [ly]{self.max_steps}[rs]', 'left'),
                (f'[ly]{self.results["exploration"]} spaces[rs]', 'left'),
                (f'[ly]~{self.results["sp_from_end"]} spaces[rs] from end', 'left'),
                (f'[lc]{self.results["avg_mem_usage"]} MB[rs]', 'left'),
                (f'[lc]{self.results["top_mem_usage"]} MB[rs]', 'left')
            ]

        if details:
            for key, val in self.algorithm.get_status():
                progress += f'\n| * {key:<14} : {"_" * 22} |'
                list_info.append((val, 'left'))
            progress += '\n==='

        progress = ListMaker.fill(
            text = progress,
            info = list_info
        )

        if coloring:
            progress = progress.replace('| ', f'[fb]| [rs]')
            progress = progress.replace('* ', f'[fb][y]* [rs]')
            progress = progress.replace('===', f'[fb]=============================================[rs]')
        else:
            progress = progress.replace('===', '=============================================')
            progress = Coloring.uncolor(progress)

        return progress


    def get_results(self, option: str, coloring: bool = True) -> str | dict[str, ...] | None:
        """
        Get the algorithm's results.

        Options:
            - 'string' | The results will be returned as a string.
            - 'dict' | The results will be returned as a dictionary.
            - <file_path> | The results will be saved to a file.
            If no other option is selected, it is assumed that a file path is given.

        Arguments:
             option: Where to save/send the results.
             coloring: Whether to use colors if the selected option is 'string'.

        Returns:
            The results as a string or dictionary or None if a different option is selected.
        """

        if option == 'dict':
            return self.results

        total_time = f'{round(self.results["total_time"] / 60, 2)} min' \
            if self.results['total_time'] > 60 else f'{self.results["total_time"]} sec'
        solve_time = f'{round(self.results["solve_time"] / 60, 2)} min' \
            if self.results['solve_time'] > 60 else f'{self.results["solve_time"]} sec'
        setup_time = round(self.results['total_time'] - self.results['solve_time'], 2)
        reached_end = f'[lg]Yes[rs]' if self.results['reached_end'] else '[lr]No[rs]'

        results = f'=========================================================\n' \
                  f'| _____________________________________________________ |\n' \
                  f'|-------------------------------------------------------|\n' \
                  f'| * Maze Size         : _______________________________ |\n' \
                  f'| * Start-End         : _______________________________ |\n' \
                  f'=========================================================\n' \
                  f'| _____________________________________________________ |\n' \
                  f'|-------------------------------------------------------|\n' \
                  f'| * Setup Time        : _______________________________ |\n' \
                  f'| * Solve Time        : _______________________________ |\n' \
                  f'| * Total Time        : _______________________________ |\n' \
                  f'| * Avg Step Time     : _______________________________ |\n' \
                  f'|-------------------------------------------------------|\n' \
                  f'| * Steps Taken       : _______________________________ |\n' \
                  f'| * Explored          : _______________________________ |\n' \
                  f'| * Progress          : _______________________________ |\n' \
                  f'| * Reached End       : _______________________________ |\n' \
                  f'|-------------------------------------------------------|\n' \
                  f'| * Avg Memory Usage  : _______________________________ |\n' \
                  f'| * Peak Memory Usage : _______________________________ |\n' \
                  f'========================================================='

        results = ListMaker.fill(
            text = results,
            info = [
                (f'[fb][lc]Maze Information[rs]', 'left'),
                (f'[lc]{self.maze.size}[rs] ( [lc]{self.maze.size_matrix}[rs] )', 'left'),
                (f'[lg]{str(self.maze.start_pos)[1:-1]}[rs] - [lr]{str(self.maze.end_pos)[1:-1]}[rs]', 'left'),
                (f'[fb][lc]{self.algorithm.__class__.__name__} Information[rs]', 'left'),
                (f'[lb]{setup_time} sec[rs]', 'left'),
                (f'[lb]{solve_time}[rs]', 'left'),
                (f'[lb]{total_time}[rs]', 'left'),
                (f'[lb]{self.results["avg_step_time"]} sec[rs]', 'left'),
                (f'[ly]{self.results["steps_taken"]}[rs] / [ly]{self.max_steps}[rs]', 'left'),
                (f'[ly]{self.results["exploration"]} spaces[rs]', 'left'),
                (f'[ly]~{self.results["sp_from_end"]} spaces[rs] from end', 'left'),
                (reached_end, 'left'),
                (f'[lc]{self.results["avg_mem_usage"]} MB[rs]', 'left'),
                (f'[lc]{self.results["top_mem_usage"]} MB[rs]', 'left')
            ]
        )

        if coloring and option == 'string':
            results = results.replace('|', f'[fb]|[rs]')
            results = results.replace('*', f'[fb][y]*[rs]')
            results = results.replace('=', f'[fb]=[rs]')
            results = results.replace('-', f'[fb]-[rs]')
        else:
            results = Coloring.uncolor(results)

        if option == 'string':
            return results

        with open(option, 'w', encoding = 'UTF-8') as file:
            file.write(results)


    def __del__(self) -> None:
        """ Stop measuring memory usage when object is deleted. """

        tracemalloc.stop()


__all__ = ['ResultsCollector']
