
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
	def createFeatureVector(self, feat_vec, t_id, current_token, previous_token, next_token):
		self.sparse_feat_vec = []

		### CAPS
		
		if current_token.form.isupper():
			self.sparse_feat_vec.append(feat_vec["CAPS"])
		
		### form
 
		# the current form:
		if "current_form_"+current_token.form in feat_vec:
			self.sparse_feat_vec.append(feat_vec["current_form_"+current_token.form])

		# if applicable, the previous form:
		if previous_token:
			if "previous_form_"+previous_token.form in feat_vec:
                        	self.sparse_feat_vec.append(feat_vec["prev_form_"+previous_token.form])

		# if applicable, the next token form:
		if next_token:
			if "next_form_"+next_token.form in feat_vec:
                        	self.sparse_feat_vec.append(feat_vec["next_form_"+next_token.form])


		### form length

		# the current form length:
		if "current_form_len_"+str(len(current_token.form)) in feat_vec:
			self.sparse_feat_vec.append(feat_vec["current_form_len_"+str(len(current_token.form))])

		# if applicable, the previous form length:
		if previous_token:
			if "previous_form_len_"+str(len(previous_token.form)) in feat_vec:
                        	self.sparse_feat_vec.append(feat_vec["previous_form_len_"+str(len(previous_token.form))])

		# if applicable, the next token form length:
		if next_token:
			if "next_form_len_"+str(len(next_token.form)) in feat_vec:
                        	self.sparse_feat_vec.append(feat_vec["next_form_len_"+str(len(next_token.form))])

		
		### position in sentence

		if "position_in_sentence_"+str(t_id) in feat_vec:
			self.sparse_feat_vec.append(feat_vec["position_in_sentence_"+str(t_id)])
		### suffixes

		# length 2

		if "suffix_"+current_token.form[-2:] in feat_vec:
			self.sparse_feat_vec.append(feat_vec["suffix_"+current_token.form[-2:]])

		# length 3

		if "suffix_"+current_token.form[-3:] in feat_vec:
			self.sparse_feat_vec.append(feat_vec["suffix_"+current_token.form[-3:]])

		# length 4

		if "suffix_"+current_token.form[-4:] in feat_vec:
			self.sparse_feat_vec.append(feat_vec["suffix_"+current_token.form[-4:]])

		# length 5

		if "suffix_"+current_token.form[-5:] in feat_vec:
			self.sparse_feat_vec.append(feat_vec["suffix_"+current_token.form[-5:]])

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
