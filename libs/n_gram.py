from collections import Counter
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
import nltk

# Make sure you have the necessary NLTK packages
nltk.download('punkt')
nltk.download('stopwords')

def clean_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Remove numbers
    text = ''.join([i for i in text if not i.isdigit()])

    # Tokenize text
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Perform stemming (you can use lemmatization instead if needed)
    ps = PorterStemmer()
    tokens = [ps.stem(word) for word in tokens]

    return tokens

def get_top_ngrams(text_list, n, top_n):
    ngram_list = []
    for text in text_list:
        tokens = clean_text(text)  # Clean the text more aggressively
        ngram_list.extend(ngrams(tokens, n))  # Generate n-grams

    ngram_counts = Counter(ngram_list)  # Count n-grams
    top_ngrams = ngram_counts.most_common(top_n)  # Get the top n n-grams
    return top_ngrams

