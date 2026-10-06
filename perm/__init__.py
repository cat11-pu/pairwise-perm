"""perm：排列组合枚举内核。

对外入口：
    PermError         参数非法、候选与元素不是同一组、编号越界时抛出
    total_count       同一个多重集的全部不同排列条数
    next_permutation  字典序里的下一条排列
    prev_permutation  字典序里的上一条排列
    permutations      按字典序列出全部去重排列
    combinations      按字典序列出全部去重组合
    is_arrangement    候选是否与元素是同一个多重集
    rank              一条排列在字典序里的编号
    unrank            编号对应的排列
    take              按编号裁切连续取出一段排列
"""

from .core import (
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

__all__ = [
    "PermError",
    "combinations",
    "is_arrangement",
    "next_permutation",
    "permutations",
    "prev_permutation",
    "rank",
    "take",
    "total_count",
    "unrank",
]
