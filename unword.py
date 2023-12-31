from bitarray import *
from datetime import *


class q_bit_array:
    def __init__(self, q):
        self.array = bitarray(4**q)
        self.len = 0
        self.full = False
        self.q = q
        self.max_len = 4**q

    def add_word(self, indexes):
        if not self.array[indexes[0]]:
            self.array[indexes[0]] = 1
            self.len += 1
            if indexes[0] != indexes[1]:
                self.array[indexes[1]] = 1
                self.len += 1
            self.full = self.len >= self.max_len

    def scan(self, sequences):
        for i in range(len(sequences)):
            j = 0
            n = len(sequences[i])
            # print(str(i) + "/" + str(len(sequences)))
            indexes = (
                word_to_index(sequences[i][0 : self.q]),
                word_to_index(reverse_complement(sequences[i][0 : self.q])),
            )
            self.add_word(indexes)

            while j < n - 1 - self.q and not (self.full):
                j += 1
                indexes = next_index(sequences[i], j, self.q, indexes)
                self.add_word(indexes)

    def absent_words(self):
        l = []
        for i in range(self.max_len):
            if not (self.array[i]):
                word = index_to_word(i, self.q)
                if word == cannonical_sequence(word):
                    l.append(word)
        return l


def reverse_complement(s: str) -> str:
    dict = {"A": "T", "T": "A", "C": "G", "G": "C"}
    s1 = ""
    for c in s[::-1]:
        s1 += dict[c]
    return s1


def cannonical_sequence(s: str) -> str:
    return min(s, reverse_complement(s))


def substrings(x: str, kmin: int = 1) -> list[str]:
    l = []
    for i in range(len(x) - 1, kmin - 1, -1):
        for j in range(0, len(x) - i + 1):
            l.append(x[j : j + i])
    return l


def word_to_index(word: str) -> int:
    n = 0
    dict = {"A": 0, "C": 1, "G": 2, "T": 3}
    for c in word:
        n = dict[c] + 4 * n
    return n


def next_index(
    sequence: str, i: int, q: int, previous: tuple[int, int]
) -> tuple[int, int]:
    dict = {"A": 0, "C": 1, "G": 2, "T": 3}
    comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
    n1 = (
        4 * (previous[0] - (4 ** (q - 1) * dict[sequence[i - 1]]))
        + dict[sequence[i + q - 1]]
    )
    n2 = (previous[1] // 4) + 4 ** (q - 1) * dict[comp[sequence[i + q - 1]]]
    return n1, n2


def index_to_word(index: int, q: int) -> str:
    dict = {0: "A", 1: "C", 2: "G", 3: "T"}
    word = ""
    n = index
    for i in range(q):
        word += dict[n >> 2 * (q - i - 1)]
        n -= (n >> 2 * (q - i - 1)) << (2 * (q - i - 1))
    return word


def is_MAW_omega(word: str, omega_list: list[q_bit_array], kmin: int) -> bool:
    subs = substrings(word, kmin)
    for w in subs:
        if not omega_list[len(w) - kmin].array[word_to_index(w)]:
            return False
    return True


def unword(kmax: int, seqs: tuple[str]) -> list[tuple[int, list[int]]]:
    t = datetime.now()
    k = 2
    l = []

    while True:
        t = datetime.now()
        print("k : " + str(k))
        omega = q_bit_array(k)
        omega.scan(seqs)

        if omega.full and k < kmax:
            print("Processed in " + str(datetime.now() - t))
            k += 1
        else:
            absent_words = omega.absent_words()
            for word in absent_words:
                l.append(word_to_index(word))
            print(str(len(l)) + " MAWs found in " + str(datetime.now() - t))
            break
    maws = [(k, l)] if l else []
    kmin = k
    omega_list = [omega]

    while k < kmax:
        t = datetime.now()
        k += 1
        print("k : " + str(k))
        omega_list.append(q_bit_array(k))
        omega_list[k - kmin].scan(seqs)
        absent_words = omega_list[k - kmin].absent_words()
        l = []
        for word in absent_words:
            if is_MAW_omega(word, omega_list, kmin):
                l.append(word_to_index(word))
        maws.append((k, l))
        print(str(len(l)) + " MAWs found in " + str(datetime.now() - t))

    return maws
