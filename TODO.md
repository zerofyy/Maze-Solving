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
- Fix the parallel implementation of base algorithm.
- `utils/input_parser/*`
- `utils/maze_solver/*`
  - Add performance measurements.
  - Might need some changes for parallel implementations of algorithms.
  - Fix buggy visual display for mazes sizes greater than 10.
- `utils/algorithms/*`

# Notes & Ideas
- ...

# Latest Changes
Began implementing multiprocessing.

- Fixed starting position not being saved as visited by algorithms.
- Reorganized algorithms in separate folders containing both sequential and parallel versions.
- Implemented an abstract representation of a parallel algorithm.
- Updated the ProgressTracker to be compatible with parallel algorithms.
- Updated TODO.