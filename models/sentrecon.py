from typing import Dict

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()


def recognize_sentiment(doc: str) -> Dict[str, float]:
    return analyser.polarity_scores(doc)


if __name__ == "__main__":
    def sentiment_analyzer_scores(sentence):
        score = analyser.polarity_scores(sentence)
        print("{:-<40} {}".format(sentence, str(score)))


    while True:
        sentiment_analyzer_scores(input("> "))
