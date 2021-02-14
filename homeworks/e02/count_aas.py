import csv
import sys
from collections import Counter
import matplotlib.pyplot as plt


directory = sys.argv[1]

fasta = []
with open(directory, "r") as protein_fasta:
    for line in protein_fasta.readlines():
        fasta.append(line.strip("\n"))



protein_annotation = []
for pos, sequence in enumerate(fasta):
    if sequence.startswith(">"):
        protein_annotation.append(pos)

for pos in sorted(protein_annotation, reverse=True):
    fasta.pop(pos)


final_fasta = "".join(fasta)

aa_distribution = Counter(final_fasta)

sorted_aa_distribution = dict(sorted(aa_distribution.items(), key = lambda x: x[1], reverse = True))

with open('/Users/huuumath/Git/fufezan-lab-advanced_python_2020-21_HD/data/mouse_aa_distribution.csv', 'w') as csv_file:  
    writer = csv.DictWriter(csv_file, fieldnames = ["aa", "count"], extrasaction='ignore')
    writer.writeheader()
    for aa, count in sorted_aa_distribution.items():
       writer.writerow({"aa": aa, "count": count})

aas = list(sorted_aa_distribution.keys())
counts = list(sorted_aa_distribution.values())

plt.bar(aas, counts)
plt.title('Mouse Aminoacid Distribution')
plt.show()

