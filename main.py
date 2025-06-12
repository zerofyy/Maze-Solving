import multiprocessing as mp

from utils.algorithms import WandererSequential, BaseAlgorithmSequential, BaseAlgorithmParallel
from utils.maze_solver import MazeSolver
from utils.maze_generator import MazeGenerator


class BAS(BaseAlgorithmSequential):
    def step(self):
        return super().step()


class BAP(BaseAlgorithmParallel):
    @staticmethod
    def _process_step(process_id, maze_data, shared_state, coms_queue):
        return BaseAlgorithmParallel._process_step(process_id, maze_data, shared_state, coms_queue)

    def step(self):
        return super().step()


if __name__ == '__main__':
    mp.freeze_support()
    mp.set_start_method('spawn', force = True)

    input('... preventing program from starting by waiting for input ...')

    algorithm = {
        'algorithm' : BAP,
        'args' : {
            # 'confused' : False
            'num_processes' : 4
        }
    }

    mazes = [
        {
            'maze' : MazeGenerator.generate(10, 'random', 'random'),
            'max_steps' : 'auto',
            'num_iterations' : 1
        }
    ]

    ms = MazeSolver(
        algorithm_args = algorithm,
        mazes = mazes,
        measure_performance = False,
        wait_after_step = 100,
        show_progress = 'visual'
    )

    ms.run()

    input('... preventing program from stopping by waiting for input ...')
