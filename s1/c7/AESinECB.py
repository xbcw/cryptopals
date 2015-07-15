import sys
from Crypto.Cipher import AES

def main(argv):
	print crack(argv[1], argv[2])

def crack(filename, key):
	ciphertext = open(filename, 'r').read().decode('base64')
	return AES.new(key, AES.MODE_ECB).decrypt(ciphertext)

if __name__ == "__main__":
	main(sys.argv)