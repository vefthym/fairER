import pandas as pd
import statistics as st
from scipy.stats.stats import spearmanr
from scipy.stats.stats import pearsonr

RREA_df = pd.read_excel("MultiKE.xlsx", convert_float=True, engine='openpyxl')
metrics_df = pd.read_excel("metrics_kg2.xlsx", convert_float=True, engine='openpyxl')

hits_1 = []
hits_5 = []
hits_10 = []
mrr = []
for index, row in RREA_df.iterrows():
    if index == 0 or index == 4 or index == 8:
        for r in list(row):
            hits_1.append(r)
    elif index == 1 or index == 5 or index == 9:
         for r in list(row):
            hits_5.append(r)
    elif index == 2 or index == 6 or index == 10:
         for r in list(row):
            hits_10.append(r)
    elif index == 3 or index == 7 or index == 11:
         for r in list(row):
            mrr.append(r)

wcc = []
deg = []
maxCS = []
for index, row in metrics_df.iterrows():
    if index == 0 or index == 3 or index == 6:
         for r in list(row):
            wcc.append(r)
    elif index == 1 or index == 4 or index == 7:
         for r in list(row):
            maxCS.append(r)
    elif index == 2 or index == 5 or index == 8:
        for r in list(row):
            deg.append(r)

h_1_wcc = spearmanr(hits_1, wcc)
h_1_deg = spearmanr(hits_1, deg)
h_1_maxCS = spearmanr(hits_1, maxCS)
h_5_wcc = spearmanr(hits_5, wcc)
h_5_deg = spearmanr(hits_5, deg)
h_5_maxCS = spearmanr(hits_5, maxCS)
h_10_wcc = spearmanr(hits_10, wcc)
h_10_deg = spearmanr(hits_10, deg)
h_10_maxCS = spearmanr(hits_10, maxCS)
mrr_wcc = spearmanr(mrr, wcc)
mrr_deg = spearmanr(mrr, deg)
mrr_maxCS = spearmanr(mrr, maxCS)
print(h_1_wcc)
print(h_1_deg)
print(h_1_maxCS)
print(h_5_wcc)
print(h_5_deg)
print(h_5_maxCS)
print(h_10_wcc)
print(h_10_deg)
print(h_10_maxCS)
print(mrr_wcc)
print(mrr_deg)
print(mrr_maxCS)
corr_df = pd.DataFrame({
    "wcc": [h_1_wcc[0], h_5_wcc[0], h_10_wcc[0], mrr_wcc[0]],
    "deg": [h_1_deg[0], h_5_deg[0], h_10_deg[0], mrr_deg[0]],
    "maxCS": [h_1_maxCS[0], h_5_maxCS[0], h_10_maxCS[0], mrr_maxCS[0]]
}).rename(index={0: "Hits@1", 1: "Hits@5", 2: "Hits@10", 3:"MRR"})
print(corr_df)