import codecs
import time
import cPickle
import gzip
import random
import os

import modules.token as tk
import modules.perceptron as perceptron
import modules.lmi as lmi

#from modules.evaluation import evaluate
from modules.affixes import find_affixes


class posTagger(object):
    def __init__(self):

        pass

    # save the model (weight vectors) to a file:
    def save(self, file_name, model):
        stream = gzip.open(file_name, "wb")
        cPickle.dump(model, stream)
        stream.close()

    # load the model (weight vectors) from a file:

    def load(self, file_name):
        stream = gzip.open(file_name, "rb")
        model = cPickle.load(stream)
        stream.close()
        return model


    def legal_prev_tags(self, tag, t_id_1):
	if tag.startswith("B"):
	    if t_id_1 != 0:
		return ["BB", "IB", "OB"]
	    else:
		return ["BB", "IB", "OB", "XB"]
	elif tag.startswith("I"):
	    return ["II", "BI"]
	elif tag.startswith("O"):
	    if t_id_1 != 0:
		return ["OO", "BO", "IO"]
	    else:
		return ["OO", "BO", "IO", "XO"]
	else:
	    return []
            

    # train the classifiers using the perceptron algorithm:
    def train(self, file_in, file_out, max_iterations, top_x, decrease_alpha, shuffle_tokens, batch_training):
        print "\tTraining file: " + file_in

        print "\tExtracting features"
        x0 = time.time()
        feat_vec = self.extractFeatures(file_in)
        x1 = time.time()
        print "\t" + str(len(feat_vec)) + " features extracted"
        print "\t\t" + str(x1 - x0) + " sec."

        print "\tCreating tokens with feature vectors"
        y0 = time.time()
        sentences = []  # save all instantiated tokens from training data, with finished feature vectors
        tag_set = set([])
        # read in sentences from file and generates the corresponding token objects:
        for sentence in tk.sentences(codecs.open(file_in, encoding='utf-8')):
            temp = []
            # create sparse feature vector representation for each token:
            for t_id, token in enumerate(sentence):
                if t_id == 0:  # first token of sentence
                    if len(sentence) > 1:
                        token.set_adjacent_tokens(None, sentence[t_id + 1])
                        token.createFeatureVector(feat_vec, t_id, sentence[t_id],
                                                  None, sentence[t_id + 1])
                    elif len(sentence) == 1:
                        token.set_adjacent_tokens(None, None)
                        token.createFeatureVector(feat_vec, t_id, sentence[t_id],
                                                  None, None)
                elif t_id == len(sentence) - 1:  # last token of sentence
                    token.set_adjacent_tokens(sentence[t_id - 1], None)
                    token.createFeatureVector(feat_vec, t_id, sentence[t_id],
                                              sentence[t_id - 1], None)
                else:
                    token.set_adjacent_tokens(sentence[t_id - 1], sentence[t_id + 1])
                    token.createFeatureVector(feat_vec, t_id, sentence[t_id],
                                              sentence[t_id - 1], sentence[t_id + 1])
                token.set_sentence_index(t_id - 1, t_id)
                temp.append(token)
                tag_set.add(token.gold_tag_1+token.gold_tag_2)
            sentences.append(temp)

        y1 = time.time()
        print "\t\t" + str(y1 - y0) + " sec."

        print "\tCreating and training classifiers"
        z0 = time.time()
        classifiers = {}

        lmi_calc = lmi.lmi([t for s in sentences for t in s], feat_vec)
        lmi_dict = lmi_calc.compute_lmi()

        # instantiate a classifier for each pos tag type:
        for tag in tag_set:
            classifiers[tag] = perceptron.classifier(tag, feat_vec, lmi_dict, top_x)

        # train the classifiers:

        alpha = 0.1  # smoothes the effect of adjustments

        # number of decreases of alpha during training
        # works only only exactly if max_iterations is divisible by alpha_decreases
        alpha_decreases = 5

        for i in range(1, max_iterations + 1):

            #batch training:
            predictions = {}
            for tag in classifiers:
                predictions[tag] = classifiers[tag].weight_vector
            print "\t\tEpoch " + str(i) + ", alpha = " + str(alpha)
            path = []
            for ind, s in enumerate(sentences):
                #if ind % (len(sentences) / 10) == 0 and not ind == 0:
                #    print "\t\t\t" + str(ind) + "/" + str(len(sentences))
                for t in s:
                    if t.t_id_1 == -1 and path:
                        # adjust classifier weights for incorrectly predicted tag and gold tag:
                        elem = sorted([(z[0],z[1]) for z in path[-1].items()], key = lambda x : x[1][0])[-1]
                        gold_tag = elem[1][-1].gold_tag_1+elem[1][-1].gold_tag_2
                        tok = elem[1][-1]
                        if elem[0] != gold_tag:
                            if batch_training:
                                predictions[gold_tag] = classifiers[gold_tag].adjust_weights(tok.sparse_feat_vec, True, alpha, predictions[gold_tag])
                                predictions[elem[0]] = classifiers[elem[0]].adjust_weights(tok.sparse_feat_vec, False, alpha, predictions[elem[0]])
                            else:
                                classifiers[gold_tag].weight_vector = classifiers[gold_tag].adjust_weights(tok.sparse_feat_vec, True, alpha, classifiers[gold_tag].weight_vector)
                                classifiers[elem[0]].weight_vector = classifiers[elem[0]].adjust_weights(tok.sparse_feat_vec, False, alpha, classifiers[elem[0]].weight_vector)
                        next_elem = elem[1][1]
                        for ind2 in range(len(path)-2, -1, -1):
                            elem = next_elem
                            gold_tag = path[ind2][elem][-1].gold_tag_1+path[ind2][elem][-1].gold_tag_2
                            tok = path[ind2][elem][-1]
                            if elem != gold_tag:
                                if batch_training:
                                    predictions[gold_tag] = classifiers[gold_tag].adjust_weights(tok.sparse_feat_vec, True, alpha, predictions[gold_tag])
                                    predictions[elem] = classifiers[elem].adjust_weights(tok.sparse_feat_vec, False, alpha, predictions[elem])
                                else:
                                    classifiers[gold_tag].weight_vector = classifiers[gold_tag].adjust_weights(tok.sparse_feat_vec, True, alpha, classifiers[gold_tag].weight_vector)
                                    classifiers[elem].weight_vector = classifiers[elem].adjust_weights(tok.sparse_feat_vec, False, alpha, classifiers[elem].weight_vector)
                            next_elem = path[ind2][elem][1]
                                
                         
                        
                        path = [{"XO" : (classifiers["XO"].classify(t.sparse_feat_vec), "", t),
                                 "XB" : (classifiers["XB"].classify(t.sparse_feat_vec), "", t)}]
                            
                    elif t.t_id_1 == -1:
                        path = [{"XO" : (classifiers["XO"].classify(t.sparse_feat_vec), "", t),
                                 "XB" : (classifiers["XB"].classify(t.sparse_feat_vec), "", t)}]
                    else:
                        temp = {}
                        for tag in [x for x in tag_set if sum([True if y in path[-1] else False for y in self.legal_prev_tags(x, t.t_id_1)]) > 0]:
                            c = classifiers[tag].classify(t.sparse_feat_vec)
                            max_arg = (0.0, "")
                            for prev_tag in self.legal_prev_tags(tag, t.t_id_1):
                                if prev_tag in path[-1]:
                                    if c*path[-1][prev_tag][0] >= max_arg[0] or max_arg[1] == "":
                                        max_arg = (c*path[-1][prev_tag][0], prev_tag, t)
                            temp[tag] = max_arg
                        path.append(temp)

            #LAST SENCENTE:
            # adjust classifier weights for incorrectly predicted tag and gold tag:
            elem = sorted([(z[0],z[1]) for z in path[-1].items()], key = lambda x : x[1][0])[-1]
            gold_tag = elem[1][-1].gold_tag_1+elem[1][-1].gold_tag_2
            tok = elem[1][-1]
            if elem[0] != gold_tag:
                if batch_training:
                    predictions[gold_tag] = classifiers[gold_tag].adjust_weights(tok.sparse_feat_vec, True, alpha, predictions[gold_tag])
                    predictions[elem[0]] = classifiers[elem[0]].adjust_weights(tok.sparse_feat_vec, False, alpha, predictions[elem[0]])
                else:
                    classifiers[gold_tag].weight_vector = classifiers[gold_tag].adjust_weights(tok.sparse_feat_vec, True, alpha, classifiers[gold_tag].weight_vector)
                    classifiers[elem[0]].weight_vector = classifiers[elem[0]].adjust_weights(tok.sparse_feat_vec, False, alpha, classifiers[elem[0]].weight_vector)
            next_elem = elem[1][1]
            for ind2 in range(len(path)-2, -1, -1):
                elem = next_elem
                gold_tag = path[ind2][elem][-1].gold_tag_1+path[ind2][elem][-1].gold_tag_2
                tok = path[ind2][elem][-1]
                if elem != gold_tag:
                    if batch_training:
                        predictions[gold_tag] = classifiers[gold_tag].adjust_weights(tok.sparse_feat_vec, True, alpha, predictions[gold_tag])
                        predictions[elem] = classifiers[elem].adjust_weights(tok.sparse_feat_vec, False, alpha, predictions[elem])
                    else:
                        classifiers[gold_tag].weight_vector = classifiers[gold_tag].adjust_weights(tok.sparse_feat_vec, True, alpha, classifiers[gold_tag].weight_vector)
                        classifiers[elem].weight_vector = classifiers[elem].adjust_weights(tok.sparse_feat_vec, False, alpha, classifiers[elem].weight_vector)
                next_elem = path[ind2][elem][1]

                
            # apply batch results to weight vectors:
            if batch_training:
                for tag in classifiers:
                    classifiers[tag].weight_vector = predictions[tag]

            # decrease alpha
            if decrease_alpha:
                if i % int(round(max_iterations ** 1.0 / float(alpha_decreases))) == 0:
                    # int(round(max_iterations ** 1/alpha_decreases)) is the number x, for which
                    # i % x == 0 is True exactly alpha_decreases times

                    alpha /= 2
            
            # shuffle tokens
            if shuffle_tokens:
                random.shuffle(sentences)

        for tag in classifiers:
            classifiers[tag].multiply_with_binary()
        # after training is completed, save classifier vectors (model) to file:
        self.save(file_out, [feat_vec, classifiers])

        z1 = time.time()
        print "\t\t" + str(z1 - z0) + " sec."

    # apply the classifiers to test data:
    def test(self, file_in, mod, file_out):

        # load classifier vectors (model) and feature vector from file:

        print "\tLoading the model and the features"
        x0 = time.time()

        model_list = self.load(mod)
        feat_vec = model_list[0]
        classifiers = model_list[1]

        x1 = time.time()
        print "\t" + str(len(feat_vec)) + " features loaded"
        print "\t\t" + str(x1 - x0) + " sec."

        print "\tTest file: " + file_in

        print "\tCreating tokens with feature vectors"
        y0 = time.time()
        sentences = []  # save all instantiated tokens from training data, with finished feature vectors
        tag_set = set()  # gather all POS types
        empty_feat_vec_count = 0

        # read in sentences from file and generates the corresponding token objects:
        for sentence in tk.sentences(codecs.open(file_in, encoding='utf-8')):
            temp = []
            # create sparse feature vector representation for each token:
            for t_id, token in enumerate(sentence):
                if t_id == 0:  # first token of sentence
                    try:
                        token.createFeatureVector(feat_vec, t_id, sentence[t_id],
                                                  None, sentence[t_id + 1])
                    except IndexError:  # happens if sentence length is 1
                        token.createFeatureVector(feat_vec, t_id, sentence[t_id],
                                                  None, None)
                elif t_id == len(sentence) - 1:  # last token of sentence
                    token.createFeatureVector(feat_vec, t_id, sentence[t_id],
                                              sentence[t_id - 1], None)
                else:
                    token.createFeatureVector(feat_vec, t_id, sentence[t_id],
                                              sentence[t_id - 1], sentence[t_id + 1])
                token.set_sentence_index(t_id - 1, t_id)
                temp.append(token)
                tag_set.add(token.gold_tag_1+token.gold_tag_2)
                if len(token.sparse_feat_vec) == 0:
                    empty_feat_vec_count += 1
            sentences.append(temp)

        print "\t\t" + str(empty_feat_vec_count) + " tokens have no features of the feature set"
        y1 = time.time()
        print "\t\t" + str(y1 - y0) + " sec."

        print "\tClassifying tokens"
        z0 = time.time()
        output = open(file_out, "w")  # temporarily save classification to file for evaluation
        path = []
        for ind, s in enumerate(sentences):
            #if ind % (len(sentences) / 10) == 0 and not ind == 0:
            #    print "\t\t\t" + str(ind) + "/" + str(len(sentences))
            for t in s:
                if t.t_id_1 == -1 and path:
                    sequence = []
                    # adjust classifier weights for incorrectly predicted tag and gold tag:
                    elem = sorted([(z[0],z[1]) for z in path[-1].items()], key = lambda x : x[1][0])[-1]
                    gold_tag = elem[1][-1].gold_tag_1+elem[1][-1].gold_tag_2
                    tok = elem[1][-1]
                    sequence.append((tok, gold_tag, elem[0]))
                    next_elem = elem[1][1]
                    for ind2 in range(len(path)-2, -1, -1):
                        elem = next_elem
                        gold_tag = path[ind2][elem][-1].gold_tag_1+path[ind2][elem][-1].gold_tag_2
                        tok = path[ind2][elem][-1]
                        sequence.append((tok, gold_tag, elem))
                        next_elem = path[ind2][elem][1]
                            
                    for x in range(len(sequence)-1,-1,-1):
                        print >> output, sequence[x][0].original_form_2.encode("utf-8") + "\t" + sequence[x][0].gold_tag_2.encode("utf-8") + \
                                 "\t" + sequence[x][2][1].encode("utf-8")
                    print >> output, ""
                    
                    path = [{"XO" : (classifiers["XO"].classify(t.sparse_feat_vec), "", t),
                             "XB" : (classifiers["XB"].classify(t.sparse_feat_vec), "", t)}]
                        
                elif t.t_id_1 == -1:
                    path = [{"XO" : (classifiers["XO"].classify(t.sparse_feat_vec), "", t),
                             "XB" : (classifiers["XB"].classify(t.sparse_feat_vec), "", t)}]
                else:
                    temp = {}
                    for tag in [x for x in tag_set if sum([True if y in path[-1] else False for y in self.legal_prev_tags(x, t.t_id_1)]) > 0]:
                        c = classifiers[tag].classify(t.sparse_feat_vec)
                        max_arg = (0.0, "")
                        for prev_tag in self.legal_prev_tags(tag, t.t_id_1):
                            if prev_tag in path[-1]:
                                if c*path[-1][prev_tag][0] >= max_arg[0]:
                                    max_arg = (c*path[-1][prev_tag][0], prev_tag, t)
                        temp[tag] = max_arg
                    path.append(temp)
        sequence = []
        # adjust classifier weights for incorrectly predicted tag and gold tag:
        elem = sorted([(z[0],z[1]) for z in path[-1].items()], key = lambda x : x[1][0])[-1]
        gold_tag = elem[1][-1].gold_tag_1+elem[1][-1].gold_tag_2
        tok = elem[1][-1]
        sequence.append((tok, gold_tag, elem[0]))
        next_elem = elem[1][1]
        for ind2 in range(len(path)-2, -1, -1):
            elem = next_elem
            gold_tag = path[ind2][elem][-1].gold_tag_1+path[ind2][elem][-1].gold_tag_2
            tok = path[ind2][elem][-1]
            sequence.append((tok, gold_tag, elem))
            next_elem = path[ind2][elem][1]
                
        for x in range(len(sequence)-1,-1,-1):
            print >> output, sequence[x][0].original_form_2.encode("utf-8") + "\t" + sequence[x][0].gold_tag_2.encode("utf-8") + \
                     "\t" + sequence[x][2][1].encode("utf-8")
        print >> output, ""
        output.close()

        z1 = time.time()
        print "\t\t" + str(z1 - z0) + " sec."

    def tag(self, file_in, mod, file_out):

        # load classifier vectors (model) and feature vector from file:

        print "\tLoading the model and the features"
        x0 = time.time()

        model_list = self.load(mod)
        feat_vec = model_list[0]
        classifiers = model_list[1]

        x1 = time.time()
        print "\t" + str(len(feat_vec)) + " features loaded"
        print "\t\t" + str(x1 - x0) + " sec."

        print "\tTag file: " + file_in

        print "\tCreating tokens with feature vectors"
        y0 = time.time()
        tokens = []  # save all instantiated tokens from training data, with finished feature vectors
        tag_set = set()  # gather all POS types
        empty_feat_vec_count = 0

        # read in sentences from file and generates the corresponding token objects:
        for sentence in tk.sentences(codecs.open(file_in, encoding='utf-8')):

            # create sparse feature vector representation for each token:
            for t_id, token in enumerate(sentence):
                if t_id == 0:  # first token of sentence
                    try:
                        token.createFeatureVector(feat_vec, t_id, sentence[t_id],
                                                  None, sentence[t_id + 1])
                    except IndexError:  # happens if sentence length is 1
                        token.createFeatureVector(feat_vec, t_id, sentence[t_id],
                                                  None, None)
                elif t_id == len(sentence) - 1:  # last token of sentence
                    token.createFeatureVector(feat_vec, t_id, sentence[t_id],
                                              sentence[t_id - 1], None)
                else:
                    token.createFeatureVector(feat_vec, t_id, sentence[t_id],
                                              sentence[t_id - 1], sentence[t_id + 1])
                tokens.append(token)
                tag_set.add(token.gold_pos)
                if len(token.sparse_feat_vec) == 0:
                    empty_feat_vec_count += 1
            tokens.append("_SENTENCE_DELIMITER_")

        print "\t\t" + str(empty_feat_vec_count) + " tokens have no features of the feature set"
        y1 = time.time()
        print "\t\t" + str(y1 - y0) + " sec."

        print "\tClassifying tokens"
        z0 = time.time()
        output = open(file_out, "w")  # temporarily save classification to file for evaluation
        for ind, t in enumerate(tokens):
            if t == "_SENTENCE_DELIMITER_":
                print >> output, ""
            else:
                if ind % (len(tokens) / 10) == 0 and not ind == 0:
                    print "\t\t" + str(ind) + "/" + str(len(tokens))

                # expand sparse token feature vectors into all dimensions:
                # expanded_feat_vec = t.expandFeatVec(len(feat_vec))

                arg_max = ["", 0.0]
                for tag in classifiers:
                    # temp = classifiers[tag].classify(expanded_feat_vec)
                    temp = classifiers[tag].classify(t.sparse_feat_vec)

                    # remember highest classification result:
                    if temp > arg_max[1]:
                        arg_max[0] = tag
                        arg_max[1] = temp

                # set predicted POS tag:
                t.predicted_pos = arg_max[0]

                # print token with predicted POS tag to file:
                print >> output, t.original_form.encode("utf-8") + "\t" + t.predicted_pos.encode("utf-8")
        output.close()

        z1 = time.time()
        print "\t\t" + str(z1 - z0) + " sec."

    # build mapping of features to vector dimensions (key=feature, value=dimension index):
    def extractFeatures(self, file_in):

        feat_vec = {}

        affixes = find_affixes(file_in, 5)

        # uppercase
        feat_vec["uppercase_1"] = len(feat_vec)
        feat_vec["uppercase_2"] = len(feat_vec)

        # capitalized
        feat_vec["capitalized_1"] = len(feat_vec)
        feat_vec["capitalized_2"] = len(feat_vec)

        for l in affixes:
            for affix_length in l:
                for affix in l[affix_length]:
                    if sum(l[affix_length][affix].values()) > 0:
                        if affixes.index(l) == 0:
                            feat_vec["suffix_token_1_" + affix] = len(feat_vec)
                            feat_vec["suffix_token_2_" + affix] = len(feat_vec)
                        elif affixes.index(l) == 1:
                            feat_vec["prefix_token_1_" + affix] = len(feat_vec)
                            feat_vec["prefix_token_2_" + affix] = len(feat_vec)
                        else:
                            feat_vec["lettercombs_token_1_" + affix] = len(feat_vec)
                            feat_vec["lettercombs_token_2_" + affix] = len(feat_vec)

        # iterate over all tokens to extract features:

        for sentence in tk.sentences(codecs.open(file_in, encoding='utf-8')):
            for tid, token in enumerate(sentence):
                
                # form:
                if not "current_form_token_1_" + token.form_1 in feat_vec:
                    feat_vec["current_form_token_1_" + token.form_1] = len(feat_vec)
                if not "current_form_token_2_" + token.form_2 in feat_vec:
                    feat_vec["current_form_token_2_" + token.form_2] = len(feat_vec)

                if not "prev_form_token_2_" + token.form_1 in feat_vec:
                    feat_vec["prev_form_token_2_" + token.form_1] = len(feat_vec)
                if tid > 0:
                    if not "prev_form_token_1_" + sentence[tid-1].form_1 in feat_vec:
                        feat_vec["prev_form_token_1_" + sentence[tid-1].form_1] = len(feat_vec)

                if not "next_form_token_1_" + token.form_2 in feat_vec:
                    feat_vec["next_form_token_1_" + token.form_2] = len(feat_vec)                    
                if tid < len(sentence)-1:
                    if not "next_form_token_2_" + sentence[tid+1].form_2 in feat_vec:
                        feat_vec["next_form_token_2_" + sentence[tid+1].form_2] = len(feat_vec)
                

                # form length
                if not "current_word_len_token_1_" + str(len(token.form_1)) in feat_vec:
                    feat_vec["current_word_len_token_1_" + str(len(token.form_1))] = len(feat_vec)
                if not "current_word_len_token_2_" + str(len(token.form_2)) in feat_vec:
                    feat_vec["current_word_len_token_2_" + str(len(token.form_2))] = len(feat_vec)

                if not "prev_word_len_token_2_" + str(len(token.form_1)) in feat_vec:
                    feat_vec["prev_word_len_token_2_" + str(len(token.form_1))] = len(feat_vec)
                if tid > 0:
                    if not "prev_word_len_token_1_" + str(len(sentence[tid-1].form_1)) in feat_vec:
                        feat_vec["prev_word_len_token_1_" + str(len(sentence[tid-1].form_1))] = len(feat_vec)

                if not "next_word_len_token_1_" + str(len(token.form_2)) in feat_vec:
                    feat_vec["next_word_len_token_1_" + str(len(token.form_2))] = len(feat_vec)
                if tid < len(sentence)-1:
                    if not "next_word_len_token_2_" + str(len(sentence[tid+1].form_2)) in feat_vec:
                        feat_vec["next_word_len_token_2_" + str(len(sentence[tid+1].form_2))] = len(feat_vec)

                # position in sentence
                if not "position_in_sentence_token_1_" + str(tid-1) in feat_vec:
                    feat_vec["position_in_sentence_token_1_" + str(tid-1)] = len(feat_vec)
                if not "position_in_sentence_token_2_" + str(tid) in feat_vec:
                    feat_vec["position_in_sentence_token_2_" + str(tid)] = len(feat_vec)

        return feat_vec


