class classifier(object):
    # initialize classifier setting all weights to 0.5:
    def __init__(self, tag, feat_vec, lmi_dict, top_x):

        self.tag = tag
        self.top_x = top_x
        self.lmi_dict = lmi_dict
        self.feat_vec = feat_vec
        self.weight_vector = [0.0 for ind in range(len(feat_vec))]
        self.binary_vector = [1 for ind in range(len(feat_vec))]
        # self.set_binaries()

    def set_binaries(self):
        feature_groups = ["form_", "word_len_", "position_", "prefix_", "suffix_", "lettercombs_"]
        for ind in range(len(self.top_x)):
            if self.top_x[ind] is not None:
                temp = sorted([(x, self.lmi_dict[x][self.tag]) for x in self.feat_vec if self.tag in self.lmi_dict[x] and feature_groups[ind] in x],
                              key = lambda x: x[1], reverse = True)[:int(self.top_x[ind])]
                for elem in temp:
                    self.binary_vector[self.feat_vec[elem[0]]] = 1
            else:
                for feature in self.feat_vec:
                    if feature_groups[ind] in feature:
                        self.binary_vector[self.feat_vec[feature]] = 1
        
    # classify a token according to its feature vector:
    def classify(self, feat_vec):
        # return sum([self.weight_vector[i]*float(feat_vec[i]) for i in range(len(feat_vec))])
        return sum([self.weight_vector[i] for i in feat_vec])

    # adjust the weights upon incorrect prediction:
    # prediction=True  -> this classifier should have tagged the token
    #     prediction=False -> this classifier incorrectly tagged the token
    def adjust_weights(self, feat_vec, prediction, step_size, temp_weight_vector):
        if prediction:
            for ind in feat_vec:
                if self.binary_vector[ind] == 1:
                    temp_weight_vector[ind] += step_size * 1.0
        else:
            for ind in feat_vec:
                if self.binary_vector[ind] == 1:
                    temp_weight_vector[ind] -= step_size * 1.0
        
        return temp_weight_vector

    def multiply_with_binary(self):
        for ind in range(len(self.binary_vector)):
            if self.binary_vector[ind] == 0:
                self.weight_vector[ind] = 0.0
