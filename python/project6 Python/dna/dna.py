import csv
import sys

# Ensure correct usage
def main():
	if len(sys.argv) != 3:
		sys.exit("Usage: python dna.py data.csv sequence.txt")

	csvfilename = sys.argv[1]
	txtfilename = sys.argv[2]

	# Read contents into memory from file
	with open(csvfilename) as csvfile:
		reader = csv.DictReader(csvfile)
		database = list(reader)


	with open(txtfilename) as f:
	    sequence = f.readline()

	dic = database[0]
	strs = []
	for key in dic:
		strs.append(key)

	values = {}
	for s in range(1, len(strs)):
		values[strs[s]] = str(count(sequence, strs[s]))

	# Check if each STR count matches the person
	for el in database:
		result = 0
		error = 0
		for key, value in el.items():
			if error < 2:
				if (key, value) in values.items():
					result += 1
					if result == len(values):
						print(el['name'])
						exit()
				else:
					error += 1
			else:
				break
	print("No match")


# Count STR repeats
def count(dna, value):

	counts = 0
	temp = 0

	l = len(value)

	for i in range(len(dna)):
		if dna[i:i + l] == value:
			temp += 1
			for j in range(i + l, len(dna), + l):
				if dna[j:j + l] == value:
					temp += 1
				else:
					if temp > counts:
						counts = temp
					temp = 0
	return counts

if __name__ == "__main__":
    main()

