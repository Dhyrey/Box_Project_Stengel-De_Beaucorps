class Node():
    def __init__(self, label: str):
        self.lab = label  # label on path leading to this node
        self.out = {}  # outgoing edges; maps characters to nodes


class tree:
    def __init__(self, s):
        """Make suffix tree, without suffix links, from s in quadratic time
        and linear space"""
        s += "$"
        self.root = Node(None)
        self.root.out[s[0]] = Node(s)  # trie for just longest suf
        # add the rest of the suffixes, from longest to shortest
        for i in range(1, len(s)):
            # start at root; we’ll walk down as far as we can go
            cur = self.root
            j = i
            while j < len(s):
                if s[j] in cur.out:
                    child = cur.out[s[j]]
                    lab = child.lab
                    # Walk along edge until we exhaust edge label or
                    # until we mismatch
                    k = j + 1
                    while k - j < len(lab) and s[k] == lab[k - j]:
                        k += 1
                    if k - j == len(lab):
                        cur = child  # we exhausted the edge
                        j = k
                    else:
                        # we fell off in middle of edge
                        cExist, cNew = lab[k - j], s[k]
                        # create “mid”: new node bisecting edge
                        mid = Node(lab[: k - j])
                        mid.out[cNew] = Node(s[k:])
                        # original child becomes mid’s child
                        mid.out[cExist] = child
                        # original child’s label is curtailed
                        child.lab = lab[k - j :]
                        # mid becomes new child of original parent
                        cur.out[s[j]] = mid
                else:
                    # Fell off tree at a node: make new edge hanging off it
                    cur.out[s[j]] = Node(s[j:])

    # def print(self, depth: int = 0):
    #     print(
    #         " " * depth
    #         + (("|\n" + " " * depth + "-->  ") if depth > 0 else "")
    #         + self.value.__repr__()
    #         + "$" * self.is_end
    #     )
    #     for child in self.children:
    #         child.print(depth + 1)


class SuffixNode:
    def __init__(self, val, is_end):
        self.value = val
        self.is_end = is_end
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)

class SuffixTree:
    def __init__(self, seqs: tuple[str]):
        self.root = SuffixNode("", False)

        self.build(seqs)

    def build(self, seqs: tuple[str]) -> SuffixNode:
        for idx, seq in enumerate(seqs):
            print(f"Building for sequence {idx}/{len(seqs)}")
            for i in range(len(seq)):
                current = self.root
                substr = seq[i:]
                while substr:
                    found = False
                    for child in current.children:
                        if child.value == substr[0]:
                            current = child
                            substr = substr[1:]
                            found = True
                            break
                    if not found:
                        break

                if not substr:
                    current.is_end = True

                while substr:
                    new = SuffixNode(substr[0], len(substr) == 1)
                    current.add_child(new)
                    current = new
                    substr = substr[1:]


if __name__ == "__main__":
    suffix_tree = Node("", False)
    Node.suffix_tree(
        suffix_tree,
        "CGGCGACTGGTGAGTACGCCAAAAATTTTGACTAGCGGAGGCTAGAAGGAGAGAGATGGGTGCGAGAGCG",
    )
