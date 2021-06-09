from cs50 import get_string

# Promts user for text
text = get_string("Text: ")

# Couts number of letter, words and sentences
letters = 0
words = 1
sentences = 0

for i in range(0, len(text)):
	if text[i].isalpha():
		letters += 1
	elif text[i] == " ":
		words += 1
	elif text[i] in [".", "!", "?"]:
		sentences += 1

# L is the average number of letters per 100 words in the text, and S is the average number of sentences per 100 words in the text
L = letters/words * 100
S = sentences/words * 100

# Calculates the approximate grade level
index = 0.0588 * L - 0.296 * S - 15.8 

round_index = round(index)

if round_index < 1:
	print("Before Grade 1")
elif round_index >= 16:
	print("Grade 16+")
else:
	print(f"Grade {round_index}")