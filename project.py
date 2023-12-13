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
            #print(x + " : " + s)
            return False
        if x1 == s[i : i + len(x)]:
            #print(x1 + " : " + s)
            return False

    return True

def substrings(x):
    l=[]
    for i in range(len(x)-1):
        for j in range(i+1,len(x)+1):
            if j-i==len(x):
                continue
            l.append(x[i:j])
    return l

def is_MAW(x,S):
    for s in S :
        if not(is_absent_in(x,s)):
            return False
    sxs = substrings(x)
    for sx in sxs :
        for s in S:
            if is_absent_in(sx,s):
                return False
    return True

print("Test is_absent")
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


print("\nTest substrings")
x4 = "ATTG"

print(x4 + " : " + str(substrings(x4)))

print("\nTest is_MAW")
s3 = "AATATTTTTTTGTTG"

print(x4 + ", [" + s3 + "] : " + str(is_MAW(x4,[s3])))
print(x4 + ", [" + s1 + ", " + s2 + "] : " + str(is_MAW(x4,[s1,s2])))