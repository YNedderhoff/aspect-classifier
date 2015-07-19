class Token(object):

    # initialize token from a line in file:
    def __init__(self, line_1, line_2):
        self.line_1 = line_1
        self.line_2 = line_2
        
        self.sparse_feat_vec = []
        self.top_x = [2, 3, 4, 5]
        self.next_token = None
        self.previous_token = None
        self.t_id_1 = -1
        self.t_id_2 = -1

        self.uppercase_1 = False
        self.uppercase_2 = False
        self.capitalized_1 = False
        self.capitalized_2 = False

        # splits line tab-wise, writes the values in parameters:
        entries = line_1.split('\t')

        if entries[0].isupper():
            self.uppercase_1 = True
        if entries[0][0].isupper():
            upper_char = False
            for char in entries[0][1:]:
                if char.isupper():
                    upper_char = True
                    break
            if not upper_char:
                self.capitalized_1 = True

        if len(entries) == 1:
            self.form_1 = entries[0].lower()
            self.original_form_1 = entries[0]
            self.gold_tag_1 = ""
            self.predicted_tag_1 = ""
        elif len(entries) == 2:
            self.form_1 = entries[0].lower()
            self.original_form_1 = entries[0]
            self.gold_tag_1 = entries[1].split("-")[0]
            self.predicted_tag_1 = ""
        elif len(entries) == 3:
            self.form_1 = entries[0].lower()
            self.original_form_1 = entries[0]
            self.gold_tag_1 = entries[1].split("-")[0]
            self.predicted_tag_1 = entries[2]

        elif len(entries) > 3:
            print "\tInput file not in expected format: Too many columns"
        else:
            print "\tInput file not in expected format: Not enough columns"
            
        # splits line tab-wise, writes the values in parameters:
        entries = line_2.split('\t')

        if entries[0].isupper():
            self.uppercase_2 = True
        if entries[0][0].isupper():
            upper_char = False
            for char in entries[0][1:]:
                if char.isupper():
                    upper_char = True
                    break
            if not upper_char:
                self.capitalized_2 = True

        if len(entries) == 1:
            self.form_2 = entries[0].lower()
            self.original_form_2 = entries[0]
            self.gold_tag_2 = ""
            self.predicted_tag_2 = ""
        elif len(entries) == 2:
            self.form_2 = entries[0].lower()
            self.original_form_2 = entries[0]
            self.gold_tag_2 = entries[1].split("-")[0]
            self.predicted_tag_2 = ""
        elif len(entries) == 3:
            self.form_2 = entries[0].lower()
            self.original_form_2 = entries[0]
            self.gold_tag_2 = entries[1].split("-")[0]
            self.predicted_tag_2 = entries[2]

        elif len(entries) > 3:
            print "\tInput file not in expected format: Too many columns"
        else:
            print "\tInput file not in expected format: Not enough columns"

    def set_adjacent_tokens(self, previous_token, next_token):

        if previous_token:
            self.previous_token = previous_token
        if next_token:
            self.next_token = next_token

    def set_sentence_index(self, t_id_1, t_id_2):
        self.t_id_1 = t_id_1
        self.t_id_2 = t_id_2

    # create the sparse feature vector for this token (addin only applicable features):
    def createFeatureVector(self, feat_vec, t_id, current_token, previous_token, next_token):

        # Uppercase

        if self.uppercase_1:
            self.sparse_feat_vec.append(feat_vec["uppercase_1"])

        if self.capitalized_1:
            self.sparse_feat_vec.append(feat_vec["capitalized_1"])
            
        if self.uppercase_2:
            self.sparse_feat_vec.append(feat_vec["uppercase_2"])

        if self.capitalized_2:
            self.sparse_feat_vec.append(feat_vec["capitalized_2"])

        # form

        # the current form:
        if "current_form_token_1_" + current_token.form_1 in feat_vec:
            self.sparse_feat_vec.append(feat_vec["current_form_token_1_" + current_token.form_1])
            
        # the current form:
        if "current_form_token_2_" + current_token.form_2 in feat_vec:
            self.sparse_feat_vec.append(feat_vec["current_form_token_2_" + current_token.form_2])

        # if applicable, the previous form:
        if previous_token:
            if "prev_form_token_1_" + previous_token.form_1 in feat_vec:
                self.sparse_feat_vec.append(feat_vec["prev_form_token_1_" + previous_token.form_1])
        
        # if applicable, the previous form:
        if "prev_form_token_2_" + current_token.form_1 in feat_vec:
            self.sparse_feat_vec.append(feat_vec["prev_form_token_2_" + current_token.form_1])

        # if applicable, the next token form:
        if "next_form_token_1_" + current_token.form_2 in feat_vec:
            self.sparse_feat_vec.append(feat_vec["next_form_token_1_" + current_token.form_2])
                
        # if applicable, the next token form:
        if next_token:
            if "next_form_token_2_" + next_token.form_2 in feat_vec:
                self.sparse_feat_vec.append(feat_vec["next_form_token_2_" + next_token.form_2])

        # form length

        # the current form length:
        if "current_word_len_token_1_" + str(len(current_token.form_1)) in feat_vec:
            self.sparse_feat_vec.append(feat_vec["current_word_len_token_1_" + str(len(current_token.form_1))])
            
        if "current_word_len_token_2_" + str(len(current_token.form_2)) in feat_vec:
            self.sparse_feat_vec.append(feat_vec["current_word_len_token_2_" + str(len(current_token.form_2))])

        # if applicable, the previous form length:
        if previous_token:
            if "prev_word_len_token_1_" + str(len(previous_token.form_1)) in feat_vec:
                self.sparse_feat_vec.append(feat_vec["prev_word_len_token_1_" + str(len(previous_token.form_1))])
                
        if "prev_word_len_token_2_" + str(len(current_token.form_1)) in feat_vec:
            self.sparse_feat_vec.append(feat_vec["prev_word_len_token_2_" + str(len(current_token.form_1))])

        # if applicable, the next token form length:
        if "next_word_len_token_1_" + str(len(current_token.form_2)) in feat_vec:
            self.sparse_feat_vec.append(feat_vec["next_word_len_token_1_" + str(len(current_token.form_2))])
            
        if next_token:
            if "next_word_len_token_2_" + str(len(next_token.form_2)) in feat_vec:
                self.sparse_feat_vec.append(feat_vec["next_word_len_token_2_" + str(len(next_token.form_2))])

        # position in sentence

        if "position_in_sentence_token_1_" + str(current_token.t_id_1) in feat_vec:
            self.sparse_feat_vec.append(feat_vec["position_in_sentence_token_1_" + str(current_token.t_id_1)])
            
        if "position_in_sentence_token_2_" + str(current_token.t_id_2) in feat_vec:
            self.sparse_feat_vec.append(feat_vec["position_in_sentence_token_2_" + str(current_token.t_id_2)])
            
        for i in self.top_x:
            if "prefix_" + current_token.form_1[:i] in feat_vec:
                self.sparse_feat_vec.append(feat_vec["prefix_token_1_" + current_token.form_1[:i]])
            if "suffix_" + current_token.form_1[-i:] in feat_vec:
                self.sparse_feat_vec.append(feat_vec["suffix_token_1_" + current_token.form_1[-i:]])

            if len(current_token.form_1) > i+1 and i > 2:

                # letter combinations in the word
                # if they don't overlap with pre- or suffixes
                for j in range(i, len(current_token.form_1)-(i*2-1)):
                    if "lettercombs_" + current_token.form_1[j:j+i] in feat_vec:
                        self.sparse_feat_vec.append(feat_vec["lettercombs_token_1_" + current_token.form_1[j:j+i]])
                        
            if "prefix_" + current_token.form_2[:i] in feat_vec:
                self.sparse_feat_vec.append(feat_vec["prefix_token_2_" + current_token.form_2[:i]])
            if "suffix_" + current_token.form_2[-i:] in feat_vec:
                self.sparse_feat_vec.append(feat_vec["suffix_token_2_" + current_token.form_2[-i:]])

            if len(current_token.form_2) > i+1 and i > 2:

                # letter combinations in the word
                # if they don't overlap with pre- or suffixes
                for j in range(i, len(current_token.form_2)-(i*2-1)):
                    if "lettercombs_" + current_token.form_2[j:j+i] in feat_vec:
                        self.sparse_feat_vec.append(feat_vec["lettercombs_token_2_" + current_token.form_2[j:j+i]])



# a generator to read a file sentence-wise and generate a Token object for each line:
def sentences(file_stream):
    # a list of Token objects of every sentence is yielded:
    sentence = []
    for line in file_stream:
        line = line.rstrip()
        if line:
            if len(sentence) == 0:
                sentence.append(Token("$START$\tX", line))
            else:
                sentence.append(Token(sentence[-1].line_2, line))
        elif sentence:
            yield sentence
            sentence = []
    if sentence:
        yield sentence
