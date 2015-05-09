import time
import codecs
import token as tk


def evaluate(file_in, out_file):

    t0 = time.time()

    print "\tEvaluate predictions"

    pos_dict = {}
    counter = 0

    prediction_count = 0

    # unique_tags will contain every existing POS tag as key, whether it exists
    # only in gold, predicted, or both. The value is the dict {'TP':0,'FN':0,'FP':0}
    unique_tags = {}

    unique_tags_scores = {}
    correct_predictions = 0

    for sentence in tk.sentences(codecs.open(file_in, encoding='utf-8')):
        for tid, token in enumerate(sentence):

            prediction_count += 1

            # add POS tags to dictionary:
            if token.gold_pos not in unique_tags:
                unique_tags[token.gold_pos] = {'TP': 0, 'FN': 0, 'FP': 0}
            if token.predicted_pos not in unique_tags:
                unique_tags[token.predicted_pos] = {'TP': 0, 'FN': 0, 'FP': 0}

            # if the prediction was correct, TP of the gold POS is increased by 1
            # otherwise, the FN of the gold POS and FP of the predicted pos are increased by 1
            if token.gold_pos == token.predicted_pos:
                correct_predictions += 1
                unique_tags[token.gold_pos]['TP'] += 1
            else:
                unique_tags[token.gold_pos]['FN'] += 1
                unique_tags[token.predicted_pos]['FP'] += 1

            # computes precision, recall, accuracy and f-score for each tag based on TP, FN, FP:
    for pos in unique_tags:
        unique_tags_scores[pos] = {'Precision': 0.00, 'Recall': 0.00, 'Accuracy': 0.00, 'F-Score': 0.00}

        if unique_tags[pos]['TP'] + unique_tags[pos]['FP'] == 0:
            unique_tags_scores[pos]['precision'] = 0.00
        else:
            unique_tags_scores[pos]['precision'] = (float(unique_tags[pos]['TP'])) / (float(unique_tags[pos]['TP']) + \
                                                                                      float(unique_tags[pos][
                                                                                          'FP'])) * 100.00

        if unique_tags[pos]['TP'] + unique_tags[pos]['FN'] == 0:
            unique_tags_scores[pos]['recall'] = 0.00
        else:
            unique_tags_scores[pos]['recall'] = (float(unique_tags[pos]['TP'])) / (float(unique_tags[pos]['TP']) + \
                                                                                   float(
                                                                                       unique_tags[pos]['FN'])) * 100.00

        if unique_tags[pos]['TP'] + unique_tags[pos]['FP'] + unique_tags[pos]['FN'] == 0:
            unique_tags_scores[pos]['accuracy'] = 0.00
        else:
            unique_tags_scores[pos]['accuracy'] = float(unique_tags[pos]['TP']) / (float(unique_tags[pos]['TP']) + \
                                                                                   float(unique_tags[pos]['FN']) + \
                                                                                   float(
                                                                                       unique_tags[pos]['FP'])) * 100.00

        if unique_tags_scores[pos]['precision'] + unique_tags_scores[pos]['recall'] == 0.00:
            unique_tags_scores[pos]['f-score'] = 0.00
        else:
            unique_tags_scores[pos]['f-score'] = (2 * float(unique_tags_scores[pos]['precision']) * \
                                                  float(unique_tags_scores[pos]['recall'])) / \
                                                 (float(unique_tags_scores[pos]['precision']) + \
                                                  float(unique_tags_scores[pos]['recall']))

    # computes overall values, then writes results to file:

    precision_sum = 0.0
    recall_sum = 0.0
    f_score_sum = 0.0

    false_tags = prediction_count - correct_predictions

    for pos in unique_tags_scores:
        precision_sum += unique_tags_scores[pos]['precision']
        recall_sum += unique_tags_scores[pos]['recall']
        f_score_sum += unique_tags_scores[pos]['f-score']

    overall_precision = precision_sum / float(len(unique_tags_scores))
    overall_recall = recall_sum / float(len(unique_tags_scores))
    overall_f_score = f_score_sum / float(len(unique_tags_scores))

    overall_accuracy = (float(correct_predictions) / float(prediction_count)) * 100

    t1 = time.time()
    print "\t\t" + str(t1 - t0) + " sec."

    print "\tWrite evaluation results to file"
    z0 = time.time()

    print >> out_file, "Total Predictions:\t" + str(prediction_count)
    print >> out_file, "Correct Predictions:\t" + str(correct_predictions)
    print >> out_file, "False Predictions:\t" + str(false_tags)
    print >> out_file, ""
    print >> out_file, "Overall Accuracy:\t" + str(round(overall_accuracy, 2))
    print >> out_file, "Overall Precision:\t" + str(round(overall_precision, 2))
    print >> out_file, "Overall Recall:\t" + str(round(overall_recall, 2))
    print >> out_file, "Overall F-Score:\t" + str(round(overall_f_score, 2))
    print >> out_file, ""

    print >> out_file, "Tagwise Accuracy, Precision, Recall and F-Score:\n"
    for pos in unique_tags_scores.keys():
        print >> out_file, pos + "\tAccuracy: " + str(round(unique_tags_scores[pos]['accuracy'], 2)) + "\tPrecision: " + \
                           str(round(unique_tags_scores[pos]['precision'], 2)) + "\tRecall: " + \
                           str(round(unique_tags_scores[pos]['recall'], 2)) + "\tF-Score: " + \
                           str(round(unique_tags_scores[pos]['f-score'], 2))

    z1 = time.time()
    print "\t\t" + str(z1 - z0) + " sec."