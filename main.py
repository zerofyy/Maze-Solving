from utils.algorithms import *
from utils.maze_solver import MazeSolver
from utils.maze_generator import MazeGenerator
from utils.assets import Coloring


if __name__ == '__main__':
    Coloring.init()

    input('... preventing program from starting by waiting for input ...')

    algorithm = {
        'algorithm' : WallHuggerThreaded,
        'args' : {
            'num_threads': 4,
            # 'confused' : False
            # 'direction' : 'right'
        }
    }

    mazes = [
        {
            'maze' : MazeGenerator.generate(24, 'middle', 'random_corner'),
            'max_steps' : 'unlimited',
            'num_iterations' : 1
        }
    ]

    ms = MazeSolver(
        algorithm_args = algorithm,
        mazes = mazes,
        measure_performance = True,
        wait_after_step = None,
        show_progress = 'detailed',
        coloring = True
    )

    ms.run()

    input('... preventing program from stopping by waiting for input ...')
