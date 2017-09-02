import sys
import pyperclip
import copy
import random
import os
# from pathlib import Path

keyfile = "totallyNotTheKeyInPlaintext.key"
debug = 0
if debug == 1:
	print("DEBUG-MODE")
substitution=True 

# autoinstall av pyperclip?
# -armor

iterations = 3

def getIterations():
	return iterations


def encrypt(plaintext,key,iterations):
	if len(plaintext)%2==1:
		plaintext+="§"
	ciphertext = ""
	seedSub = random.randint(0,9)
	seedExp = random.randint(0,9)
	seedRev = random.randint(0,9)
	counter = 0

	# Substitution
	while (counter < len(plaintext)):
		for i in range (0,len(key)):
			if(substitution):
				newValue= (ord(str(plaintext[counter]))+((ord(key[i])%26)))
				ciphertext+= chr((newValue)%3000)
			else:
				ciphertext+= chr((ord(str(plaintext[counter]))))
			counter += 1
			if (counter>=len(plaintext)):
				break
	if (seedRev>3):
		ciphertext = ciphertext[::-1]
	

	# Transposition
	exponent = 2
	tempCiphertext = ""
	while ( len(ciphertext)>=(2**exponent) ):
		for i in range (0,len(ciphertext),2**exponent):
			tempCiphertext+= ciphertext[(i+((2**exponent)//2)):(i+(2**exponent))]+ciphertext[i:(i+((2**exponent)//2))]
		exponent+=1
		ciphertext = copy.deepcopy(tempCiphertext)
		tempCiphertext=""

	# New transpositinon
	tempCiphertext=""
	for i in range(len(ciphertext)):
		placement=((ord(key[i%len(key)])+i+seedExp)%len(ciphertext))
		tempCiphertext=ciphertext[:i]+ciphertext[i+1:]
		tempCiphertext=tempCiphertext[:placement]+ciphertext[i]+tempCiphertext[placement:]
		ciphertext = copy.deepcopy(tempCiphertext)


	#fjern character 32
	#Sjekk om du kan bruke markering i stedet for kopiering
	ciphertext = ciphertext.replace(" ","ߐ")
	ciphertext = ciphertext.replace(chr(10),"******")
	ciphertext = "!----"+str(seedExp)+str(seedSub)+(str(seedRev))+ciphertext+"----!"
	pyperclip.copy(ciphertext)
	if (len(ciphertext)>=50 and iterations<=1):
		return ciphertext
	else:
		return encrypt(ciphertext,key,iterations-1)

def decrypt(ciphertext,key):
	#print("decrypt")
	if debug==1:
		print("1",ciphertext)
	ciphertext = ciphertext[5:len(ciphertext)-5]
	seedExp=int(ciphertext[0])
	seedSub=int(ciphertext[1])
	seedRev=int(ciphertext[2])
	ciphertext=ciphertext[3:]
	if debug==1:
		print("2",ciphertext)


	# ciphertext =ciphertext[1:]

	ciphertext = ciphertext.replace("ߐ"," ")
	ciphertext = ciphertext.replace("******",chr(10))

	for i in range(len(ciphertext)-1,-1,-1):
		placement=((ord(key[i%len(key)])+i+seedExp)%len(ciphertext))
		tempCiphertext=ciphertext[:placement]+ciphertext[placement+1:]
		tempCiphertext=tempCiphertext[:i]+ciphertext[placement]+tempCiphertext[i:]
		ciphertext = copy.deepcopy(tempCiphertext)

	tempCiphertext=""
	exponent = 2
	while ( len(ciphertext)>=(2**exponent)):
		for i in range (0,len(ciphertext),2**exponent):
			part1 =ciphertext[i:(i+((2**exponent)//2))]
			part2 =ciphertext[(i+((2**exponent)//2)):(i+(2**exponent))]
			tempCiphertext+= part2+part1
		if debug==1:
			print("3",tempCiphertext)
		exponent+=1
		ciphertext = copy.deepcopy(tempCiphertext)
		tempCiphertext=""
	if seedRev>3:
		ciphertext = ciphertext[::-1]
	if debug==1:
		print("4",ciphertext)
		print("")
	textSize=len(ciphertext)
	plaintext=""
	counter = 0
	while ( counter < textSize):
		for i in range(0,len(key)):
			if(substitution):
				# newValue = ord(str(ciphertext[counter]))-((ord(key[i])+seedExp+i))-seedSub
				newValue= (ord(str(ciphertext[counter]))-((ord(key[i])%26)))
				plaintext += chr((newValue)%250)
			else:
				plaintext+= chr((ord(str(ciphertext[counter]))))
			counter += 1
			if (counter >= textSize):
				break
	if (plaintext[-1]=="§"):
		plaintext=plaintext[:-1]

	if ((plaintext[0:5]=="!----")and(plaintext[len(plaintext)-5:]=="----!")):
		return(decrypt(plaintext,key))
	else:
		return plaintext

def trimCiphertext(ciphertext):
	startPosition=0
	for i in range(len(ciphertext)):
		if(ciphertext[i:i+5]=="!----"):
			startPosition=i
			break
	ciphertext=ciphertext[startPosition:]

	endPosition=0
	for i in range(len(ciphertext),0,-1):
		if(ciphertext[i-5:i]=="----!"):
			endPosition=i
			break
	ciphertext= ciphertext[0:i]
	return ciphertext

def continous():
	os.system('cls' if os.name == 'nt' else 'clear')
	print("\n### SuperKrypt ###\n")
	print('Enter "-h" to view available commands\n')
	counter = 0
	
	while True:

		if counter <3:
			print("Enter text to be encryped, or press enter to encrypt/decrypt your clipboard")
		else:
			print("Enter text:")
		inputText=input()
		# 
		if len(inputText)==0:
			inputText = pyperclip.paste()
			print("Using text from clipboard: ")
		parseInput(inputText,counter)

		counter +=1

def getKey():
	file = open(keyfile, 'r')
	return file.readline()

def setKey(newKey):
	file = open(keyfile, 'w')
	file.seek(0)
	file.truncate()
	file.write(newKey)
	key = newKey

def initKey():
	try:
	    file = open(keyfile, 'r')
	    firstLine=file.readline()
	    if(firstLine==""):
	    	file.write(key)
	    else:
	    	key = firstLine
	except IOError:
	    file = open(keyfile, 'w')
	    file.write("default_key")

def parseInput(text,counter):
	trimmedText = trimCiphertext(text)
	if text=="-fast-decode":
		text = pyperclip.paste()
		print("Message: ",decrypt(text,getKey()))
		print("\n press any key to close")
		input()

	elif text=="-h" or text=="--help" or text=="-H" or text=="--HELP":
		print("\n\nAvailable commands:")
		print("\n_____________________________________")
		print("--chat   | activates chat mode")
		print("--setkey | sets a new key")
		print("--getkey | displays the current key")
		print("--reset  | resets the keys to default")
		print("_____________________________________")
		print("This program has two main uses.")
		print("1: Decrypt encrypted messages from clipboard, or from input if given")
		print("2: Encrypt plaintext from clipboard, or from input if given")
		print("_____________________________________")
		print("Chat-mode runs an infinite loop waiting for encryption/decryption tasks")
		print("_____________________________________")
		print("Terminal/CMD often misrepresents letters, please use 'ctrl+v' instead of copying manually")
		print("\n\n")

	elif text=="" or text=="-C" or text=="-c" or text=="--chat" or text=="--CHAT":
		continous()
	elif text=="-resetkeys" or text=="-resetkey" or text=="-reset" or text=="-r":
		print("are you sure you want to reset the key to default? (y/n)")
		if(input()=="y"or"Y"):
			setKey("default_key")
			print("The key has been reset!")

	# elif text=="--setiterations" or text=="setIterations" or text[:]=="-i" or text[:]=="-I" or text[:]=="--iterations" or text[:]=="--Iterations":
	# 	print("Enter number of encryption layers:")
	# 	setIterations(input())
	# 	print("iterations is now: ",getIterations())

	elif text[:8]=="--setkey" or text[:8]=="--setKey":
		tempKey = text[8:].strip().replace('"','').replace("'","")
		if (len(tempKey)>0):
			print("new key is: ",tempKey)
			setKey(tempKey)
		else:
			print("Enter new key:")
			setKey(input())

	elif text[:8]=="--getkey" or text[:8]=="--getKey":
		print('The current key is: "'+getKey()+'"')	

	elif ((trimmedText[0:5]=="!----")and(trimmedText[len(trimmedText)-5:]=="----!")):
		print("Decrypting:",trimmedText)
		print("Message: ",decrypt(trimmedText,getKey()))
	else:
		print("")
		if (len(text)<=30):
			print('Encrypting: "'+text+'"')
		else:
			print("Encrypting!")
		print("Ciphertext: ",encrypt(text,getKey(),getIterations()))
		if counter<3:
			print("The ciphertext has been copied to your clipboard \n")

initKey()

if len(sys.argv)>=2:
	text=sys.argv[1]
	print("Using input text")
else:
	text = pyperclip.paste()
	print("Using text from clipboard")
parseInput(text,0)
print('get help and view available commands by entering "-h"')

#TODO: Plugin til nettleser som automatisk krypterer før det sendes via facebook ?