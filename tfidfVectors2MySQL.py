import sys
sys.path.append('../')
import config
import pymysql.cursors
import spacy
from spacy.en import English
parser = English()
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.corpus import stopwords
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from tempfile import SpooledTemporaryFile
from scipy import io as scipyio
from codeTimer import SeparateTimeTrackers
        
timer1 = SeparateTimeTrackers("FirstTimer")

nlp = spacy.load('en')

timer1.timer()

# A custom stoplist
STOPLIST = set(stopwords.words('english') + ["n't", "'s", "'m", "ca"] + list(ENGLISH_STOP_WORDS))
# List of symbols we don't care about
SYMBOLS = " ".join(string.punctuation).split(" ") + ["-----", "---", "...", "“", "”", "'ve"]

# Every step in a pipeline needs to be a "transformer". 
# Define a custom transformer to clean text using spaCy
class CleanTextTransformer(TransformerMixin):
    """
    Convert text to cleaned text
    """

    def transform(self, X, **transform_params):
        return [cleanText(text) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}
    
# A custom function to clean the text before sending it into the vectorizer
def cleanText(text):
    # get rid of newlines
    text = text.strip().replace("\n", " ").replace("\r", " ")
    
    # replace twitter @mentions
    mentionFinder = re.compile(r"@[a-z0-9_]{1,15}", re.IGNORECASE)
    text = mentionFinder.sub("@MENTION", text)
    
    # replace HTML symbols
    text = text.replace("&amp;", "and").replace("&gt;", ">").replace("&lt;", "<")
    
    # lowercase
    text = text.lower()

    return text

# A custom function to tokenize the text using spaCy
# and convert to lemmas
def tokenizeText(sample):

    # get the tokens using spaCy
    tokens = parser(sample)

    # lemmatize
    lemmas = []
    for tok in tokens:
        lemmas.append(tok.lemma_.lower().strip() if tok.lemma_ != "-PRON-" else tok.lower_)
    tokens = lemmas

    # stoplist the tokens
    tokens = [tok for tok in tokens if tok not in STOPLIST]

    # stoplist symbols
    tokens = [tok for tok in tokens if tok not in SYMBOLS]

    # remove large strings of whitespace
    while "" in tokens:
        tokens.remove("")
    while " " in tokens:
        tokens.remove(" ")
    while "\n" in tokens:
        tokens.remove("\n")
    while "\n\n" in tokens:
        tokens.remove("\n\n")

    return tokens

        
timer1.timer()      

connection = pymysql.connect(host='localhost',
                             user='root',
                             password=config.MYSQL_SERVER_PASSWORD,
                             db='youtubeProjectDB',
                             charset='utf8mb4', 
                             cursorclass=pymysql.cursors.DictCursor)

timer1.timer()  

with connection.cursor() as cursor:

    # Get just the English language records which don't yet have a tfidfVector
    
            sql = """    
            SELECT captionsText, captions.id FROM captions
            WHERE language LIKE '%en%' AND tfidfVector IS NULL;"""
            cursor.execute(sql)
            manyCaptions = cursor.fetchall()
                        
timer1.timer()

print (len(manyCaptions), ' records found to be vectorized..')

with open('vocab_from_allEnglish_captions_and_some_texts.pickle', 'rb') as f:
    v = pickle.load(f)  

print ('length of vocabulary dictionary used is: ', len(v)) 
    
vectorizer = TfidfVectorizer(tokenizer=tokenizeText, ngram_range=(1,1), vocabulary=v)   

pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', vectorizer)])

timer1.timer()

for item in manyCaptions:
    document = [item['captionsText']]
    captionsID = item['id']
    p = pipe.fit_transform(document)
    f = SpooledTemporaryFile(max_size=1000000000)
    scipyio.mmwrite(f, p[0])
    f.seek(0)    # important line..
    fileContent = f.read()
    with connection.cursor() as cursor:        
        sql = """UPDATE captions SET tfidfVector=%s WHERE id=%s"""    
        cursor.execute(sql, (fileContent, captionsID))
        connection.commit() 
connection.close()   
timer1.timer()
