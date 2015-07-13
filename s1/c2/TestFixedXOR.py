import FixedXOR

str1 = "1c0111001f010100061a024b53535009181c"
str2 = "686974207468652062756c6c277320657965"
expected_result = "746865206b696420646f6e277420706c6179"
result = FixedXOR.fixed_xor(str1, str2)
print "Expected Result: %s" % expected_result
print "Actual Result: %s" % result