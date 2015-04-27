class classifier(object):

        # initialize classifier setting all weights to 0.5:
	def __init__(self, dimensions):
		self.weight_vector = [0.5 for ind in range(dimensions)]

        # classify a token according to its feature vector:
	def classify(self, feat_vec):
		#return sum([self.weight_vector[i]*float(feat_vec[i]) for i in range(len(feat_vec))])
                #return sum([self.weight_vector[i] for i in feat_vec])
                for i in feat_vec:
                        print len(self.weight_vector)
                        self.weight_vector[i] = -100
                
        # adjust the weights upon incorrect prediction:
        #     prediction=True  -> this classifier should have tagged the token
        #     prediction=False -> this classifier incorrectly tagged the token
	def adjust_weights(self, feat_vec, prediction, step_size):
##		if prediction:
##			for ind in range(len(feat_vec)):
##				self.weight_vector[ind] = self.weight_vector[ind] + \
##                                                          step_size*float(feat_vec[ind])
##		else:
##			for ind in range(len(feat_vec)):
##				self.weight_vector[ind] = self.weight_vector[ind] - \
##                                                          step_size*float(feat_vec[ind])
                if prediction:
			for ind in feat_vec:
				self.weight_vector[ind] = self.weight_vector[ind] + \
                                                          step_size*1.0
		else:
			for ind in feat_vec:
				self.weight_vector[ind] = self.weight_vector[ind] - \
                                                          step_size*1.0
