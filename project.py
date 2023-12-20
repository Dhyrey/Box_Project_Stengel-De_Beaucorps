from dataclasses import dataclass
from sys import argv, exit
from itertools import product
from readfa import *
from csv import *

@dataclass
class sequence:
    description: str
    sequence: str


def reverse_complement(s: str) -> str:
    dict = {"A": "T", "T": "A", "C": "G", "G": "C"}
    s1 = ""

    for c in s:
        s1 += dict[c]

    return s1


def cannonical_sequence(s: str) -> str:
    return min(s, reverse_complement(s))


def is_absent_in(x: str, s: str) -> bool:
    x1 = reverse_complement(x)

    for i in range(len(s) - len(x)):
        if x == s[i : i + len(x)]:
            # print(x + " : " + s)
            return False
        if x1 == s[i : i + len(x)]:
            # print(x1 + " : " + s)
            return False

    return True


def substrings(x: str) -> list[str]:
    l = []
    for i in range(len(x) - 1):
        for j in range(i + 1, len(x) + 1):
            if j - i == len(x):
                continue
            l.append(x[i:j])
    return l


def is_MAW(x: str, S: list[str]) -> bool:
    for s in S:
        if not (is_absent_in(x, s)):
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


def tests() -> None:
    s1 = "ATGTCGGACCGGTT"
    s2 = "ATTGCCCATTACCG"

    x1 = "ATG"
    x2 = "TGC"
    x3 = "TTG"

    print("Test is_absent")
    s1 = "ATGTCGGACCGGTT"
    s2 = "ATTGCCCATTACCG"

    assert is_absent_in(x1, s1) == False, "RIP bozo"
    assert is_absent_in(x2, s1) == True, "RIP bozo"
    assert is_absent_in(x3, s1) == True, "RIP bozo"
    assert is_absent_in(x1, s2) == False, "RIP bozo"
    assert is_absent_in(x2, s2) == False, "RIP bozo"
    assert is_absent_in(x3, s2) == False, "RIP bozo"

    print("Passed")

    print("\nTest substrings")
    x4 = "ATTG"

    assert substrings(x4) == ["A", "AT", "ATT", "T", "TT", "TTG", "T", "TG"], "RIP bozo"
    print("Passed")

    print("\nTest is_MAW")
    s3 = "AATATTTTTTTGTTG"

    assert is_MAW(x4, [s3]) == True, "RIP bozo"
    assert is_MAW(x4, [s1, s2]) == False, "RIP bozo"
    print("Passed")

def write_tsv(data: list[int,list[str]],filename: str):
    file = open(filename,"w")
    for d_line in data :
        s_line = str(d_line[0])+"\t"+",".join(d_line[1])+"\n"
        file.write(s_line)
    file.close()


def naive(kmax: int, sequences: list[str]):
    data = []
    for k in range(3, kmax + 1):
        all_combinations = product("ATGC", repeat=k)
        all_combinations_strings = map(lambda x: "".join(x), all_combinations)
        all_maws = list(
            filter(lambda x: is_MAW(x, sequences), all_combinations_strings)
        )
        n = len(all_maws) 
        if n != 0 :
            print(str(k) + " : " + str(n) + " MAWs")
            data.append([k,all_maws])
    
    return data


def main():
    if len(argv) < 3:
        print(f"Usage : {argv[0]} <file> <kmax>")
        exit(1)

    # sequences = parse_file(argv[1])
    # raw_sequences = list(map(lambda x: x.sequence, sequences))
    raw_sequences = readfq_file(argv[1])


    kmax = int(argv[2])

    data = naive(kmax, raw_sequences)

    write_tsv(data,(argv[1][:len(argv[1])-3])+".csv")

    tests()


if __name__ == "__main__":
    main()
