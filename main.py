from cryptography.fernet import Fernet

cipher = Fernet("key-123245")

def init_encryption():
	key = "Hello! You found the secret message! Contact secretmessage@usc.edu to claim your reward!"
	cipher = Fernet(key)

def encode_data(msg):
	return cipher.encrypt(msg.encode())

def decode_data(dat):
	return cipher.decrypt(dat).decode()

def bank_to_msg(bank):
	res = ""
	for ele in bank:
		res+=str(ele)
		res+="\n"
	return res
	
def msg_to_bank(msg):
	bank = []
	return msg.split("\n")

import random

def generate(word_bank, digit_bank, minimumLength, needUppercase, needDigits, needSymbols):
	pwd = ""
	WORDS_TO_INCLUDE=1
	generation_iterations = 0
	
	while len(pwd)<minimumLength:
		if (generation_iterations%10==9):
			WORDS_TO_INCLUDE = WORDS_TO_INCLUDE + 1
		pwd = ""
		
		# Choose 3 words from word bank
		words = [ word_bank[random.randint(0,len(word_bank)-1)] for _ in range(WORDS_TO_INCLUDE) ]
		# Randomly capitalize some words
		if (needUppercase):
			for i in range(random.randint(1,min(8,WORDS_TO_INCLUDE))):
				words[i] = words[i][0].upper() + words[i][1:]
		# randomly append digits to the end or beginning of random words
		if (needDigits):
			for i in range(random.randint(1,min(5,WORDS_TO_INCLUDE))):
				dgt = digit_bank[random.randint(0,len(digit_bank)-1)] 
				if (random.randint(0,1)==0):
					words[i] = words[i] + str(dgt)
				else:
					words[i] = str(dgt) + words[i]
		# randomly append symbols to the end or beginning of random words
		if (needSymbols):
			for i in range(random.randint(1,min(3,WORDS_TO_INCLUDE))):
				sym = "!@#$%^&*(){}[]?/=-,.><|\\"[random.randint(0,len("!@#$%^&*(){}[]?/=-,.><|\\")-1)]
				if (random.randint(0,1)==0):
					words[i] = words[i] + sym
				else:
					words[i] = sym + words[i]
		# construct the password in a random sequence
		while (words):
			pwd += words.pop(random.randint(0,len(words)-1))
		
		generation_iterations = generation_iterations + 1
	return pwd

if __name__ == "__main__":
	init_encryption()
	word_bank = ["funny", "unicorn", "banana", "house", "kitten"]
	digit_bank = [7, 11, 67, 222, 1010]
	min_length = 8
	needCapitalize = True
	needDigits = True
	needSymbols = True
	password = generate(word_bank, digit_bank, min_length, needCapitalize, needDigits, needSymbols)
	print(password)