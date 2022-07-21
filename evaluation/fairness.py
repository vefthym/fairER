import util


# returns the statistical parity difference (ideal: 0, worst: 1)
def get_spd(clusters, preds, data):
    num_protected = 0
    num_results = len(clusters) * 1.0

    for cluster in clusters:
        left_id = cluster[0]
        right_id = cluster[1]
        #label = preds['label'][preds['id'] == str(left_id)+'_'+str(right_id)]
        is_protected = util.pair_is_protected(preds[preds['id'] == str(left_id)+'_'+str(right_id)].iloc[0], data)
        #print(left_id, right_id, label.all())
        if is_protected:
            num_protected += 1
    predict_protected_prob = num_protected / num_results
    predict_nonprotected_prob = 1 - predict_protected_prob

    spd = predict_nonprotected_prob - predict_protected_prob
    print('predict_protected_prob:', predict_protected_prob)
    print('predict_nonprotected_prob:', predict_nonprotected_prob)

    return spd


# returns the equality of opportunity difference (ideal: 0, worst: 1)
def get_eod(clusters, preds, data):
    num_protected_matches_correct = 0
    correct_results = 0

    for cluster in clusters:
        left_id = cluster[0]
        right_id = cluster[1]
        label = preds['label'][preds['id'] == str(left_id)+'_'+str(right_id)]
        is_protected = util.pair_is_protected(preds[preds['id'] == str(left_id)+'_'+str(right_id)].iloc[0], data)
        if label.all() == 1:
            correct_results += 1
            if is_protected:
                num_protected_matches_correct += 1

    if correct_results == 0:
        return None

    predict_protected_match_prob = num_protected_matches_correct / correct_results
    predict_nonprotected_match_prob = 1 - predict_protected_match_prob

    eod = predict_nonprotected_match_prob - predict_protected_match_prob

    print('predict_protected_match_prob:', predict_protected_match_prob)
    print('predict_nonprotected_match_prob:', predict_nonprotected_match_prob)
    return eod
