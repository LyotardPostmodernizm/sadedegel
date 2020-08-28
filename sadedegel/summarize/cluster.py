from typing import List
from math import ceil

from sklearn.cluster import KMeans  # type: ignore
from sklearn.decomposition import PCA  # type: ignore
from sklearn.pipeline import Pipeline  # type: ignore

from ._base import ExtractiveSummarizer
from ..bblock import Sentences


class KMeansSummarizer(ExtractiveSummarizer):

    _tags = ExtractiveSummarizer._tags + ['cluster'] 

    def __init__(self, n_clusters=2, random_state=42, normalize=True):
        self.normalize = normalize
        self.n_clusters = n_clusters
        self.random_state = random_state

    def _predict(self, sentences: List[Sentences]):
        if len(sentences) == 0:
            raise ValueError(f"Ensure that document contains a few sentences for summarization")

        doc = sentences[0].document

        effective_n_clusters = min(self.n_clusters, len(doc))

        scores = 1 / (KMeans(n_clusters=effective_n_clusters, random_state=self.random_state).fit_transform(
            doc.bert_embeddings).min(axis=1) + 1e-10)

        if self.normalize:
            return scores / scores.sum()
        else:
            return scores


class AutoKMeansSummarizer(ExtractiveSummarizer):
    """Kmeans cluster automatically deciding on the number of clusters to be used based on document length."""

    _tags = ExtractiveSummarizer._tags + ['cluster'] 

    def __init__(self, n_cluster_to_length=0.05, min_n_cluster=2, random_state=42, normalize=True):
        self.normalize = normalize
        self.n_cluster_to_length = n_cluster_to_length
        self.min_n_cluster = min_n_cluster
        self.random_state = random_state

    def _predict(self, sentences: List[Sentences]):
        if len(sentences) == 0:
            raise ValueError(f"Ensure that document contains a few sentences for summarization")

        doc = sentences[0].document

        effective_n_clusters = min(max(ceil(len(doc) * self.n_cluster_to_length), self.min_n_cluster), len(doc))

        scores = 1 / (KMeans(n_clusters=effective_n_clusters, random_state=self.random_state).fit_transform(
            doc.bert_embeddings).min(axis=1) + 1e-10)

        if self.normalize:
            return scores / scores.sum()
        else:
            return scores


class DecomposedKMeansSummarizer(ExtractiveSummarizer):
    """BERT embeddings are high in dimension and potentially carry redundant information that can cause
        overfitting or curse of dimensionality effecting in clustering embeddings.

        DecomposedKMeansSummarizer adds a PCA step (or any othe lsinear/non-linear dimensionality reduction technique)
         before clustering to obtain highest variance in vector fed into clustering
    """

    _tags = ExtractiveSummarizer._tags + ['cluster'] 

    def __init__(self, n_clusters=2, n_components=48, random_state=42, normalize=True):
        self.normalize = normalize
        self.n_clusters = n_clusters
        self.n_components = n_components
        self.random_state = random_state

    def _predict(self, sentences: List[Sentences]):
        if len(sentences) == 0:
            raise ValueError(f"Ensure that document contains a few sentences for summarization")

        doc = sentences[0].document

        effective_n_clusters = min(self.n_clusters, len(doc))
        effective_n_components = min(self.n_components, len(doc))

        pipeline = Pipeline(
            [('pca', PCA(effective_n_components)),
             ('kmeans', KMeans(effective_n_clusters, random_state=self.random_state))])

        scores = 1 / (pipeline.fit_transform(doc.bert_embeddings).min(axis=1) + 1e-10)

        if self.normalize:
            return scores / scores.sum()
        else:
            return scores
