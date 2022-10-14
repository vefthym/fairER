def get_accuracy(clusters, preds):
    correct_results = 0
    num_results = len(clusters) * 1.0

    for cluster in clusters:
        left_id = cluster[0]
        right_id = cluster[1]
        # label = preds['label'][(preds['left_id'] == left_id) & (preds['right_id'] == right_id)]
        label = preds['label'][preds['id'] == str(left_id)+'_'+str(right_id)]
        #print(left_id, right_id, label.all())
        if label.all() == 1:
            correct_results += 1

    accuracy = correct_results / num_results
    # print("accuracy: ", accuracy)
    return accuracy

"""
    Version for KGs
"""
def get_accuracy_KG(clusters, candidates):
    correct_results = 0
    num_results = len(clusters) * 1.0

    for cluster in clusters:

        left_id = cluster[0]
        right_id = cluster[1]
        if left_id == right_id:
            correct_results += 1

    accuracy = correct_results / num_results
    return accuracy