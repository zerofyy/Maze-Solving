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
❌ |-|-|-| wanderer_parallel.py
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
- Refactor the parallel implementation of base algorithm.
- Fix "jumping spaces" when processes make moves. Might be because the main process doesn't wait after sending STEP commands.
- `utils/input_parser/*`
- `utils/maze_solver/*`
  - Add performance measurements.
  - Might need some changes for parallel implementations of algorithms.
  - Fix buggy visual display for mazes sizes greater than 10.
- `utils/algorithms/*`

# Notes & Ideas
- ...

# Latest Changes
Somewhat fixed the parallel implementation of the base algorithm.

- Changed all complex objects to dictionaries for use in parallel processing.
- Added function to Maze to return all its data as a dictionary.
- Fixed the ProgressTracker not showing the location of all processes.
- Fixed the ProgressTracker incorrectly calculated the closest distance to the end position.
- Updated TODO.