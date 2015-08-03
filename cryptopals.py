import sys
import utils
import struct
from Crypto.Cipher import AES

def hex_to_base64(input_string):

	int(input_string,16)
	return input_string.decode('hex').encode('base64').strip('\n')


def fixed_xor(str1, str2):
	return ''.join(
			  	chr(ord(a) ^ ord(b)) for a,b in zip(str1.decode('hex') ,str2.decode('hex'))
			  ).encode('hex')


def single_byte_xor(input_string):
	high_score = -sys.maxint - 1
	best_char = 0
	best_string = ''
	for i in range(ord(' '), ord('z')):
		try_string = ''.join(chr(ord(a) ^ ord(chr(i))) for a in input_string.decode('hex'))
		current_score = utils.frequency_score(try_string)
		if current_score > high_score:
			high_score = current_score
			best_char = chr(i)
			best_string = try_string
	return best_string, best_char, high_score

def detect_single_char_xor(filename):
	try:
		file = open(filename, 'r')
	except Exception as e:
		print "Error: %s" % str(e)
	high_score = 0
	best_result = 0
	for line in file:
		result = single_byte_xor(line.strip())
		if result[2] > high_score:
			high_score = result[2]
			best_result = result
	return best_result

def repeating_key_xor(input_string, key):
	encrypted_data = ''
	for i,c in enumerate(input_string):
		encrypted_data += chr(ord(c) ^ ord(key[i%3]))
	return encrypted_data.encode('hex')

def break_repeating_key_xor(filename):
	file_string = open(filename, 'r').read().decode('base64')
	data = list(file_string)
	keysize = utils.get_keysize(file_string)[0][0]
	blocks = utils.get_keysized_blocks(data, keysize)
	transposed_blocks = utils.transpose_blocks(blocks)
	key = ''
	for block in transposed_blocks:
		key += single_byte_xor(block.encode('hex'))[1]
	result = ''
	keysize = len(key)
	for i, c in enumerate(file_string):
		result += chr(ord(c) ^ ord(key[i%keysize]))
	return key, result

def decrypt_aes_ecb(filename, key):
	ciphertext = open(filename, 'r').read().decode('base64')
	return AES.new(key, AES.MODE_ECB).decrypt(ciphertext)

def decrypt_aes_ecb_string(ciphertext, key):
	return AES.new(key, AES.MODE_ECB).decrypt(ciphertext)

def detect_aes_ecb(filename):
	ciphertext = open(filename, 'r')
	low_score = sys.maxint
	best_line = ''
	block_size = 16
	for line in ciphertext:
		blocks = []
		for i in range(0, len(line)/block_size):
			blocks.append(line[i*block_size:i*block_size+block_size])
		if len(set(blocks)) < low_score:
			low_score = len(set(blocks))
			best_line = line
	return best_line

def pad_pkcs7(input_string, block_size):
	padding = block_size - len(input_string)
	while len(input_string) < block_size:
		input_string += struct.pack('B', padding)
	return input_string

def decrypt_aes_cbc(filename, key, iv):
	block_size = 16
	ciphertext = open(filename, 'r').read().decode('base64')
	block = ''
	decrypted_blocks = ''
	for i in range(0, len(ciphertext)/block_size):
		block = decrypt_aes_ecb_string(ciphertext[block_size*i:block_size*i+block_size], key)
		if i > 0:
			decrypted_blocks += fixed_xor(block.encode('hex'), ciphertext[block_size*(i-1):block_size*i].encode('hex'))
		else:
			decrypted_blocks += fixed_xor(block.encode('hex'), pad_pkcs7(iv, block_size).encode('hex'))
	return decrypted_blocks

def encryption_oracle(input_string):
	return input_string


