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
⬛ |-| Replace width and height with size (always a square maze).
❌ | utils/algorithms/base_algorithm.py
❌ | utils/maze_solver/*
❌ | utils/aglorithms/*
```

# Notes & Ideas
- Starting position of the maze is bottom left, and ending position is top right.

# Latest Changes
Improved and fixed the maze generator.

- Fixed the path generation to always have a path from beginning to end.
  - Though, it only works for square mazes.