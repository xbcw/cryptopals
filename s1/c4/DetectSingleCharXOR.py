import sys
import cryptopals.s1.c3.SingleByteXOR as SingleByteXOR

def main(argv):
	return detect(argv[1])

def detect(filename):
	try:
		file = open(filename, 'r')
	except Exception as e:
		print "Error: %s" % str(e)
	high_score = 0
	best_result = 0
	for line in file:
		result = SingleByteXOR.single_byte_xor(line.strip())
		if result[2] > high_score:
			high_score = result[2]
			best_result = result
	return best_result


if __name__ == "__main__":
	main(sys.argv)