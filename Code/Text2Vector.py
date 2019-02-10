

'''
imports
'''
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scipy import sparse
from sklearn.decomposition import TruncatedSVD
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import gensim
from Preprocessing import Preprocessing

'''
Define objects
'''

prepFuncs = Preprocessing()



class TextRepresentaion():

    def tf_idf(self, db_wikis, db_reviews, stop, dim, WV, PreProcessing_Func, n_gram):
        
        corpus = []
        for wiki in db_wikis['text']:
            corpus.append(PreProcessing_Func(prepFuncs.toLower(prepFuncs.FilterPunc(wiki))))

        tfidf_vectorizer = TfidfVectorizer(max_features = dim, stop_words = stop, ngram_range=(1,n_gram))        
        tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
        
        corpus_test = []
        for review in db_reviews['text']:
            corpus_test.append(PreProcessing_Func(prepFuncs.toLower(prepFuncs.FilterPunc(review))))
            
        tfidf_matrix_Test = tfidf_vectorizer.transform(corpus_test)

        return tfidf_matrix, tfidf_matrix_Test

    def docAveraging(self, sent, WV, dim):

        summ = [0.0] * (dim)
        A = 0.0;
        sent_A = (re.sub(r"[\n(\[\])]", "", sent)).split(" ")
        for word in sent_A:
            if word in WV : #and word not in stop:
                A = A + 1.0
                for i in range(0, dim):
                    summ[i] = summ[i] + float((WV[word])[i])
        if A != 0:
            for i in range(0, dim):
                summ[i] = summ[i] / A

        return summ;

    def WordAveraging(self, db_wikis, db_reviews, stop, dim, WV, PreProcessing_Func, n_gram):

        trainingMatrix = np.zeros((0, dim))
        testMatrix = np.zeros((0, dim))
  
        for wiki in db_wikis['text']:
            trainingMatrix = np.append(trainingMatrix, [np.asarray(docAveraging(prepFuncs.toLower(prepFuncs.FilterPunc(wiki).strip()), WV, dim))], axis=0)#.decode('utf8').strip()), WV, dim))], axis=0)

        for review in db_reviews['text']:
            testMatrix = np.append(testMatrix, [docAveraging(prepFuncs.toLower(prepFuncs.FilterPunc(review).strip()), WV, dim)], axis=0)

        return sparse.csr_matrix(trainingMatrix), sparse.csr_matrix(testMatrix)
   
    
    def LSA(self, db_wikis, db_reviews, stop, dim, WV, PreProcessing_Func, n_gram):

        tfidf_matrix, tfidf_matrix_Test = self.tf_idf(db_wikis, db_reviews, stop, dim, WV, PreProcessing_Func, n_gram)
        lsa = TruncatedSVD(n_components = dim - 1, n_iter=100)
        lsa_matrix_train = lsa.fit_transform(tfidf_matrix)
        lsa_matrix_test = lsa.transform(tfidf_matrix_Test)

        return sparse.csr_matrix(lsa_matrix_train), sparse.csr_matrix(lsa_matrix_test)


    def LDA(self, db_wikis, db_reviews, stop, dim, WV, PreProcessing_Func, n_gram):
        print (dim)
        corpus = []
        for wiki in db_wikis['text']:
            corpus.append(prepFuncs.toLower(prepFuncs.FilterPunc(wiki).strip()))#.decode('utf8').strip()))

        corpus_test = []
        for review in db_reviews['text']:
            corpus_test.append(prepFuncs.toLower(prepFuncs.FilterPunc(review).strip()))

        doc_clean = [prepFuncs.clean(doc, stop).split() for doc in corpus]
        doc_Test = [prepFuncs.clean(doc, stop).split() for doc in corpus_test]

        Lda = gensim.models.ldamodel.LdaModel

        common_dictionary = gensim.corpora.Dictionary(doc_clean)
        common_corpus = [common_dictionary.doc2bow(text) for text in doc_clean]
        # Train the model on the corpus.
        lda = Lda(common_corpus, num_topics = dim)

        lda_corpus = lda[common_corpus]
        all_topics_csr = gensim.matutils.corpus2csc(lda_corpus)
        all_topics_numpy = all_topics_csr.toarray()
        trainingMatrix = all_topics_numpy.transpose()

        # Create a new corpus, made of previously unseen documents.
        other_texts = doc_Test
        other_corpus = [common_dictionary.doc2bow(text) for text in other_texts]

        # unseen_doc = other_corpus[0]
        lda_corpus_test = lda[other_corpus]  # get topic probability distribution for a document
        all_topics_csr = gensim.matutils.corpus2csc(lda_corpus_test)
        all_topics_numpy_test = all_topics_csr.toarray()
        testMatrix = all_topics_numpy_test.transpose()

        return sparse.csr_matrix(trainingMatrix), sparse.csr_matrix(testMatrix)


    def doc2Vec(self, db_wikis, db_reviews, stop, dim, WV, PreProcessing_Func):

        trainingMatrix = np.zeros((0, dim))
        testMatrix = np.zeros((0, dim))

        corpus = []
        for wiki in db_wikis['text']:
            corpus.append(prepFuncs.toLower(prepFuncs.FilterPunc(wiki).strip()))#.decode('utf8').strip()))

        corpus_test = []
        for review in db_reviews['text']:
            corpus_test.append(PreProcessing_Func(prepFuncs.toLower(prepFuncs.FilterPunc(review))))

        doc_clean = [prepFuncs.clean(doc, stop).split() for doc in corpus]
        doc_Test = [prepFuncs.clean(doc, stop).split() for doc in corpus_test]

        documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(doc_clean)]
        model = Doc2Vec(documents, vector_size = dim, window=8, min_count=1, workers=4)

        for i in range (0, len(doc_clean)):
            trainingMatrix = np.append(trainingMatrix, [model.infer_vector(doc_clean[i])], axis=0)
        for i in range (0, len(doc_Test)):
            testMatrix = np.append(testMatrix, [model.infer_vector(doc_Test[i])], axis=0)

        return sparse.csr_matrix(trainingMatrix), sparse.csr_matrix(testMatrix)
        

