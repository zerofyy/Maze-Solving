<h1 align="center">
  Sequential and Multithreaded Maze Solving Algorithms with Live Visualization and Performance Tracking.
</h1>

<p align="center">
  <a href="#-overview">📄 Overview</a> •
  <a href="#-maze-generation">🧩 Maze Generation</a> •
  <a href="#-implemented-algorithms">🤖 Implemented Algorithms</a> •
  <a href="#-usage">⚙ Usage</a> •
  <a href="#-adding-your-own-algorithms">🛠 Custom Algorithms</a>
</p>

![example-visualization](https://i.ibb.co/MDg3bZW7/Untitled-Project.gif)

## 📄 Overview
This project features sequential and multithreaded implementations of several maze-solving algorithms, along with a simple maze generator based on Prim's algorithm, and real-time visualization and performance tracking.

### Key Features
* **Random Maze Generator:** Fast random maze generator using a modified version of Prim's algorithm.
* **Live Display:** Watch algorithms solve mazes in real-time with clean, colored visualization.
* **Performance Tracking:** Detailed metrics for algorithm comparison and analysis.
* **Custom Algorithm Support:** Easy-to-use framework for implementing custom algorithms.


## 🧩 Maze Generation
The random maze generation process is done in three steps:

* **Grid Initialization:**
Given a size ***N***, a binary matrix is created where 1 represents an empty space and 0 represents a wall. The matrix contains ***N x N*** empty spaces surrounded by walls, while its size is equal to ***N x 2 + 1*** for both rows and columns.
* **Path Generation:**
Starting from the top-left empty space, the algorithm iterates through the remaining spaces in a spiral pattern. For each empty space, an adjacent empty space is added following the spiral and gradually building the maze.
* **Finalization:**
The result is a maze with exactly one unique path between any two empty spaces, allowing the start and end positions to be placed anywhere.

### Notes
Although this maze generation approach is relatively fast ( *O(n)* time ), it is limited to creating square mazes with very distinct path patterns.
The characteristics of the paths can be improved by changing the iteration pattern used during maze generation ( ex. using a zig-zag pattern instead of a spiral ).

Additionally, for mazes with an even size ( ***N*** is even ), a small correction is made at the center to prevent loops, especially when the start or end position is placed at the exact center.

The code for this module is located in `utils/maze_generator/`.


## 🤖 Implemented Algorithms
| Algorithm   | Description                                                                                | Sequential | Threaded |
|-------------|--------------------------------------------------------------------------------------------|------------|----------|
| Wanderer    | Explores the maze through random moves with the option to avoid previously visited spaces. | ✅         | ✅     |
| Wall Hugger | Explores the maze by sticking to the left or right side.                                   | ✅         | ✅     |
| BFS         | Explores the maze by prioritizing neighboring, non-visited spaces.                         | ✅         | ✅     |
| DFS         | Explores the maze by going as far as possible before backtracking, similar to Wanderer.    | ✅         | ❌     |



## ⚙ Usage
### Installation
```bash
# Clone the repository
git clone https://github.com/zerofyy/Maze-Solving.git
cd Maze-Solving

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### Configuration
```py
if __name__ == '__main__':
    
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
        {'maze' : maze_s, 'max_steps' : 100, 'num_iterations' : 1},
        {'maze' : maze_s, 'max_steps' : 'fewest', 'num_iterations' : 10},
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
```


## 🛠 Adding Your Own Algorithms
* Make a new folder inside `utils/algorithms/` with the name of your algorithm ( ex. `utils/algorithms/my_algorithm/` ).
* Inside that folder, add the following files: `__init__.py`, `my_algorithm_sequential.py`, `my_algorithm_threaded.py`.
  Replace "my_algorithm" from the python files' names with the name of your algorithm. If your algorithm runs only sequentially, then the threaded file is not needed and vice versa.
* Add the algorithm logic and necessary code to each file ( see below ).
* Done! Now you can use your algorithm classes in `main.py` like shown in the configuration example above.

### Algorithm Logic Examples
```py
# __init__.py
from .my_algorithm_sequential import *
from .my_algorithm_threaded import *
```

```py
# my_algorithm_sequential.py
import random

from utils.algorithms import BaseAlgorithmSequential
from utils.maze_generator import Maze


class MyAlgorithmSequential(BaseAlgorithmSequential):

    def setup(self, maze: Maze) -> None:
        super().setup(maze)
        # Update self.memory if necessary

    def _step_logic(self) -> tuple[int, int]:
        new_pos = random.choice(self.get_legal_moves())
        return new_pos


__all__ = ['MyAlgorithmSequential']
```

```py
# my_algorithm_threaded.py
import random
import time

from utils.algorithms import BaseAlgorithmThreaded
from utils.maze_generator import Maze


class MyAlgorithmThreaded(BaseAlgorithmThreaded):

    def setup(self, maze: Maze, wait_for_flag: bool = False, num_threads: int = 4) -> None:
        super().setup(maze, wait_for_flag, num_threads)
        # Update self.memory if necessary

    def _step_logic(self, tid: int) -> tuple[int, int]:
        random.seed(time.time() + tid)
        new_pos = random.choice(self.get_legal_moves(tid))
        return new_pos


__all__ = ['MyAlgorithmThreaded']
```

### Notes
For more information on how to properly implement your own algorithms check out the abstract classes ( located in `utils/algorithms/base_algorithm/` ) and the already implemented algorithms.