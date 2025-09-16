# PoCN_project

Projects repository for the Physics of Complex Network course.

## Repository structure
 - `Data/`  Input/Output data for the task_40 output data in `final_edjes_file/` and `final_nodes_file/`.
 - `code/`  Source code full scripts for the two tasks.

### Task 40 Subways II (score 1.0)
Reconstruction of subway network of different cities:
- folder: `code/task_24/`
  - `edges.py`, `nodes.py` scripts to extract information from data.
  - `main.py` main script to write output files.
  
### Task 24 Entanglement Percolation (score 0.6)
Study of entanglement percolation with quantum-swap on ER and WS graph and application on real data:
- folder `code/task_40/`
  - `scpp.py`,`percolation.py`,`generate_model.py`, `theo solution.py` contain the key functions to reproduce the main results.
  - `italy_graph.py` contain the simulation on the italian network.
  - `main.py`, `italy.py`  main scripts to analyze entanglement percolation. 


