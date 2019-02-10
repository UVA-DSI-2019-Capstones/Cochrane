
'''
imports
'''

import numpy as np
import pandas as pd
from operator import itemgetter


def calculateSim_R2W(db_wikis, db_reviews, matrix_train, matrix_test, stop, dim, simMeasure, arg, dependency, WV, n_top, resultFile):
    recognized_dependencies = {}
    df_result = pd.DataFrame(columns=['Query', 'Retrieved_document', 'Similarity', 'Rank'])
    accuracy = 0
    numberOfdependencies = 0
    
    doi = db_reviews['doi']
    wiki_title = db_wikis['title']
    review_title = db_reviews['title']

    
    for test in range(0, (matrix_test.shape[0])):
        testRep = matrix_test[test,:]
        distances = []
        for i in range(0,(matrix_train.shape)[0]):
            v_train = matrix_train[i, :].toarray().tolist()[0]
            v_test = testRep.toarray().tolist()[0]
        
            if (sum(v_test) == 0 or sum(v_train) == 0):
                print("Hi")
                distances.append(0)
            else:
                distances.append(simMeasure(v_train, v_test))

        similarity_values = []
        if arg == np.argmin:
            indexes = (np.asarray(distances).argsort()[::-1][(-1*n_top):])
            similarity_values = (itemgetter(*indexes)(distances))
            predicted_labels = np.asarray(wiki_title)[[indexes]]
            
        elif arg == np.argmax:
            indexes = (np.asarray(distances).argsort()[(-1*n_top):][::-1])
            similarity_values = (itemgetter(*indexes)(distances))
            predicted_labels = np.asarray(wiki_title)[[indexes]]       
        
        for rank in range(0, len(predicted_labels)):
            df_sample = pd.DataFrame([[review_title[test], predicted_labels[rank], similarity_values[rank], (rank + 1)]],columns=['Query', 'Retrieved_document', 'Similarity', 'Rank'])
            df_result = df_result.append(df_sample, ignore_index=True)
   
        if (doi[test] in dependency.keys()):
            numberOfdependencies += len(dependency[doi[test]])
            for predicted_label in predicted_labels:
                if (predicted_label in dependency[doi[test]]):                    
                    accuracy += 1
                    if(doi[test] not in recognized_dependencies):
                        recognized_dependencies[doi[test]] = []
                        recognized_dependencies[doi[test]].append(predicted_label)
                    else:
                        recognized_dependencies[doi[test]].append(predicted_label)
        

        if (doi[test] in recognized_dependencies):
            print([doi[test]], dependency[doi[test]], recognized_dependencies[doi[test]]) 
        else: 
            print([doi[test]], dependency[doi[test]], "[]") 
    df_result.to_csv(resultFile)
    print (numberOfdependencies)
    print ("accuracy: " + str(float(accuracy)/(numberOfdependencies)))
    
def calculateSim_W2R( db_reviews, db_wikis,  matrix_train, matrix_test, stop, dim, simMeasure, arg, dependency, WV, n_top, resultFile):
    df_result = pd.DataFrame(columns=['Query', 'Retrieved_document', 'Similarity', 'Rank'])
    accuracy = 0
    numberOfdependencies = 0
    
    doi = db_reviews['doi']
    wiki_title = db_wikis['title']
    review_title = db_reviews['title']

    for test in range(0, (matrix_test.shape[0])):
            testRep = matrix_test[test,:]
            distances = []
            for i in range(0,(matrix_train.shape)[0]):
                distances.append(simMeasure(matrix_train[i, :].toarray().tolist()[0], testRep.toarray().tolist()[0]))

            similarity_values = []
            if arg == np.argmin:
                indexes = (np.asarray(distances).argsort()[::-1][(-1*n_top):])
                similarity_values = (itemgetter(*indexes)(distances))
                predicted_labels = np.asarray(wiki_title)[[indexes]]
                
            elif arg == np.argmax:
                indexes = (np.asarray(distances).argsort()[(-1*n_top):][::-1])
                similarity_values = (itemgetter(*indexes)(distances))
                predicted_labels = np.asarray(wiki_title)[[indexes]]           

            for rank in range(0, len(predicted_labels)):
                df_sample = pd.DataFrame([[review_title[test], predicted_labels[rank], similarity_values[rank], (rank + 1)]],columns=['Query', 'Retrieved_document', 'Similarity', 'Rank'])
                df_result = df_result.append(df_sample, ignore_index=True)
   
            if (doi[test] in dependency.keys()):
                numberOfdependencies += len(dependency[doi[test]])
                for predicted_label in predicted_labels:
                    if (predicted_label in dependency[doi[test]]):
                        accuracy += 1
                    
    df_result.to_csv(resultFile)
    print (numberOfdependencies)
    print ("accuracy: " + str(float(accuracy)/(numberOfdependencies)))