# Julian McClellan
# Workshop 6
# Advanced Python for Streaming Analytics

import nltk
import random
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords, wordnet, movie_reviews
from nltk.stem import PorterStemmer
from nltk.corpus import state_union


a = "The professional Counter-Strike: Global Offensive scene is easily accessible for first time viewers. Terrorists try to plant the bomb and Counter-Terrorists try to stop them. Guns shoot things. There are only 5 people on each team and a map provides a good view of top-down player positions. Although the game is based on simple mechanics, there is a high skill ceiling."

# Part 2
print("Part 2\n\n\n\n")
a_token = sent_tokenize(a)
a_token = [word_tokenize(sent) for sent in a_token]
print("Sentence tokenized, with each sentence word tokenized.")
print(a_token)


# Part 3
print("Part 3\n\n\n\n")
# Remove stopwords from sentence
a_token = [[word for word in sent if word not in stopwords.words("english")] for sent in a_token]
ps = PorterStemmer()

# Part 4
print("Part 4\n\n\n\n")
for sent in a_token:
    for word in sent:
        print("\n")
        print(ps.stem(word))


# Part 5
print("Part 5\n\n\n\n")
tokenized = PunktSentenceTokenizer(a).tokenize(a)

def process_content():
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            print(tagged)
    except Exception as e:
        print(str(e))
process_content()

# Part 6
print("Part 6\n\n\n\n")
def process_content_2():
    try: 
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            chunkGram = r"""Chunk:{<RB.?>*<VB.?>*<NNP>+<NN>?}"""
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)
            for subtree in chunked.subtrees():
                print(subtree)
            # chunked.draw()
    except Exception as e:
        print(str(e))
process_content_2()

from nltk.corpus import gutenberg
sample = gutenberg.raw("bible-kjv.txt")
tok = sent_tokenize(sample)
for x in range(5):
    print(tok[x])
    print("\n")

# Part 7
print("Part 7\n\n\n\n")
XXX = "Gun"
YYY = "Terrorist"
VVV = "Shoot"
syns = wordnet.synsets(XXX)
print(syns[0].name())
print("\n")
print(syns[0].lemmas()[0].name())

syns = wordnet.synsets(YYY)
print(syns[0].name())
print("\n")
print(syns[0].lemmas()[0].name())

syns = wordnet.synsets(VVV)
print(syns[0].name())
print("\n")
print(syns[0].lemmas()[0].name())

synonyms, antonyms = [], []
for syn in wordnet.synsets(XXX):
    for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())
        print(set(synonyms))
        print("\n")
        print(set(antonyms))

# Part 8
print("Part 8\n\n\n\n")
documents = [(list(movie_reviews.words(fileid)), category)
            for category in movie_reviews.categories()
            for fileid in movie_reviews.fileids(category)]

random.seed(69)
random.shuffle(documents)

print(documents[1])
print("\n")
all_words = []
for w in movie_reviews.words():
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)
print(all_words.most_common(15))
print("\n")
print(all_words["stupid"])

# Part 9 Twitter sentiment analysis
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer


#consumer key, consumer secret, access token, access secret.
ckey="yqzFKO2G6FtQ75V56JKw5ak3X"
csecret="8Jj3xLkNCQOEB2dySve6lLP1eB9AO5hhnToa9D8CX2qHF3vEUI"
atoken="779845755922243585-FjFB2ibAG8ydTv3m2aHBgFfafQS6d8W"
asecret="MjvHhEZLeR5bg0joApyr0ORKZ3yIRPoz0PoozVPTMBYTU"
print(SentimentIntensityAnalyzer.polarity_scores.__doc__)
# Return a float for sentiment strength based on the input text.
# Positive values are positive valence, negative value are negative
# valence.


class listener(StreamListener):
    SID = SentimentIntensityAnalyzer()
    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        print(tweet, self.SID.polarity_scores(tweet))
        print("\n")
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["car"])
