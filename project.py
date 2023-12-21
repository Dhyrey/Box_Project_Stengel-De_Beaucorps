from dataclasses import dataclass
from sys import argv, exit
from itertools import product
from readfa import *
from csv import *
from functools import cache
from suffix_tree import tree, SuffixTree


@dataclass
class sequence:
    description: str
    sequence: str


@cache
def reverse_complement(s: str) -> str:
    dict = {"A": "T", "T": "A", "C": "G", "G": "C"}
    s1 = ""

    for c in s[::-1]:
        s1 += dict[c]

    return s1


@cache
def cannonical_sequence(s: str) -> str:
    return min(s, reverse_complement(s))


@cache
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


def substrings(x: str) -> list[str]:
    l = []
    for i in range(len(x)):
        for j in range(i + 1, len(x) + 1):
            if j - i == len(x):
                continue
            l.append(x[i:j])
    return l


def is_MAW(x: str, S: tuple[str]) -> bool:
    for s in S:
        if not (is_absent_in(x, s, False)):
            return False
    sxs = substrings(x)
    for sx in sxs:
        for s in S:
            if is_absent_in(sx, s):
                return False
    return True


def read_file_lines(filename: str) -> list[str]:
    with open(filename, "r") as f:
        return f.readlines()


def parse_file(filename: str) -> list[sequence]:
    lines = read_file_lines(filename)
    assert len(lines) % 2 == 0, "Wrong format ?"

    sequences = []

    for i in range(0, len(lines), 2):
        assert lines[i][0] == ">", "Wrong format ?"
        seq = sequence(lines[i][1:].strip(), lines[i + 1].strip())
        sequences.append(seq)

    return sequences


def write_tsv(data: list[tuple[int, list[str]]], filename: str) -> None:
    file = open(filename, "w")
    for d_line in data:
        s_line = str(d_line[0]) + "\t" + ",".join(d_line[1]) + "\n"
        file.write(s_line)
    file.close()


def naive(kmax: int, sequences: tuple[str]) -> list[tuple[int, list[str]]]:
    data = []
    for k in range(3, kmax + 1):
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

    return data


def bfs(kmax: int, seqs: tuple[str]) -> set[str]:
    current = list("ACGT")
    maws: set[str] = set()
    seen: set[str] = set()
    k = 1
    toexplore = []
    while k <= kmax and current:
        for mot in current:
            reversed = reverse_complement(mot)
            if reversed in seen:
                continue

            if any(map(lambda x: mot.endswith(x) or reversed.startswith(x), maws)):
                continue

            if any(map(lambda seq: not is_absent_in(mot, seq), seqs)):
                for c in "ATGC":
                    toexplore.append(mot + c)
                continue

            maws.add(mot)

        k += 1
        current = toexplore.copy()
        toexplore = []

    return maws


def tests() -> None:
    s1 = "ATGTCGGACCGGTT"
    s2 = "ATTGCCCATTACCG"
    s3 = "AAAAAAAAAAA"

    x1 = "ATG"
    x2 = "TGC"
    x3 = "TTG"
    x4 = "A"
    x5 = "G"

    print("Test is_absent")
    s1 = "ATGTCGGACCGGTT"
    s2 = "ATTGCCCATTACCG"

    assert is_absent_in(x1, s1) == False, "RIP bozo"
    assert is_absent_in(x2, s1) == True, "RIP bozo"
    assert is_absent_in(x3, s1) == True, "RIP bozo"
    assert is_absent_in(x1, s2) == False, "RIP bozo"
    assert is_absent_in(x2, s2) == False, "RIP bozo"
    assert is_absent_in(x3, s2) == False, "RIP bozo"
    assert is_absent_in(x4, s1) == False, "RIP bozo"
    assert is_absent_in(x5, s3) == True, "RIP bozo"

    print("Passed")

    print("\nTest substrings")
    x4 = "ATTG"

    assert substrings(x4) == [
        "A",
        "AT",
        "ATT",
        "T",
        "TT",
        "TTG",
        "T",
        "TG",
        "G",
    ], "RIP bozo"
    print("Passed")

    print("\nTest is_MAW")
    s3 = "AATATTTTTTTGTTG"

    assert is_MAW(x4, (s3,)) == True, "RIP bozo"
    assert is_MAW(x4, (s1, s2)) == False, "RIP bozo"
    print("Passed")


def main():
    if len(argv) < 3:
        print(f"Usage : {argv[0]} <file> <kmax> <naive | bfs>")
        exit(1)

    # sequences = parse_file(argv[1])
    # raw_sequences = list(map(lambda x: x.sequence, sequences))
    # tests()

    raw_sequences = tuple(readfq_file(argv[1]))
    tree(raw_sequences[0])
    return

    kmax = int(argv[2])

    if argv[3] == "naive":
        data = naive(kmax, raw_sequences)
        write_tsv(data, (argv[1][: len(argv[1]) - 3]) + ".csv")
    elif argv[3] == "bfs":
        data = bfs(kmax, raw_sequences)
        for maw in data:
            print(len(maw), maw)

    # laura = ["AAACG", "AACCG", "AACGT", "ACCGA", "ACCGT"]
    # elie =  ["ACGCG","ACGTA","CCGCG","CGCGA"]
    # for maw in laura:
    #     print(is_absent_in(maw, raw_sequences[0], True))


if __name__ == "__main__":
    main()
