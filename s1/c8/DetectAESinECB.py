import sys
import distance
from Crypto.Cipher import AES

def main(argv):
	scan(argv[1])

def scan(filename):
	ciphertext = open(filename, 'r')
	key = 'YELLOW SUBMARINE'
	low_score = 999999
	best_line = ''
	for line in ciphertext:
		blocks = []
		block = ''
		for c in line:
			if len(block) == 64:
				blocks.append(block)
				#print block
				block = ''
			else:
				block += c
		score = 0
		for b in blocks:
			for i in range(0,len(blocks)):
				score += distance.hamming(b, blocks[i])
		print score
		if score < low_score:
			low_score = score
			best_line = line
	print "Low score: %s" % low_score
	return ciphertext

if __name__ == "__main__":
	main(sys.argv)