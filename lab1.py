# Получение матрицы вводом от пользователя
# Главное меню
def get_matrix():
    new_matrix = []
    print('Как вводить матрицу?')
    print('[0] Ввести матрицу из файла (Файл желательно, чтобы находился прям в одной директории с программой')
    print('[1] Ввести матрицу самостоятельно вводом с клавиатуры в программу')

    answer = int(input())
    if answer == 1:
        print('Сколько у вас строк в матрице?')
        rows = int(input())
        if rows != 1:
            for i in range(rows):
                a = []
                for j in range(rows + 1):
                    print('Введите элемент: строка', i + 1, ', столбец:', j + 1)
                    a.append(float(input()))
                new_matrix.append(a)
            print('Ваша матрица: ')
            print(new_matrix)
            return new_matrix
        else:
            print('Матрица должна быть 2*2 3*3 или больше.')
            return get_matrix()
    elif answer == 0:
        print('Введите название файла: ')
        return get_matrix_from_file(input())
    else:
        print('К сожалению произошла ошибка с файлом, попробуйте ещё раз')
        return get_matrix()


# Получение матрицы из файла
def get_matrix_from_file(filename):
    with open(filename) as f:
        matrix_from_file = [list(map(float, row.split())) for row in f.readlines()]
    print('Матрица:')
    print_matrix(matrix_from_file, 5)
    return matrix_from_file


# Реализация метода Гаусса
def do_gauss_method(input_matrix):
    check_square_matrix(input_matrix)
    is_singular(input_matrix)
    print('Начинаем метод Гаусса')
    length_of_matrix = len(input_matrix)
    do_triangle_matrix(input_matrix)
    input_answer_matrix = [0 for i in range(length_of_matrix)]
    for k in range(length_of_matrix - 1, -1, -1):
        input_answer_matrix[k] = (input_matrix[k][-1] - sum(
            [input_matrix[k][j] * input_answer_matrix[j] for j in range(k + 1, length_of_matrix)])) / input_matrix[k][k]
    print('Ответы: ')
    for i in range(len(input_answer_matrix)):
        print('x[', i + 1, '] =', "%5.3f" % input_answer_matrix[i])
    return input_answer_matrix


# Проверяем матрицу
def check_square_matrix(input_matrix):
    print('Проверка есть ли решения у матрицы')
    for i in range(len(input_matrix)):
        if len(input_matrix) + 1 != len(input_matrix[i]):
            raise Exception('Размер матрицы неверен.')
        count = 0
        for j in range(len(input_matrix[i])-1):
            if input_matrix[i][j] == 0:
                count += 1
        if count == len(input_matrix[i])-1:
            raise Exception('Ошибка: у матрицы нет решений')
    print('Проверка прошла успешно.')


def do_triangle_matrix(input_matrix):
    print('Создание треугольной матрицы')
    length_of_matrix = len(input_matrix)  # = кол-во строк
    for k in range(length_of_matrix - 1):
        print('Итерация №', k + 1)
        print('Матрица до: ')
        print_matrix(input_matrix, 5)
        get_max_element_in_column(input_matrix, k)
        print('Матрицы после: ')
        print_matrix(input_matrix, 5)
        for i in range(k + 1, length_of_matrix):
            div = input_matrix[i][k] / input_matrix[k][k]
            input_matrix[i][-1] -= div * input_matrix[k][-1]
            for j in range(k, length_of_matrix):
                input_matrix[i][j] -= div * input_matrix[k][j]
        print_matrix(input_matrix, 5)
    return length_of_matrix


# Проверка на вырожденность матрицы
def is_singular(input_matrix):
    print('Проверка на вырожденность')
    if count_determinant_for_square_matrix(input_matrix) == 0:
        raise Exception('Ваша матрица вырожденная')
    else:
        print('Проверка на вырожденность успешно пройдена')


# Ищем главный элемент в столбце
def get_max_element_in_column(input_matrix, number_of_column):
    max_element = input_matrix[number_of_column][number_of_column]
    max_row = number_of_column
    for j in range(number_of_column + 1, len(input_matrix)):
        if abs(input_matrix[j][number_of_column]) > abs(max_element):
            max_element = input_matrix[j][number_of_column]
            max_row = j
    if max_row != number_of_column:
        input_matrix[number_of_column], input_matrix[max_row] = input_matrix[max_row], input_matrix[number_of_column]
    print('The max element between not fixed rows is', "%.4f" % max_element, 'in row', max_row + 1)
    return input_matrix


# Печать матрицы в комфортном для чтения виде
def print_matrix(input_matrix, decimals):
    for i in range(len(input_matrix)):
        for j in range(len(input_matrix[i])):
            print('|', "%10.4f" % (input_matrix[i][j]))
        print()


# Create residual vector (вектор невязок)
def do_residual_vector(input_matrix, input_answer_matrix):
    big_matrix = []
    little_matrix = []
    for i in range(len(input_matrix)):
        big_matrix.append(input_matrix[i][0:len(input_matrix)])
        little_matrix.append(input_matrix[i][len(input_matrix):])
    x_matrix = input_answer_matrix
    temp = [0 for i in range(len(input_matrix))]
    residual_vector = [0 for i in range(len(input_matrix))]
    print('Вектор невязок:')
    for i in range(len(big_matrix)):
        temp[i] = 0
        for j in range(len(big_matrix)):
            temp[i] += x_matrix[j] * big_matrix[i][j]
        residual_vector[i] = temp[i] - little_matrix[i][0]
        print('r[', i + 1, '] =', residual_vector[i], end='\n')


# Считаем детерминант матрицы
def count_determinant_for_square_matrix(input_matrix):
    determinant = 1
    for i in range(len(input_matrix)):
        determinant *= input_matrix[i][i]
    print('Детерминант вашей матрицы: =', round(determinant, 5))
    return round(determinant, 5)


try:
    main_matrix = get_matrix()
    answer_matrix = do_gauss_method(main_matrix)
    do_residual_vector(main_matrix, answer_matrix)
except Exception as ex:
    template = "Появилось исключение \n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)