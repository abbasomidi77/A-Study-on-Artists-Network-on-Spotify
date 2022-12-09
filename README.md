# CPSC572 Networks Project Code

## Installation

Requires Python3

```bash
python3 install spotipy
```

```bash
python3 install csv
```

## Usage

To generate nodes and edges csv lists:

```bash
python3 getNetwork.py
```
Output as **final_edges.csv** and **final_nodes.csv** in files folder

To run path analysis:

```bash
python3 analysis.py
```

Note: input provided as **nodestats.csv** in files folder exported from Gephi after statistical and network analysis performed on nodes and edges

Get output as **best_paths.csv** and **best_paths_scores.csv** in files folder
