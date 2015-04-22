import codecs
import time
import token as tk

def findAffixes(filein, lenList):

	suffixesLen2 = []
	suffixesLen3 = []
	suffixesLen4 = []
	suffixesLen5 = []

	prefixesLen2 = []
	prefixesLen3 = []
	prefixesLen4 = []
	prefixesLen5 = []
	
	# A list with all existing suffixes is generated
	print "\tReading prefixes and suffixes"
	t0 = time.time()
	for sid, sentence in enumerate(tk.sentences(codecs.open(filein,encoding='utf-8'))):
		for tid,token in enumerate(sentence):

			#suffixes
			for i in range(2,6):
				if len(token.form[-i:]) == i:
					if not len(token.form) == i:
						if i == 2: suffixesLen2.append(token.form[-i:])
						if i == 3: suffixesLen3.append(token.form[-i:])
						if i == 4: suffixesLen4.append(token.form[-i:])
						if i == 5: suffixesLen5.append(token.form[-i:])

				if len(token.form[:i]) == i:
					if not len(token.form) == i:
						if i == 2: prefixesLen2.append(token.form[:i])
						if i == 3: prefixesLen3.append(token.form[:i])
						if i == 4: prefixesLen4.append(token.form[:i])
						if i == 5: prefixesLen5.append(token.form[:i])
			
	t1 = time.time()
	print "\t\t"+str(t1-t0)+" sec."
	print "\tComputing top prefixes and suffixes"
	t0 = time.time()

	# List comprehension: i.e. [[5, word1], [12, word2], ...]; then sorted, reversed with [::-1]
	# [0:lenList] , meaning the first <lenList> elements in the list, are writtein in the variable
	suffixesLen2Top = sorted([[suffixesLen2.count(x), x] for x in set(suffixesLen2)])[::-1][0:lenList]
	suffixesLen3Top = sorted([[suffixesLen3.count(x), x] for x in set(suffixesLen3)])[::-1][0:lenList]
	suffixesLen4Top = sorted([[suffixesLen4.count(x), x] for x in set(suffixesLen4)])[::-1][0:lenList]
	suffixesLen5Top = sorted([[suffixesLen5.count(x), x] for x in set(suffixesLen5)])[::-1][0:lenList]

	prefixesLen2Top = sorted([[prefixesLen2.count(x), x] for x in set(prefixesLen2)])[::-1][0:lenList]
	prefixesLen3Top = sorted([[prefixesLen3.count(x), x] for x in set(prefixesLen3)])[::-1][0:lenList]
	prefixesLen4Top = sorted([[prefixesLen4.count(x), x] for x in set(prefixesLen4)])[::-1][0:lenList]
	prefixesLen5Top = sorted([[prefixesLen5.count(x), x] for x in set(prefixesLen5)])[::-1][0:lenList]

	t1 = time.time()
	print "\t\t"+str(t1-t0)+" sec."
	print "\n"

	print "\t\tSuffixes:"
	print "\t\t\t" + str(suffixesLen2Top)
	print "\t\t\t" + str(suffixesLen3Top)
	print "\t\t\t" + str(suffixesLen4Top)
	print "\t\t\t" + str(suffixesLen5Top)
	print "\n"
	print "\t\tPrefixes:"
	print "\t\t\t" + str(prefixesLen2Top)
	print "\t\t\t" + str(prefixesLen3Top)
	print "\t\t\t" + str(prefixesLen4Top)
	print "\t\t\t" + str(prefixesLen5Top)
	print "\n"

