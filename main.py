import multiprocessing as mp

from utils.algorithms import WandererSequential, BaseAlgorithmSequential, BaseAlgorithmParallel
from utils.maze_solver import MazeSolver
from utils.maze_generator import MazeGenerator


if __name__ == '__main__':
    mp.freeze_support()
    mp.set_start_method('spawn', force = True)


    input('... preventing program from starting by waiting for input ...')


    class BAS(BaseAlgorithmSequential):
        def step(self):
            return super().step()


    class BAP(BaseAlgorithmParallel):
        def _process_step(self, process_id, shared_state, coms_queue):
            return super()._process_step(process_id, shared_state, coms_queue)

        def step(self):
            return super().step()


    algorithm = {
        'algorithm' : BAP,
        'args' : {
            # 'confused' : False
            'num_processes' : 2
        }
    }

    mazes = [
        {
            'maze' : MazeGenerator.generate(8, 'random', 'random'),
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
