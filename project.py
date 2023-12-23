#!/bin/env python3

from sys import argv, exit
from itertools import product
from readfa import *
from csv import *
from datetime import *
from naive import *
from bfs import *
from unword import *


def filter_sequences(seqs: list[str]) -> tuple[str, ...]:
    alphabet = set("ATGC")
    return tuple(map(lambda seq: "".join(filter(lambda x: x in alphabet, seq)), seqs))


def write_tsv(
    data: list[tuple[int, list[str | int]]], filename: str, is_index_form: bool = False
) -> None:
    file = open(filename, "w")
    for d_line in data:
        s_line = ""
        if is_index_form:
            s_line = str(d_line[0]) + "\t" + index_to_word(d_line[1][0], d_line[0])
            for i in range(1, len(d_line[1])):
                s_line += "," + index_to_word(d_line[1][i], d_line[0])
            s_line += "\n"
        else:
            s_line = str(d_line[0]) + "\t" + ",".join(d_line[1]) + "\n"
        file.write(s_line)
    file.close()
    print("file saved.")


def main():
    if len(argv) < 5:
        print(f"Usage : {argv[0]} <fasta file> <output file> <kmax> <method>")
        print("\tWhere method is either of naive | bfs | unword")
        exit(1)

    print("Parsing file.")
    t = datetime.now()
    parsed_sequences = readfq_file(argv[1])
    print("Parsed in " + str(datetime.now() - t))

    print("Filtering unwanted characters.")
    t = datetime.now()
    filtered_sequences = filter_sequences(parsed_sequences)
    print("Filtered in " + str(datetime.now() - t))

    kmax = int(argv[3])
    output_file = argv[2]

    print("Calculating MAWs using the " + argv[4] + " algorithm.")
    if argv[4] == "naive":
        data = naive(kmax, filtered_sequences)
        write_tsv(data, output_file)
    elif argv[4] == "bfs":
        data = bfs(kmax, filtered_sequences)
        write_tsv(data, output_file)
    elif argv[4] == "unword":
        data = unword(kmax, filtered_sequences)
        write_tsv(data, output_file, True)


if __name__ == "__main__":
    main()
