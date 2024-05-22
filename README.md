# Battling Knights

## Description

"Battling Knights" is a turn-based strategy game where four knights, each starting in a different corner of an 8x8 board, navigate the arena to collect items, engage in combat, and attempt to be the last knight standing. The knights—Red, Blue, Green, and Yellow—can collect various items that enhance their attack and defense abilities. Knights must move carefully to avoid drowning in the surrounding water and to maximize their chances in battles against other knights. The game simulates their movements and encounters based on an input file of instructions, ultimately producing a JSON file that details the final state of the board, including the positions and statuses of the knights and items.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Solution Detail](#solution-detail)


## Installation

### 1: Code Execution
Ensure that Python is installed on your system. You can download it from python.org.
To check if Python is installed, run:
`python --version`

### 2: Test Execution
Install pytest to run the tests. You can install pytest using pip:
`pip install pytest`

To verify the installation, run:
`pytest --version`


## Usage

1: Ensure that both the code file `battling_knights.py` and the input file `moves.txt` are located in the same directory.
2: The format of the moves.txt file must be:
```
    GAME-START
    <Knight>:<Direction>
    <Knight>:<Direction>
    <Knight>:<Direction>
    ...
    GAME-END
```
3: Run the code file `battling_knights.py` using a Python compiler.
4: The highlights of the game will be printed to the console/terminal.
5: The final state of the board in JSON format will be stored in the `final_state.json` file, which can be found in the same directory as the code file.

## Solution Detail

### Input Validation:
1: Ensure the `moves.txt` file is available to read moves from.
2: Ensure all the moves in `moves.txt` are valid.

### Initialization:
1: Initialize the game board with knights and items. The default positions of each knight and item are described in the problem description.    

### Processing:
1: For each move, identify the knight and the direction, and apply this move to the knight. After each move, check the following:
    Is the knight drowned?
    Is the knight on any item?
    Is the knight in a fight with another knight?

### Final Output:
1: After all the moves are processed, convert the knights' and items' positions into JSON format and store it in final_state.json.