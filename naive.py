from itertools import product
from datetime import datetime


def reverse_complement(s: str) -> str:
    dict = {"A": "T", "T": "A", "C": "G", "G": "C"}
    s1 = ""

    for c in s[::-1]:
        s1 += dict[c]

    return s1


def cannonical_sequence(s: str) -> str:
    return min(s, reverse_complement(s))


def is_absent_in(x: str, s: str, do_print=False) -> bool:
    x1 = reverse_complement(x)

    for i in range(len(s) - len(x) + 1):
        substr = s[i : i + len(x)]

        if x == substr:
            if do_print:
                print(f"found {x}/{x1} at index {i}")
            return False
        if x1 == substr:
            if do_print:
                print(f"found {x}/{x1} at index {i}")
            return False

    if do_print:
        print(f"not found : {x}/{x1} not in s")
    return True


def substrings(x: str, kmin: int = 1) -> list[str]:
    l = []
    for i in range(len(x) - 1, kmin - 1, -1):
        for j in range(0, len(x) - i + 1):
            l.append(x[j : j + i])
    return l


def is_MAW(x: str, S: tuple[str, ...]) -> bool:
    for s in S:
        if not (is_absent_in(x, s, False)):
            return False
    sxs = substrings(x)
    for sx in sxs:
        for s in S:
            if is_absent_in(sx, s):
                return False
    return True


def naive(kmax: int, sequences: tuple[str]) -> list[tuple[int, list[str]]]:
    data = []
    for k in range(3, kmax + 1):
        t = datetime.now()
        all_combinations = product("ATGC", repeat=k)
        all_combinations_strings = map(lambda x: "".join(x), all_combinations)
        all_maws = list(
            filter(
                lambda x: x == cannonical_sequence(x) and is_MAW(x, sequences),
                all_combinations_strings,
            )
        )
        n = len(all_maws)
        if n != 0:
            print(str(k) + " : " + str(n) + " MAWs")
            data.append((k, all_maws))
        print("Processed in " + str(datetime.now() - t))

    return data
