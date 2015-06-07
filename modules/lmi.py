from math import log

class lmi(object):
    
    def __init__(self, tokens, feat_vec):
        self.tokens = tokens
        self.feat_vec = feat_vec
        self.top_x = [2, 3, 4, 5]
        
    #@property
    def compute_lmi(self):
        pos_tags = {}
        lmi_dict = {}
        for feat in self.feat_vec:
            lmi_dict[feat] = {}

        for token in self.tokens:

            if token.gold_pos in pos_tags:
                pos_tags[token.gold_pos] += 1
            else:
                pos_tags[token.gold_pos] = 1
        
            # Uppercase

            if token.uppercase:
                if token.gold_pos in lmi_dict["uppercase"]:
                    lmi_dict["uppercase"][token.gold_pos] += 1
                else:
                    lmi_dict["uppercase"][token.gold_pos] = 1

            if token.capitalized:
                upper_char = False
                for char in token.form[1:]:
                    if char.isupper():
                        upper_char = True
                if not upper_char:
                    if token.gold_pos in lmi_dict["capitalized"]:
                        lmi_dict["capitalized"][token.gold_pos] += 1
                    else:
                        lmi_dict["capitalized"][token.gold_pos] = 1
    
    
            # form
    
            # the current form:
            if token.gold_pos in lmi_dict["current_form_" + token.form]:
                lmi_dict["current_form_" + token.form][token.gold_pos] += 1
            else:
                lmi_dict["current_form_" + token.form][token.gold_pos] = 1
    
            # if applicable, the previous form:
            if token.previous_token:
                if token.gold_pos in lmi_dict["prev_form_" + token.previous_token.form]:
                    lmi_dict["prev_form_" + token.previous_token.form][token.gold_pos] += 1
                else:
                    lmi_dict["prev_form_" + token.previous_token.form][token.gold_pos] = 1

            # if applicable, the next token form:
            if token.next_token:
                if token.gold_pos in lmi_dict["next_form_" + token.next_token.form]:
                    lmi_dict["next_form_" + token.next_token.form][token.gold_pos] += 1
                else:
                    lmi_dict["next_form_" + token.next_token.form][token.gold_pos] = 1

            # form length
    
            # the current form length:
            if token.gold_pos in lmi_dict["current_word_len_" + str(len(token.form))]:
                lmi_dict["current_word_len_" + str(len(token.form))][token.gold_pos] += 1
            else:
                lmi_dict["current_word_len_" + str(len(token.form))][token.gold_pos] = 1
    
            # if applicable, the previous form length:
            if token.previous_token:
                if token.gold_pos in lmi_dict["prev_word_len_" + str(len(token.previous_token.form))]:
                    lmi_dict["prev_word_len_" + str(len(token.previous_token.form))][token.gold_pos] += 1
                else:
                    lmi_dict["prev_word_len_" + str(len(token.previous_token.form))][token.gold_pos] = 1

            # if applicable, the next token form length:
            if token.next_token:
                if token.gold_pos in lmi_dict["next_word_len_" + str(len(token.next_token.form))]:
                    lmi_dict["next_word_len_" + str(len(token.next_token.form))][token.gold_pos] += 1
                else:
                    lmi_dict["next_word_len_" + str(len(token.next_token.form))][token.gold_pos] = 1
    
            # position in sentence
    
            if token.gold_pos in lmi_dict["position_in_sentence_" + str(token.t_id)]:
                lmi_dict["position_in_sentence_" + str(token.t_id)][token.gold_pos] += 1
            else:
                lmi_dict["position_in_sentence_" + str(token.t_id)][token.gold_pos] = 1
                
            for i in self.top_x:
                if "prefix_" + token.form[:i] in lmi_dict:
                    if token.gold_pos in lmi_dict["prefix_" + token.form[:i]]:
                        lmi_dict["prefix_" + token.form[:i]][token.gold_pos] += 1
                    else:
                        lmi_dict["prefix_" + token.form[:i]][token.gold_pos] = 1
                if "suffix_" + token.form[-i:] in lmi_dict:
                    if token.gold_pos in lmi_dict["suffix_" + token.form[-i:]]:
                        lmi_dict["suffix_" + token.form[-i:]][token.gold_pos] += 1
                    else:
                        lmi_dict["suffix_" + token.form[-i:]][token.gold_pos] = 1
    
                if len(token.form) > i+1 and i > 2:
    
                    # letter combinations in the word
                    # if they don't overlap with pre- or suffixes
                    for j in range(i, len(token.form)-(i*2-1)):
                        if "lettercombs_" + token.form[j:j+i] in lmi_dict:
                            if token.gold_pos in lmi_dict["lettercombs_" + token.form[j:j+i]]:
                                lmi_dict["lettercombs_" + token.form[j:j+i]][token.gold_pos] += 1
                            else:
                                lmi_dict["lettercombs_" + token.form[j:j+i]][token.gold_pos] = 1

        # compute lmi
        for feature in lmi_dict:
            temp = sum(lmi_dict[feature].values())
            for pos_tag in lmi_dict[feature]:
                lmi_dict[feature][pos_tag] = round(float(lmi_dict[feature][pos_tag])*log(float(lmi_dict[feature][pos_tag])/(float(pos_tags[pos_tag])*float(temp)), 2), 2)

        """
        form_counter = 0
        word_len_counter = 0
        position_counter = 0
        prefix_counter = 0
        suffix_counter = 0
        lettercombs_counter = 0
        for feature in lmi_dict:
            if "form_" in feature:
                form_counter += 1
            elif "word_len_" in feature:
                word_len_counter += 1
            elif "position_" in feature:
                position_counter += 1
            elif "prefix_" in feature:
                prefix_counter += 1
            elif "suffix_" in feature:
                suffix_counter += 1
            elif "lettercombs_" in feature:
                lettercombs_counter += 1
        print form_counter
        print word_len_counter
        print position_counter
        print prefix_counter
        print suffix_counter
        print lettercombs_counter
        """
        """
        temp = {}
        for feature in lmi_dict:
            for pos_tag in lmi_dict[feature]:
                if pos_tag in temp:
                    temp[pos_tag].append([feature, lmi_dict[feature][pos_tag]])
                else:
                    temp[pos_tag] = [[feature, lmi_dict[feature][pos_tag]]]
        for pos_tag in temp:
            temp[pos_tag] = [[x[0],str(x[1])] for x in sorted(temp[pos_tag], key = lambda x: x[1], reverse=True)]
        lmi_values = open("lmi3.txt", "w")
        line = ""
        pos_tags = temp.keys()
        for pos_tag in pos_tags:
            line += pos_tag + "\t"
        line = line[:-1]
        lmi_values.write(line.encode("utf-8") + "\n")
        max_len = 0
        for pos_tag in pos_tags:
            if len(temp[pos_tag]) > max_len:
                max_len = len(temp[pos_tag])
        print max_len
        for ind in range(max_len):
            line = ""
            for pos_tag in pos_tags:
                try:
                    line += ",".join(temp[pos_tag][ind]) + "\t"
                except IndexError:
                    line += ",".join(temp[pos_tag][-1]) + "\t"
            line = line[:-1]
            if ind < max_len - 1:
                lmi_values.write(line.encode("utf-8") + "\n")
            else:
                lmi_values.write(line.encode("utf-8"))
        lmi_values.close()

        
        temp = []
        for feature in lmi_dict:
            temp += [x for x in lmi_dict[feature].values()]
            #print lmi_dict[feature].values()[:5]

        lmi_values = open("lmi.txt", "w")
        for value in sorted(temp):
            lmi_values.write(str(value)+"\n")
        lmi_values.close()
        """
        return lmi_dict
