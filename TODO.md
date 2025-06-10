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
✅ |-|-| base_algorithm.py
✅ |-|-| wanderer.py
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
```
❌ | utils/input_parser/*
✅ | utils/maze_generator/*
✅ | utils/algorithms/base_algorithm.py
⬛ |-| Might need some changes for parallel implementations of algorithms.
🔄 | utils/maze_solver/*
⬛ |-| Add performance measurements.
⬛ |-| Might need some changes for parallel implementations of algorithms.
⬛ |-| Fix buggy visual display for mazes sizes greater than 10.
❌ | utils/aglorithms/*
```

# Notes & Ideas
- ...

# Latest Changes
Refactored MazeGenerator and MazeSolver.

- Made a separate class for mazes instead of saving them inside MazeGenerator.
- Made MazeGenerator static.
- Made MazeSolver non-static.
- Made a separate class for progress tracking and displaying real time progress.
- Removed max_steps from BaseAlgorithm.