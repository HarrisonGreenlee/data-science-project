"""
    wordclouds.py file

    Takes the books and turns the top couple of genres into word clouds
    and the most popular books into word clouds as well.
"""

import nltk

# nltk.download("punkt")
# nltk.download("averaged_perceptron_tagger")
# nltk.download("gutenberg")

import matplotlib.pyplot as plt  # pip install matplotlib

import pandas as pd
from matplotlib import rcParams
from wordcloud import STOPWORDS, WordCloud  # pip install wordcloud
from nltk.corpus import gutenberg
from book_processor import remove_header_footer


def tag_parts_of_speech(text):
    """
    tokenizes the book and then tags the words with the appropriate parts of speech
    """
    tokens = nltk.word_tokenize(text, language="english")
    tagged_tokens = nltk.pos_tag(tokens)
    # print(tagged_tokens)
    return tagged_tokens


def add_to_stopwords(stopwords):
    """
    function that adds stopwords to the stopwords list used
    when creating a word cloud.
    """
    additional_stop_words = [
        "might",
        "went",
        "though",
        "thus",
        "whose",
        "will",
        "know",
        "said",
        "well",
        "thought",
        "must",
        "nothing",
        "began",
        "upon",
        "although",
        "many",
        "much",
        "sometimes",
        "replied",
        "reply",
        "come",
        "came",
        "every",
        "even",
        "sure",
        "seemed",
        "take",
        "added",
        "tried",
        "without",
        "going",
        "getting",
        "anything",
        "make",
        "took",
    ]
    stopwords.update(additional_stop_words)
    return stopwords


def create_book_word_cloud(dataframe):
    """
    create the word cloud from the clean dataframe of a book
    """

    stopwords = add_to_stopwords(STOPWORDS)

    # need to convert to string, WordCloud.generate only accepts strings
    words_string = " ".join(dataframe["words"].str.lower())

    wordcloud = WordCloud(
        stopwords=stopwords,
        background_color="white",
        max_words=70,
        min_word_length=4,
        normalize_plurals=False,
    ).generate(words_string)

    # make word cloud visible
    rcParams["figure.figsize"] = 10, 10
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


def get_book_df():
    """
    reads in a book, removes header and footer, tokenizes and tags the text to be able
    to remove proper nouns,
    """

    with open("books/46/46_rawdata.txt", "r", encoding="utf8") as file:
        book_text = file.read().replace("\n", " ")
        clean_text = remove_header_footer(book_text)

    tagged_words = tag_parts_of_speech(clean_text)

    book_df = pd.DataFrame(tagged_words, columns=["words", "part"])

    # removing proper nouns from the dataframe in attempt to not have
    # character names appear in word cloud.
    book_df = book_df[book_df.part != "NNP"]
    book_df = book_df[book_df.part != "NNPS"]
    return book_df


def main():
    book_df = get_book_df()
    create_book_word_cloud(book_df)


if __name__ == "__main__":
    main()
