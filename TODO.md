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
✅ |-| assets/
✅ |-|-| __init__.py
✅ |-|-| list_maker.py
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
✅ |-| maze_solver/
✅ |-|-| __init__.py
✅ |-|-| maze_solver.py
✅ |-|-| results_collector.py
```

# TODO
- Fix parallel implementation being extremely slow:
  - Processes don't wait for commands, they just keep a history of steps that can be replayed by the `step()` function.
- Fix algorithms jumping spaces when running in parallel.
  - Not sure if this is fixed or not.
- Fix buggy visual display for different maze sizes on different screen resolutions.
- Implement the input parser.
- Implement proper code in main.
- Add new algorithms.

# Notes & Ideas
- ...

# Latest Changes
Refactoring and new implementations.

- BaseAlgorithmSequential class changes:
  - Added a new `memory` variable to be more like the parallel implementation.
  - Changed the `visited_spaces` variable to `visited_pos`.
  - Moved the `current_pos` and `visited_pos` variables in the algorithm's memory.
  - Changed the `visited_pos` item in the algorithm's memory from type list to type set.
  - Added a new `reached_end` item in the algorithm's memory to be more like the parallel implementation.
  - Implemented changes to allow for algorithms to have more control over class and memory variables:
    - Moved some of the logic from the `step()` function to an `_after_step()` function that can be overwritten.
    - Added `get_current_pos()` and `get_visited_pos()` functions that can be overwritten.
  - Replaced the `_build_status_dict()` function with `get_status()` that returns a dictionary in a display-ready format.
  - Reverted the `step()` function return type to `new_position | None, reached_end`.
  - Reverted to using a `Maze` instance instead of `maze_data`.
  - Removed the wall check from the `is_at_end()` function as algorithms should always pick from moves given by the `get_legal_moves()` function.
  - Some docstring changes.
- BaseAlgorithmParallel class changes:
  - Removed `current_pos`, `visited_spaces`, and `coms_queue` variables.
  - Renamed the `shared_memory` variable to `memory` to be more like the sequential implementation.
  - Changed the memory item `visited_spaces` to `visited_pos`.
  - Added new memory item `step_flag` to each process as a replacement for the communication queue.
  - Added new memory item `response` to each process for checking if steps were made.
  - Removed the `step_logic` item from the algorithm's memory.
  - Implemented changes to allow for algorithms to have more control over class and memory variables:
    - Moved some of the logic from the `step()` function to an `_after_step()` function that can be overwritten.
    - Added `get_current_pos()` and `get_visited_pos()` functions that can be overwritten.
  - Replaced the `_build_status_dict()` function with `get_status()` that returns a dictionary in a display-ready format.
  - Reverted the `step()` function return type to `new_position | None, reached_end`.
  - Removed the wall check from the `is_at_end()` function as algorithms should always pick from moves given by the `get_legal_moves()` function.
  - Updated the `_process_step()` function to support the new changes.
  - Processes no longer set their positions to None after terminating.
  - Some docstring changes.
- Wanderer algorithm changes:
  - Updated to support the base algorithm changes.
  - Significantly improved backtracking. The algorithm no longer gets stuck exploring the same spaces multiple times.
- MazeSolver class changes:
  - Changed the maximum number of allowed steps when using the `auto` option.
  - Reverted to only supporting a return type of `position, reached_end` when calling `algorithm.step()`.
- ResultsCollector class changes:
  - Changed variable `algorithm_time` to `solve_time`.
  - Implemented support for the algorithm changes.
  - Moved the system call for coloring console text from MazeSolver.
  - Added `_color()` function for easier coloring of text.
  - Changed some colors in the displays.
  - Improved the real time progress display.
  - Improved the results display.
  - Updated to support algorithm changes.
- Added `utils/assets/` module:
  - Added ListMaker class for cleaner representation of information (algorithm results and statistics).
- Small changes to the MazeGenerator class.
- Small changes to the Maze class.
- Updated TODO.