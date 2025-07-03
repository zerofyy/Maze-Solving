from utils.algorithms import *
from utils.maze_solver import MazeSolver
from utils.maze_generator import MazeGenerator
from utils.assets import Coloring


Coloring.init()


if __name__ == '__main__':
    input('... preventing program from starting by waiting for input ...')

    # Choose which algorithms to run
    algorithms = [
        {'algorithm' : DFSSequential, 'args' : {}},
        {'algorithm' : WandererThreaded, 'args' : {'num_threads' : 4, 'confused' : False}}
    ]

    # Choose mazes to run the algorithms on
    maze_s = MazeGenerator.generate(size = 10, start_pos = 'top_left', end_pos = 'bottom_right')
    maze_m = MazeGenerator.generate(size = 50, start_pos = 'random_corner', end_pos = 'middle')
    maze_l = MazeGenerator.generate(size = 100, start_pos = 'random_any', end_pos = 'random_any')
    mazes = [
        {'maze' : maze_s, 'max_steps' : 100, 'num_iterations' : 10},
        {'maze' : maze_s, 'max_steps' : 'fewest', 'num_iterations' : 1},
        {'maze' : maze_m, 'max_steps' : 'auto', 'num_iterations' : 5},
        {'maze' : maze_l, 'max_steps' : 'unlimited', 'num_iterations' : 1}
    ]

    # Run the solver
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
