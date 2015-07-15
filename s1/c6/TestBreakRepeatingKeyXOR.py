import BreakRepeatingKeyXOR

str1 = "this is a test"
str2 = "wokka wokka!!!"
print "wokka wokka test..."
print BreakRepeatingKeyXOR.hamming_distance(str1, str2)

filename = "6.txt"
result = BreakRepeatingKeyXOR.crack(filename)
print result[1]
print result[0]