# Project Structure
```
✅ | main.py
✅ | README.md
✅ | TODO.md
✅ | requirements.txt
⬛ |
✅ | utils/
✅ |-| __init__.py
⬛ |-|
✅ |-| assets/
✅ |-|-| __init__.py
✅ |-|-| coloring.py
✅ |-|-| display.py
✅ |-|-| list_maker.py
⬛ |-|
✅ |-| algorithms/
✅ |-|-| __init__.py
⬛ |-|-|
✅ |-|-| base_algorithm/*
✅ |-|-| wanderer/*
✅ |-|-| wall_hugger/*
✅ |-|-| bfs/*
✅ |-|-| dfs/*
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
- Try out different iteration patterns for paths during maze generation.
- Add more algorithms.

# Notes & Ideas
- ...

# Latest Changes
Added content to README and made some final changes.

- Added an option to check whether a specific position is the end position for sequential and threaded algorithms.
- Updated the `is_at_end()` function for threaded algorithms to set the `reached_end` flag in memory, instead of it being set by the `_after_step()` function.
- Improved the approximation for the `fewest` max steps option in the MazeSolver class.
- Docstring changes and code organization.
- Small changes to the results display generated by the ResultsCollector class.
- Added content to README.
- Updated TODO.