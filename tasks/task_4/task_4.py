import re
import time

from typing import Any, List
from exception import GiveUp, NotCorrectInput

def clean_board() -> list:
    return [["*"] * 8 for i in range(8)]

def load_figures_on_the_board(board: list) -> list:
    board[0] = ['R', 'K', 'B', 'K', 'Q', 'B', 'K', 'R']
    board[1] = ['P' for i in board[1]]
    board[6] = ['p' for i in board[6]]
    board[7] = [str(i.lower())for i in board[0]]
    
    return board

def print_board(board: list) -> None:
    result = ''

    for line in range(len(board)):
        result += "".join(board[line]) + '\n'
    
    print(result)

def check_move(board: list, coor: tuple) -> bool:
    pass

def move(board: list, coor: list) -> list:
    pass

def transform_coor(line: str) -> List[list, list]:
    coor_x = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7
    }

    coor_y = {
        '1': 0,
        '2': 1,
        '3': 2,
        '4': 3,
        '5': 4,
        '6': 5,
        '7': 6,
        '8': 7
    }

    return [[coor_x[line[0]], coor_y[line[1]]], 
            [coor_x[line[2]], coor_y[line[3]]]]

def check_coor(coor: str) -> bool:
    return any([len(coor) != 4, 
                    not re.match("[a-h]", coor[0]),
                    not re.match("[1-8]", coor[1]),
                    not re.match("[a-h]", coor[2]),
                    not re.match("[1-8]", coor[3])])

if __name__ == "__main__":
    board = list(load_figures_on_the_board(clean_board()))    
    color = 1

    print_board(board)
    
    while True:
        if color % 2 == 0:
            player = 'чёрных'
        if color % 2 != 0:
            player = 'белых'

        try:
            coor = input(f"Ход {player}: ").lower()
            
            if coor == "give up":
                raise GiveUp

            if check_coor(coor):
                raise NotCorrectInput
        
        except NotCorrectInput:
            print('Неверный ход')
            time.sleep(1)
            print('Попробуйте ещё раз')
            continue

        except GiveUp:
            print(f"{player[0].upper() + player[1:-2]}ые сдались!")
            time.sleep(1)
            break

        coor = transform_coor(coor)

        try:
            if not check_move(coor):
                raise NotCorrectInput

        except NotCorrectInput:
            print('Неверный ход')
            time.sleep(1)
            print('Попробуйте ещё раз')
            continue

        move(coor)

        color += 1
        print_board(board)

    print('Матч завершён!')