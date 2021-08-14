import fairsearchcore as fsc
from fairsearchcore.models import FairScoreDoc


def pre_process_fair(k=10, p=0.25, alpha=0.1):
    # create the Fair object
    fair = fsc.Fair(k, p, alpha)

    # create an mtable using alpha adjusted
    mtable = fair.create_adjusted_mtable()
    # print("Number of required protected results by rank to satisfy fairness:", mtable)

    fair.adjust_alpha()

    return fair


if __name__ == '__main__':
    k = 10  # number of topK elements returned (value should be between 10 and 400)
    p = 0.25  # proportion of protected candidates in the topK elements (value should be between 0.02 and 0.98)
    alpha = 0.1  # significance level (value should be between 0.01 and 0.15)

    # create the Fair object
    fair = fsc.Fair(k, p, alpha)

    # create an mtable using alpha unadjusted
    #mtable = fair.create_unadjusted_mtable()

    # analytically calculate the fail probability
    # analytical = fair.compute_fail_probability(mtable)

    # create an mtable using alpha adjusted
    mtable = fair.create_adjusted_mtable()
    print(mtable)

    # again, analytically calculate the fail probability
    # analytical = fair.compute_fail_probability(mtable)

    #M = 1000  # number of rankings you want to generate (works better with big numbers)

    # generate rankings using the simulator (M lists of k objects of class fairsearchcore.models.FairScoreDoc)
   # rankings = fsc.generate_rankings(M, k, p)

    # experimentally calculate the fail probability
    # experimental = fsc.compute_fail_probability(rankings, mtable)

    # get alpha adjusted (used to create an adjusted mtable)
    #alpha_adjusted = fair.adjust_alpha()

    # let's manually create an unfair ranking (False -> unprotected, True -> protected)
    # in this example the first document (docid=20) has a score of 20, the last document (docid=1) a score of 1
    unfair_ranking = [FairScoreDoc(20, 20, False), FairScoreDoc(19, 19, False), FairScoreDoc(18, 18, False),
                      FairScoreDoc(17, 17, False), FairScoreDoc(16, 16, False), FairScoreDoc(15, 15, False),
                      FairScoreDoc(14, 14, False), FairScoreDoc(13, 13, False), FairScoreDoc(12, 12, False),
                      FairScoreDoc(11, 11, False), FairScoreDoc(10, 10, False), FairScoreDoc(9, 9, False),
                      FairScoreDoc(8, 8, False), FairScoreDoc(7, 7, False), FairScoreDoc(6, 6, True),
                      FairScoreDoc(5, 5, True), FairScoreDoc(4, 4, True), FairScoreDoc(3, 3, True),
                      FairScoreDoc(2, 2, True), FairScoreDoc(1, 1, True)]
    [print(d.is_protected, end=',') for d in unfair_ranking]
    print()

    # let's check the ranking is considered fair
    print('Fair ranking' if fair.is_fair(unfair_ranking[:k]) else 'Unfair ranking')

    # now re-rank the unfair ranking
    re_ranked = fair.re_rank(unfair_ranking)
    [print(d.is_protected, end=',') for d in re_ranked]
    print()

    # now let's see if the new ranking is fair
    print('Fair ranking' if fair.is_fair(re_ranked) else 'Unfair ranking')
