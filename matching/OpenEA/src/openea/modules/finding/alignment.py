import gc
import multiprocessing
import time

import numpy as np

from openea.modules.finding.similarity import sim
from openea.modules.utils.util import task_divide, merge_dic
from cmath import sqrt
import pickle


def greedy_alignment(kgs, test_ent_lists, mode, embed1, embed2, top_k, nums_threads, metric, normalize, csls_k, accurate):
    """
    Search alignment with greedy strategy.

    Parameters
    ----------
    embed1 : matrix_like
        An embedding matrix of size n1*d, where n1 is the number of embeddings and d is the dimension.
    embed2 : matrix_like
        An embedding matrix of size n2*d, where n2 is the number of embeddings and d is the dimension.
    top_k : list of integers
        Hits@k metrics for evaluating results.
    nums_threads : int
        The number of threads used to search alignment.
    metric : string
        The distance metric to use. It can be 'cosine', 'euclidean' or 'inner'.
    normalize : bool, true or false.
        Whether to normalize the input embeddings.
    csls_k : int
        K value for csls. If k > 0, enhance the similarity by csls.

    Returns
    -------
    alignment_rest :  list, pairs of aligned entities
    hits1 : float, hits@1 values for alignment results
    mr : float, MR values for alignment results
    mrr : float, MRR values for alignment results
    """
    t = time.time()
    TTA_flag = 0
    sim_mat = sim(embed1, embed2, metric=metric, normalize=normalize, csls_k=csls_k)
    num = sim_mat.shape[0]

    updated_sim_lists = dict()
    if nums_threads > 1:
        hits = [0] * len(top_k)
        mr, mrr = 0, 0
        alignment_rest = set()
        rests = list()
        search_tasks = task_divide(np.array(range(num)), nums_threads)
        pool = multiprocessing.Pool(processes=len(search_tasks))
        for task in search_tasks:
            mat = sim_mat[task, :]
            rests.append(pool.apply_async(calculate_rank, (kgs, test_ent_lists, mode, task, mat, top_k, accurate, num, csls_k)))
        pool.close()
        pool.join()
        for rest in rests:
            sub_mr, sub_mrr, sub_hits, sub_hits1_rest, sub_sim_lists = rest.get()
            mr += sub_mr
            mrr += sub_mrr
            hits += np.array(sub_hits)
            alignment_rest |= sub_hits1_rest
            updated_sim_lists.update(sub_sim_lists)
    else:
        mr, mrr, hits, alignment_rest, updated_sim_lists = calculate_rank(kgs, test_ent_lists, mode, list(range(num)), sim_mat, top_k, accurate, num, csls_k)
    assert len(alignment_rest) == num
    hits = np.array(hits) / num * 100
    for i in range(len(hits)):
        hits[i] = round(hits[i], 3)
    cost = time.time() - t
    if accurate:
        if csls_k > 0:
            print("accurate results with csls: csls={}, hits@{} = {}%, mr = {:.3f}, mrr = {:.6f}, time = {:.3f} s ".
                  format(csls_k, top_k, hits, mr, mrr, cost))
        else:
            print("accurate results: hits@{} = {}%, mr = {:.3f}, mrr = {:.6f}, time = {:.3f} s ".
                  format(top_k, hits, mr, mrr, cost))
            if mrr >= 0.30:
                TTA_flag = 0.30
            elif mrr >= 0.20:
                TTA_flag = 0.20
            elif mrr >= 0.10:
                TTA_flag = 0.10
    else:
        if csls_k > 0:
            print("quick results with csls: csls={}, hits@{} = {}%, time = {:.3f} s ".format(csls_k, top_k, hits, cost))
        else:
            print("quick results: hits@{} = {}%, mr = {:.3f}, mrr = {:.6f} time = {:.3f} s ".format(top_k, hits, mr, mrr, cost))
            if mrr >= 0.30:
                TTA_flag = 0.30
            elif mrr >= 0.20:
                TTA_flag = 0.20
            elif mrr >= 0.10:
                TTA_flag = 0.10
    hits1 = hits[0]
    all_hits = hits
    del sim_mat
    gc.collect()
    
    return alignment_rest, hits1, mr, mrr, TTA_flag, updated_sim_lists, all_hits


