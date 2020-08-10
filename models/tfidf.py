import math
import string

import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


class TfIdf:
    def __init__(self):
        self.df = pd.DataFrame()
        self.df.index.name = "__documents"
        self.df["__norm"] = 0
        self.df["__class"] = ""

        self.ps = PorterStemmer()

    def submit_document(self, doc, _class):
        """
        Submites a document to the classifier
        :param doc: String
        :param _class: String
        :return: None
        """
        terms = self.__process_doc(doc)

        if len(terms) == 0:
            return

        for term in terms:
            if term not in self.df.columns:
                self.df[term] = 0

        doc_dict = {}
        for term in [col for col in self.df.columns if not col.startswith("__")]:
            doc_dict[term] = 0.0
        doc_dict["__class"] = _class
        doc_series = pd.Series(doc_dict, name=doc)
        self.df = self.df.append(doc_series)

    def fit(self):
        """
        Recalculates the entire dataframe values
        :return: None
        """
        terms = [col for col in self.df.columns if not col.startswith("__")]

        for doc in self.df.index.values:
            doc_dict = {}
            for term in terms:
                doc_dict[term] = self.__tfidf(term, self.__process_doc(doc))

            vec = np.array(list(doc_dict.values()))
            norm = np.linalg.norm(vec)
            doc_dict["__norm"] = norm
            doc_dict["__class"] = self.df.loc[doc]["__class"]
            self.df.loc[doc] = pd.Series(doc_dict)

    def classify_document(self, doc):
        """
        Classifies a document
        :param doc: String
        :return: A tuple of probability in [0, 1] and the class
        """
        tokens = self.__process_doc(doc)

        if len(tokens) == 0:
            return 1, "None"

        terms = [col for col in self.df.columns if not col.startswith("__")]
        sim_values = []

        for doc in self.df.index.values:
            a_norm = self.df.loc[doc]["__norm"]
            a_vec = np.array([self.df.loc[doc][t] for t in terms])

            b_vec = []
            for term in terms:
                b_vec.append(self.__tfidf(term, tokens))
            b_vec = np.array(b_vec)
            b_norm = np.linalg.norm(b_vec)

            if b_norm == 0:
                sim_values.append(-np.inf)
            else:
                dot = np.dot(a_vec, b_vec)
                sim = dot / (a_norm * b_norm)
                sim_values.append(sim)

        return (np.amax(sim_values) + 1) / 2, self.df.iloc[np.where(sim_values == np.amax(sim_values))[0][0]]["__class"]

    def save(self, path):
        import fileSystem.fs
        self.df.to_csv(path)

    def load(self, path):
        import fileSystem.fs
        self.df = pd.read_csv(path, index_col=0)
        print(self.df)

    def __tfidf(self, term, doc):
        """
        Calculates the combined score
        :param term: String
        :param doc: Array of String
        :return: None
        """
        corpus = [self.__process_doc(ind) for ind in self.df.index.values]
        return self.__tf(term, doc) * self.__idf(term, corpus)

    def __process_doc(self, doc):
        """
        Processes the document
        :return: Array of String
        """
        tokens = [w for w in word_tokenize(doc.lower()) if w not in string.punctuation]
        lemmatized_words = [self.ps.stem(t) for t in tokens]
        return lemmatized_words

    def __tf(self, term, doc):
        """
        Returns the TF classification for a given term
        :param term: String
        :param doc: Array of String
        :return: Float
        """
        return doc.count(term) / len(doc)

    def __idf(self, term, corpus):
        """
        Calculates the IDF classification of a term in a corpus
        :param term: String
        :param corpus: Array of Documents
        :return: Float
        """
        nt = 0
        for doc in corpus:
            if term in doc:
                nt += 1

        return math.log(len(corpus) / nt, 10)

    def __repr__(self):
        return str(self.df.head())


if __name__ == "__main__":
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    tfidf = TfIdf()
    tfidf.submit_document("Hello", "welcome")
    tfidf.submit_document("Hi there", "welcome")
    tfidf.submit_document("Goodbye", "Goodbyes")

    tfidf.fit()
    while True:
        print(tfidf.classify_document(input("> ")))
