import sys
import utils
import struct
import os
import random
import difflib
import math
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

def detect_single_char_xor(ciphertext):
	high_score = 0
	best_result = 0
	for line in ciphertext.split('\n'):
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

def break_repeating_key_xor(ciphertext):
	ciphertext = ciphertext.decode('base64')
	data = list(ciphertext)
	keysize = utils.get_keysize(ciphertext)[0][0]
	blocks = utils.get_keysized_blocks(data, keysize)
	transposed_blocks = utils.transpose_blocks(blocks)
	key = ''
	for block in transposed_blocks:
		key += single_byte_xor(block.encode('hex'))[1]
	result = ''
	keysize = len(key)
	for i, c in enumerate(ciphertext):
		result += chr(ord(c) ^ ord(key[i%keysize]))
	return key, result

def decrypt_aes_ecb(ciphertext, key):
	return AES.new(key, AES.MODE_ECB).decrypt(ciphertext)

def get_ecb_string(ciphertext):
	low_score = sys.maxint
	best_line = ''
	block_size = 16
	for line in ciphertext.split('\n'):
		if len(line) > 0:
			blocks = []
			for i in range(0, len(line)/block_size):
				blocks.append(line[i*block_size:i*block_size+block_size])
			if len(set(blocks)) < low_score:
				low_score = len(set(blocks))
				best_line = line
	return best_line

def detect_ecb(cipher):
	block_size = 16
	ciphertext = cipher(pad_pkcs7('A', 128))
	return detect_repeating_block(ciphertext, block_size)

def detect_repeating_block(ciphertext, block_size):
	blocks = []
	for i in range(0, len(ciphertext)/block_size):
		blocks.append(ciphertext[i*block_size:i*block_size+block_size])
	if len(set(blocks)) != len(blocks):
		return True
	else:
		return False

def pad_pkcs7(input_string, block_size):
	padding = block_size - len(input_string)
	while len(input_string) < block_size:
		input_string += struct.pack('B', padding)
	return input_string

def decrypt_aes_cbc(ciphertext, key, iv):
	block_size = 16
	block = ''
	decrypted_blocks = ''
	for i in range(0, len(ciphertext)/block_size):
		block = decrypt_aes_ecb(ciphertext[block_size*i:block_size*i+block_size], key)
		if i > 0:
			decrypted_blocks += fixed_xor(block.encode('hex'), ciphertext[block_size*(i-1):block_size*i].encode('hex'))
		else:
			decrypted_blocks += fixed_xor(block.encode('hex'), pad_pkcs7(iv, block_size).encode('hex'))
	return decrypted_blocks.decode('hex')

def encrypt_random_aes(input_string):
	key_length = 16
	key = os.urandom(key_length)
	iv = os.urandom(key_length)
	if random.random() > 0.5:
		obj = AES.new(key, AES.MODE_CBC, iv)
		print "Using CBC Mode"
	else:
		obj = AES.new(key, AES.MODE_ECB)
		print "Using ECB Mode"
	new_string = os.urandom(random.randint(5,10)) + input_string + os.urandom(random.randint(5,10))
	padding = 0
	while(padding < len(new_string)):
		padding += 16
	return obj.encrypt(pad_pkcs7(new_string,padding))

def encrypt_ecb_static_key_appended_text(input_string, ciphertext, key=os.urandom(16)):
	obj = AES.new(key, AES.MODE_ECB)
	new_string = input_string + ciphertext
	padding = 0
	while(padding < len(new_string)):
		padding += 16
	return obj.encrypt(pad_pkcs7(new_string,padding))

def get_block_size(my_string, ciphertext):
	prev_diff = 0
	for i in range(1, len(my_string)):
		diff = 0
		block = encrypt_ecb_static_key_appended_text(my_string[0:i], ciphertext)
		for block_index,c in enumerate(block):
			try:
				if block[block_index] != prev_block[block_index]:
					diff += 1
			except:
				diff += 1
		if i != 1:
			if prev_diff != diff:
				return diff - prev_diff
		prev_diff = diff
	return -1

def match_dictionary(match_string, ciphertext, block_size, key):
	print match_string
	dict = []
	for c in range(ord(' '), ord('z')):
		new_input_string = 'A'*block_size + chr(c)
		encrypted_string = encrypt_ecb_static_key_appended_text(new_input_string, ciphertext, key)
		if match_string == encrypted_string:
			return ord(c)