def stable_alignment(embed1, embed2, metric, normalize, csls_k, nums_threads, cut=100, sim_mat=None):
    t = time.time()
    if sim_mat is None:
        sim_mat = sim(embed1, embed2, metric=metric, normalize=normalize, csls_k=csls_k)

    kg1_candidates, kg2_candidates = dict(), dict()

    num = sim_mat.shape[0]
    x_tasks = task_divide(np.array(range(num)), nums_threads)
    pool = multiprocessing.Pool(processes=len(x_tasks))
    rests = list()
    total = 0
    for task in x_tasks:
        total += len(task)
        mat = sim_mat[task, :]
        rests.append(pool.apply_async(arg_sort, (task, mat, 'x_', 'y_')))
    assert total == num
    pool.close()
    pool.join()
    for rest in rests:
        kg1_candidates = merge_dic(kg1_candidates, rest.get())

    sim_mat = sim_mat.T
    num = sim_mat.shape[0]
    y_tasks = task_divide(np.array(range(num)), nums_threads)
    pool = multiprocessing.Pool(processes=len(y_tasks))
    rests = list()
    for task in y_tasks:
        mat = sim_mat[task, :]
        rests.append(pool.apply_async(arg_sort, (task, mat, 'y_', 'x_')))
    pool.close()
    pool.join()
    for rest in rests:
        kg2_candidates = merge_dic(kg2_candidates, rest.get())

    # print("kg1_candidates", len(kg1_candidates))
    # print("kg2_candidates", len(kg2_candidates))

    print("generating candidate lists costs time {:.3f} s ".format(time.time() - t))
    t = time.time()
    matching = galeshapley(kg1_candidates, kg2_candidates, cut)
    n = 0
    for i, j in matching.items():
        if int(i.split('_')[-1]) == int(j.split('_')[-1]):
            n += 1
    cost = time.time() - t
    print("stable alignment precision = {:.3f}%, time = {:.3f} s ".format(n / len(matching) * 100, cost))


def arg_sort(idx, sim_mat, prefix1, prefix2):
    candidates = dict()
    for i in range(len(idx)):
        x_i = prefix1 + str(idx[i])
        rank = (-sim_mat[i, :]).argsort()
        y_j = [prefix2 + str(r) for r in rank]
        candidates[x_i] = y_j
    return candidates


def calculate_rank(kgs, test_ent_lists, mode, idx, sim_mat, top_k, accurate, total_num, csls_k):
    ent_ids1_rev = dict()
    for key in kgs.ent_ids1:
        ent_ids1_rev[kgs.ent_ids1[key]] = key

    assert 1 in top_k
    mr = 0
    mrr = 0
    hits = [0] * len(top_k)
    hits1_rest = set()

    sim_lists = {}
    print("idx length")
    print(len(idx))

    for i in range(len(idx)):
        rank_sim_list = list()
        gold = idx[i]

        if accurate:
            rank = (-sim_mat[i, :]).argsort()
            temp_rank = list((-sim_mat[i, :]).argsort())

            if mode == "test" and csls_k == 0:
                if len(test_ent_lists) > 0:
                    similarities_sorted = list(np.sort((-sim_mat[i, :])))
                    # 500 for smaller sim_lists file. Otherwise, len(rank)
                    for r in range(len(rank)):
                        rank_sim_list.append((temp_rank[r], similarities_sorted[r]))
                sim_lists[(gold, ent_ids1_rev[test_ent_lists[gold]])] = rank_sim_list

        else:
            rank = np.argpartition(-sim_mat[i, :], np.array(top_k) - 1)
        hits1_rest.add((gold, rank[0]))
        assert gold in rank

        rank_index = np.where(rank == gold)[0][0]

        mr += (rank_index + 1)
        mrr += 1 / (rank_index + 1)
        for j in range(len(top_k)):
            if rank_index < top_k[j]:
                hits[j] += 1
    mr /= total_num
    mrr /= total_num
    
    return mr, mrr, hits, hits1_rest, sim_lists


def galeshapley(suitor_pref_dict, reviewer_pref_dict, max_iteration):
    """ The Gale-Shapley algorithm. This is known to provide a unique, stable
    suitor-optimal matching. The algorithm is as follows:

    (1) Assign all suitors and reviewers to be unmatched.

    (2) Take any unmatched suitor, s, and their most preferred reviewer, r.
            - If r is unmatched, match s to r.
            - Else, if r is matched, consider their current partner, r_partner.
                - If r prefers s to r_partner, unmatch r_partner from r and
                  match s to r.
                - Else, leave s unmatched and remove r from their preference
                  list.
    (3) Go to (2) until all suitors are matched, then end.

    Parameters
    ----------
    suitor_pref_dict : dict
        A dictionary with suitors as keys and their respective preference lists
        as values
    reviewer_pref_dict : dict
        A dictionary with reviewers as keys and their respective preference
        lists as values
    max_iteration : int
        An integer as the maximum iterations

    Returns
    -------
    matching : dict
        The suitor-optimal (stable) matching with suitors as keys and the
        reviewer they are matched with as values
    """
    suitors = list(suitor_pref_dict.keys())
    matching = dict()
    rev_matching = dict()

    for i in range(max_iteration):
        if len(suitors) <= 0:
            break
        for s in suitors:
            r = suitor_pref_dict[s][0]
            if r not in matching.values():
                matching[s] = r
                rev_matching[r] = s
            else:
                r_partner = rev_matching.get(r)
                if reviewer_pref_dict[r].index(s) < reviewer_pref_dict[r].index(r_partner):
                    del matching[r_partner]
                    matching[s] = r
                    rev_matching[r] = s
                else:
                    suitor_pref_dict[s].remove(r)
        suitors = list(set(suitor_pref_dict.keys()) - set(matching.keys()))
    return matching
