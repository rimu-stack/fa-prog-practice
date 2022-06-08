import copy
import re
import time

from typing import Any, List
from exception import GiveUp, NotCorrectInput, FigureOnWay, SaveInFile
from pprint import pprint

def clean_board() -> list:
    return [["*"] * 8 for i in range(8)]

def load_figures_on_the_board(board: list) -> list:
    board[0] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    board[1] = ['P' for i in board[1]]
    board[6] = ['p' for i in board[6]]
    board[7] = [str(i.lower())for i in board[0]]
    
    return board

def print_board(board: list) -> None:
    result = '  ABCDEFGH' + '\n'
    i = 8

    for line in range(len(board)):
        result += f"{i} " + "".join(board[line]) + f" {i}" + '\n'
        i -= 1
    
    result += '  ABCDEFGH'
    print(result)

def check_move_figure(board: list, coor: list, figures: list) -> bool:
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
    
    if figure in ['P', 'p']:
        if all([dx == dy, end_point in figures, 
                coor[0][1] - coor[1][1] == 1,
                coor[0][0] - coor[1][0] == 1]):
            return True

        if figure == 'p':
            if coor[0][1] == 6:
                if all([dy == 2, dx == 0]):
                    return True
            if all([coor[0][1] - coor[1][1] == 1, dy == 0]):
                return True
        
        if figure == 'P':
            if coor[0][1] == 1:
                if all([dy == 2, dx == 0]):
                    return True
            if all([coor[0][1] - coor[1][1] == -1, dy == 0]):
                return True
    
    return False

def check_way(board: list, coor: list, figures: list) -> bool:
    figure = board[coor[0][1]][coor[0][0]]

    if figure is ['N', 'n']:
        return True
    
    x = coor[0][1]
    y = coor[0][0]
    
    while True:
        if all([y == coor[1][0], x == coor[1][1]]):
            return True

        if x > coor[1][1]:
            x -= 1
        if x < coor[1][1]:
            x += 1
        if y > coor[1][0]:
            y -= 1
        if y < coor[1][0]:
            y += 1
        
        if board[x][y] == '*':
            continue

        return False

def move_figure(board: list, coor: list) -> list:
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

def change_p(board: list, coor: list, figure: str) -> list:
    board[coor[1]][coor[0]] = str(figure)
    return board

def input_new_p(figures: list) -> str:
    while True:
        figure = input('Введите фигуру заместо пешки: ')

        if all([len(figure) == 1,
                figure in figures]):
            return figure
        
        print('Вы ввели некоректные данные, попробуйте снова')

def save_in_txt(move: str, history: dict) -> None:
    name = str(move.split(' ')[2])

    with open(f"{name}.txt", 'a+') as file:
        for step in history.values():
            file.write(step['move'] + '\n')

if __name__ == "__main__":
    board = list(load_figures_on_the_board(clean_board()))    
    color = 1
    history = {}

    print_board(board)
    
    while True:
        if color % 2 == 0:
            player = 'чёрных'
            figures = ['r', 'n', 'b', 'k', 'q', 'p']
            
        if color % 2 != 0:
            player = 'белых'
            figures = ['R', 'N', 'B', 'K', 'Q', 'P']

        try:
            move = input(f"Ход {player}: ").lower()
            
            if move == "give up":
                raise GiveUp
            
            if move.startswith('save in'):
                save_in_txt(move, history)
                raise SaveInFile

            if check_coor(move):
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

        except SaveInFile:
            print('Загрузка завершена')
            time.sleep(1)
            continue

        coor = transform_coor(move)

        try:
            if not check_move_figure(board, coor, figures):
                raise NotCorrectInput

            if not check_way(board, coor, figures):
                raise FigureOnWay

        except NotCorrectInput:
            print('Неверный ход')
            time.sleep(1)
            print('Попробуйте ещё раз')
            continue

        except FigureOnWay:
            print('Неверный ход. На пути союзник')
            time.sleep(1)
            print('Попробуйте ещё раз')
            continue

        board = move_figure(board, coor)

        if 'p' in board[0]:
            new_figure = input_new_p(figures)
            board = change_p(board, [0, board[0].index('p')], new_figure)
        if 'P' in board[7]:
            new_figure = input_new_p(figures)
            board = change_p(board, [7, board[7].index('P')], new_figure)

        step = str(color)
        history[step] = {
            'move': move, 
            'board': copy.deepcopy(board)
        }
        color += 1
        print_board(board)

    pprint(history)
    print('Матч завершён!')