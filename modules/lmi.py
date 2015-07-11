from math import log

class lmi(object):
    
    def __init__(self, tokens, feat_vec):
        self.tokens = tokens
        self.feat_vec = feat_vec
        self.top_x = [2, 3, 4, 5]
        
    def compute_lmi(self):
        pos_tags = {}
        lmi_dict = {}
        for feat in self.feat_vec:
            lmi_dict[feat] = {}

        for token in self.tokens:

            if token.gold_tag_1 in pos_tags:
                pos_tags[token.gold_tag_1] += 1
            else:
                pos_tags[token.gold_tag_1] = 1
        
            # Uppercase

            if token.uppercase_1:
                if token.gold_tag_1 in lmi_dict["uppercase_1"]:
                    lmi_dict["uppercase_1"][token.gold_tag_1] += 1
                else:
                    lmi_dict["uppercase_1"][token.gold_tag_1] = 1

            if token.capitalized_1:
                upper_char = False
                for char in token.form_1[1:]:
                    if char.isupper():
                        upper_char = True
                if not upper_char:
                    if token.gold_tag_1 in lmi_dict["capitalized_1"]:
                        lmi_dict["capitalized_1"][token.gold_tag_1] += 1
                    else:
                        lmi_dict["capitalized_1"][token.gold_tag_1] = 1

            # form
    
            # the current form:
            if token.gold_tag_1 in lmi_dict["current_form_token_1_" + token.form_1]:
                lmi_dict["current_form_token_1_" + token.form_1][token.gold_tag_1] += 1
            else:
                lmi_dict["current_form_token_1_" + token.form_1][token.gold_tag_1] = 1
    
            # if applicable, the previous form:
            if token.previous_token:
                if token.gold_tag_1 in lmi_dict["prev_form_token_1_" + token.previous_token.form_1]:
                    lmi_dict["prev_form_token_1_" + token.previous_token.form_1][token.gold_tag_1] += 1
                else:
                    lmi_dict["prev_form_token_1_" + token.previous_token.form_1][token.gold_tag_1] = 1

            # if applicable, the next token form:
            if token.next_token:
                if token.gold_tag_1 in lmi_dict["next_form_token_1_" + token.next_token.form_1]:
                    lmi_dict["next_form_token_1_" + token.next_token.form_1][token.gold_tag_1] += 1
                else:
                    lmi_dict["next_form_token_1_" + token.next_token.form_1][token.gold_tag_1] = 1

            # form length
    
            # the current form length:
            if token.gold_tag_1 in lmi_dict["current_word_len_token_1_" + str(len(token.form_1))]:
                lmi_dict["current_word_len_token_1_" + str(len(token.form_1))][token.gold_tag_1] += 1
            else:
                lmi_dict["current_word_len_token_1_" + str(len(token.form_1))][token.gold_tag_1] = 1
    
            # if applicable, the previous form length:
            if token.previous_token:
                if token.gold_tag_1 in lmi_dict["prev_word_len_token_1_" + str(len(token.previous_token.form_1))]:
                    lmi_dict["prev_word_len_token_1_" + str(len(token.previous_token.form_1))][token.gold_tag_1] += 1
                else:
                    lmi_dict["prev_word_len_token_1_" + str(len(token.previous_token.form_1))][token.gold_tag_1] = 1

            # if applicable, the next token form length:
            if token.next_token:
                if token.gold_tag_1 in lmi_dict["next_word_len_token_1_" + str(len(token.next_token.form_1))]:
                    lmi_dict["next_word_len_token_1_" + str(len(token.next_token.form_1))][token.gold_tag_1] += 1
                else:
                    lmi_dict["next_word_len_token_1_" + str(len(token.next_token.form_1))][token.gold_tag_1] = 1
    
            # position in sentence
    
            if token.gold_tag_1 in lmi_dict["position_in_sentence_token_1_" + str(token.t_id_1)]:
                lmi_dict["position_in_sentence_token_1_" + str(token.t_id_1)][token.gold_tag_1] += 1
            else:
                lmi_dict["position_in_sentence_token_1_" + str(token.t_id_1)][token.gold_tag_1] = 1
                
            for i in self.top_x:
                if "prefix_token_1_" + token.form_1[:i] in lmi_dict:
                    if token.gold_tag_1 in lmi_dict["prefix_token_1_" + token.form_1[:i]]:
                        lmi_dict["prefix_token_1_" + token.form_1[:i]][token.gold_tag_1] += 1
                    else:
                        lmi_dict["prefix_token_1_" + token.form_1[:i]][token.gold_tag_1] = 1
                if "suffix_token_1_" + token.form_1[-i:] in lmi_dict:
                    if token.gold_tag_1 in lmi_dict["suffix_token_1_" + token.form_1[-i:]]:
                        lmi_dict["suffix_token_1_" + token.form_1[-i:]][token.gold_tag_1] += 1
                    else:
                        lmi_dict["suffix_token_1_" + token.form_1[-i:]][token.gold_tag_1] = 1
    
                if len(token.form_1) > i+1 and i > 2:
    
                    # letter combinations in the word
                    # if they don't overlap with pre- or suffixes
                    for j in range(i, len(token.form_1)-(i*2-1)):
                        if "lettercombs_token_1_" + token.form_1[j:j+i] in lmi_dict:
                            if token.gold_tag_1 in lmi_dict["lettercombs_token_1_" + token.form_1[j:j+i]]:
                                lmi_dict["lettercombs_token_1_" + token.form_1[j:j+i]][token.gold_tag_1] += 1
                            else:
                                lmi_dict["lettercombs_token_1_" + token.form_1[j:j+i]][token.gold_tag_1] = 1


            if token.gold_tag_2 in pos_tags:
                pos_tags[token.gold_tag_2] += 1
            else:
                pos_tags[token.gold_tag_2] = 1
        
            # Uppercase

            if token.uppercase_2:
                if token.gold_tag_2 in lmi_dict["uppercase_2"]:
                    lmi_dict["uppercase_2"][token.gold_tag_2] += 1
                else:
                    lmi_dict["uppercase_2"][token.gold_tag_2] = 1

            if token.capitalized_2:
                upper_char = False
                for char in token.form_2[1:]:
                    if char.isupper():
                        upper_char = True
                if not upper_char:
                    if token.gold_tag_2 in lmi_dict["capitalized_2"]:
                        lmi_dict["capitalized_2"][token.gold_tag_2] += 1
                    else:
                        lmi_dict["capitalized_2"][token.gold_tag_2] = 1

            # form
    
            # the current form:
            if token.gold_tag_2 in lmi_dict["current_form_token_2_" + token.form_2]:
                lmi_dict["current_form_token_2_" + token.form_2][token.gold_tag_2] += 1
            else:
                lmi_dict["current_form_token_2_" + token.form_2][token.gold_tag_2] = 1
    
            # if applicable, the previous form:
            if token.previous_token:
                if token.gold_tag_2 in lmi_dict["prev_form_token_2_" + token.previous_token.form_2]:
                    lmi_dict["prev_form_token_2_" + token.previous_token.form_2][token.gold_tag_2] += 1
                else:
                    lmi_dict["prev_form_token_2_" + token.previous_token.form_2][token.gold_tag_2] = 1

            # if applicable, the next token form:
            if token.next_token:
                if token.gold_tag_2 in lmi_dict["next_form_token_2_" + token.next_token.form_2]:
                    lmi_dict["next_form_token_2_" + token.next_token.form_2][token.gold_tag_2] += 1
                else:
                    lmi_dict["next_form_token_2_" + token.next_token.form_2][token.gold_tag_2] = 1

            # form length
    
            # the current form length:
            if token.gold_tag_2 in lmi_dict["current_word_len_token_2_" + str(len(token.form_2))]:
                lmi_dict["current_word_len_token_2_" + str(len(token.form_2))][token.gold_tag_2] += 1
            else:
                lmi_dict["current_word_len_token_2_" + str(len(token.form_2))][token.gold_tag_2] = 1
    
            # if applicable, the previous form length:
            if token.previous_token:
                if token.gold_tag_2 in lmi_dict["prev_word_len_token_2_" + str(len(token.previous_token.form_2))]:
                    lmi_dict["prev_word_len_token_2_" + str(len(token.previous_token.form_2))][token.gold_tag_2] += 1
                else:
                    lmi_dict["prev_word_len_token_2_" + str(len(token.previous_token.form_2))][token.gold_tag_2] = 1

            # if applicable, the next token form length:
            if token.next_token:
                if token.gold_tag_2 in lmi_dict["next_word_len_token_2_" + str(len(token.next_token.form_2))]:
                    lmi_dict["next_word_len_token_2_" + str(len(token.next_token.form_2))][token.gold_tag_2] += 1
                else:
                    lmi_dict["next_word_len_token_2_" + str(len(token.next_token.form_2))][token.gold_tag_2] = 1
    
            # position in sentence
    
            if token.gold_tag_2 in lmi_dict["position_in_sentence_token_2_" + str(token.t_id_2)]:
                lmi_dict["position_in_sentence_token_2_" + str(token.t_id_2)][token.gold_tag_2] += 1
            else:
                lmi_dict["position_in_sentence_token_2_" + str(token.t_id_2)][token.gold_tag_2] = 1
                
            for i in self.top_x:
                if "prefix_token_2_" + token.form_2[:i] in lmi_dict:
                    if token.gold_tag_2 in lmi_dict["prefix_token_2_" + token.form_2[:i]]:
                        lmi_dict["prefix_token_2_" + token.form_2[:i]][token.gold_tag_2] += 1
                    else:
                        lmi_dict["prefix_token_2_" + token.form_2[:i]][token.gold_tag_2] = 1
                if "suffix_token_2_" + token.form_2[-i:] in lmi_dict:
                    if token.gold_tag_2 in lmi_dict["suffix_token_2_" + token.form_2[-i:]]:
                        lmi_dict["suffix_token_2_" + token.form_2[-i:]][token.gold_tag_2] += 1
                    else:
                        lmi_dict["suffix_token_2_" + token.form_2[-i:]][token.gold_tag_2] = 1
    
                if len(token.form_2) > i+1 and i > 2:
    
                    # letter combinations in the word
                    # if they don't overlap with pre- or suffixes
                    for j in range(i, len(token.form_2)-(i*2-1)):
                        if "lettercombs_token_2_" + token.form_2[j:j+i] in lmi_dict:
                            if token.gold_tag_2 in lmi_dict["lettercombs_token_2_" + token.form_2[j:j+i]]:
                                lmi_dict["lettercombs_token_2_" + token.form_2[j:j+i]][token.gold_tag_2] += 1
                            else:
                                lmi_dict["lettercombs_token_2_" + token.form_2[j:j+i]][token.gold_tag_2] = 1

        # compute lmi
        for feature in lmi_dict:
            temp = sum(lmi_dict[feature].values())
            for pos_tag in lmi_dict[feature]:
                lmi_dict[feature][pos_tag] = round(float(lmi_dict[feature][pos_tag])*log(float(lmi_dict[feature][pos_tag])/(float(pos_tags[pos_tag])*float(temp)), 2), 2)

        return lmi_dict
