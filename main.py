from utils.algorithms import Wanderer
from utils.maze_solver import MazeSolver
from utils.maze_generator import MazeGenerator


algorithm = {
    'algorithm' : Wanderer,
    'args' : {
        'confused' : False
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

input('...')

'''
Maximum Steps Options:
    - <int> | Exact number of allowed steps.
    - 'auto' | Equal to `(maze_size * 2 + 1) ^ 2`.
    - 'fewest' | Equal to `(start_pos - end_pos + size)`.
    - 'unlimited' | Unlimited number of allowed steps.
'''
