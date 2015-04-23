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

	topX = [2, 3, 4, 5] # All the affix lenghts that should be computed
	
	# Creates lists for suffixes and affixes, containing as many dictionaries as topX elements

	suffixes = []
	prefixes = []

	for i in range(0, len(topX)):
		suffixes.append({})
		prefixes.append({})

	print "\tReading prefixes and suffixes"
	t0 = time.time()

	# After the following loop, every dictionary in both lists contains
	# all affixes that fit in that list as a key, and the respective occurence 
	# number as it's value

	for sentence in tk.sentences(codecs.open(filein,encoding='utf-8')):
		for token in sentence:
			for i in topX: # for every affix length i want
				if len(token.form) > i: # if it was == or <, it wouldn't be an affix

					# token.form[-i:] is the suffix with length i
					
					# suffixes[i-2] is the dictionary for suffixes with length i
					# in the list 'suffixes'

					if token.form[-i:] in suffixes[i-2]:
						suffixes[i-2][token.form[-i:]] += 1
					else: 
						suffixes[i-2][token.form[-i:]] = 1
				if len(token.form) > i:

					# the same as for suffixes

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

			# revD has numbers as keys, and the respective suffixes with that length
			# in a list as it's value

			revD = reverse(d)
			topList = []
			for v in sorted(revD.keys())[::-1]: # loop over the sorted keys, highest first
				for element in revD[v]:
					if counter < lenList:

						# the values are appended to 'topList' until the number
						# of elements we want to have in that list ('lenList')
						# is reached

						topList.append([v, element])
						counter+=1
			print "\t\t\t"+str(topList)
	t1 = time.time()
	print "\t\t"+str(t1-t0)+" sec."
