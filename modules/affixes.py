import codecs
import time
import token as tk

from math import log


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

    labels = {}

    for i in top_x:
        suffixes[i] = {}
        prefixes[i] = {}
        letter_combs[i] = {}

    print "\tReading prefixes and suffixes"
    t0 = time.time()

    # after the following loop, every dictionary in both lists contains all affixes
    # that fit in that list as a key, and the respective frequency as it's value:
    for sentence in tk.sentences(codecs.open(file_in, encoding='utf-8')):
        for token in sentence:

            if token.gold_tag_2 in labels:
                labels[token.gold_tag_2] += 1
            else:
                labels[token.gold_tag_2] = 1

            for i in top_x: # for every desired affix length
                if len(token.form_2) > i: # word must be longer than suffix length

                    # token.form_2[-i:] is the suffix with length i

                    # suffixes[i-2] is the dictionary for suffixes with length i
                    # in the list 'suffixes'

                    if token.form_2[-i:] in suffixes[i]:
                        if token.gold_tag_2 in suffixes[i][token.form_2[-i:]]:
                            suffixes[i][token.form_2[-i:]][token.gold_tag_2] += 1
                        else:
                            suffixes[i][token.form_2[-i:]][token.gold_tag_2] = 1
                    else:
                        suffixes[i][token.form_2[-i:]] = {token.gold_tag_2: 1}
                if len(token.form_2) > i: # word must be longer than prefix length

                    # the same as for suffixes

                    if token.form_2[:i] in prefixes[i]:
                        if token.gold_tag_2 in prefixes[i][token.form_2[:i]]:
                            prefixes[i][token.form_2[:i]][token.gold_tag_2] += 1
                        else:
                            prefixes[i][token.form_2[:i]][token.gold_tag_2] = 1
                    else:
                        prefixes[i][token.form_2[:i]] = {token.gold_tag_2: 1}

                if len(token.form_2) > i+1 and i > 2:

                    # letter combinations in the word
                    # if they don't overlap with pre- or suffixes
                    for j in range(i, len(token.form_2)-(i*2-1)):
                        if token.form_2[j:j+i] in letter_combs[i]:
                            if token.gold_tag_2 in letter_combs[i][token.form_2[j:j+i]]:
                                letter_combs[i][token.form_2[j:j+i]][token.gold_tag_2] += 1
                            else:
                                letter_combs[i][token.form_2[j:j+i]][token.gold_tag_2] = 1
                        else:
                            letter_combs[i][token.form_2[j:j+i]] = {token.gold_tag_2: 1}

    t1 = time.time()
    print "\t\t"+str(t1-t0)+" sec."
    return [suffixes, prefixes, letter_combs]
