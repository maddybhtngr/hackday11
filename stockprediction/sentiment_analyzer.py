from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize


def document_sentiment(data: str):
    tokens = word_tokenize(data)
    test_subset = tokens

    sid = SentimentIntensityAnalyzer()
    pos_word_list = []
    neu_word_list = []
    neg_word_list = []

    for word in test_subset:
        if (sid.polarity_scores(word)['compound']) >= 0.1:
            pos_word_list.append(word)
        elif (sid.polarity_scores(word)['compound']) <= -0.1:
            neg_word_list.append(word)
        else:
            neu_word_list.append(word)

    total_words = len(pos_word_list) + len(neg_word_list)
    return (len(pos_word_list) - len(neg_word_list)) / (total_words + 0.0001)

