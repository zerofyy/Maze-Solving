import multiprocessing as mp

from utils.algorithms import WandererSequential, WandererParallel
from utils.maze_solver import MazeSolver
from utils.maze_generator import MazeGenerator


if __name__ == '__main__':
    mp.freeze_support()
    mp.set_start_method('spawn', force = True)

    input('... preventing program from starting by waiting for input ...')

    algorithm = {
        'algorithm' : WandererParallel,
        'args' : {
            'num_processes': 4,
            'confused' : False
        }
    }

    mazes = [
        {
            'maze' : MazeGenerator.generate(4, 'middle', 'random_corner'),
            'max_steps' : 'auto',
            'num_iterations' : 1
        }
    ]

    ms = MazeSolver(
        algorithm_args = algorithm,
        mazes = mazes,
        measure_performance = True,
        wait_after_step = None,
        show_progress = 'visual'
    )

    ms.run()

    input('... preventing program from stopping by waiting for input ...')