if __name__ == '__main__':

    t0 = time.time()

    import argparse

    argpar = argparse.ArgumentParser(description='')

    mode = argpar.add_mutually_exclusive_group(required=True)
    mode.add_argument('-train', dest='train', action='store_true', help='run in training mode')
    mode.add_argument('-test', dest='test', action='store_true', help='run in test mode')
    mode.add_argument('-ev', dest='evaluate', action='store_true', help='run in evaluation mode')
    mode.add_argument('-tag', dest='tag', action='store_true', help='run in tagging mode')

    argpar.add_argument('-i', '--infile', dest='in_file', help='in file', required=True)
    argpar.add_argument('-e', '--epochs', dest='epochs', help='epochs', default='1')
    argpar.add_argument('-m', '--model', dest='model', help='model', default='model')
    argpar.add_argument('-o', '--output', dest='output_file', help='output file', default='output.txt')
    argpar.add_argument('-t1', '--topxform', dest='top_x_form', help='top x form', default=None)
    argpar.add_argument('-t2', '--topxwordlen', dest='top_x_word_len', help='top x word len', default=None)
    argpar.add_argument('-t3', '--topxposition', dest='top_x_position', help='top x position', default=None)
    argpar.add_argument('-t4', '--topxprefix', dest='top_x_prefix', help='top x prefix', default=None)
    argpar.add_argument('-t5', '--topxsuffix', dest='top_x_suffix', help='top x suffix', default=None)
    argpar.add_argument('-t6', '--topxlettercombs', dest='top_x_lettercombs', help='top x letter combs', default=None)
    argpar.add_argument('-decrease-alpha', dest='decrease_alpha', action='store_true', help='decrease alpha', default=False)
    argpar.add_argument('-shuffle-tokens', dest='shuffle_tokens', action='store_true', help='shuffle tokens', default=False)
    argpar.add_argument('-batch-training', dest='batch_training', action='store_true', help='batch training', default=False)

    args = argpar.parse_args()


    t = posTagger()
    if os.stat(args.in_file).st_size == 0:
        print "Input file is empty"
    else:
        if args.train:
            print "Running in training mode\n"
            if not args.top_x_form:
                print args.top_x_form
            top_x = [args.top_x_form, args.top_x_word_len, args.top_x_position, args.top_x_prefix, args.top_x_suffix, args.top_x_lettercombs]
            t.train(args.in_file, args.model, int(args.epochs), top_x, args.decrease_alpha, args.shuffle_tokens, args.batch_training)

        elif args.test:
            print "Running in test mode\n"
            t.test(args.in_file, args.model, args.output_file)
        elif args.evaluate:
            print "Running in evaluation mode\n"
            out_stream = open(args.output_file, 'w')
            evaluate(args.in_file, out_stream)
            out_stream.close()
        elif args.tag:
            print "Running in tag mode\n"
            t.tag(args.in_file, args.model, args.output_file)
    t1 = time.time()
    print "\n\tDone. Total time: " + str(t1 - t0) + "sec.\n"
