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
- Finish the Wall Hugger algorithm.
  - Fix its logic, so it doesn't get stuck in loops near the center of the maze.
- Implement the input parser.
- Implement proper code in main.
- Add new algorithms.

# Notes & Ideas
- ...

# Latest Changes
Switched to threading, began implementing a new algorithm, and improved performance.

- Replaced multiprocessing with threading.
- Minor changes to sequential algorithms to match the structure of threaded algorithms.
- Significantly improved the efficiency of threaded algorithms.
- Began implementation of a new algorithm: Wall Hugger.
- Docstring changes.
- Updated TODO.