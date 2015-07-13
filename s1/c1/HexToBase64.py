import sys

def main(argv):
	input_string = argv[1]
	print hex_to_base64(input_string)

def hex_to_base64(input_string):
	try:
		int(input_string,16)
	except ValueError as e:
		print "Error: '%s' is not a hexidecimal number." % input_string
		return -1
	return input_string.decode('hex').encode('base64').strip('\n')

if __name__ == "__main__":
	main(sys.argv)