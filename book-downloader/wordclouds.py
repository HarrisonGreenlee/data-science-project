"""
    wordclouds.py file

    Takes the books and turns the top couple of genres into word clouds
    and the most popular books into word clouds as well.
"""

# import collections
# import matplotlib

# import matplotlib.cm as cm
import matplotlib.pyplot as plt  # pip install matplotlib

# import numpy as np
import pandas as pd
from matplotlib import rcParams
from wordcloud import STOPWORDS, WordCloud
import wordcloud  # pip install wordcloud

dataset = pd.read_csv("books.csv", encoding="latin-1")
all_titles = " ".join(dataset["title"].str.lower())


stopwords = STOPWORDS

wordcloud = WordCloud(
    stopwords=stopwords, background_color="white", max_words=50
).generate(all_titles)

rcParams["figure.figsize"] = 10, 10
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Wordcloud of Book titles")
plt.show()
