import re, nltk
from nltk.stem import WordNetLemmatizer

class Preprocessor:
    def remove_stopwords(self, text):
        stopwordsList = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
        regexSeq = " |\\b".join(stopwordsList)
        regexSeq = "\\b"+regexSeq
        text = re.sub(regexSeq,"", text)
        return text

    def caseFolding(self, text):
        text = re.sub("[^A-Za-z_]", " ", text)
        text = re.sub(" +"," ",text)
        text = text.lower()
        return text

    def rreplace(self, s, old, new):
        return (s[::-1].replace(old[::-1],new[::-1], 1))[::-1]

    def stemming(self, text):
        # Porter stemmer
        text = self.caseFolding(text)
        text = self.remove_stopwords(text)
        words = text.split(" ")
        stemmed = []
        for word in words:
            if word.endswith("sses"):
                word = self.rreplace(word, "sses", "ss")
            elif word.endswith("ies"):
                word = self.rreplace(word, "ies", "i")
            elif word.endswith("s"):
                word = self.rreplace(word, "s", " ")
            elif len(word) > 1 and word.endswith("ement"):
                word = self.rreplace(word, "ement", "")
            stemmed.append(word)
        return stemmed

    def lemmetize(self, text):
        #nltk.download('wordnet')
        l = WordNetLemmatizer()
        text = l.lemmatize(text)
        return text