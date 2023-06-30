def get_accuracy(clusters, preds, k):
    correct_results = 0
    # num_results = len(clusters) * 1.0
    num_results = int(k) * 1.0

    i = 0
    for cluster in clusters:
        if i < int(k):
            left_id = cluster[0]
            right_id = cluster[1]
            # label = preds['label'][(preds['left_id'] == left_id) & (preds['right_id'] == right_id)]
            label = preds['label'][preds['id'] == str(left_id)+'_'+str(right_id)]
            #print(left_id, right_id, label.all())
            if label.all() == 1:
                correct_results += 1
        i += 1

    accuracy = correct_results / num_results
    # print("accuracy: ", accuracy)
    return accuracy

"""
    Version for KGs
"""
def get_accuracy_KG(clusters, candidates, k):
    print(k)
    correct_results = 0
    # num_results = len(clusters) * 1.0
    num_results = int(k) * 1.0
    i = 0
    for cluster in clusters:
        if  i < int(k):
            left_id = cluster[0]
            right_id = cluster[1]
            if left_id == right_id:
                correct_results += 1
        i += 1

    accuracy = correct_results / num_results
    return accuracy