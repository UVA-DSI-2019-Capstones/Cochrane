'''
Main File for retrieving Wikipedia Articles for Reviews

'''
'''
imports
'''
#import sys
#sys.path.append('C:\\Users\\Erfaneh\\Google Drive\\Cochrane\\Codes\\Cochrane-Examples2\\')
#%%
import numpy as np
import re
from Reads import ReadData
from nltk.corpus import stopwords
from SimilarityMeasures import Similarity
from Text2Vector import TextRepresentaion
from Preprocessing import Preprocessing
from document_Retrieval import calculateSim_W2R


#%%#########################################

'''
Define parameters
'''
path_main = "/home/erfaneh/googledrive/Projects/Cochrane/"
path_CochraneReviews = path_main+'DataSet/citedCochrane.db'
path_WikipediaArticles = path_main+"DataSet/cleaned_wikitext.db"
path_dependency_file = path_main + "DataSet/dependency.csv"

dim = 2500
n_top = 50

#%%#########################################

'''
Define Objects
'''
FileReading = ReadData()
SimilarityMeasures = Similarity()
text2Vec = TextRepresentaion()
prepFuncs = Preprocessing()

#%%#########################################
'''
Read Data
'''
stop = set(stopwords.words('english'))
db_reviews = FileReading.readReviews(path_CochraneReviews)
db_wikis = FileReading.readWikipedia(path_WikipediaArticles)
db_wikis = db_wikis.rename(index=str, columns={"field1": "title", "field2": "id", "field3": "text"})
dependencies = FileReading.readDependencyW2R(path_dependency_file)
WV = FileReading.readWV("/home/erfaneh/Desktop/Drives/Datasets/WV/glove.6B."+str(dim)+"d.txt", stop)

#%%#########################################
PreprocessingFunctions = [prepFuncs.ExtractNouns, prepFuncs.identity] 
Text2VecFunctions = [text2Vec.tf_idf] #, text2Vec.LDA, text2Vec.doc2Vec] #text2Vec.tf_idf, 
SimilarityFunctions = [SimilarityMeasures.cosine_similarity, SimilarityMeasures.manhattan_distance, SimilarityMeasures.euclidean_distance, SimilarityMeasures.kldivergence_distance,  SimilarityMeasures.hellinger_distance]
 
for textRep in Text2VecFunctions:
    for prepFunc in PreprocessingFunctions:
        for n_gram in (1, 2, 3):
            print (dim)
            matrix_train, matrix_test = textRep(db_reviews, db_wikis, stop, dim, WV, prepFunc, n_gram)
            for simMeasure in SimilarityFunctions:
                resultFile = path_main + "Results/W2R_" + re.split('\s|\.', str(textRep))[3] + "_" + re.split('\s|\.', str(prepFunc))[3] + "_" + re.split('\s|\.', str(simMeasure))[3] +"_ngram"+ str(n_gram) + "_dim" + str(dim) + "_k" + str(n_top) + ".csv"
                print(resultFile)
                if 'distance' not in str(simMeasure):
                    calculateSim_W2R(db_reviews, db_wikis, matrix_train, matrix_test, stop, dim, simMeasure, np.argmax, dependencies, WV, n_top, resultFile)
                else:
                    calculateSim_W2R(db_reviews, db_wikis, db_reviews, matrix_train, matrix_test, stop, dim, simMeasure, np.argmin, dependencies, WV, n_top, resultFile)
                    
