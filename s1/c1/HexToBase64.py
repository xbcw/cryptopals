import sys
import os

def main(argv):
	print hex_to_base64(argv[1])

def hex_to_base64(input_string):
	try:
		int(input_string,16)
		return input_string.decode('hex').encode('base64').strip('\n')
	except ValueError as e:
		print "Error in '%s': '%s' is not a hexidecimal number." % (os.path.basename(__file__), input_string)
		return -1
	except Exception as e:
		print "Error in '%s': %s" % (os.path.basename(__file__), str(e))
		return -1

if __name__ == "__main__":
	main(sys.argv)