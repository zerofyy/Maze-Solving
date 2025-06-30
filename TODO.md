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
✅ |-|-|-| base_algorithm_threaded.py
✅ |-|-| wanderer/
✅ |-|-|-| __init__.py
✅ |-|-|-| wanderer_sequential.py
✅ |-|-|-| wanderer_threaded.py
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
- InputParser:
  1. Keeps a list of all algorithms and asks for their setup arguments to be set.
  2. Option to add mazes and set their arguments.
  3. Display options.
  4. Run.
- Proper main code.
- New algorithms: Radar (makes moves that lead closer to the end), BFS, DFS, A*.
- Write readme.

# Notes & Ideas
- ...

# Latest Changes
Maze generation fixes and new algorithms.

- Fixed the maze generation creating a small loop at the center in mazes of even sizes.
- Finished the WallHugger algorithm (both Sequential and Threaded).
- Updated TODO.