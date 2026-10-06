"""perm：排列组合枚举内核（字典序下一排列、去重全排列、组合生成、字典序编号与反编号、按序裁切）。

组件：
    PermError         参数非法、候选与元素不是同一组、编号越界时抛出
    total_count       同一个多重集的全部不同排列条数
    next_permutation  字典序里的下一条排列，已经是最后一条时返回 None
    prev_permutation  字典序里的上一条排列，已经是第一条时返回 None
    permutations      按字典序列出全部去重排列
    combinations      按字典序列出全部去重组合
    is_arrangement    候选是否与元素是同一个多重集
    rank              一条排列在字典序里的编号，从 0 开始
    unrank            编号对应的排列
    take              按编号裁切连续取出一段排列

约定：
    * 元素是同一类型且可比较的对象；相同的元素视为不可区分，因此同一个多重集里
      每条排列只出现一次，编号与排列一一对应；
    * 元素只参与比较与相等判断，内核不改写调用方传入的序列；
    * 元素为空时看作一条空排列，编号 0；
    * 全程只依赖调用参数，不做任何输入输出，不读时钟，不使用随机数。
"""

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


class PermError(ValueError):
    """排列组合枚举里的参数与编号错误。"""


def _counts(items):
    """把序列整理成元素到出现次数的映射。"""
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


def _factorial(number):
    """number 的阶乘；调用方只传非负整数。"""
    result = 1
    for factor in range(2, number + 1):
        result *= factor
    return result


def _arrangements(counts, slots):
    """把 counts 里的元素填满 slots 个位置的方法数。"""
    total = _factorial(slots)
    for count in counts.values():
        total //= _factorial(count)
    return total


def _check_int(value, name):
    """校验一个非负整数参数，返回它本身。"""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("%s 必须是整数" % (name,))
    if value < 0:
        raise PermError("%s 不能为负" % (name,))
    return value


def total_count(items):
    """同一个多重集的全部不同排列条数。"""
    counts = _counts(items)
    return _factorial(sum(counts.values()))


def next_permutation(items):
    """字典序里 items 的下一条排列；已经是最后一条时返回 None。

    入参不被改写，结果是一个新列表。
    """
    seq = list(items)
    pivot = len(seq) - 2
    while pivot >= 0 and seq[pivot] >= seq[pivot + 1]:
        pivot -= 1
    if pivot < 0:
        return None
    spot = len(seq) - 1
    while seq[spot] < seq[pivot]:
        spot -= 1
    seq[pivot], seq[spot] = seq[spot], seq[pivot]
    seq[pivot + 1:] = reversed(seq[pivot + 1:])
    return seq


def prev_permutation(items):
    """字典序里 items 的上一条排列；已经是第一条时返回 None。"""
    seq = list(items)
    pivot = len(seq) - 2
    while pivot >= 0 and seq[pivot] <= seq[pivot + 1]:
        pivot -= 1
    if pivot < 0:
        return None
    spot = len(seq) - 1
    while seq[spot] >= seq[pivot]:
        spot -= 1
    seq[pivot], seq[spot] = seq[spot], seq[pivot]
    return seq


def permutations(items):
    """按字典序列出同一个多重集的全部不同排列，每条都是一个列表。"""
    seq = list(items)
    counts = _counts(seq)
    out = []
    _collect(sorted(seq), counts, [], len(seq), out)
    return out


def _collect(keys, counts, prefix, size, out):
    """按字典序把排列追加到 out。"""
    if len(prefix) == size:
        out.append(list(prefix))
        return
    for key in keys:
        if counts[key] > 0:
            counts[key] -= 1
            prefix.append(key)
            _collect(keys, counts, prefix, size, out)
            prefix.pop()
            counts[key] += 1


def combinations(items, k):
    """按字典序列出全部不同组合，每条组合都是一个元组。

    元素按大小排序后再枚举，元素相同而位置不同的组合只算一条，
    重复元素不会带来重复结果。
    """
    k = _check_int(k, "k")
    seq = sorted(items)
    size = len(seq)
    if k > size:
        return []
    out = []
    spots = list(range(k))
    while True:
        combo = tuple(seq[spot] for spot in spots)
        out.append(combo)
        spot = k - 1
        while spot >= 0 and spots[spot] == size - k + spot:
            spot -= 1
        if spot < 0:
            break
        spots[spot] += 1
        for tail in range(spot + 1, k):
            spots[tail] = spots[tail - 1] + 1
    return out


def is_arrangement(items, candidate):
    """candidate 是否与 items 是同一个多重集。"""
    return _counts(items) == _counts(list(candidate))


def rank(items, arrangement):
    """一条排列在其多重集的字典序里的编号，从 0 开始。

    候选与元素不是同一组时报错。
    """
    target = list(arrangement)
    if not is_arrangement(items, target):
        raise PermError("候选与元素不是同一个多重集")
    counts = _counts(items)
    keys = sorted(counts)
    result = 0
    for position, item in enumerate(target):
        for key in keys:
            if key >= item:
                break
            if counts[key] == 0:
                continue
            counts[key] -= 1
            result += _arrangements(counts, len(target) - position - 1)
        counts[item] -= 1
    return result


def unrank(items, index):
    """编号 index 对应的排列；编号越界时报错。"""
    index = _check_int(index, "index")
    seq = list(items)
    counts = _counts(seq)
    size = len(seq)
    if index >= total_count(seq):
        raise PermError("编号越界")
    keys = sorted(counts)
    out = []
    for position in range(size):
        for key in keys:
            if counts[key] == 0:
                continue
            counts[key] -= 1
            block = _arrangements(counts, size - position - 1)
            if index <= block:
                out.append(key)
                break
            index -= block
            counts[key] += 1
    return out


def take(items, start, count):
    """按编号裁切：从 start 号开始连续取 count 条排列。

    只取需要的那些编号，不物化整段枚举；start 越过末尾时返回空列表。
    """
    start = _check_int(start, "start")
    count = _check_int(count, "count")
    seq = list(items)
    total = total_count(seq)
    if start >= total:
        return []
    limit = min(count, total)
    return [unrank(seq, index) for index in range(start, limit)]
