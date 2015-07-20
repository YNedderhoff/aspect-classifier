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
    false_predictions = 0

    TP = 0.0
    FN = 0.0
    FP = 0.0

    for sentence in tk.sentences(codecs.open(file_in, encoding='utf-8')):
        gold_targets = []
        predicted_targets = []
        
        gold_target = []
        predicted_target = []
        
        i_found_predicted = False
        i_found_gold = False
        
        for tid, token in enumerate(sentence):         
            
            if token.predicted_tag_2 == "I":
                i_found_predicted = True
                predicted_target.append(token.t_id_2)
            else:
                if len(predicted_target) > 0:
                    i_found_predicted = False
                    predicted_targets.append(predicted_target)
                    predicted_target = []
            
            if i_found_predicted:
                predicted_target.append(token.form_2)

            if token.gold_tag_2 == "I":
                i_found_gold = True
                gold_target.append(token.t_id_2)
            else:
                if len(gold_target) > 0:
                    i_found_gold = False
                    gold_targets.append(gold_target)
                    gold_target = []
            
            if i_found_gold:
                gold_target.append(token.form_2)

        for prediction in predicted_targets:
            if prediction in gold_targets:
                TP += 1.0
                del gold_targets[gold_targets.index(prediction)]
            else:
                FP += 1.0
        FN += len(gold_targets)
        """
        for tid, token in enumerate(sentence):

            prediction_count += 1

            # add POS tags to dictionary:
            if token.gold_tag_2 not in unique_tags:
                unique_tags[token.gold_tag_2] = {'TP': 0, 'FN': 0, 'FP': 0}
            if token.predicted_tag_2 not in unique_tags:
                unique_tags[token.predicted_tag_2] = {'TP': 0, 'FN': 0, 'FP': 0}

            # if the prediction was correct, TP of the gold POS is increased by 1
            # otherwise, the FN of the gold POS and FP of the predicted pos are increased by 1
            if token.gold_tag_2 == token.predicted_tag_2:
                correct_predictions += 1
                unique_tags[token.gold_tag_2]['TP'] += 1
            else:
                false_predictions += 1
                unique_tags[token.gold_tag_2]['FN'] += 1
                unique_tags[token.predicted_tag_2]['FP'] += 1

            # computes precision, recall, accuracy and f-score for each tag based on TP, FN, FP:
    for pos in unique_tags:

        TP += unique_tags[pos]['TP']
        FN += unique_tags[pos]['FN']
        FP += unique_tags[pos]['FP']

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
    """
    # computes overall values, then writes results to file:

    if TP+FP != 0:
        micro_averaged_precision = TP/(TP+FP)*100
    else:
        micro_averaged_precision = 0.0
    if TP+FN != 0:
        micro_averaged_recall = TP/(TP+FN)*100
    else:
        micro_averaged_recall = 0.0
    if micro_averaged_precision+micro_averaged_recall != 0:
        micro_averaged_f_score = (2*micro_averaged_precision*micro_averaged_recall)/(micro_averaged_precision+micro_averaged_recall)
    else:
        micro_averaged_f_score = 0.0


    t1 = time.time()
    print "\t\t" + str(t1 - t0) + " sec."

    print "\tWrite evaluation results to file"
    z0 = time.time()

    print >> out_file, "Overall Precision (mic-av):\t" + str(round(micro_averaged_precision, 2))
    print >> out_file, "Overall Recall (mic-av):\t" + str(round(micro_averaged_recall, 2))
    print >> out_file, "Overall F-Score (mic-av):\t" + str(round(micro_averaged_f_score, 2))
    print ""

    print "\t\tOverall Precision (mic-av):\t" + str(round(micro_averaged_precision, 2))
    print "\t\tOverall Recall (mic-av):\t" + str(round(micro_averaged_recall, 2))
    print "\t\tOverall F-Score (mic-av):\t" + str(round(micro_averaged_f_score, 2))
    print ""
    print "\t\tFor details see the output file."

    z1 = time.time()
    print "\t\t" + str(z1 - z0) + " sec."