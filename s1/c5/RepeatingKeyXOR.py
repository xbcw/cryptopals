import sys

def main(argv):
	print encrypt(argv[1], argv[2])

def encrypt(data, key):
	encrypted_data = ''
	for i,c in enumerate(data):
		encrypted_data += chr(ord(c) ^ ord(key[i%3]))

	return encrypted_data.encode('hex')