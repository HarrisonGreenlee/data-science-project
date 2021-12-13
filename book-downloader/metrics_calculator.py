import nltk
import string
from readability import Readability
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


def tag_parts_of_speech(text):
    text = text.translate(string.punctuation)
    tokens = nltk.word_tokenize(text, language="english")
    return nltk.pos_tag(tokens)


def calc_parts_of_speech_histogram(text):
    tagged_tokens = tag_parts_of_speech(text)
    parts_of_speech = [tagged_token[1] for tagged_token in tagged_tokens]
    possible_parts_of_speech = ("CC", "CD", "DT", "EX", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNP", "NNPS", "NNS", "PDT", "PRP", "RB", "RBR", "RBS", "RP", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WRB")
    parts_of_speech_hist = {possible_part_of_speech: parts_of_speech.count(possible_part_of_speech) for possible_part_of_speech in possible_parts_of_speech}
    return parts_of_speech_hist


def pos_hist_to_word_count(pos_hist):
    return sum(pos_hist.values())


def simplify_parts_of_speech_histogram(parts_of_speech_hist):
    return {
        "NOUN": parts_of_speech_hist["NN"]
        + parts_of_speech_hist["NNP"]
        + parts_of_speech_hist["NNPS"]
        + parts_of_speech_hist["NNS"],
        "ADJECTIVE": parts_of_speech_hist["JJ"]
        + parts_of_speech_hist["JJR"]
        + parts_of_speech_hist["JJS"],
        "ADVERB": parts_of_speech_hist["RB"]
        + parts_of_speech_hist["RBR"]
        + parts_of_speech_hist["RBS"],
        "VERB": parts_of_speech_hist["VB"]
        + parts_of_speech_hist["VBD"]
        + parts_of_speech_hist["VBG"]
        + parts_of_speech_hist["VBN"]
        + parts_of_speech_hist["VBP"]
        + parts_of_speech_hist["VBZ"],
    }


def action_description_ratio(simplified_parts_of_speech_hist):
    action = simplified_parts_of_speech_hist['ADVERB'] + simplified_parts_of_speech_hist['VERB']
    description = simplified_parts_of_speech_hist['NOUN'] + simplified_parts_of_speech_hist['ADJECTIVE']
    return action/(action+description)


def calc_metrics(filepath):
    with open(filepath, 'r', encoding="utf8") as file:
        book_text = file.read().replace('\n', '')
    pos_hist = calc_parts_of_speech_histogram(book_text)
    word_count = pos_hist_to_word_count(pos_hist)
    simplified_pos_hist = simplify_parts_of_speech_histogram(pos_hist)
    adi = action_description_ratio(simplified_pos_hist)
    r = Readability(book_text)
    fk = r.flesch_kincaid()
    return {'flesch_kincaid': fk.score, 'adi': adi, 'word_count': word_count}