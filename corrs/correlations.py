import pandas as pd
import statistics as st
from scipy.stats.stats import spearmanr
from scipy.stats.stats import pearsonr

RREA_df = pd.read_excel("RREA.xlsx", convert_float=True, engine='openpyxl')
metrics_df = pd.read_excel("metrics.xlsx", convert_float=True, engine='openpyxl')

hits_1 = []
hits_5 = []
hits_10 = []
for index, row in RREA_df.iterrows():
    if index == 0 or index == 3 or index == 6:
        for r in list(row):
            hits_1.append(r)
    elif index == 1 or index == 4 or index == 7:
         for r in list(row):
            hits_5.append(r)
    elif index == 2 or index == 5 or index == 8:
         for r in list(row):
            hits_10.append(r)
wcc = []
b_index = []
ccc = []
for index, row in metrics_df.iterrows():
    if index == 0 or index == 3 or index == 6:
         for r in list(row):
            wcc.append(r)
    elif index == 1 or index == 4 or index == 7:
         for r in list(row):
            b_index.append(r)
    elif index == 2 or index == 5 or index == 8:
        for r in list(row):
            ccc.append(r)
h_1_wcc = spearmanr(hits_1, wcc)
h_1_b_index = spearmanr(hits_1, b_index)
h_1_ccc = spearmanr(hits_1, ccc)
h_5_wcc = spearmanr(hits_5, wcc)
h_5_b_index = spearmanr(hits_5, b_index)
h_5_ccc = spearmanr(hits_5, ccc)
h_10_wcc = spearmanr(hits_10, wcc)
h_10_b_index = spearmanr(hits_10, b_index)
h_10_ccc = spearmanr(hits_10, ccc)
print(h_1_wcc)
print(h_1_b_index)
print(h_1_ccc)
print(h_5_wcc)
print(h_5_b_index)
print(h_5_ccc)
print(h_10_wcc)
print(h_10_b_index)
print(h_10_ccc)
corr_df = pd.DataFrame({
    "wcc": [h_1_wcc[0], h_5_wcc[0], h_10_wcc[0]],
    "b_index": [h_1_b_index[0], h_5_b_index[0], h_10_b_index[0]],
    "CCC": [h_1_ccc[0], h_5_ccc[0], h_10_ccc[0]]
}).rename(index={0: "Hits@1", 1: "Hits@5", 2: "Hits@10"}).T
print(corr_df)