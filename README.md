# BOX Project 2023
## Minimal Absent Words in Plasmids

### The goal
This tool is used to find Minimal Absent Words (MAWs) in a dataset of sequences.

A minimal absent word is a word of which all the substrings are present in the dataset, while not being present itself. A word is present if it or it's reverse complement appears in a sequence.

The reverse complement of a word is obtained by reversing it and replacing it's letters according to the following permutation : 
`A <-> T`, `C <-> G`.


### Dependencies
All dependencies (only one) can be installed as follows : 
```shell
❯ pip install -r requirements.txt
```
It is good practice to do so in a [virtual environment](https://virtualenv.pypa.io/en/latest/).

### Usage
The tool should be run in the following way :
```shell
❯ python3 project.py <fasta file> <output file> <kmax> <method>
```
where :
+ `<fasta file>` is the fasta format file containing the collection of input sequences to search for MAWs,
+ `<output file>` is the file where the output will be sent (to not clobber stdout with possibly huge outputs),
+ `<kmax>` is the value of `k` up to which the tool will search for MAWs (`k` being the length of the MAWs),
+ `<method>` is any value of `naive`, `bfs` or `unword`. This represents the algorithm used to search for MAWs. Consider using `unword` for any practical use.

### Output
Example run :
```shell
❯ python3 project.py all_ebi_plasmids.fa all_ebi_plasmids.tsv 11 unword
Parsing file.
Parsed in 0:00:00.108295
Filtering unwanted characters.
Filtered in 0:00:06.840071
Calculating MAWs using the unword algorithm
k : 2
Processed in 0:00:00.002552
k : 3
Processed in 0:00:00.002662
k : 4
Processed in 0:00:00.004592
k : 5
Processed in 0:00:00.005589
k : 6
Processed in 0:00:00.021544
k : 7
Processed in 0:00:00.230751
k : 8
Processed in 0:00:01.026024
k : 9
Processed in 0:00:03.889221
k : 10
Processed in 0:00:41.625250
k : 11
17 MAWs found in 0:01:55.408126
File saved.
```

The file `all_ebi_plasmids.tsv` then contains the MAWs found, separated by length :
```shell
❯ cat all_ebi_plasmids.tsv
11	ACCCTACATAC,ACTAGTACGCC,ACTAGTCTACG,AGACTAGTCTC,AGGAACCTAGG,AGGATCCTAGG,AGGGTACCTTA,CACATACTAGG,CCTAGGCTAAG,CGGAACTAGTA,CTAGGGTCCTA,CTAGTTAGCCC,GGGCCCTAGAC,GGTCCCTAGTA,GTACTATCCTA,GTAGGCCTACA,TAGGGTCCTAA
```