import numpy as np

from openea.modules.finding.alignment import greedy_alignment


def valid(mode, transl_ents, embeds1, embeds2, mapping, top_k, threads_num, metric='inner', normalize=False, csls_k=0, accurate=False):
    if mapping is None:
        _, hits1_12, mr_12, mrr_12, TTA_flag, _ = greedy_alignment(mode, embeds1, embeds2, top_k, threads_num,
                                                      metric, normalize, csls_k, accurate)
    else:
        test_embeds1_mapped = np.matmul(embeds1, mapping)
        _, hits1_12, mr_12, mrr_12, TTA_flag, _ = greedy_alignment(mode, test_embeds1_mapped, embeds2, top_k, threads_num,
                                                      metric, normalize, csls_k, accurate)
    return hits1_12, mrr_12, TTA_flag


def test(test_ent_lists, mode, embeds1, embeds2, mapping, top_k, threads_num, metric='inner', normalize=False, csls_k=0, accurate=True):
    if mapping is None:
        alignment_rest_12, hits1_12, mr_12, mrr_12, TTA_flag, update_sim_lists, all_hits  = greedy_alignment(test_ent_lists, mode, embeds1, embeds2, top_k, threads_num,
                                                                      metric, normalize, csls_k, accurate)
    else:
        test_embeds1_mapped = np.matmul(embeds1, mapping)
        alignment_rest_12, hits1_12, mr_12, mrr_12, TTA_flag, update_sim_lists, all_hits = greedy_alignment(test_ent_lists, mode, test_embeds1_mapped, embeds2, top_k, threads_num,
                                                                      metric, normalize, csls_k, accurate)

    performance = dict()
    performance["acc"] = all_hits
    performance["mr"] = mr_12
    performance["mrr"] = mrr_12
    return alignment_rest_12, hits1_12, mrr_12, TTA_flag, update_sim_lists, performance


def early_stop(flag1, flag2, flag):
    if flag <= flag2 <= flag1:
        print("\n == should early stop == \n")
        return flag2, flag, True
    else:
        return flag2, flag, False
