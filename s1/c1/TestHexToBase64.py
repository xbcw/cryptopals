import HexToBase64
import unittest

print "Test 'aaaa'"
print HexToBase64.hex_to_base64("aaaa")

print "Test 'aaa'"
try:
	print HexToBase64.hex_to_base64("aaa")
except Exception as e:
	print "Error: %s\n" % e

print "Crypto-challenges Set 1 Challenge 1"
cc_input = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
cc_result = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
result = HexToBase64.hex_to_base64(cc_input)
print len(cc_result)
print len(result)
if cc_result == result:
	print "correct"
else:
	print "incorrect"

