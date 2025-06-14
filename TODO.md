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
❌ |-| maze_solver/
✅ |-|-| __init__.py
🔄 |-|-| maze_solver.py
✅ |-|-| results_collector.py
```

# TODO
- Fix algorithms jumping spaces when running in parallel.
- Add performance measurements to MazeSolver.
- Fix buggy visual display for different maze sizes on different screen resolutions.
- Implement the input parser.
- Implement proper code in main.
- Add new algorithms.

# Notes & Ideas
- ...

# Latest Changes
Finished the performance measurements for algorithms.

- Rewrote the docstring of `step()` function in BaseAlgorithmParallel to better explain what's being returned.
- Updated `step()` function in BaseAlgorithmSequential to better match the same function in the parallel implementation.
- Updated MazeSolver to only accept status dictionaries when calling `step()`, and not boolean (reached_end) variables.
- Replaced ProgressTracker with ResultsCollector:
  - Added measurements for average step time, average memory usage, and most memory usage.
  - Refactored the code.
- Changed MazeSolver to support the new ResultsCollector class.
- Updated TODO.