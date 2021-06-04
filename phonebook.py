from cs50 import get_string

phonebook = {
	"Brian": "+14158609458",
	"David": "+14156678494"
}

name = get_string("Name: ")
if name in phonebook:
	number = phonebook[name]
	print(f"Number: {number}")
