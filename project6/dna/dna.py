import csv
import sys

# Ensure correct usage

if len(sys.argv) != 3:
	sys.exit("Usage: python dna.py data.csv sequence.txt")

csvfilename = sys.argv[1]
txtfilename = sys.argv[2]

# Read teams into memory from file

with open(csvfilename) as csvfile:
	reader = csv.DictReader(csvfile)
	database = list(reader)
print(database)		

with open(txtfilename) as f:
    sequence = f.readline()

print(type(sequence))

# Count STR repeats
# def count(dna, str)










