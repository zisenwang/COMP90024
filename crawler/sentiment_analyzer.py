import re
# import nltk
from textblob import TextBlob as tb

class simpleClassifier():

    def preprocess(self,x):
        x = x.lower()
        x = x.encode('ascii', 'ignore').decode()
        x = re.sub(r'https*\S+', ' ', x)
        x = re.sub(r'@\S+', ' ', x)
        x = re.sub(r'#\S+', ' ', x)
        x = re.sub(r'\'\w+', '', x)
        x = re.sub(r'\w*\d+\w*', '', x)
        x = re.sub(r'\s{2,}', ' ', x)
        return x

    def classify(self,tweet):
        """
        :param tweet: specific tweet text
        :return: one of 'positive' and negative
        """
        # subjectivity
        # take in a single tweet text data only
        # certain threshold should be determined instead of 0
        return 'positive' if tb(self.preprocess(tweet)).polarity > 0 else 'negative'

def test():
    pass

if __name__=='__main__':

    clf = simpleClassifier()
    print(tb('i love you').polarity)
    print(tb('i hate you').polarity)
    # >0 positive
    test1 = clf.classify('i love you')
    # <0 negative
    test2 = clf.classify('i hate you')
    print(test1,test2)
    pass

