# Computing Algorithms - Dynamic Programming - Pay in Coins

## Overview

This problem involves calculating the number of ways a given amount can be paid using a specified number of coins. The coin values are prime numbers, including a gold coin equivalent to the total amount.

---

## Objectives

- Implement a dynamic programming solution to find all combinations of coins.
- Handle different input scenarios including fixed and ranged coin counts.

---

## Problem Description

### Input Format (`input.txt`)

- **Single integer**: Amount to be paid using all possible combinations of coins.
- **Two integers**: Amount and a fixed number of coins.
- **Three integers**: Amount, minimum, and maximum number of coins.

### Output Format (`output.txt`)

- Total number of ways to pay the amount for each input line.

---

## Example

### Input
5
8 3
8 2 5

### Output
6
2
10

### Explanation
1. **6 Ways for $5**: `5`, `2+3`, `1+1+3`, `1+2+2`, `1+1+1+2`, `1+1+1+1+1`
2. **2 Ways for $8 with 3 Coins**: `5+2+1`, `3+3+2`
3. **10 Ways for $8 with 2-5 Coins**

---

## Implementation Requirements

1. **Algorithm Design**:
  - Custom dynamic programming algorithm.
  - Accepts input file path from the command line.