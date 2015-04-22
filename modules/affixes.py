import codecs
import time
import token as tk

def reverse(dictionary):
	newDict = {}
	for element in dictionary:
		if not dictionary[element] in newDict.keys():
			newDict[dictionary[element]] = [element]
		else:
			newDict[dictionary[element]].append(element)
	return newDict

def findAffixes(filein, lenList):

	topX = [2, 3, 4, 5]

	suffixes = []
	prefixes = []

	for i in range(0, len(topX)):
		suffixes.append({})
		prefixes.append({})

	print "\tReading prefixes and suffixes"
	t0 = time.time()
	for sentence in tk.sentences(codecs.open(filein,encoding='utf-8')):
		for token in sentence:
			for i in topX:
				if len(token.form[-i:]) == i:
					if not len(token.form) == i:
						if token.form[-i:] in suffixes[i-2]:
							suffixes[i-2][token.form[-i:]] += 1
						else: 
							suffixes[i-2][token.form[-i:]] = 1
				if len(token.form[:i]) == i:
					if not len(token.form) == i:
						if token.form[:i] in prefixes[i-2]:
							prefixes[i-2][token.form[:i]] += 1
						else: prefixes[i-2][token.form[:i]] = 1
		
	t1 = time.time()
	print "\t\t"+str(t1-t0)+" sec."

	print "\tComputing top prefixes and suffixes"
	t0 = time.time()

	for l in [suffixes, prefixes]:
		if [suffixes, prefixes].index(l) == 0: print "\t\tSuffixes:"
		else: print "\t\tPrefixes:"
		for d in l:
			counter = 0
			revD = reverse(d)
			topList = []
			for v in sorted(revD.keys())[::-1]:
				for element in revD[v]:
					if counter < lenList:
						topList.append([v, element])
						counter+=1
			print "\t\t\t"+str(topList)
	t1 = time.time()
	print "\t\t"+str(t1-t0)+" sec."
