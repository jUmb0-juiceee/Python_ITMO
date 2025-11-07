# Вариант 17 - Root = 17; height = 4
# left_leaf = (root-4)^2, right_leaf = (root+3)*2

from pprint import pprint


def gen_bin_tree(root=17, height=4, left_branch=lambda root: (root - 4) ** 2, right_branch=lambda root: (root + 3) * 2):

    def turn_list_to_dict(tree, now=0):
        if now >= len(tree):
            return []
        else:
            ans = {tree[now]: [turn_list_to_dict(tree, now * 2 + 1), turn_list_to_dict(tree, now * 2 + 2)]}
            return ans

    if height == 0:
        numbers = {root}
        return numbers
    else:
        numbers = [root]
        cnt = 1
        while cnt <= height:
            for i in numbers[-(2 ** (cnt - 1)):]:
                numbers.append(left_branch(i))
                numbers.append(right_branch(i))
            cnt += 1
        numbers = turn_list_to_dict(numbers)
        return numbers


def main():
    try:
        print('Если хотите дать алгоритму на вход свои значения root и height - введите +, если нет - введите - ('
              'значения по умолчанию root = 17, height = 4)')
        while True:
            sign = str(input())
            if sign == '-':
                print(gen_bin_tree())
                break
            if sign == '+':
                print('Введите свои значения параметров root и height в строчку')
                a, b = map(int, input().split())
                print(gen_bin_tree(a, b))
                break
            else:
                print('Попробуйте ещё раз корректно ввести свой ответ на предыдыщий вопрос (введите + или -)')

    except ValueError as e:
        print(f'Ошибка ввода данных: {e}')

    except Exception as ex:
        print(f'Непредвиденная ошибка: {ex}')


if __name__ == '__main__':
    main()
