# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 15:39:45 2019

@author: Erfaneh

Read DBs & Files
 
"""
import pandas as pd
import numpy as np
import sqlite3
import os

class ReadData():
    def readWikipedia(self, database):
        db_file = database
        with sqlite3.connect(db_file) as db:
            #df = pd.read_sql_query('select * FROM cleaned_wikitext', db)
            df = pd.read_sql_query('select id, title, revision_text FROM page', db)
        return (df)    
    
    def readReviews(self, database):
        db_file = database
        with sqlite3.connect(db_file) as db:
            df = pd.read_sql_query('select *, abstract || " " || summary || " " || objectives || " " ||  conclusions || " " || background || " " || methods || " " || results || " " || discussion as text from post', db)
            #df = pd.read_sql_query('SELECT doi, title, abstract || " " || summary || " " || objectives || " " ||  conclusions || " " || background || " " || methods || " " || results || " " || discussion as text FROM post', db)
        return (df)    
    
    def readDependencyR2W(self, filePath):
        dependency = {}
        dependency_columns = pd.read_csv(filePath, sep=',')    
        for i in  range(0,len(dependency_columns['Page'])):
            doi = dependency_columns['DOI'][i]
            page =  dependency_columns['Page'][i]
            if doi in dependency.keys():
                dependency[doi].append(page)
            else:
                dependency[doi] = []
                dependency[doi].append(page)        
        return dependency
        
    def readDependencyW2R(self, filePath):
        dependency = {}
        dependency_columns = pd.read_csv(filePath, sep=',')        
        for i in  range(0,len(dependency_columns['Page'])):
            doi = dependency_columns['DOI'][i]
            page =  dependency_columns['Page'][i]
            if page in dependency.keys():
                dependency[page].append(doi)
            else:
                dependency[page] = []
                dependency[page].append(doi)
        return dependency
        
    def readWV(self, path, stop):
        WV = {}
        exists = os.path.isfile(path)
        if exists:                    
            file_1 = open(path, "r")
            for line in file_1:
                line = line.replace("\n", "")
                wordV = line.split(" ")
                key = wordV[0]
                if key not in stop:
                    del wordV[0]
                    WV[key] = np.asarray(wordV,dtype=float)           
        else:
            print ("File "+ path +" not exists")
            
        return WV
    
    
