# things we need for NLP
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

# things we need for Tensorflow
import numpy as np
import tflearn
# tensorflow can be imported via the code from line 10 or from line 11; use the one that works on your machine
#import tensorflow as tf
from tensorflow.python.framework import ops as tf
import random
import pickle

# import our chat-bot intents file
import json
with open('intents.json') as json_data:
    intents = json.load(json_data)

words = []
classes = []
documents = []
# set which words to ignore and not count as matches
ignore_words = ['?']
# loop through each sentence in our intents patterns until we are through
# patterns are  (sample) sentences / questions / keywords and intents are categories (each item in one intent
# shares a tag and belongs to the same classification
# "intent" and "intents" seem to be "known" key names; ['intents'] however is the NAME of a list (interpreted as such), as is ['patterns']
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        # information on tokenization: https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/text/Tokenizer
        # more: https://chatbotsmagazine.com/contextual-chat-bots-with-tensorflow-4391749d0077
        # "We create a list of documents (sentences), each sentence is a list of stemmed words and each document is
        # associated with an intent (a class). (...) we need to transform it further: from documents of words into tensors of numbers."
        w = nltk.word_tokenize(pattern)
        # add to our words list
        words.extend(w)
        # add to documents in our corpus
        documents.append((w, intent['tag']))
        # add to our classes list (unless it already exists)
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# stem and lower each word and remove duplicates
# about stemming: https://www.h2kinfosys.com/blog/stemming-and-lemmatization/
# "Stemming is a text normalizing technique that cuts down affixes of words, to extract its base form or root words.
# Stemming is a crude process and sometimes, the root word, also called the stem, may not have grammatical meaning."
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# remove duplicates
classes = sorted(list(set(classes)))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "unique stemmed words", words)


# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)

# create train and test lists
train_x = list(training[:,0]) # patterns -> inputs
train_y = list(training[:,1]) # responses -> outputs

# reset underlying graph data
tf.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and set up tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
# Start training (apply gradient descent algorithm)
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
model.save('model.tflearn')

def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

# manually pass a sentence to be categorized HERE; otherwise handled via frontend
p = bow("is your shop open today?", words)
print (p)
print (classes)

print(model.predict([p]))

# save all of our data structures
pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )


# set minimum threshold for viable categorization
ERROR_THRESHOLD = 0.25
def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # a random response from the intent; only relevant if multiple responses exist
                    return random.choice(i['responses']), i['link']

            results.pop(0)

# to do:

# tokenize items as is
# read: https://de.slideshare.net/ahmadhussein45/expert-system-with-python-2

# use NLTK to process input
# => Good URL on how to use NLTK to process strings
# => https://stackoverflow.com/questions/8897593/how-to-compute-the-similarity-between-two-text-documents

# pass this pre-processed input to a quantification function

# count matches between input and patterns
# => potentially just use a dict instead of tensorflow? see https://stackoverflow.com/questions/47992091/how-to-match-the-keywords-in-paragraph-using-python-nltk/47992508
# => tutorial on how to use the respective indicators:
# => https://bommaritollc.com/2014/06/30/advanced-approximate-sentence-matching-python/

# find good algorithm: percentage of patterns matched? total count?
# => when counting matches by hand, either only count unique matches OR weigh matches with longer strings more
# example: query is "kann ich mit 4 freunden draußen sitzen?", and the tag "outdoor" has that exact question. that would yield only ONE point otherwise
# it might even come so that "freunde" and "sitzen" are individual items for the tag "indoors" - yielding two points and associating the query with
# that category! so either for matches, only tokenize unique matches (full phrases match the longest match, not single words from it as well)
# or weigh them by length. or both! experiment with what works best...
# maybe: transform everything into lists; then just get unique list entries, then just compare list contents
# convert array to lists: https://www.journaldev.com/32797/python-convert-numpy-array-to-list
# convert everything to lowercase: https://stackoverflow.com/questions/1801668/convert-a-python-list-with-strings-all-to-lowercase-or-uppercase
# unique lists: https://www.geeksforgeeks.org/python-get-unique-values-list/
# sort lists alphabetically: https://www.kite.com/python/answers/how-to-sort-a-list-alphabetically-in-python
# compare lists: https://www.geeksforgeeks.org/python-percentage-similarity-of-lists/

# !!!

