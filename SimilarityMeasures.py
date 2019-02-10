from math import *
from decimal import Decimal
from gensim.matutils import kullback_leibler, jaccard, hellinger, sparse2full


class Similarity():
    """ similarity measures function """

    def euclidean_distance(self, x, y):
        """ return euclidean distance between two lists """

        return sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))

    def manhattan_distance(self, x, y):
        """ return manhattan distance between two lists """

        return sum(abs(a - b) for a, b in zip(x, y))

    def minkowski_distance(self, x, y, p_value):
        """ return minkowski distance between two lists """

        return self.nth_root(sum(pow(abs(a - b), p_value) for a, b in zip(x, y)),
                             p_value)

    def nth_root(self, value, n_root):
        """ returns the n_root of an value """

        root_value = 1 / float(n_root)
        return round(Decimal(value) ** Decimal(root_value), 3)

    def cosine_similarity(self, x, y):
        """ return cosine similarity between two lists """

        numerator = sum(a * b for a, b in zip(x, y))
        denominator = self.square_rooted(x) * self.square_rooted(y)
        if (denominator == 0):
            return numerator
        return round(numerator / float(denominator), 3)

    def square_rooted(self, x):
        """ return 3 rounded square rooted value """

        return round(sqrt(sum([a * a for a in x])), 3)

    def jaccard_similarity(self, x, y):

        """ returns the jaccard similarity between two lists """

        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        return intersection_cardinality / float(union_cardinality)

    def kldivergence_distance(self, x, y):
        replaceZero = 0.000001
        """ return KL-divergence between two lists """
        return kullback_leibler([replaceZero if e == 0 else e for e in x], [replaceZero if e == 0 else e for e in y])

    def hellinger_distance(self, x, y):

        """ return hellinger between two lists """

        return hellinger(x, y)

    def get_jaccard_sim(self, str1, str2):
        a = set(str1.split())
        b = set(str2.split())
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))

