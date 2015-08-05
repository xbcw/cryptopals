import sys
import cryptopals
import math
import utils
import os

CHALLENGES = {}
CHALLENGE_NAME = {
	1: 'Hex to Base64',
	2: 'Fixed XOR',
	3: 'Single Byte XOR',
	4: 'Detect Single-character XOR',
	5: 'Implementing Repeating-key XOR',
	6: 'Break Repeating-key XOR',
	7: 'AES in ECB mode',
	8: 'Detect AES in ECB mode',
	9: 'Implement PKCS#7 Padding',
	10: 'Implement CBC Mode',
	11: 'ECB/CBC detection oracle',
	12: 'Byte-at-a-time ECB decryption (Simple)'
}

def main(argv):
	run = sorted(CHALLENGES.keys())

	if len(sys.argv) > 1:
		for i in range(1, len(sys.argv)):
			try:
				n = int(sys.argv[i])
			except ValueError:
				print "Arguments must be integers. Exiting..."
				sys.exit(1)
			if n not in CHALLENGES:
				print "Challenge %d does not exist." % n
				print
				continue

			CHALLENGES[int(sys.argv[i])]()
			print

def challenge(num):
	def decorator(func):
		def header(*args, **kwargs):
			print "--------------------------------------"
			print "Crypto-challenge: %s" % CHALLENGE_NAME[num]
			print "Set %d Challenge %d" % (math.ceil(num/8.0), num - 8*(math.ceil(num/8.0)-1))
			print "--------------------------------------"
			func(*args, **kwargs)
		CHALLENGES[num] = header
		return header
	return decorator

def expect(expected, actual):
	if actual != expected:
		print "Test failed."
		print "Expected: " + repr(str(expected))
		print "Actual:   " + repr(str(actual))
		return False
	else:
		print "Test successful."
		print "Expected: " + repr(str(expected))
		print "Actual:   " + repr(str(actual))
		return True


@challenge(1)
def c1():
	test_input = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
	expected_result = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
	result = cryptopals.hex_to_base64(test_input)
	expect(expected_result, result)

@challenge(2)
def c2():
	str1 = "1c0111001f010100061a024b53535009181c"
	str2 = "686974207468652062756c6c277320657965"
	expected_result = "746865206b696420646f6e277420706c6179"
	result = cryptopals.fixed_xor(str1, str2)
	expect(expected_result, result)

@challenge(3)
def c3():
	input_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
	result = cryptopals.single_byte_xor(input_string)
	print "Key:     " + result[1]
	print "Score:   " + str(result[2])
	print "String:  " + result[0]

@challenge(4)
def c4():
	filename = "data/4.txt"
	ciphertext = utils.get_ciphertext(filename)
	result = cryptopals.detect_single_char_xor(ciphertext)
	print "Key:     " + result[1]
	print "Score:   " + str(result[2])
	print "String:  " + result[0]

@challenge(5)
def c5():
	test_string = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
	test_key = "ICE"
	expected_result = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
	result = cryptopals.repeating_key_xor(test_string, test_key)
	expect(expected_result, result)

@challenge(6)
def c6():
	str1 = "this is a test"
	str2 = "wokka wokka!!!"
	result = utils.hamming_distance(str1, str2)
	expect(37.0, result)

	filename = "data/6.txt"
	ciphertext = utils.get_ciphertext(filename)
	result = cryptopals.break_repeating_key_xor(ciphertext)
	print
	print result[1]
	print result[0]


@challenge(7)
def c7():
	key = "YELLOW SUBMARINE"
	filename = "data/7.txt"
	ciphertext = utils.get_ciphertext(filename).decode('Base64')
	print cryptopals.decrypt_aes_ecb(ciphertext, key)

@challenge(8)
def c8():
	filename = "data/8.txt"
	ciphertext = utils.get_ciphertext(filename)
	print cryptopals.get_ecb_string(ciphertext)

@challenge(9)
def c9():
	block_size = 20
	input_string = "YELLOW SUBMARINE"
	expected_result = "YELLOW SUBMARINE\x04\x04\x04\x04"
	result = cryptopals.pad_pkcs7(input_string, block_size)
	expect(expected_result, result)
	expect(len(expected_result), len(result))

@challenge(10)
def c10():
	filename = "data/10.txt"
	key = "YELLOW SUBMARINE"
	iv = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
	ciphertext = utils.get_ciphertext(filename).decode('base64')
	print cryptopals.decrypt_aes_cbc(ciphertext, key, iv)

@challenge(11)
def c11():
	cipher = cryptopals.encrypt_random_aes
	if cryptopals.detect_ecb(cipher):
		print "Detected ECB Mode"
	else:
		print "Detected CBC Mode"

@challenge(12)
def c12():
	# 'secret' setup
	unknown_text = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\naGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\ndXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\nYnkK'.decode('base64')
	unknown_key = 'ASKD8uweJ39qifjC'
	my_string = 'A'*32
	ciphertext = cryptopals.encrypt_ecb_static_key_appended_text(my_string, unknown_text, unknown_key)

	# crack ciphertext
	block_size = cryptopals.get_block_size(my_string, ciphertext)
	match_string = cryptopals.encrypt_ecb_static_key_appended_text('A'*(block_size-1), ciphertext, unknown_key)
	print cryptopals.match_dictionary(match_string, ciphertext, block_size-1, unknown_key)

if __name__ == "__main__":
	main(sys.argv)
