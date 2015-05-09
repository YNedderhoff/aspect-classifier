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


def find_affixes(file_in, len_list):
    top_x = [2, 3, 4, 5] # all the affix lenghts that should be computed

    # creates lists for suffixes and prefixes, containing as many dictionaries as top_x elements:
    suffixes = {}
    prefixes = {}
    letter_combs = {}

    for i in top_x:
        suffixes[i] = {}
        prefixes[i] = {}
        letter_combs[i] = {}

    print "\tReading prefixes and suffixes"
    t0 = time.time()

    # after the following loop, every dictionary in both lists contains all affixes
    # that fit in that list as a key, and the respective frequency as it's value:
    for sentence in tk.sentences(codecs.open(file_in,encoding='utf-8')):
        for token in sentence:
            for i in top_x: # for every desired affix length
                if len(token.form) > i: # word must be longer than suffix length

                    # token.form[-i:] is the suffix with length i

                    # suffixes[i-2] is the dictionary for suffixes with length i
                    # in the list 'suffixes'

                    if token.form[-i:] in suffixes[i]:
                        if token.gold_pos in suffixes[i][token.form[-i:]]:
                            suffixes[i][token.form[-i:]][token.gold_pos] += 1
                        else:
                            suffixes[i][token.form[-i:]][token.gold_pos] = 1
                    else:
                        suffixes[i][token.form[-i:]] = {token.gold_pos: 1}
                if len(token.form) > i: # word must be longer than prefix length

                    # the same as for suffixes

                    if token.form[:i] in prefixes[i]:
                        if token.gold_pos in prefixes[i][token.form[:i]]:
                            prefixes[i][token.form[:i]][token.gold_pos] += 1
                        else:
                            prefixes[i][token.form[:i]][token.gold_pos] = 1
                    else:
                        prefixes[i][token.form[:i]] = {token.gold_pos: 1}

                if len(token.form) > i+1 and i > 2:

                    # letter combinations in the word
                    # if they don't overlap with pre- or suffixes
                    for j in range(i, len(token.form)-(i*2-1)):
                        if token.form[j:j+i] in letter_combs[i]:
                            if token.gold_pos in letter_combs[i][token.form[j:j+i]]:
                                letter_combs[i][token.form[j:j+i]][token.gold_pos] += 1
                            else:
                                letter_combs[i][token.form[j:j+i]][token.gold_pos] = 1
                        else:
                            letter_combs[i][token.form[j:j+i]] = {token.gold_pos: 1}

    t1 = time.time()
    print "\t\t"+str(t1-t0)+" sec."

    print "\tComputing top prefixes and suffixes"
    t0 = time.time()

    for l in [suffixes, prefixes, letter_combs]:

        if [suffixes, prefixes, letter_combs].index(l) == 0: print "\t\tSuffixes:"
        elif [suffixes, prefixes, letter_combs].index(l) == 1: print "\t\tPrefixes:"
        else: print "\t\tLetter Combinations:"

        for x in top_x:
            if len(l[x]) > 0:
                print "\t\t\tLength: "+str(x)
                for elem in sorted(l[x].items(), key = lambda x: sum(x[1].values()), reverse = True)[:len_list]:
                    print "\t\t\t\t"+elem[0]+"\t"+str(sorted(elem[1].items(), key = lambda x: x[1], reverse = True)[:5])

    t1 = time.time()
    print "\t\t"+str(t1-t0)+" sec."