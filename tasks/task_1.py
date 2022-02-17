# Вариант №1

# Реализовать программу, с которой можно играть в игру «Быки и коровы» 
# Программа загадывает число, пользователь вводит очередной вариант 
# отгадываемого числа, программа возвращает количество быков и коров и в случае
# выигрыша игрока сообщает о победе и завершается.
# Взаимодействие с программой производится через консоль, при запросе данных от
# пользователя программа сообщает, что ожидает от пользователя и проверяет 
# корректность ввода.

from random import randint
 
def check_number(number: str) -> bool:
    appart = [el for el in number]

    return True if len(appart) == len(set(appart)) else False


def enter_number() -> str:
    while True:
        enter = input()
        enter = enter.replace(' ', '')

        if check_number(enter) != True:
            print('Есть ещё одно условие: необходимо ввести 4 разные цифры. Повторите попытку, зная это:)')
            continue

        if enter.isdigit() and len(enter) == 4:
            return enter

        if len(enter) != 4 and enter.isdigit():
            print("Необходимо ввести 4-х значное число!")
            continue

        if not enter:
            print("Вы ничего не ввели")
            continue

        print("Это не число!")

def create_number() -> int:
    while True:
        number = ''

        for i in range(4):
            number += str(randint(0, 9))

        if check_number(number):
            return int(number)


if __name__ == "__main__":
    count, number = 0, create_number()
    print(f'Загаданное число: {number}')

    while True:
        count += 1
        print("Попытка: " + str(count))
        print("Введите 4-х значное число: ")

        arr1, arr2  = [], []
        attempt = enter_number()
        for el in str(number):
            arr1.append(el)
        for el in str(attempt):
            arr2.append(el)

        if number == int(attempt):
            print("Победа!")
            break

        else:
            cow, bull = 0, 0

            for x in range(4):
                if arr1[x] == arr2[x]:
                    bull += 1

                elif arr2[x] in arr1:
                    cow += 1

        print("Быков: " + str(bull) + " Коров: " + str(cow))
        print("----------------------")