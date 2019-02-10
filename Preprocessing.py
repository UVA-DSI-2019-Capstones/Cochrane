from nltk.stem import PorterStemmer
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
import string
import spacy

#from textblob import TextBlob
nlp = spacy.load('en')
stop = set(stopwords.words('english'))

class Preprocessing():
    def toLower(self, text):
        return text.lower()

    def stemming(self, text):
        tokens = word_tokenize(text)
        ps = PorterStemmer()
        tokens = [ps.stem(t) for t in tokens]
        return ' '.join(tokens)

    def Lemmatizer(self, text):
        tokens = word_tokenize(text)
        wnl = WordNetLemmatizer()
        tokens = [wnl.lemmatize(t) for t in tokens]
        return ' '.join(tokens)

    def FilterPunc(self, text):
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word.isalpha()]
        return ' '.join(tokens)

    def stopwordRemoval(self, text, stop_words):
        tokens = word_tokenize(text)
        tokens = [w for w in tokens if not w in stop_words]
        return ' '.join(tokens)

    def clean(self, doc, stop):
        exclude = set(string.punctuation)
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        #normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return punc_free
    
    def ExtractNouns(self, text):
        nouns = []
        text2 = nlp(text)
        for word in text2:
            if(word.pos_ == 'NOUN'):
                nouns.append(str(word))
        #print(len(nouns))
        return " ".join(nouns)
    
    def identity(self, text):
        return text
    
    def ExtractVerb(self, text):
        nouns = []
        text2 = nlp(text)
        for word in text2:
            if(word.pos_ == 'VERB'):
                nouns.append(str(word))
        #print(len(nouns))
        return " ".join(nouns)
    
    def ExtractVerbANDNoun(self, text):
        nouns = []
        text2 = nlp(text)
        for word in text2:
            if(word.pos_ == 'NOUN' or word.pos_ == 'VERB'):
                nouns.append(str(word))
        #print(len(nouns))
        return " ".join(nouns)