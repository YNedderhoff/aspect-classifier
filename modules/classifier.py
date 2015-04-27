class classifier(object):
	def __init__(self, tag, dimensions):
		self.tag = tag
		self.dimensions = dimensions
		self.weight_vector = [0.5 for ind in range(dimensions)]



	
	def classify(self, feat_vec):
		return sum([self.weight_vector[i]*float(feat_vec[i]) for i in range(len(feat_vec))])




	def adjust_weights(self, feat_vec, prediction, step_size):
		if prediction:
			for ind in range(len(feat_vec)):
				self.weight_vector[ind] = self.weight_vector[ind] + step_size*float(feat_vec[ind])
		else:
			for ind in range(len(feat_vec)):
				self.weight_vector[ind] = self.weight_vector[ind] - step_size*float(feat_vec[ind])



