"""perm 枚举内核的行为测试。

期望值都写成结果本身：排列与组合写成显式表，编号写成整数，错误写成异常类型。
在项目根目录执行：

    python3 -m unittest discover -s tests -v
"""

import unittest

from perm.core import (
    PermError,
    combinations,
    is_arrangement,
    next_permutation,
    permutations,
    prev_permutation,
    rank,
    take,
    total_count,
    unrank,
)


class PermTest(unittest.TestCase):
    """排列组合枚举内核的对外行为。"""

    def test_01_total_count_matches_arrangement_totals(self):
        cases = (
            ([], 1),
            ([7], 1),
            ([1, 2], 2),
            ([1, 2, 3], 6),
            ([1, 1, 2], 3),
            ([1, 1, 2, 2], 6),
            ([1, 1, 1, 2, 2], 10),
            ([1, 2, 3, 4, 5], 120),
            ("aab", 3),
            ("abracadabra", 83160),
        )
        for items, expected in cases:
            self.assertEqual(total_count(items), expected, "总数 %r" % (items,))
            self.assertEqual(total_count(list(items)), expected, "总数 %r" % (items,))
        self.assertEqual(total_count([1, 1, 1, 1]), 1, "全同元素只有一条")
        self.assertEqual(total_count([1, 1, 2, 2, 2, 2]), 15, "两个一四个二")

    def test_02_next_permutation_walks_forward(self):
        cases = (
            ([1, 2, 3], [1, 3, 2]),
            ([1, 3, 2], [2, 1, 3]),
            ([2, 1, 3], [2, 3, 1]),
            ([2, 3, 1], [3, 1, 2]),
            ([3, 1, 2], [3, 2, 1]),
            ([1, 1, 2], [1, 2, 1]),
            ([1, 2, 1], [2, 1, 1]),
            ([1, 2, 2, 3], [1, 2, 3, 2]),
            ([1, 3, 2, 1], [2, 1, 1, 3]),
            (["b", "a", "b"], ["b", "b", "a"]),
        )
        for items, expected in cases:
            original = list(items)
            got = next_permutation(items)
            self.assertEqual(got, expected, "下一排列 %r" % (items,))
            self.assertEqual(list(items), original, "入参被改写 %r" % (items,))
        for items in ([3, 2, 1], [2, 1, 1], [1, 1], [3, 2, 1, 1], [7], []):
            self.assertIsNone(next_permutation(items), "已是最后一条 %r" % (items,))

    def test_03_prev_permutation_walks_backward(self):
        cases = (
            ([3, 2, 1], [3, 1, 2]),
            ([3, 1, 2], [2, 3, 1]),
            ([2, 3, 1], [2, 1, 3]),
            ([2, 1, 3], [1, 3, 2]),
            ([1, 3, 2], [1, 2, 3]),
            ([2, 1, 1], [1, 2, 1]),
            ([1, 2, 1], [1, 1, 2]),
        )
        for items, expected in cases:
            self.assertEqual(prev_permutation(items), expected, "上一排列 %r" % (items,))
        for items in ([1, 2, 3], [1, 1, 2], [1, 2, 2], [1], []):
            self.assertIsNone(prev_permutation(items), "已是第一条 %r" % (items,))
        rows = [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
        for position, items in enumerate(rows):
            previous = prev_permutation(items)
            if position == 0:
                self.assertIsNone(previous, "第一条之前没有排列")
                continue
            self.assertEqual(previous, rows[position - 1], "上一排列 %r" % (items,))
            self.assertEqual(next_permutation(previous), items, "前后互逆 %r" % (previous,))

    def test_04_permutations_are_distinct_and_in_lexicographic_order(self):
        cases = (
            ([], [[]]),
            ([4], [[4]]),
            ([1, 2], [[1, 2], [2, 1]]),
            ([1, 2, 3], [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]),
            ([1, 1, 2], [[1, 1, 2], [1, 2, 1], [2, 1, 1]]),
            ([1, 1, 2, 2], [[1, 1, 2, 2], [1, 2, 1, 2], [1, 2, 2, 1],
                            [2, 1, 1, 2], [2, 1, 2, 1], [2, 2, 1, 1]]),
            ("aba", [["a", "a", "b"], ["a", "b", "a"], ["b", "a", "a"]]),
        )
        for items, expected in cases:
            got = permutations(items)
            self.assertEqual(len(got), total_count(items), "条数与总数 %r" % (items,))
            self.assertEqual(got, expected, "全排列 %r" % (items,))
            self.assertEqual(len(got), len({tuple(row) for row in got}), "排列重复 %r" % (items,))
            self.assertEqual(got, sorted(got), "字典序 %r" % (items,))

    def test_05_combinations_are_distinct_and_in_lexicographic_order(self):
        cases = (
            ([1, 2, 3, 4], 2, [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]),
            ([1, 2, 3, 4, 5], 3, [(1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5),
                                  (1, 4, 5), (2, 3, 4), (2, 3, 5), (2, 4, 5), (3, 4, 5)]),
            ([1, 1, 2], 2, [(1, 1), (1, 2)]),
            ([1, 1, 2, 2], 2, [(1, 1), (1, 2), (2, 2)]),
            ([1, 1, 1], 2, [(1, 1)]),
            ([1, 2, 3], 0, [()]),
            ([1, 2, 3], 3, [(1, 2, 3)]),
            ([1, 2, 3], 4, []),
        )
        for items, k, expected in cases:
            got = combinations(items, k)
            self.assertEqual(got, expected, "组合 %r 取 %d" % (items, k))
            self.assertEqual(len(got), len(set(got)), "组合重复 %r 取 %d" % (items, k))
            self.assertEqual(list(got), sorted(got), "组合字典序 %r 取 %d" % (items, k))
        self.assertEqual(combinations([3, 1, 2, 1], 2), [(1, 1), (1, 2), (1, 3), (2, 3)])

    def test_06_rank_locates_an_arrangement(self):
        cases = (
            ([1, 2, 3], [1, 2, 3], 0),
            ([1, 2, 3], [1, 3, 2], 1),
            ([1, 2, 3], [3, 1, 2], 4),
            ([1, 2, 3], [3, 2, 1], 5),
            ([1, 1, 2], [1, 1, 2], 0),
            ([1, 1, 2], [1, 2, 1], 1),
            ([1, 1, 2], [2, 1, 1], 2),
            ([1, 1, 2, 2], [2, 1, 2, 1], 4),
            ([1, 1, 2, 2], [2, 2, 1, 1], 5),
            ([1, 1, 2, 2, 2], [1, 2, 2, 2, 1], 3),
            ([1, 1, 2, 2, 2], [2, 1, 2, 1, 2], 5),
            ([1, 1, 2, 2, 2], [2, 2, 1, 2, 1], 8),
            ([1, 1, 2, 2, 2], [2, 2, 2, 1, 1], 9),
            ([1, 2, 3, 4], [3, 1, 4, 2], 13),
            ([1, 2, 3, 4], [4, 3, 2, 1], 23),
            ("aab", ["a", "b", "a"], 1),
        )
        for items, arrangement, expected in cases:
            self.assertEqual(rank(items, arrangement), expected, "编号 %r 里的 %r" % (items, arrangement))
        self.assertEqual(rank((1, 2, 3), (3, 2, 1)), 5, "元组入参")
        self.assertEqual(rank([1, 1, 2], [2, 1, 1]), 2, "重复元素")
        for index, row in enumerate([[1, 1, 2, 2], [1, 2, 1, 2], [1, 2, 2, 1],
                                     [2, 1, 1, 2], [2, 1, 2, 1], [2, 2, 1, 1]]):
            self.assertEqual(rank([1, 1, 2, 2], row), index, "逐条编号 %r" % (row,))

    def test_07_unrank_inverts_rank_and_rejects_bad_indexes(self):
        cases = (
            ([], 1),
            ([1, 2, 3], 6),
            ([1, 1, 2], 3),
            ([1, 1, 2, 2], 6),
            ([1, 1, 2, 2, 2], 10),
            ([1, 2, 3, 4], 24),
            ("aab", 3),
        )
        for items, expected_total in cases:
            total = total_count(items)
            self.assertEqual(total, expected_total, "总数 %r" % (items,))
            for index in range(total):
                arrangement = unrank(items, index)
                self.assertEqual(len(arrangement), len(list(items)), "%d 号长度 %r" % (index, items))
                self.assertEqual(rank(items, arrangement), index, "%d 号的反编号" % index)
            for over in (total, total + 1, 4096):
                with self.assertRaises(PermError):
                    unrank(items, over)
        self.assertEqual(unrank([1, 1, 2, 2], 3), [2, 1, 1, 2], "三号排列")
        self.assertEqual(unrank([1, 1, 2, 2], 0), [1, 1, 2, 2], "零号排列")

    def test_08_take_slices_the_enumeration_by_index(self):
        items = [1, 1, 2, 2]
        rows = [[1, 1, 2, 2], [1, 2, 1, 2], [1, 2, 2, 1], [2, 1, 1, 2], [2, 1, 2, 1], [2, 2, 1, 1]]
        self.assertEqual(total_count(items), 6, "总数")
        self.assertEqual(take(items, 0, 3), rows[0:3], "从 0 号取 3 条")
        self.assertEqual(take(items, 0, 6), rows, "取满")
        self.assertEqual(take(items, 2, 3), rows[2:5], "从 2 号取 3 条")
        self.assertEqual(take(items, 5, 1), rows[5:6], "最后一条")
        self.assertEqual(take(items, 4, 10), rows[4:6], "尾段少于条数")
        self.assertEqual(take(items, 6, 2), [], "越过末尾")
        self.assertEqual(take(items, 0, 0), [], "条数为零")
        self.assertEqual(take([], 0, 3), [[]], "空元素只有一条空排列")
        for start in range(6):
            for count in range(4):
                self.assertEqual(take(items, start, count), rows[start:start + count],
                                 "第 %d 号起取 %d 条" % (start, count))

    def test_09_invalid_arguments_are_reported(self):
        for bad in (True, False, 1.5, "2", None):
            with self.assertRaises(TypeError):
                combinations([1, 2, 3], bad)
        with self.assertRaises(PermError):
            combinations([1, 2, 3], -1)
        for bad in (True, False, 2.0, None):
            with self.assertRaises(TypeError):
                unrank([1, 2, 3], bad)
        for bad in (-1, -7):
            with self.assertRaises(PermError):
                unrank([1, 2, 3], bad)
        with self.assertRaises(PermError):
            unrank([1, 2, 3], 6)
        for bad in (True, False, 1.5, "2"):
            with self.assertRaises(TypeError):
                take([1, 2, 3], bad, 1)
        for bad in (True, False, 1.5, "2"):
            with self.assertRaises(TypeError):
                take([1, 2, 3], 0, bad)
        with self.assertRaises(PermError):
            take([1, 2, 3], -1, 1)
        with self.assertRaises(PermError):
            take([1, 2, 3], 0, -1)
        for bad in (7, 1.5, None):
            with self.assertRaises(TypeError):
                total_count(bad)

    def test_10_arrangement_validation(self):
        self.assertTrue(is_arrangement([1, 1, 2], [2, 1, 1]))
        self.assertTrue(is_arrangement("aba", "aab"))
        self.assertTrue(is_arrangement([], []))
        self.assertTrue(is_arrangement((1, 2, 3), [3, 2, 1]))
        self.assertFalse(is_arrangement([1, 1, 2], [1, 2, 2]))
        self.assertFalse(is_arrangement([1, 2, 3], [1, 2]))
        self.assertFalse(is_arrangement([1, 2], [1, 2, 3]))
        self.assertFalse(is_arrangement([1, 1, 2], [1, 1, 2, 2]))
        self.assertFalse(is_arrangement([1, 2, 3], [1, 2, 4]))
        with self.assertRaises(PermError):
            rank([1, 1, 2], [1, 2, 2])
        with self.assertRaises(PermError):
            rank([1, 2, 3], [1, 2])
        with self.assertRaises(PermError):
            rank([1, 2, 3], [3, 2, 4])
        self.assertEqual(rank([1, 1, 2], [1, 1, 2]), 0, "最小排列编号为零")
        self.assertEqual(rank([1, 1, 2, 2, 2], [1, 1, 2, 2, 2]), 0, "最小排列编号为零")
        self.assertEqual(rank([1, 2, 3, 4], [1, 2, 3, 4]), 0, "最小排列编号为零")


if __name__ == "__main__":
    unittest.main()
