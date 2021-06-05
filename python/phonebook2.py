from cs50 import get_string

import csv

file = open("phonebook.csv", "a") #append mode

name = get_string("Name: ")
number = get_string("Number: ")

writer = csv.writer(file)

writer.writerow([name, number])

file.close()


### ANOTHER WAY TO DO IT

# with open("phonebook.csv", "a") as file: 

	# name = get_string("Name: ")
	# number = get_string("Number: ")

	# writer = csv.writer(file)

	# writer.writerow([name, number])
