import requests
import bs4
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np

df = pd.read_csv("Data/Grey Anatomy.csv", index_col=0)
print(df)
# -------------------------------- PLOT HEATMAP ------------------------------
color_map = 'RdPu'
title = 'Greys Anatomy - Rate IMDb'
# sns.heatmap(df, annot=False, cmap=color_map, annot_kws={"size":8}, linewidths=.5)
# plt.title(title, fontsize=15)
# plt.show()

# ---------------------------------- PLOT histogram -------------------------

season=df.iloc[[4]]
print(season)
season_t = season.T
season_t['C'] = np.arange(len(season_t))
season_t['death'] = '0'
season_t.iloc[23,2]='1'
season_t.set_index('C', inplace=True)
season_t.dropna(subset = ["Season_5"], inplace=True)
fig = px.bar(season_t,
             x=np.arange(len(season_t)),
             y='Season_5',
             color = 'death')


fig.show()
# y1=pd.Series(season1.iloc[[0]])
# print(y1)
# hist = df.hist()
# plt.show()