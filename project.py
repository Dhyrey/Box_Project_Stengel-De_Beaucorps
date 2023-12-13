def reverse_complement(s):
    dict = {"A": "T", "T": "A", "C": "G", "G": "C"}
    s1 = ""

    for c in s:
        s1 += dict[c]

    return s1


def cannonical_sequence(s):
    return min(s, reverse_complement(s))


def is_absent_in(x, s):
    x1 = reverse_complement(x)

    for i in range(len(s) - len(x)):
        if x == s[i : i + len(x)]:
            print(x + " : " + s)
            return False
        if x1 == s[i : i + len(x)]:
            print(x1 + " : " + s)
            return False

    return True


s1 = "ATGTCGGACCGGTT"
s2 = "ATTGCCCATTACCG"

x1 = "ATG"
x2 = "TGC"
x3 = "TTG"

print(x1 + ", " + s1 + " : " + str(is_absent_in(x1, s1)))
print(x2 + ", " + s1 + " : " + str(is_absent_in(x2, s1)))
print(x3 + ", " + s1 + " : " + str(is_absent_in(x3, s1)))
print(x1 + ", " + s2 + " : " + str(is_absent_in(x1, s2)))
print(x2 + ", " + s2 + " : " + str(is_absent_in(x2, s2)))
print(x3 + ", " + s2 + " : " + str(is_absent_in(x3, s2)))
