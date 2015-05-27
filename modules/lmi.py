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
            if token.gold_pos in lmi_dict["current_form_len_" + str(len(token.form))]:
                lmi_dict["current_form_len_" + str(len(token.form))][token.gold_pos] += 1
            else:
                lmi_dict["current_form_len_" + str(len(token.form))][token.gold_pos] = 1
    
            # if applicable, the previous form length:
            if token.previous_token:
                if token.gold_pos in lmi_dict["prev_form_len_" + str(len(token.previous_token.form))]:
                    lmi_dict["prev_form_len_" + str(len(token.previous_token.form))][token.gold_pos] += 1
                else:
                    lmi_dict["prev_form_len_" + str(len(token.previous_token.form))][token.gold_pos] = 1

            # if applicable, the next token form length:
            if token.next_token:
                if token.gold_pos in lmi_dict["next_form_len_" + str(len(token.next_token.form))]:
                    lmi_dict["next_form_len_" + str(len(token.next_token.form))][token.gold_pos] += 1
                else:
                    lmi_dict["next_form_len_" + str(len(token.next_token.form))][token.gold_pos] = 1
    
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


        #compute averages of lmis of groups of features
        averages = {}
        
        for feature in lmi_dict:
            if feature == "uppercase":
                if "uppercase" in averages:
                    averages["uppercase"] = [averages["uppercase"][0]+sum(lmi_dict[feature].values()), averages["uppercase"][1]+1.0]
                else:
                    averages["uppercase"] = [sum(lmi_dict[feature].values()), 1.0]   
            elif feature == "capitalized":
                if "capitalized" in averages:
                    averages["capitalized"] = [averages["capitalized"][0]+sum(lmi_dict[feature].values()), averages["capitalized"][1]+1.0]
                else:
                    averages["capitalized"] = [sum(lmi_dict[feature].values()), 1.0]
            elif "form_len" in feature:
                if "form_len" in averages:
                    averages["form_len"] = [averages["form_len"][0]+sum(lmi_dict[feature].values()), averages["form_len"][1]+1.0]
                else:
                    averages["form_len"] = [sum(lmi_dict[feature].values()), 1.0]
            elif "form_" in feature:
                if "form_" in averages:
                    averages["form_"] = [averages["form_"][0]+sum(lmi_dict[feature].values()), averages["form_"][1]+1.0]
                else:
                    averages["form_"] = [sum(lmi_dict[feature].values()), 1.0]
            elif "position_" in feature:
                if "position_" in averages:
                    averages["position_"] = [averages["position_"][0]+sum(lmi_dict[feature].values()), averages["position_"][1]+1.0]
                else:
                    averages["position_"] = [sum(lmi_dict[feature].values()), 1.0]
            elif "fix_" in feature:
                if "fix_" in averages:
                    averages["fix_"] = [averages["fix_"][0]+sum(lmi_dict[feature].values()), averages["fix_"][1]+1.0]
                else:
                    averages["fix_"] = [sum(lmi_dict[feature].values()), 1.0]
            elif "lettercombs" in feature:
                if "lettercombs" in averages:
                    averages["lettercombs"] = [averages["lettercombs"][0]+sum(lmi_dict[feature].values()), averages["lettercombs"][1]+1.0]
                else:
                    averages["lettercombs"] = [sum(lmi_dict[feature].values()), 1.0]
            else:
                print "This should not happen"
                print feature

        for average in averages:
            averages[average] = round(averages[average][0]/averages[average][1], 2)

        for average in averages:
            if average != "uppercase":
                averages[average] = averages["uppercase"]/averages[average]



        #normalize lmi values
        for feature in lmi_dict:
            if feature == "uppercase":
                pass
            elif feature == "capitalized":
                for pos_tag in lmi_dict[feature]:
                    lmi_dict[feature][pos_tag] = lmi_dict[feature][pos_tag]*averages["capitalized"]
            elif "form_len" in feature:
                for pos_tag in lmi_dict[feature]:
                    lmi_dict[feature][pos_tag] = lmi_dict[feature][pos_tag]*averages["form_len"]
            elif "form_" in feature:
                for pos_tag in lmi_dict[feature]:
                    lmi_dict[feature][pos_tag] = lmi_dict[feature][pos_tag]*averages["form_"]
            elif "position_" in feature:
                for pos_tag in lmi_dict[feature]:
                    lmi_dict[feature][pos_tag] = lmi_dict[feature][pos_tag]*averages["position_"]
            elif "fix_" in feature:
                for pos_tag in lmi_dict[feature]:
                    lmi_dict[feature][pos_tag] = lmi_dict[feature][pos_tag]*averages["fix_"]
            elif "lettercombs" in feature:
                for pos_tag in lmi_dict[feature]:
                    lmi_dict[feature][pos_tag] = lmi_dict[feature][pos_tag]*averages["lettercombs"]

            else:
                print "This should not happen"
                print feature


        temp = []
        for feature in lmi_dict:
            temp += [x for x in lmi_dict[feature].values()]
            #print lmi_dict[feature].values()[:5]
        """
        lmi_values = open("lmi.txt", "w")
        for value in sorted(temp):
            lmi_values.write(str(value)+"\n")
        lmi_values.close()
        """
        return lmi_dict
