# Project Plan
```
❌ | main.py
❌ | README.md
✅ | TODO.md
✅ | requirements.txt
⬛ |
❌ | utils/
✅ |-| __init__.py
⬛ |-|
✅ |-| assets/
✅ |-|-| __init__.py
✅ |-|-| coloring.py
✅ |-|-| display.py
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
- The visual display is a bit slow when using colors.
- Add a `fast: bool = False` argument to `get_current_pos()` and `get_visited_pos()` and `get_end_distance()` that will return cached versions of those values, rather than accessing them from memory.
- Look into more ways to speedup parallel algorithms.
- Implement the input parser.
- Implement proper code in main.
- Add new algorithms.

# Notes & Ideas
- ...

# Latest Changes
Significantly improved the real time progress display.

- Added a new Coloring module (`assets/coloring.py`) for working with colored strings.
- Added a new Display module (`assets/display.py`) for displaying information in the terminal.
- Updated the ListMaker class to automatically calculate the directional offset when using color codes.
- ResultsCollector class changes:
  - Moved the system call for colors to the Coloring class.
  - Removed real time progress display options and all printing functionality.
  - Moved the distance from end position calculation to the `update()` function.
  - Removed the `_color()`, `_get_text_display()`, and `_get_visual_display()` functions.
  - Changed the `get_progress()` function to only return a nicely formatted string of the algorithm's progress.
  - Changed the `get_progress()` function to properly crop detailed information.
- Updated the MazeSolver class to use the Display module along with the ResultsCollector class for real time progress.
- Removed the key name spacing in the `get_status()` function for all current algorithms. 
- Added a `best_pos` argument to the `get_current_pos()` function for parallel algorithms that returns the position closest to the end of the maze.
- Some docstring changes.
- Updated TODO.