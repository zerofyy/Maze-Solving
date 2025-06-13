# Project Plan
```
❌ | main.py
❌ | README.md
✅ | TODO.md
❌ | requirements.txt
⬛ |
❌ | utils/
✅ |-| __init__.py
⬛ |-|
❌ |-| algorithms/
🔄 |-|-| __init__.py
⬛ |-|-|
✅ |-|-| base_algorithm/
✅ |-|-|-| __init__.py
✅ |-|-|-| base_algorithm_sequential.py
✅ |-|-|-| base_algorithm_parallel.py
✅ |-|-| wanderer/
✅ |-|-|-| __init__.py
✅ |-|-|-| wanderer_sequential.py
✅ |-|-|-| wanderer_parallel.py
❌ |-|-| ...
⬛ |-|
❌ |-| input_parser/
❌ |-|-| __init__.py
❌ |-|-| input_parser.py
⬛ |-|
✅ |-| maze_generator/
✅ |-|-| __init__.py
✅ |-|-| maze_generator.py
✅ |-|-| maze.py
⬛ |-|
❌ |-| maze_solver/
✅ |-|-| __init__.py
🔄 |-|-| maze_solver.py
✅ |-|-| progress_tracker.py
```

# TODO
- Change `step()` in BaseAlgorithmSequential to also return a status dictionary instead of a boolean.
- Change MazeSolver to only work with status dictionaries.
- Fix algorithms jumping spaces when running in parallel.
- Add performance measurements to MazeSolver.
- Fix buggy visual display for different maze sizes on different screen resolutions.
- Implement the input parser.
- Implement proper code in main.
- Add new algorithms.

# Notes & Ideas
- ...

# Latest Changes
Reworked BaseAlgorithmParallel class and implemented parallelization of Wanderer algorithm.

- Maze class changes:
  - Changed variable `maze` to `matrix`.
- BaseAlgorithmSequential class changes:
  - Replaced Maze instance with maze data (`maze: Maze` --> `maze_data: dict[str, ...] = Maze.get_maze_data()`).
  - Removed `can_take_step()` function.
  - Changed `get_legal_moves()` function to return an empty list if steps cannot be taken.
  - Changed `get_legal_moves()` function to support getting legal moves from specific positions.
  - Changed `step()` function to no longer be abstract.
  - Changed `step()` function to return two values, a tuple of coordinates and a boolean signaling whether the end is reached.
  - Added an abstract function `_step_logic()` for implementing algorithm logic.
- BaseAlgorithmParallel class changes:
  - Implemented changes from BaseAlgorithmSequential class to make both classes more like one another.
  - Fixed default number of processes not working.
  - Replaced variable `shared_state` with `shared_memory`.
  - Replaced key `is_solved` with `reached_end` in `shared_memory`.
  - Moved key `visited_spaces` from `shared_memory[process_id]` to root of `shared_memory`.
  - Added key `step_logic` to `shared_memory` (value equals to `self._step_logic`).
  - Replaced variable `coms_queue` with `com_queue`.
  - Changed `_process_step()` to no longer be abstract.
  - Added `manager` variable for easier implementation of other parallel algorithms.
- Wanderer algorithm changes:
  - Updated WandererSequential class to be compatible with the new BaseAlgorithmSequential class changes.
  - Updated WandererSequential step logic to not get stuck in long corridors as often.
  - Added WandererParallel class and algorithm that follows the same logic as the sequential version.
- Other changes:
  - Updated ProgressTracker class to include an empty line between the text and visual progress displays.
  - Updated ProgressTracker class to ignore maze positions with value `None`.
  - Fixed MazeSolver class not calling `ProgressTracker.get_progress()` for the final step.
  - Updated MazeSolver class to support new return types of `step()` functions.
  - Updated TODO.