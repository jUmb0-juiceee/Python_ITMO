import timeit
import matplotlib.pyplot as plt
from functools import lru_cache


# для применения кэширования можно раскомментировать следующую строчку
# @lru_cache()
def gen_bin_tree_iterative(root=17, height=4, left_branch=lambda root: (root - 4) ** 2,
                           right_branch=lambda root: (root + 3) * 2):
    def turn_list_to_dict(tree, now=0):
        if now >= len(tree):
            return []
        else:
            ans = {tree[now]: [turn_list_to_dict(tree, now * 2 + 1), turn_list_to_dict(tree, now * 2 + 2)]}
            return ans

    if height == 0:
        tree = {root}
        return tree
    else:
        tree = [root]
        cnt = 1
        while cnt <= height:
            for i in tree[-(2 ** (cnt - 1)):]:
                tree.append(left_branch(i))
                tree.append(right_branch(i))
            cnt += 1
        tree = turn_list_to_dict(tree)
        return tree


# для применения кэширования можно раскомментировать следующую строчку
# @lru_cache()
def gen_bin_tree_recursive(root: int, height: int, left_branch=lambda root: (root - 4) ** 2,
                           right_branch=lambda root: (root + 3) * 2) -> dict[int: list[dict, dict]]:
    if height == 0:
        return {}
    height -= 1
    bin_tree = {
        root: [gen_bin_tree_recursive(left_branch(root), height), gen_bin_tree_recursive(right_branch(root), height)]}
    return bin_tree


def benchmark(func, height, number=1, repeat=5):
    # несколько повторов для усреднения
    times = timeit.repeat(lambda: func(17, height), number=number, repeat=repeat)
    min_time = min(times)  # вычисляем среднее время из серии измерений
    return min_time


def main():
    height_data = list(range(10))
    res_recursive = []
    res_iterative = []
    for n in height_data:
        print(n)
        res_recursive.append(benchmark(gen_bin_tree_recursive, n, 1000, 5))
        res_iterative.append(benchmark(gen_bin_tree_iterative, n, 1000, 5))

    plt.plot(height_data, res_recursive, label="Рекурсивный")
    plt.plot(height_data, res_iterative, label="Итеративный")
    plt.xlabel("height")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение построения дерева рекурсивным и итеративным алгоритмами по среднему времени выполнения")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
