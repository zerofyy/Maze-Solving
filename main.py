import multiprocessing as mp

from utils.algorithms import WandererSequential, WandererParallel
from utils.maze_solver import MazeSolver
from utils.maze_generator import MazeGenerator
from utils.assets import Coloring


if __name__ == '__main__':
    mp.freeze_support()
    mp.set_start_method('spawn', force = True)

    Coloring.init()

    input('... preventing program from starting by waiting for input ...')

    algorithm = {
        'algorithm' : WandererSequential,
        'args' : {
            # 'num_processes': 4,
            'confused' : False
        }
    }

    mazes = [
        {
            'maze' : MazeGenerator.generate(40, 'middle', 'random_corner'),
            'max_steps' : 'unlimited',
            'num_iterations' : 1
        }
    ]

    ms = MazeSolver(
        algorithm_args = algorithm,
        mazes = mazes,
        measure_performance = True,
        wait_after_step = None,
        show_progress = 'visual',
        coloring = True
    )

    ms.run()

    input('... preventing program from stopping by waiting for input ...')
