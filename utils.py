import operator

FREQUENCY = {
			'a': 8.167,
			'A': 8.167/6,
			'b': 1.492,
			'B': 1.492/6,
			'c': 2.782,
			'C': 2.782/6,
			'd': 4.253,
			'D': 4.253/6,
			'e': 12.702,
			'E': 12.702/6,
			'f': 2.228,
			'F': 2.228/6,
			'g': 2.015,
			'G': 2.015/6,
			'h': 6.094,
			'H': 6.094/6,
			'i': 6.966,
			'I': 6.966/6,
			'j': 0.153,
			'J': 0.153/6,
			'k': 0.772,
			'K': 0.772/6,
			'l': 4.025,
			'L': 4.025/6,
			'm': 2.406,
			'M': 2.406/6,
			'n': 6.749,
			'N': 6.749/6,
			'o': 7.507,
			'O': 7.507/6,
			'p': 1.929,
			'P': 1.929/6,
			'q': 0.095,
			'Q': 0.095/6,
			'r': 5.987,
			'R': 5.987/6,
			's': 6.327,
			'S': 6.327/6,
			't': 9.056,
			'T': 9.056/6,
			'u': 2.758,
			'U': 2.758/6,
			'v': 0.978,
			'V': 0.978/6,
			'w': 2.361,
			'W': 2.361/6,
			'x': 0.150,
			'X': 0.150/6,
			'y': 1.974,
			'Y': 1.974/6,
			'z': 0.074,
			'Z': 0.074/6,
	        '*': 0.0197,
	        '!': 0.023,
	        '@': 0.0229,
	        '=': 0.01,
	        '.': 0.0231,
	        '_': 0.014,
	        '$': 0.014,
	        '#': 0.013,
	        ',': 0.01,
	        '\\': 0.009,
	        '/': 0.009,
	        '-': 0.002,
	        '&': 0.001,
	        '`': 0.001,
	        '<': 0.001,
	        '>': 0.001,
	        '+': 0.001,
	        '{': 0.001,
	        '}': 0.001,
	       	':': 0.001,
	        ' ': 12.8,
	        '\n': 8.0,
	        '1': 1.0,
	        '2': 1.0,
	        '3': 1.0,
	        '4': 1.0,
	        '5': 1.0,
	        '6': 1.0,
	        '7': 1.0,
	        '8': 1.0,
	        '9': 1.0,
	        '0': 1.0,
			}

# Returns score based on English letter frequency
def frequency_score(input_string):
	score = 0.0
	for i in input_string:
		if i in FREQUENCY:
			score += FREQUENCY[i]
	return score

# Returns number of differing bits between two equal length strings
def hamming_distance(str1, str2):
	bin_str1 = format(int(str1.encode('hex'), 16), '#0512b')
	bin_str2 = format(int(str2.encode('hex'), 16), '#0512b')
	distance = 0.0
	for x in range(0, len(bin_str1)):
		if bin_str1[x] is not bin_str2[x]:
			distance += 1.0
	return distance

# returns the dataset broken into keysize blocks
def get_keysized_blocks(ciphertext, keysize):
	blocks = []
	for x in range(0, len(ciphertext)/keysize):
		blocks.append(''.join(ciphertext[keysize*x:keysize*(x+1)]))
	return blocks

# takes all the characters of a block of strings and places them in blocks based on position
def transpose_blocks(blocks):
	result = []
	for block in blocks:
		for i in range(0, len(blocks[0])):
			if len(result) <= i:
				result.append(block[i])
			else:
				result[i] += block[i]
	return result

# guesses keysize for a ciphertext
def get_keysize(ciphertext):
	scores = {}
	for keysize in range(2, 40):
		result = 0
		samples = 10
		for i in range(0, samples):
			result += hamming_distance(ciphertext[keysize*i:keysize*(i+1)], ciphertext[keysize*(i+1):keysize*(i+2)])

		scores[keysize] = (result/samples)/keysize

	sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))

	return sorted_scores