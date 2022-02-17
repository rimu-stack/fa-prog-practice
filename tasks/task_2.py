# Написать калькулятор для строковых выражений вида '<число> <операция> <число>
# ', где <число> - не отрицательное целое число меньшее 100, записанное словами
# Результат выполнения операции вернуть в виде текстового представления числа. 
# Пример calc("двадцать пять плюс тринадцать") -> "тридцать восемь"

# Выполненные доп. задания:
# 1) Реализовать текстовый калькулятор для выражения из произвольного 
# количества операций с учетом приоритета операций. 
# Пример: calc("пять плюс два умножить на три минус один") -> "десять"
# Сложность 3

# 2) Добавить поддержку приоритета операций с помощью скобок. 
# Пример: calc("скобка открывается пять плюс два скобка закрывается умножить 
# на три минус один") -> "двадцать".
# Сложность 3

# 3) Добавить возможность использования отрицательных чисел. 
# Пример: calc("пять минус минус один") -> "шесть".
# Сложность 1



import re

def calc(condition: str) -> str:
    
    condition, after_operations = condition.lower(), []
    condition_split = condition.split()
    
    units = {
        'ноль': '0',
        'один': '1',
        'два': '2',
        'три': '3',
        'четыре': '4',
        'пять': '5',
        'шесть': '6',
        'семь': '7',
        'восемь': '8',
        'девять': '9',
        'десять': '10',
        'одиннадцать': '11',
        'двенадцать': '12',
        'тринадцать': '13',
        'четырнадцать': '14',
        'пятнадцать': '15',
        'шестнадцать': '16',
        'семнадцать': '17',
        'восемнадцать': '18',
        'девятнадцать': '19',
    }
    
    tenths = {
        'двадцать': '20',
        'тридцать': '30',
        'сорок': '40',
        'пятьдесят': '50',
        'шестьдесят': '60',
        'семьдесят': '70',
        'восемьдесят': '80',
        'девяносто': '90',
    }
    
    operations = {
        'плюс': '+',
        'минус': '-',
        'умножить': '*',
        'степени': '**',
    }

    bracket_1 = {
        'скобка': '',
    }
    direction_open = {
        'открывается': '',
    }
    direction_close = {
        
        'закрывается': '',
    }

    for i in range(len(condition_split)):
        if (condition_split[i] in bracket_1.keys() and 
            condition_split[i+1] in direction_open.keys()):
            after_operations.append('(')
            continue

        if (condition_split[i] in bracket_1.keys() and 
            condition_split[i+1] in direction_close.keys()):
            after_operations.append(')')
            continue

        if condition_split[i] in tenths.keys():
            if (i != len(condition_split)-1): 
                if condition_split[i+1] in units.keys():
                    after_operations.append(str(int(tenths[condition_split[i]]) + int(units[condition_split[i+1]])))
                    continue
        
        if (condition_split[i] in units.keys() and 
            condition_split[i-1] in tenths.keys() and 
            i != 0):
            continue
        
        if condition_split[i] in units.keys():
            after_operations.append(units[condition_split[i]])
            continue
        
        if condition_split[i] in tenths.keys():
            after_operations.append(tenths[condition_split[i]])
            continue
        
        if condition_split[i] in operations.keys():
            after_operations.append(operations[condition_split[i]])
            continue
        
    #print(after_operations)
    line = ' '.join(after_operations)
    answer = eval(line)
    #print(answer)
    return print(transformation(answer))

def transformation(answer: int) -> str:
    answer_append = []
    dic = {
        'ноль': '0',
        'один': '1',
        'два': '2',
        'три': '3',
        'четыре': '4',
        'пять': '5',
        'шесть': '6',
        'семь': '7',
        'восемь': '8',
        'девять': '9',
        'десять': '10',
        'одиннадцать': '11',
        'двенадцать': '12',
        'тринадцать': '13',
        'четырнадцать': '14',
        'пятнадцать': '15',
        'шестнадцать': '16',
        'семнадцать': '17',
        'восемнадцать': '18',
        'девятнадцать': '19',
        'двадцать': '20',
        'тридцать': '30',
        'сорок': '40',
        'пятьдесят': '50',
        'шестьдесят': '60',
        'семьдесят': '70',
        'восемьдесят': '80',
        'девяносто': '90',
        'минус': '-',
    }

    dic = {v:k for k, v in dic.items()}

    if answer < -100:
        return 'Меньше минус ста'
    if answer > 100:
        return 'Больше ста'

    if answer > 19:
        y = answer//10*10
        answer_append.append(dic[str(y)])
            
        if answer % 10 == 0:
            return ' '.join(answer_append)  
                
        
        if answer % 10 != 0:
            z = answer % 10
            answer_append.append(dic[str(z)])
            return ' '.join(answer_append)
            
    if answer < 20 and answer > 0:
            
        answer_append.append(dic[str(answer)])
        return ' '.join(answer_append) 

    if answer == 0:
        return 'ноль'

    if answer < 0:
        answer = -answer
        answer_append.append('минус')
        
        if answer > 19:
            y = answer//10*10
            answer_append.append(dic[str(y)])
                
            if answer % 10 == 0:
                return ' '.join(answer_append)  
                
        
        if answer % 10 != 0:
            z = answer % 10
            answer_append.append(dic[str(z)])
            return ' '.join(answer_append)
            
        if answer < 20:
            answer_append.append(dic[str(answer)])
            return ' '.join(answer_append)                 
            

if __name__ == '__main__':
    while True:
        condition = input("Введите выражения (для выхода используйте 'exit') ")
        
        if condition == 'exit':
            break
        
        if not re.search(r'[0-9A-z]', condition):
            calc(condition)
            
        else:
            print('Неверно')


#двадцать пять плюс тринадцать
#пять плюс два умножить на три минус один
#скобка открывается пять плюс два скобка закрывается умножить на три минус один
#пять минус минус один