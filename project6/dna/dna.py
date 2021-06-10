import csv
import sys


# Ensure correct usage
def main():

	if len(sys.argv) != 3:
		sys.exit("Usage: python dna.py data.csv sequence.txt")

	csvfilename = sys.argv[1]
	txtfilename = sys.argv[2]

	# Read teams into memory from file

	with open(csvfilename) as csvfile:
		reader = csv.DictReader(csvfile)
		database = list(reader)
	dic = database[0]
	with open(txtfilename) as f:
	    sequence = f.readline()


	strs = []
	for key in dic:
		strs.append(key)

	values = {}
	for s in range(1, len(strs)):
		# print(f"{strs[s]}: {count(sequence, strs[s])}")
		values[strs[s]] = count(sequence, strs[s])


	# print(values)

	# for key,value in values.items():
	# 	print(values[key])

# Count STR repeats

def count(dna, value):

	counts = 0
	temp = 0 

	l = len(value)

	for i in range (len(dna)):
		if dna[i : i + l] == value:
			temp += 1
			for j in range(i + l, len(dna), + l):
				if dna[j : j + l] == value:
					temp += 1
				else:
					if temp > counts:
						counts = temp
					temp = 0
	return counts
	# print(f" {str} : {count}")

if __name__ == "__main__":
    main()

