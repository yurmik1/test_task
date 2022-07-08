import random


def hor_check(y, x, marker):  # проверка по горизонтали
    count = 1
    for i in range(1, 5):  # двигаемся направо
        if (matrix[y][x + i] if (x + i) <= 9 else 0) == marker:
            count += 1
        else:
            break
    for i in range(1, 5):  # двигаемся налево
        if (matrix[y][x - i] if (x - i) >= 0 else 0) == marker:
            count += 1
        else:
            break
    return count  # выводим количество маркеров


def ver_check(y, x, marker):  # проверка по вертикали
    count = 1
    for i in range(1, 5):  # двигаемся вниз
        if (matrix[y + i][x] if (y + i) <= 9 else 0) == marker:
            count += 1
        else:
            break
    for i in range(1, 5):  # двигаемся вверх
        if (matrix[y - i][x] if (y - i) >= 0 else 0) == marker:
            count += 1
        else:
            break
    return count


def dia_check_r(y, x, marker):  # проверка по диагонали вправо
    count = 1
    for i in range(1, 5):  # двигаемся вверх
        if (matrix[y - i][x + i] if ((y - i) >= 0) and ((x + i) <= 9) else 0) == marker:
            count += 1
        else:
            break
    for i in range(1, 5):  # двигаемся вниз
        if (matrix[y + i][x - i] if ((y + i) <= 9) and ((x - i) >= 0) else 0) == marker:
            count += 1
        else:
            break
    return count


def dia_check_l(y, x, marker):  # проверка по диагонали влево
    count = 1
    for i in range(1, 5):  # двигаемся вверх
        if (matrix[y - i][x - i] if ((y - i) >= 0) and ((x - i) >= 0) else 0) == marker:
            count += 1
        else:
            break
    for i in range(1, 5):  # двигаемся вниз
        if (matrix[y + i][x + i] if ((y + i) <= 9) and ((x + i) <= 9) else 0) == marker:
            count += 1
        else:
            break
    return count


def man_input():  # ввод человека
    x_in = float('inf')
    y_in = float('inf')
    while ((x_in and y_in) not in [num for num in range(0, 10)]) or ((x_in, y_in) in history_steps):
        try:
            x_in, y_in = map(int, input('Введите координаты клетки через пробел в формате "X Y".\n'
                                        'Например "2 1"\nX Y: ').split())
        except ValueError as exc:
            print(f'Ошибка: {exc}. Введите снова.')
    return x_in, y_in


def rec_exit():  # реквест на повтор игры
    answer = ''
    while answer not in ['да', 'нет']:
        try:
            answer = input('Повторить игру? Введите "Да" или "Нет" ').lower()
        except ValueError as exc:
            print(f'Ошибка: {exc}. Введите снова.')
    return True if answer == 'нет' else False


def bot_input():  # ввод бота
    x_in = float('inf')
    y_in = float('inf')
    while (x_in, y_in) in history_steps:
        x_in = random.randrange(0, 9, 1)
        y_in = random.randrange(0, 9, 1)
    return x_in, y_in


def all_check(y, x, marker):  # проверка всех проверок
    a = hor_check(y, x, marker)
    b = ver_check(y, x, marker)
    c = dia_check_r(y, x, marker)
    d = dia_check_l(y, x, marker)
    if 5 in [a, b, c, d]:
        return True
    else:
        return False


def draw_win():  # проверка на ничью
    if len(history_steps) == 101 and loser_man == False and loser_bot == False:
        print('Ничья')
        return True
    else:
        return False


def print_matrix(matrix):  # печать матрицы
    print('  0 1 2 3 4 5 6 7 8 9')
    for x, i in enumerate(matrix):
        print(x, *i)
    return


while True:
    print('Игра - обратные крестики нолики. Режим игры - человек и компьютер.\nПервым ходит человек. Проиграет '
          'тот, кто соберет 5 символов в ряд.\nИгроку нужно вводить кординаты точки для '
          'установки маркера (X).\nКоординаты поля выглядятследующим способом:')
    print('координаты x, y -  0..9')
    print('x →', end=' ')
    for i in range(10):  # Начало игры . Печать координат
        print(i, end=' ')
    print('')
    print('y ↓ 1')
    for i in range(2, 10):
        print(f'    {i}')

    loser_man = False
    loser_bot = False
    marker_man = 'X'
    marker_bot = 'O'
    history_steps = [(float('inf'), float('inf'))]  # инициализация списка шагов
    n = 10
    matrix = [["-" for i in range(n)] for j in range(n)]  # составление поля
    tmp = input('Для начала игры введите любой символ и нажмите на клавиатуре "Enter"')
    print('Игровое поле:')
    print_matrix(matrix)

    while not (loser_man or loser_bot):
        x, y = man_input()  # ход человека
        history_steps.append((x, y))  # добавление хода в реестр
        matrix[y][x] = marker_man  # добавление хода в матрицу
        loser_man = all_check(y, x, marker_man)  # проверка на проигрыш
        if loser_man:
            break
        if draw_win():  # проверка на ничью
            break

        x, y = bot_input()  # ход бота
        if all_check(y, x, marker_bot):  # проверка хода бота, если бот попадает на проигрыш, то повторить ход
            x, y = bot_input()
        history_steps.append((x, y))  # добавление хода в реестр
        matrix[y][x] = marker_bot  # добавление хода в матрицу
        loser_bot = all_check(y, x, marker_bot)  # проверка на проигрыш
        if loser_bot:
            break
        if draw_win():  # проверка на ничью
            break

        print_matrix(matrix)

        if not (loser_man or loser_bot):
            print('Продолжается игра')

    print_matrix(matrix)
    print(f'loser man - {loser_man}  |  loser bot - {loser_bot}') # печать результата
    if rec_exit():  # запрос на повтор
        break
