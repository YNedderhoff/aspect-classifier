import codecs
import time
import token as tk

def reverse(dictionary):
	new_dict = {}
	for element in dictionary:
		if not dictionary[element] in new_dict.keys():
			new_dict[dictionary[element]] = [element]
		else:
			new_dict[dictionary[element]].append(element)
	return new_dict

def findAffixes(file_in, len_list):
	top_x = [2, 3, 4, 5] # all the affix lenghts that should be computed
	
	# creates lists for suffixes and prefixes, containing as many dictionaries as top_x elements:
	suffixes = []
	prefixes = []

	for i in range(0, len(top_x)):
		suffixes.append({})
		prefixes.append({})

	print "\tReading prefixes and suffixes"
	t0 = time.time()

	# after the following loop, every dictionary in both lists contains all affixes
	# that fit in that list as a key, and the respective frequency as it's value:
	for sentence in tk.sentences(codecs.open(filein,encoding='utf-8')):
		for token in sentence:
			for i in top_x: # for every desired affix length
				if len(token.form) > i: # word must be longer than suffix length

					# token.form[-i:] is the suffix with length i
					
					# suffixes[i-2] is the dictionary for suffixes with length i
					# in the list 'suffixes'

					if token.form[-i:] in suffixes[i-2]:
						suffixes[i-2][token.form[-i:]] += 1
					else: 
						suffixes[i-2][token.form[-i:]] = 1
				if len(token.form) > i: # word must be longer than prefix length

					# the same as for suffixes

					if token.form[:i] in prefixes[i-2]:
						prefixes[i-2][token.form[:i]] += 1
					else:
                                                prefixes[i-2][token.form[:i]] = 1
		
	t1 = time.time()
	print "\t\t"+str(t1-t0)+" sec."
	
	print "\tComputing top prefixes and suffixes"
	t0 = time.time()

	for l in [suffixes, prefixes]:
		if [suffixes, prefixes].index(l) == 0: print "\t\tSuffixes:"
		else: print "\t\tPrefixes:"
		
		for d in l:
			counter = 0

			# rev_d has numbers as keys, and the respective suffixes with that length
			# in a list as it's value

			rev_d = reverse(d)
			top_list = []
			for v in sorted(rev_d.keys())[::-1]: # loop over the sorted keys, highest first
				for element in rev_d[v]:
					if counter < len_list:

						# the values are appended to 'topList' until the number
						# of elements we want to have in that list ('lenList')
						# is reached

						top_list.append([v, element])
						counter+=1

			print "\t\t\t"+str(top_list)

	t1 = time.time()
	print "\t\t"+str(t1-t0)+" sec."
