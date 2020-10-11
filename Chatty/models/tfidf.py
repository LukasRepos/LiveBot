import math
import string
from typing import Tuple, List

import numpy as np
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from Chatty.saveState.saves import get_conn


class TfIdf:
    def __init__(self) -> None:
        self.df = pd.DataFrame()
        self.df.index.name = "__documents"
        self.df["__norm"] = 0
        self.df["__class"] = ""
        self.df["__original"] = ""

        self.ps = PorterStemmer()

    def submit_document(self, doc: str, _class: str) -> None:
        terms = self.__process_doc(doc)

        if len(terms) == 0:
            return

        if " ".join(terms) in self.df.index.values:
            self.df.at[" ".join(terms), "__class"] = _class
            return

        for term in terms:
            if term not in self.df.columns:
                self.df[term] = 0

        doc_dict = {}
        for term in [col for col in self.df.columns if not col.startswith("__")]:
            doc_dict[term] = 0.0
        doc_dict["__class"] = _class
        doc_dict["__original"] = doc
        doc_series = pd.Series(doc_dict, name=" ".join(self.__process_doc(doc)))
        self.df = self.df.append(doc_series)

    def fit(self) -> None:
        terms = [col for col in self.df.columns if not col.startswith("__")]

        for doc in self.df.index.values:
            doc_dict = {}
            for term in terms:
                doc_dict[term] = self.__tfidf(term, doc.split())

            vec = np.array(list(doc_dict.values()))
            norm = np.linalg.norm(vec)
            doc_dict["__norm"] = norm
            doc_dict["__class"] = self.df.loc[doc]["__class"]
            doc_dict["__original"] = self.df.loc[doc]["__original"]
            self.df.loc[doc] = pd.Series(doc_dict)

    def classify_document(self, doc: str) -> Tuple[int, str, str]:
        tokens = self.__process_doc(doc)

        if len(tokens) == 0:
            return 1, "None", "None"

        terms = [col for col in self.df.columns if not col.startswith("__")]
        sim_values = []

        b_vec = []
        for term in terms:
            b_vec.append(self.__tfidf(term, tokens))
        b_vec = np.array(b_vec)
        b_norm = np.linalg.norm(b_vec)

        if b_norm == 0:
            sim_values.append(-np.inf)
            return -np.inf, self.df.iloc[0]["__class"], self.df.index.values[0]

        for doc in self.df.index.values:
            a_norm = self.df.loc[doc]["__norm"]
            a_vec = self.df.loc[doc][terms]

            dot = np.dot(a_vec, b_vec)
            sim = dot / (a_norm * b_norm)
            sim_values.append(sim)

        return (np.amax(sim_values) + 1) / 2, self.df.iloc[np.where(sim_values == np.amax(sim_values))[0][0]]["__class"], self.df.iloc[np.where(sim_values == np.amax(sim_values))[0][0]]["__original"]

    def save(self) -> None:
        get_conn().save_df("RESERVED_TFIDF", self.df, index=True)

    def load(self) -> None:
        self.df = get_conn().to_df("RESERVED_TFIDF", index="__documents")

    def __tfidf(self, term: str, doc: List[str]) -> float:
        corpus = [ind.split() for ind in self.df.index.values]
        return self.__tf(term, doc) * self.__idf(term, corpus)

    def __process_doc(self, doc: str) -> List[str]:
        tokens = [w for w in word_tokenize(doc.lower()) if w not in string.punctuation]
        lemmatized_words = [self.ps.stem(t) for t in tokens]
        return lemmatized_words

    def __tf(self, term: str, doc: List[str]) -> float:
        return doc.count(term) / len(doc)

    def __idf(self, term: str, corpus: List[str]) -> float:
        nt = 0
        for doc in corpus:
            if term in doc:
                nt += 1

        return math.log(len(corpus) / nt, 10)

    def __repr__(self) -> str:
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
