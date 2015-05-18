class lmi(object):
    
    def __init__(self, tokens, feat_vec):
        self.tokens = tokens
        self.feat_vec = feat_vec
        
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

            if token.form.isupper():
                if token.gold_pos in lmi_dict["uppercase"]:
                    lmi_dict["uppercase"][token.gold_pos] += 1
                else:
                    lmi_dict["uppercase"][token.gold_pos] = 1
    
    
            if token.form[0].isupper():
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

            #BIS HIER

            # form length
    
            # the current form length:
            if "current_form_len_" + str(len(token.form)) in feat_vec:
                self.sparse_feat_vec.append(feat_vec["current_form_len_" + str(len(token.form))])
    
            # if applicable, the previous form length:
            if previous_token:
                if "previous_form_len_" + str(len(previous_token.form)) in feat_vec:
                    self.sparse_feat_vec.append(feat_vec["previous_form_len_" + str(len(previous_token.form))])
    
            # if applicable, the next token form length:
            if next_token:
                if "next_form_len_" + str(len(next_token.form)) in feat_vec:
                    self.sparse_feat_vec.append(feat_vec["next_form_len_" + str(len(next_token.form))])
    
            # position in sentence
    
            if "position_in_sentence_" + str(t_id) in feat_vec:
                self.sparse_feat_vec.append(feat_vec["position_in_sentence_" + str(t_id)])
                
            for i in self.top_x:
                if "prefix_" + token.form[:i] in feat_vec:
                    self.sparse_feat_vec.append(feat_vec["prefix_" + token.form[:i]])
                if "suffix_" + token.form[-i:] in feat_vec:
                    self.sparse_feat_vec.append(feat_vec["suffix_" + token.form[-i:]])
    
                if len(token.form) > i+1 and i > 2:
    
                    # letter combinations in the word
                    # if they don't overlap with pre- or suffixes
                    for j in range(i, len(token.form)-(i*2-1)):
                        if "lettercombs_" + token.form[j:j+i] in feat_vec:
                            self.sparse_feat_vec.append(feat_vec["lettercombs_" + token.form[j:j+i]])
