# Klotski_Puzzle_Solver

## Overview
The Klotski Puzzle Solver is a Python program that efficiently solves Klotski puzzles using various search algorithms. This project showcases a strong understanding of data structures and algorithms, particularly A* search with the Manhattan distance heuristic and Depth-First Search (DFS), to explore and solve complex Klotski puzzle configurations.

## Features
* A* Search: The program employs the A* search algorithm, which is a popular choice for solving puzzles, incorporating the Manhattan distance heuristic to guide its search process. This heuristic helps estimate the minimum number of moves required to reach the goal state, leading to efficient and informed exploration of puzzle states.

* Depth-First Search (DFS): In addition to A* search, the solver utilizes Depth-First Search to explore complex puzzle configurations more thoroughly. DFS can be particularly effective for certain Klotski puzzles, ensuring a comprehensive examination of potential solutions.

* Visualization Tools: The Klotski Puzzle Solver includes visualization tools to provide a clear and intuitive view of the solving process and results. Users can watch as the program navigates through puzzle states to reach the solution.

## Input Format
The input is a plain text file that stores an initial puzzle configuration. See below for an example of the input file content. It contains 20 digits arranged in 5 rows and 4 digits per row. The empty squares are denoted by 0. The single pieces are denoted by 7. The 2x2 piece is denoted by 1. The 5 1x2 pieces are denoted by one of {2, 3, 4, 5, 6}, but the numbers are assigned at random.
```
2113
2113
4665
4775
7007
```
## Output Format
The two output files should store the DFS and A* solution for the input file provided.

See below for an example of the content of the output file. The empty squares are denoted by 0. The single pieces are denoted by 4. The 2x2 piece is denoted by 1. The horizontal 1x2 pieces are denoted by 2. The vertical 1x2 pieces are denoted by 3.
```
Cost of the solution: 116
3113
3113
3223
3443
4004

3113
3113
3223
3443
0404
⋮
```
## Usage
Clone this repository to your local machine and navigate to the project directory. Run the solver with your preferred input puzzle with the following command.
```
python3 main.py  <input file>  <DFS output file>  <A* output file>
```
