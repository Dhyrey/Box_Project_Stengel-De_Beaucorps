from datetime import datetime


def reverse_complement(s: str) -> str:
    dict = {"A": "T", "T": "A", "C": "G", "G": "C"}
    s1 = ""

    for c in s[::-1]:
        s1 += dict[c]

    return s1


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


def bfs(kmax: int, seqs: tuple[str]) -> list[tuple[int, list[str]]]:
    current = list("ACGT")
    maws: set[str] = set()
    seen: set[str] = set()
    k = 1
    toexplore = []
    while k <= kmax and current:
        print(str(k) + " : " + str(len(current)) + "/" + str(4**k))
        t = datetime.now()
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

        print("Processed in " + str(datetime.now() - t))
        k += 1
        current = toexplore.copy()
        toexplore = []

    lengths = list(set(map(len, maws)))
    lengths.sort()
    to_return = []
    for i in lengths:
        to_return.append((i, list(filter(lambda maw: len(maw) == i, maws))))
    return to_return
