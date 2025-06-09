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
⬛ |-|
❌ |-| maze_solver/
✅ |-|-| __init__.py
🔄 |-|-| maze_solver.py
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
Finished MazeGenerator, added Wanderer algorithm, and started work on MazeSolver.

- Finished the Maze Generator.
  - Replaced `width` and `height` with `size`. It can now generate square mazes only.
  - Added options to set starting and ending positions, or pick them randomly.
  - The last generated maze is now saved within the class for easier algorithm testing.
  - Fixed an issue where if the maze size is an even number, the middle space was unreachable.
- Finished the base algorithm (abstract representation of other algorithms).
- Added Wanderer algorithm.
- Began work on the Maze Solver.
  - Added functionality to run a chosen algorithm on different mazes.
  - Added real time progress display.
- Updated requirements.txt to include `sty` for console coloring.