import requests
import bs4
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np

df = pd.read_excel('Data/GameofThrones.xlsx')
deaths = pd.read_excel('Data/got_deaths.xlsx')
df.rename(columns={"US viewers (million)": "views", "Imdb Rating": "Rating", 'Notable Death Count':'Death_Count'}, inplace=True)
df.drop(['IMDB votes','Runtime (mins)','Episode Number','IMDB Description','Writer','Director', 'Episode Name' ,'Original Air Date' ], axis=1, inplace=True)

# ------------------------------------ Heat Map -----------------------------------
# color_map = 'RdPu'
# title = 'Game of Thrones - Rate IMDb'
# df1=pd.read_csv("Data/Heatmap_GOT.csv", index_col=0)
# sns.heatmap(df1, annot=True, cmap=color_map, annot_kws={"size":8}, linewidths=.5)
# plt.title(title, fontsize=15)
# plt.show()

# --------------------------- Views per season bar plot ------------------------------

# views =df.groupby(['Season']).mean().reset_index()
# fig = px.bar(views,
#              x='Season',
#              y= 'views',
#              color='Season',
#              title = "Views (in millions) per season")
# fig.show()


# ------------------------------- Dataset Re-formatting -----------------------------
df["episode"] = df["Season"].astype(str) + ","+df["Number in Season"].astype(str)
deaths["episode"] = deaths["death_season"].astype(str) + ","+ deaths["death_episode"].astype(str)

merged = pd.merge(df, deaths, on='episode', how='inner')
new_merged = merged.groupby(['episode','views','Rating', 'Season', 'Death_Count']).size().reset_index(name='deaths')

# -------------------------- Plotting -----------------------------
# plt.figure()
#
# # FIGURE 1 - Summative Scatter plot
# ax = plt.subplot(1,2,1)
# ax = sns.scatterplot(data=new_merged,
#                      x="views", y="Rating",
#                      hue="deaths", size="deaths")
# # plt.legend(bbox_to_anchor=(1.05, 1),  borderaxespad=0.)
#
# FIGURE 2 - Annotated Scatter plot
ax = plt.subplot(1,2,2)
p1 = sns.scatterplot(data=merged, x="views", y="Rating",hue="Season" )
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

for n in range(0, merged.shape[0]):
    p1.text(merged.views[n] + 0.2, merged.Rating[n], merged.episode[n], horizontalalignment='left', color='black', fontsize=5)
# plt.show()


#  ------------------------ Battles per episode ------------------------------------

# Create dataframe with main battles
d = {'Name': ["Frozen Lake Battle", " Loot Train Attack",
              "Battle of Blackwater", "Battle of Castle Black", "Battle of the Bastards", "Fall of King’s Landing",
              "Battle of Winterfell", "Dance of Dragons", "Stormbron"],
     'Episode': [6, 4,  9, 9, 9, 5, 3, 9, 2],
     'Season': [7, 7,  2, 4, 6, 8, 8, 5, 7]
     }
d = pd.DataFrame(data=d)
d["episode"] = d["Season"].astype(str) + ","+ d["Episode"].astype(str)
d.drop(['Season','Episode' ], axis=1, inplace=True)
merged = pd.merge(df, d, on='episode', how='outer')
merged = merged.replace(np.nan, '', regex=True)

p1=sns.scatterplot(data=merged, x="views", y="Rating", hue = 'Season')
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
for n in range(0, merged.shape[0]):
    p1.text(merged.views[n] + 0.2, merged.Rating[n], merged.Name[n], horizontalalignment='center', color='black',weight='semibold', fontsize=9)
plt.show()

