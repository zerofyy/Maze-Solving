from utils.algorithms import *
from utils.maze_solver import MazeSolver
from utils.maze_generator import MazeGenerator
from utils.assets import Coloring


if __name__ == '__main__':
    Coloring.init()

    input('... preventing program from starting by waiting for input ...')

    algorithms = [
        # {'algorithm': WandererSequential, 'args': {'confused': False}},
        # {'algorithm': WandererThreaded, 'args': {'num_threads': 4, 'confused' : False}},
        # {'algorithm': WallHuggerSequential, 'args': {'direction': 'left'}},
        # {'algorithm': WallHuggerThreaded, 'args': {'num_threads': 2}},
        # {'algorithm': BFSSequential, 'args': {}},
        # {'algorithm': BFSThreaded, 'args': {'num_threads': 4}},
        # {'algorithm': DFSSequential, 'args': {}},
    ]

    mazes = [
        {'maze' : MazeGenerator.generate(24, start_pos = 'random_corner', end_pos = 'random_corner'),
         'max_steps' : 'fewest', 'num_iterations' : 1}
    ]


    for algorithm in algorithms:
        solver = MazeSolver(
            algorithm_args = algorithm,
            mazes = mazes,
            measure_performance = True,
            wait_after_step = None,
            show_progress = 'detailed',
            coloring = True
        )

        solver.run(wait_after_iter = True)

    input('... preventing program from stopping by waiting for input ...')
