class Token(object):

    # initialize token from a line in file:
    def __init__(self, line):

        self.sparse_feat_vec = []
        self.top_x = [2, 3, 4, 5]
        self.next_token = None
        self.previous_token = None
        self.t_id = -1

        self.uppercase = False
        self.capitalized = False

        # splits line tab-wise, writes the values in parameters:
        entries = line.split('\t')

        if entries[0].isupper():
            self.uppercase = True
        if entries[0][0].isupper():
            upper_char = False
            for char in entries[0][1:]:
                if char.isupper():
                    upper_char = True
                    break
            if not upper_char:
                self.capitalized = True

        if len(entries) == 1:
            self.form = entries[0].lower()
            self.original_form = entries[0]
            self.gold_pos = ""
            self.predicted_pos = ""
        elif len(entries) == 2:
            self.form = entries[0].lower()
            self.original_form = entries[0]
            self.gold_pos = entries[1]
            self.predicted_pos = ""
        elif len(entries) == 3:
            self.form = entries[0].lower()
            self.original_form = entries[0]
            self.gold_pos = entries[1]
            self.predicted_pos = entries[2]

        elif len(entries) > 3:
            print "\tInput file not in expected format: Too many columns"
        else:
            print "\tInput file not in expected format: Not enough columns"

    def set_adjacent_tokens(self, previous_token, next_token):

        if previous_token:
            self.previous_token = previous_token
        if next_token:
            self.next_token = next_token

    def set_sentence_index(self, t_id):
        self.t_id = t_id

    # create the sparse feature vector for this token (addin only applicable features):
    def createFeatureVector(self, feat_vec, t_id, current_token, previous_token, next_token):

        # Uppercase

        if self.uppercase:
            self.sparse_feat_vec.append(feat_vec["uppercase"])

        if self.capitalized:
            self.sparse_feat_vec.append(feat_vec["capitalized"])

        # form

        # the current form:
        if "current_form_" + current_token.form in feat_vec:
            self.sparse_feat_vec.append(feat_vec["current_form_" + current_token.form])

        # if applicable, the previous form:
        if previous_token:
            if "prev_form_" + previous_token.form in feat_vec:
                self.sparse_feat_vec.append(feat_vec["prev_form_" + previous_token.form])

        # if applicable, the next token form:
        if next_token:
            if "next_form_" + next_token.form in feat_vec:
                self.sparse_feat_vec.append(feat_vec["next_form_" + next_token.form])

        # form length

        # the current form length:
        if "current_word_len_" + str(len(current_token.form)) in feat_vec:
            self.sparse_feat_vec.append(feat_vec["current_word_len_" + str(len(current_token.form))])

        # if applicable, the previous form length:
        if previous_token:
            if "prev_word_len_" + str(len(previous_token.form)) in feat_vec:
                self.sparse_feat_vec.append(feat_vec["prev_word_len_" + str(len(previous_token.form))])

        # if applicable, the next token form length:
        if next_token:
            if "next_word_len_" + str(len(next_token.form)) in feat_vec:
                self.sparse_feat_vec.append(feat_vec["next_word_len_" + str(len(next_token.form))])

        # position in sentence

        if "position_in_sentence_" + str(t_id) in feat_vec:
            self.sparse_feat_vec.append(feat_vec["position_in_sentence_" + str(t_id)])
            
        for i in self.top_x:
            if "prefix_" + current_token.form[:i] in feat_vec:
                self.sparse_feat_vec.append(feat_vec["prefix_" + current_token.form[:i]])
            if "suffix_" + current_token.form[-i:] in feat_vec:
                self.sparse_feat_vec.append(feat_vec["suffix_" + current_token.form[-i:]])

            if len(current_token.form) > i+1 and i > 2:

                # letter combinations in the word
                # if they don't overlap with pre- or suffixes
                for j in range(i, len(current_token.form)-(i*2-1)):
                    if "lettercombs_" + current_token.form[j:j+i] in feat_vec:
                        self.sparse_feat_vec.append(feat_vec["lettercombs_" + current_token.form[j:j+i]])

    # expand sparse feature vectors into all dimensions (by adding 0s):
    def expandFeatVec(self, dimensions):
        result = []
        for i in range(dimensions):
            if i in self.sparse_feat_vec:
                result.append(1)
            else:
                result.append(0)
        return result


# a generator to read a file sentence-wise and generate a Token object for each line:
def sentences(file_stream):
    # a list of Token objects of every sentence is yielded:
    sentence = []
    for line in file_stream:
        line = line.rstrip()
        if line:
            sentence.append(Token(line))
        elif sentence:
            yield sentence
            sentence = []
    if sentence:
        yield sentence
