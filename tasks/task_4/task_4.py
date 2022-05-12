import re
import time

from typing import Any, List
from exception import GiveUp, NotCorrectInput

def clean_board() -> list:
    return [["*"] * 8 for i in range(8)]

def load_figures_on_the_board(board: list) -> list:
    board[0] = ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R']
    board[1] = ['P' for i in board[1]]
    board[6] = ['p' for i in board[6]]
    board[7] = [str(i.lower())for i in board[0]]
    
    return board

def print_board(board: list) -> None:
    result = ''

    for line in range(len(board)):
        result += "".join(board[line]) + '\n'
    
    print(result)

def check_move(board: list, coor: list, figures: list) -> bool:
    figure = board[coor[0][1]][coor[0][0]]
    end_point = board[coor[1][1]][coor[1][0]]

    if figure == '*':
        print('Поле не может ходить самостоятельно!')
        return False

    if figure not in figures:
        print('Вы не можете ходить за противника!')
        return False
    
    if end_point in figures:
        print('Вы не можете пойти на эту клетку, там стоит другая Ваша фигура')
        return False
    
    figures = [i.lower() for i in figures]
    
    dy = abs(coor[0][1] - coor[1][1])
    dx = abs(coor[0][0] - coor[1][0])

    if figure in ['K', 'k']:
        if all([dx == 1, dy == 1]):
                return True
    
    if figure in ['N', 'n']:
        if any([all([dx == 1, dy == 2]),
                all([dx == 2, dy == 1])]):
            return True
    
    if figure in ['R', 'r']:
        if any([coor[0][1] == coor[1][1],
                coor[0][0] == coor[1][0]]):
            return True
    
    if figure in ['B', 'b']:
        if dx == dy:
            return True
    
    if figure in ['Q', 'q']:
        if any([coor[0][1] == coor[1][1],
                coor[0][0] == coor[1][0],
                dx == dy]):
            return True
    
    return False

def move(board: list, coor: list) -> list:
    board[coor[1][1]][coor[1][0]] = str(board[coor[0][1]][coor[0][0]])
    board[coor[0][1]][coor[0][0]] = '*'

    return board

def transform_coor(line: str) -> list:
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
        '1': 7,
        '2': 6,
        '3': 5,
        '4': 4,
        '5': 3,
        '6': 2,
        '7': 1,
        '8': 0
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
            figures = ['r', 'n', 'b', 'k', 'q', 'p']
            
        if color % 2 != 0:
            player = 'белых'
            figures = ['R', 'N', 'B', 'K', 'Q', 'P']

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
            if not check_move(board, coor, figures):
                raise NotCorrectInput

        except NotCorrectInput:
            print('Неверный ход')
            time.sleep(1)
            print('Попробуйте ещё раз')
            continue

        move(board, coor)

        color += 1
        print_board(board)

    print('Матч завершён!')

# from task_4 import clean_board, load_figures_on_the_board, transform_coor, check_move