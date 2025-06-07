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
❌ |-|-| __init__.py
❌ |-|-| base_algorithm.py
❌ |-|-| ...
⬛ |-|
❌ |-| input_parser/
❌ |-|-| __init__.py
❌ |-|-| input_parser.py
⬛ |-|
✅ |-| maze_generator/
✅ |-|-| __init__.py
🔄 |-|-| maze_generator.py
⬛ |-|
❌ |-| maze_solver/
❌ |-|-| __init__.py
❌ |-|-| maze_solver.py
```

# TODO
```
❌ | utils/input_parser/*
🔄 | utils/maze_generator/*
⬛ |-| Generated mazes often don't have a path from start to finish.
❌ | utils/algorithms/base_algorithm.py
❌ | utils/maze_solver/*
❌ | utils/aglorithms/*
```

# Notes & Ideas
- ...

# Latest Changes
Began work on the maze generator.

- Added MazeGenerator class.
  - Added functions for generating a random maze.