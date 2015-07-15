import sys
import operator
import cryptopals.s1.c3.SingleByteXOR as SingleByteXOR

def main(argv):
	result = crack(argv[1])
	print "====DECRYPTED MESSAGE===="
	print result[1]
	print "=======END MESSAGE======="
	print
	print "==========KEY============"
	print result[0]
	print "========================="

def crack(filename):
	file_string = open(filename, 'r').read().decode('base64')
	data = list(file_string)
	keysizes = get_keysize(file_string)
	keysize = keysizes[0][0]
	blocks = get_keysized_blocks(data, keysize)
	transposed_blocks = transpose_blocks(blocks)
	key = ''
	for block in transposed_blocks:
		key += SingleByteXOR.single_byte_xor(block.encode('hex'))[1]
	result = decrypt(file_string, key)
	return key, result

def decrypt(file_string, key):
	result = ''
	keysize = len(key)
	for i, c in enumerate(file_string):
		result += chr(ord(c) ^ ord(key[i%keysize]))
	return result

def get_keysized_blocks(data, keysize):
	blocks = []
	for x in range(0, len(data)/keysize):
		blocks.append(''.join(data[keysize*x:keysize*(x+1)]))
	return blocks

def transpose_blocks(blocks):
	result = []
	for block in blocks:
		for i in range(0, len(blocks[0])):
			if len(result) <= i:
				result.append(block[i])
			else:
				result[i] += block[i]
	return result

def get_keysize(data):
	scores = {}
	for keysize in range(2, 40):
		result = 0
		samples = 10
		for i in range(0, samples):
			result += hamming_distance(data[keysize*i:keysize*(i+1)], data[keysize*(i+1):keysize*(i+2)])

		scores[keysize] = (result/samples)/keysize

	sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))

	return sorted_scores

def hamming_distance(str1, str2):
	bin_str1 = format(int(str1.encode('hex'), 16), '#0512b')
	bin_str2 = format(int(str2.encode('hex'), 16), '#0512b')
	distance = 0.0
	for x in range(0, len(bin_str1)):
		if bin_str1[x] is not bin_str2[x]:
			distance += 1.0
	return distance

if __name__ == "__main__":
	main(sys.argv)