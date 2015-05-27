class classifier(object):
    # initialize classifier setting all weights to 0.5:
    def __init__(self, tag, feat_vec, lmi_dict, threshold):

        self.tag = tag
        self.feat_vec = feat_vec
        self.weight_vector = [0.5 for ind in range(len(feat_vec))]
        self.lmi_dict = lmi_dict
        self.threshold = threshold
        self.binary_vector = [0 for ind in range(len(self.feat_vec))]
        self.set_binaries()

    def set_binaries(self):

        for feature in self.feat_vec:

            if self.tag in self.lmi_dict[feature] and self.lmi_dict[feature][self.tag] <= self.threshold:
                self.binary_vector[self.feat_vec[feature]] = 1

    # classify a token according to its feature vector:
    def classify(self, feat_vec):
        # return sum([self.weight_vector[i]*float(feat_vec[i]) for i in range(len(feat_vec))])
        return sum([self.weight_vector[i] for i in feat_vec])

    # adjust the weights upon incorrect prediction:
    # prediction=True  -> this classifier should have tagged the token
    #     prediction=False -> this classifier incorrectly tagged the token
    def adjust_weights(self, feat_vec, prediction, step_size):
        if prediction:
            for ind in feat_vec:
                if self.binary_vector[ind] == 1:
                    self.weight_vector[ind] += step_size * 1.0
        else:
            for ind in feat_vec:
                if self.binary_vector[ind] == 1:
                    self.weight_vector[ind] -= step_size * 1.0

    def multiply_with_binary(self):
        for ind in range(len(self.binary_vector)):
            if self.binary_vector[ind] == 0:
                self.weight_vector[ind] = 0.0