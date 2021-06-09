from cs50 import get_string

# Prompts user for card number
number = get_string("Number: ")

# American Express uses 15-digit numbers
# MasterCard uses 16-digit numbers
# Visa uses 13 and 16-digit numbers

# Check length of the number
length = len(number)
if length not in [15, 16, 13]:
	print("INVALID\n")
	exit()

#Calculate checksum
sum = 0
double = 0
int1 = ""
int2 = ""

# Multiply every other digit by 2, starting with the number’s second-to-last digit, and then add those products’ digits together
for i in range(len(number) - 2, -1, -2):
	double = int(number[i])*2
	if len(str(double)) != 1:
		int1 = str(double)[0]
		sum += int(int1)
		int2 = str(double)[1]
		sum += int(int2)
	else:
		sum += double

# Add the sum to the sum of the digits that weren’t multiplied by 2
for i in range(len(number) - 1, -1, -2):
	sum += int(number[i])

# If the total’s last digit is not 0, number is invalid
if sum % 10 != 0:
	print("INVALID\n")
	exit()

# All American Express numbers start with 34 or 37
# Most MasterCard numbers start with 51, 52, 53, 54, or 55
# Visa numbers start with 4

# Check for starting

if number.startswith(("34", "37")) and length == 15:
	print("AMEX\n")
	exit()

if number[0] == "5" and 1 <= int(number[1]) <= 5 and length == 16:
	print("MASTERCARD\n")
	exit()

if number.startswith(("4")) and length in [13, 16]:
	print("VISA\n")
	exit()













