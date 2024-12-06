# Computing Algorithms - Graph Algorithms - K-Shortest Loopless Paths

## Overview

This problem involves finding the K-shortest loopless paths in a directed graph from a source to a destination vertex. The first path must be the shortest, and subsequent paths are approximations.

## Objectives

- Implement a custom algorithm to solve the K-shortest paths problem.
- Use efficient data structures for graph traversal.

## Problem Description

### Input Format (`input.txt`)

1. **Two integers**: Number of vertices (`N`) and edges (`M`).
2. **Edge list**: `ai bi wi` where `ai` is the start vertex, `bi` is the end vertex, and `wi` is the edge weight.
3. **Two vertices and K**: Source (`s`), destination (`d`), and number of paths (`K`).

### Output Format (`output.txt`)

- List of K-shortest paths and their costs.

## Example

### Input
6 9
C D 3
C E 2
D F 4
E D 1
E F 2
E G 3
F G 2
F H 1
G H 2
C H 3

### Output
5, 7, 8

### Explanation
1. **Path 1**: `C→E→F→H` - Cost = 5
2. **Path 2**: `C→E→G→H` - Cost = 7
3. **Path 3**: `C→D→F→H` - Cost = 8

## Implementation Requirements

1. **Algorithm Design**:
  - Implement a custom K-shortest paths algorithm.
  - Command-line input for the file path.