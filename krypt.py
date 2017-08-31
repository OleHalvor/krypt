import sys
import pyperclip
import copy
import random
# from pathlib import Path

keyfile = "totallyNotTheKeyInPlaintext.key"
# global key
#key ="hest"
debug = 0
if debug == 1:
	print("DEBUG-MODE")
substitution=True 

# transposition flytt til høure med verdi av nkkel[i]mod(length av message)
# Støtte for flere lag med kryptering
# autoinstall av pyperclip?
# -armor

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
				newValue= (ord(str(plaintext[counter]))+((ord(key[i])+seedExp+i))+seedSub)
				ciphertext+= chr((newValue)%3000)
			else:
				ciphertext+= chr((ord(str(plaintext[counter]))))
			counter += 1
			if (counter>=len(plaintext)):
				break
	if (seedRev>3):
		ciphertext = ciphertext[::-1]
	#ciphertext = ciphertext.replace(' ', '___').replace('"', "'") tester å fjerne denne
	

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
	# print("Before trans: ",ciphertext)
	for i in range(len(ciphertext)):
		placement=((ord(key[i%len(key)])+i+seedExp)%len(ciphertext))
		# print("placement:",i,placement)
		tempCiphertext=ciphertext[:i]+ciphertext[i+1:]
		# print("tempc:",tempCiphertext)
		tempCiphertext=tempCiphertext[:placement]+ciphertext[i]+tempCiphertext[placement:]
		ciphertext = copy.deepcopy(tempCiphertext)
		# print("   inside: ",ciphertext)
	# print("After trans: ",ciphertext)

	# for i in range(len(ciphertext)-1,0,-1):
	# 	placement=((ord(key[i%len(key)])+i)%len(ciphertext))
	# 	tempCiphertext=ciphertext[:plaintext]+ciphertext[placement+1:]
	# 	tempCiphertext=tempCiphertext[:i]+ciphertext[placement]+tempCiphertext[i:]
	# 	ciphertext = copy.deepcopy(tempCiphertext)



	
	#fjern character 32
	#Sjekk om du kan bruke markering i stedet for kopiering
	ciphertext = ciphertext.replace(" ","___")
	ciphertext = ciphertext.replace(chr(10),"******")
	#Checksum key
	totalValue=0
	for i in range(len(key)):
		totalValue+=ord(key[i])
	keyValueToAdd=100-(totalValue%100)
	ciphertext = chr(keyValueToAdd)+ciphertext

	#Checksum message
	totalValue=0
	for i in range(len(ciphertext)):
		totalValue+=ord(ciphertext[i])
	messageValueToAdd = 100-(totalValue%100)


	ciphertext = "!----"+str(seedExp)+str(seedSub)+(str(seedRev))+chr(messageValueToAdd)+ciphertext+"----!"
	pyperclip.copy(ciphertext)
	if(iterations<=1):
		return ciphertext
	else:
		# print("Encrypt again: ",iterations)
		return encrypt(ciphertext,key,iterations-1)

def decrypt(ciphertext,key):
	if debug==1:
		print("1",ciphertext)
	ciphertext = ciphertext[5:len(ciphertext)-5]
	seedExp=int(ciphertext[0])
	seedSub=int(ciphertext[1])
	seedRev=int(ciphertext[2])
	ciphertext=ciphertext[3:]
	if debug==1:
		print("2",ciphertext)

	totalValue=0
	for i in range(0,len(ciphertext)):
		totalValue+=ord(ciphertext[i])
	if totalValue%100!=0:
		# print("________________________________________________________________")
		# print("WARNING: This message does not verify. It may have been altered or has become corrupted")
		pass
	if debug==1:
		print(" checksum: ",totalValue)
	#print("Total checksum value: ",totalValue)
	ciphertext =ciphertext[1:]

	totalValue=0
	for i in range(len(key)):
		totalValue+=ord(key[i])
	if ((totalValue+ord(ciphertext[0]))%100)!=0:
		# print("________________________________________________________________")
		print("WARNING: Key missmatch")
		# print("________________________________________________________________")
	ciphertext =ciphertext[1:]

	ciphertext = ciphertext.replace("___"," ")

	# print("before",ciphertext)
	for i in range(len(ciphertext)-1,-1,-1):
		# print(i)
		# print("move amount:",str(ord(key[i%len(key)])))
		placement=((ord(key[i%len(key)])+i+seedExp)%len(ciphertext))
		# print(placement)
		tempCiphertext=ciphertext[:placement]+ciphertext[placement+1:]
		tempCiphertext=tempCiphertext[:i]+ciphertext[placement]+tempCiphertext[i:]
		# print("inne",tempCiphertext)
		ciphertext = copy.deepcopy(tempCiphertext)
	# print("after",ciphertext)


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
	#ciphertext = ciphertext.replace('___', ' ').replace("'", '"') tester å fjerne denne også
	if debug==1:
		print("4",ciphertext)
		print("")
	textSize=len(ciphertext)
	plaintext=""
	counter = 0
	while ( counter < textSize):
		for i in range(0,len(key)):
			if(substitution):
				newValue = ord(str(ciphertext[counter]))-((ord(key[i])+seedExp+i))-seedSub
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
	print("--CHAT-MODE--")
	counter = 0
	while True:
		if counter <3:
			print("Enter text to be encryped, or press enter to encrypt/decrypt your clipboard")
		else:
			print("Enter text:")
		inputText=input()
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
	    file.write("Det er alltid lurt å ha lange nøkler, slik at man ikke så lett blir brute forcet!")

def parseInput(text,counter):
	trimmedText = trimCiphertext(text)
	if text=="-fast-decode":
		text = pyperclip.paste()
		print("Message: ",decrypt(text,getKey()))
		print("\n press any key to close")
		input()

	elif text=="-h" or text=="-help" or text=="help" or text=="-H" or text=="-HELP"or text=="HELP":
		print("Available commands:")
		print("_____________________________________")
		print("-c/-chat | activates chat mode")
		print("-setkey  | sets a new key")
		print("-getkey  | displays the current key")
		print("-reset   | resets the keys to default")
		print("_____________________________________")
		print("This program has two main uses.")
		print("1: Decrypt encrypted messages from clipboard, or from input if given")
		print("2: Encrypt plaintext from clipboard, or from input if given")
		print("_____________________________________")
		print("Chat-mode runs an infinite loop waiting for encryption/decryption tasks")

	elif text=="-e"or text=="-E" or text=="" or text=="-start" or text=="-c" or text=="-chat" or text=="-CHAT" or text=="-C":
		continous()
	elif text=="-resetkeys" or text=="-resetkey" or text=="-reset" or text=="-r":
		print("are you sure you want to reset the key to default? (y/n)")
		if(input()=="y"or"Y"):
			setKey("Det er alltid lurt å ha lange nøkler, slik at man ikke så lett blir brute forcet!")
			print("The key has been reset!")

	elif text=="--setiterations" or text=="setIterations":
		print("Enter number of encryption layers:")
		iterations=input()

	elif text[:7]=="-setkey" or text[:7]=="-setKey":
		print("Enter the new key")
		setKey(input())

	elif text[:7]=="-getkey" or text[:7]=="-getKey":
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
		print("Ciphertext: ",encrypt(text,getKey(),10))
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
print('You can use chat-mode by running "python krypt.py -chat", or get help by using "-h"')

#TODO: Plugin til nettleser som automatisk krypterer før det sendes via facebook

