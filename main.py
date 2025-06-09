from utils.algorithms import Wanderer
from utils.maze_solver import MazeSolver


algorithm_settings = {'algorithm' : Wanderer, 'max_steps' : 'auto', 'confused' : False}
mazes = [{'size' : 10, 'start_pos' : 'random', 'end_pos' : 'middle', 'num_iterations' : 1}]

MazeSolver.run(
    algorithm_settings,
    mazes,
    wait_after_step = 20,
    real_time_progress = 'visual'
)
input('...')