# STEP 1: tokenize the INTENTS via NLTK
# this already happened. the resulting list without duplicates is "classes"
# STEP 2: tokenize the INPUT via NLTK
# STEP 3: create multi dimensional lists
# STEP 4: compare these lists
# STEP 5: save the matching scores
# STEP 6: rank the matching scores


# easier via NLTK: https://stackoverflow.com/questions/49939450/unique-word-frequency-using-nltk
# TOKENIZE of the NLTK to split sentences into single words
# https://dev.to/coderasha/compare-documents-similarity-using-python-nlp-4odp
# now, only leave unique words: https://www.tutorialspoint.com/python_text_processing/python_filter_duplicate_words.htm
# some ideas: https://stackoverflow.com/questions/19648959/lists-in-python-using-nltk
# google some more...
# how to compare these? where do the tokenized words go? what is the format?
# => convert to a LIST (idea: with THREE dimensions)
# automatically NUMBER every (intent) list generated
# some ideas: https://stackoverflow.com/questions/12203652/in-python-create-a-list-with-a-variable-in-the-name
# https://stackoverflow.com/questions/48598222/appending-items-to-a-list-and-ensuring-unique-name-by-incrementing-number
# possible do this via a list of lists, yes (with answers at position 3 (= 2) in the rows (= [2][0])
# append each new list to the list of lists, the superlist contains all the lists
# the sublists contain the tag (= category) in row 1, the key words in row 2, and the reply in row 3
# compare list [n][1] to the input after tokenization => GOOGLE HOW TO DO THAT
# SAVE the resulting match percentage in the list of lists; it contains to values: the position of the list and the match
# the match percentage is then compared; the one with the highest "wins" and its corresponding position number
# is used to go to the respective list and get the reply from position ([0][n])[2][0]
# find highest value of a list: https://www.tutorialspoint.com/python/list_max.htm
# could just save the position of that in a respective temp variable then, use this to
# what if two values are the same?
# percentage-wise match? would punish many key words... (a list with just one generic word would always win)
# absolute match? punish few key words... (a list with tons of words would always win)
# WEIGH BOTH THE SAME
# better idea:
# go through every category and count the matching words (absolute number). save that number as "number 1"
# now divide that number by the amount of items in each category - this gives the percentage wise match. save that number as "number 2".
# compare every number 1 to one another. the category with the highest score is in place 1, the category with the second most matches is place 2...
# save that resulting placement as "placement 1" for every category
# now just compare the scoring with regards to "number 2". again reward placements for every category and save them as "placement 2"
# for every category, add the value of placement 1 + value of placement 2 into the new variable "placement 3", then divide this by two
# this is a ranking that weighs both counting methods equally
# return the reply of the category with the lowest placement 3 score

# get number of elements in list: https://stackabuse.com/python-get-number-of-elements-in-a-list/
# get number of matching elements between two lists: https://www.geeksforgeeks.org/python-count-of-matching-elements-among-lists-including-duplicates/
# divide number of matches by the number of words in tag-list. this varies between 0 and 1 (nothing and everything)
# total number of matches and percentage wise match should both count for 50%
# both should have the same RANGE, but ACROSS categories
# alle wörter zählen, durch anzahl kategorien teilen, das als divisor

# sort the LIST
# compare the LISTS (input is also to become such a prepared list!)
# compare the different lists

# google search for "python categorize input word keywords"
# => https://stackoverflow.com/questions/62883961/how-to-categorize-a-list-of-data-by-keyword-in-python
# => https://stackoverflow.com/questions/1490061/classifying-text-based-on-groups-of-keywords
#
# -use 3 dimensional lists: dimension 1 (category), dimension 2 (loooots of key words), dimension 3 (reply) => give item [2][0] as reply, use category [0][0] as category, and [1][n] for key words (while in...)
# -convert every single word into a list item of its own
# -ignore puntucation and ()"' and so on
# -convert the list to lowercase
# -filter out duplicates
# -order the list alphabetically
# -do the same for the input
# -match lists percentage-wise
# -weigh longer strings for higher percentage
# -algorithm: number of characters of each matching word gets counted

# add points for respective tag whenever it matches (see line above - find a good way to quantify a good fit)

# at the end: list categories with most points
# => optional: point threshold?

# give list with best matches
# => compare this to the results of the DL algorithm

print("\n----------\n")
print(classify('is your shop open today?'))
print("\n----------\n")

response('is your shop open today?')

# to do:
# call expert system classification
# compare the results