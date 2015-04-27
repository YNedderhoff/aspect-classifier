class Token(object):

        # initialize token from a line in file:
	def __init__(self, line):

		# splits line tab-wise, writes the values in parameters:
		entries = line.split('\t')
		if len(entries) == 2:
			self.form = entries[0].lower()
			self.gold_pos = entries[1]
			self.predicted_pos = ""
		elif len(entries) == 3:
			self.form = entries[0].lower()
			self.gold_pos = entries[1]
			self.predicted_pos = entries [2]

		elif len(entries) > 3: print "\tInput file not in expected format: Too many columns"
		else: print "\tInput file not in expected format: Not enough columns"

        # create the sparse feature vector for this token (addin only applicable features):
	def createFeatureVector(self, feat_vec, current_token, previous_token, next_token):
		self.sparse_feat_vec = []
		
		# the current token feature:
		self.sparse_feat_vec.append(feat_vec["current_form_"+current_token.form])

		# if applicable, the previous token feature:
		if previous_token:
                        self.sparse_feat_vec.append(feat_vec["prev_form_"+previous_token.form])

		# token is the first word in sentence:
		else:
                        self.sparse_feat_vec.append(feat_vec["initial_token"])

		# if applicable, the next token feature:
		if next_token:
                        self.sparse_feat_vec.append(feat_vec["next_form_"+next_token.form])

        # expand sparse feature vectors into all dimensions (by adding 0s):
	def expandFeatVec(self, dimensions):
		result = []
		for i in range(dimensions):
			if i in self.sparse_featvec:
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
