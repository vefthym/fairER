import lemon
import os
import inspect

#load dataset
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

dataset = lemon.utils.datasets.deepmatcher.structured_amazon_google(root= parentdir+"/resources/DeepMatcherDatasets/")

#train
matcher = lemon.utils.matchers.MagellanMatcher()
matcher.fit(
    dataset.train.records.a,
    dataset.train.records.b,
    dataset.train.record_id_pairs,
    dataset.train.labels,
)

#evaluate
matcher.evaluate(
    dataset.test.records.a,
    dataset.test.records.b,
    dataset.test.record_id_pairs,
    dataset.test.labels,
)

#explain
exp = lemon.explain(
    dataset.records.a,
    dataset.records.b,
    dataset.test.record_id_pairs.iloc[0:1],
    matcher.predict_proba,
)
exp

#save and load explanations
#exp.save("exp.json")
#lemon.MatchingAttributionExplanation.load("exp.json")
