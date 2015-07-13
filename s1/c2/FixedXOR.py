import sys

def main(argv):

	print fixed_xor(argv[1], argv[2])

def fixed_xor(str1, str2):

	if not len(str1) == len(str2):
		print "Error: Strings must be equal length. '%s' has length %d and '%s' has length %d." % (str1, len(str1), str2, len(str2))
		return -1

	return ''.join(
				  	chr(ord(a) ^ ord(b)) for a,b in zip(str1.decode('hex') ,str2.decode('hex'))
				  ).encode('hex')

if __name__ == "__main__":
	main(sys.argv)