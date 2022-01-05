# things we need for NLP
# things we need for NLP
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

# things needed for the performance measuring algorithm
import time

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

# define number of epochs early on
numberOfEpochs = 1000

# get time before any of the sophisticated chatbot operations are performed
timeBefore_building = time.time() * 1000.0

# define empty arrays for the dictionary / neural network (?)
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
        # tokenize each word in the sentence. information on tokenization: https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/text/Tokenizer, https://chatbotsmagazine.com/contextual-chat-bots-with-tensorflow-4391749d0077
        # "We create a list of documents (sentences), each sentence is a list of stemmed words and each document is associated with an intent (a class). (...) we need to transform it further: from documents of words into tensors of numbers."
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
# "Stemming is a text normalizing technique that cuts down affixes of words, to extract its base form or root words. Stemming is a crude process and sometimes, the root word, also called the stem, may not have grammatical meaning."
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
model.fit(train_x, train_y, n_epoch=numberOfEpochs, batch_size=8, show_metric=True)
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
                    # pick a random response from the intent; only relevant if multiple responses exist
                    # return random.choice(i['responses'])
                    return random.choice(i['responses']), i['link']

            results.pop(0)


# get time before neural network is built
timeAfter_building = time.time() * 1000.0
timeDifferenceBuildingFloat = (timeAfter_building - timeBefore_building)
timeDifferenceBuilding = "{:.2f}".format(timeDifferenceBuildingFloat)

# print the classification for a pre-defined sentence
print("\n----------\n")
# questionToAsk = input("Please enter the question you want to ask: ")

# for the measurement:
questionToAsk = "Kann ich mit 5 Freunden draussen an einem Tisch im Biergarten sitzen?"
answerExpected = "Ein Tisch darf aus maximal zehn Personen zuzueglich bis zu zehn minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt lebt."
answerReceived = str(response(questionToAsk)[0])

print("----------\n")
timeBeforeAnswer = time.time() * 1000.0
print(classify(questionToAsk))
print("\n")
print(response(questionToAsk))
timeAfterAnswer = time.time() * 1000.0
timeDifferenceAnswerFloat = (timeAfterAnswer - timeBeforeAnswer)
timeDifferenceAnswer = "{:.2f}".format(timeDifferenceAnswerFloat)
print("\n----------\n")
print("It took " + timeDifferenceBuilding + " miliseconds to train and build the NN model" + ".\n")
print("The number of epochs was " + str(numberOfEpochs) + " (" + str(float(timeDifferenceBuilding)/float(numberOfEpochs)) + " ms per epoch).\n")
print("It took " + timeDifferenceAnswer + " miliseconds to answer the question via the NN model.")

# determine whether the result was correct
if (answerExpected == answerReceived):
     correctAnswer = "yes"
else:
     correctAnswer = "no"



# BAREBONES CHATBOT

# intents:
# row 0 = first intent, row 1 = second intent...
# position 0 = score, position 1 = score moderated by number of patterns, pos 2 = ranking by score,
# pos 3 = ranking by moderated score, pos 4 = mixed ranking (used for output)

# to do: sind nicht alle wirklich nur ein eintrag - weiter zerhacken

timeBeforeBarebones = timeAfter_building

arrayIntents = [[0, 0, 99, 99, 99, "gastgewerbe_indoor", "Ein Tisch darf aus maximal vier Personen zuzueglich bis zu 6 minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt leben.", "indoor", " geschlossene Raeume", "geschlossener Raum", "drinnen", "im Inneren", "innen", "sitzen", "essen", "Tisch"], [0, 0, 99, 99, 99, "gastgewerbe_outdoor", "Ein Tisch darf aus maximal zehn Personen zuzueglich bis zu zehn minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt lebt.", "outdoor", "out-door", "Biergarten", "draussen", "im Freien", "an der frischen Luft ", "ausserhalb", "sitzen", "essen", "Tisch"], [0, 0, 99, 99, 99, "gemeinsamer_haushalt", "Fuer Personen die in einem Haushalt leben gelten die Beschraenkungen auf eine Personenzahl nicht.", "gemeinsamer Haushalt", "zusammen leben", "gemeinsam leben", "ein Haushalt", "zusammen Wohnen"], [0, 0, 99, 99, 99, "test_pcr", "Mit einem negativen PCR-Test darf man innerhalb von 72 Stunden ein Gastgewerbe betreten.", "PCR-Test", " molekularbiologischer Test", "Gueltigkeit", "gueltig", "Wie lange", "Gurgeltest", "PCR-Gurgeltest", "Gueltigkeitsdauer", " Zutrittstests"], [0, 0, 99, 99, 99, "berechtigung", "Der Kunde muss einen den Nachweis einer geringen epidemiologischen Gefahr erbringen, dh. Sie muessen getestet, genesen oder geimpft sein.", "Berechtigung", " notwendig", "noetig", "braucht", "brauche", "betreten", "Nachweisen", "Zutritt", "Wann", "wann", "hinein", "darf", "duerfen", "Gasthaus", "Restaurant", "Cafe"], [0, 0, 99, 99, 99, "test_antigen", "Mit einem negativem Antigentest einer Befugten stelle darf man innerhalb von 48 Stunden ein Gastgewerbe betreten)", "Antigentest", "befugte Stelle", "Teststelle", "Gueltigkeit", "Wie lange", "Testcenter", "Test-Center", "Teststrasse", "Test Strasse", "Gueltigkeitsdauer"], [0, 0, 99, 99, 99, "test_selbst", "Mit einem behördlich erfassten negativen Selbsttest darf man 24 Stunden ein Gastgewerbe betreten", "Selbsttest", " Antigentest", "Gueltigkeit", "Wie lange", "behördliche Datenverarbeitung", "registrierter Test", "registrierter Selbsttest", "Gueltigkeitsdauer"]]

splitInput = questionToAsk.split()

for i in range(len(splitInput) - 1): # iterate through input
    if (splitInput[i] == "nicht"):
        splitInput.pop(i+1)

# remove duplicates
splitInput = list(dict.fromkeys(splitInput))

# get barebones score
for i in range(len(splitInput)): # iterate through input
    for j in range(len(arrayIntents)): # iterate through rows
        for k in range(len(arrayIntents[j])): # iterate through columns
            if splitInput[i] == arrayIntents[j][k]:
                if splitInput[i-1] != "nicht":
                    arrayIntents[j][0] = arrayIntents[j][0] + 1

# get score moderated by length
for i in range(len(splitInput)): # iterate through input
    for j in range(len(arrayIntents)): # iterate through rows
        if arrayIntents[j][0] != 0: # otherwise division by zero
            arrayIntents[j][1] = ((arrayIntents[j][0])/(len((arrayIntents[j])) - 6))


def rankByScore(regIntents, ref, trg):

    # sort by score
    rankedIntents = sorted(regIntents, key=lambda x: x[ref], reverse=True)

    # write place
    n = 0  # rank counter
    m = 0  # duplicate counter

    for j in range(len(rankedIntents) - 1): # iterate through rows
        if rankedIntents[j][ref] != rankedIntents[j+1][ref]:        # no more duplicates
            if rankedIntents[j][ref] != rankedIntents[j-1][ref]:    # first after duplicates
                n = n + m
                rankedIntents[j][trg] = n
                n = n + 1
                m = 0
            else:                                               # last of duplicates
                rankedIntents[j][trg] = n
                m = m + 1
        else:                                                   # duplicate
            rankedIntents[j][trg] = n
            m = m + 1

    # rank last position
    lastPos = (len(rankedIntents) - 1)

    if rankedIntents[lastPos - 1][ref] > rankedIntents[lastPos][ref]:
        rankedIntents[lastPos][trg] = (rankedIntents[lastPos - 1][trg] + 1)
    else:
        rankedIntents[lastPos][trg] = (rankedIntents[lastPos - 1][trg])

    return rankedIntents

# get rank for regular score
# https://stackoverflow.com/questions/20183069/how-to-sort-multidimensional-array-by-column
# print ("Pure score:")
# print (rankByScore(arrayIntents, 0, 2))
rankIntents = rankByScore(arrayIntents, 0, 2)

# get rank for moderated score
# print ("Moderated score:")
# print (rankByScore(arrayIntents, 1, 3))
rankIntents = rankByScore(rankIntents, 1, 3)

# get mixed rank
# for every row, write value of (([2]+[3])/2) at position 4
for j in range(len(rankIntents)): # iterate through rows
    rankIntents[j][4] = (((rankIntents[j][2])+(rankIntents[j][3])))

rankIntents = sorted(rankIntents, key=lambda x: x[4], reverse=False)

timeAfterBarebones = time.time() * 1000.0
timeDifferenceBarebones = (timeAfterBarebones - timeBeforeBarebones)

# output
print("Answer based on the barebones model: \n")
print(rankIntents[0][6])
print("It took " + str(timeDifferenceBarebones) + " milliseconds to process the data for the barebones model, \n")

# print debug info for BB model
# for j in range(len(arrayIntents)):
#    print("Kategorie " + str(rankIntents[j][5]) + " hat " + str(rankIntents[j][0]) + " Punkte; bereinigter Score: " + str(rankIntents[j][1])
#          + ", \nfinaler Rang: " + str(rankIntents[j][4]) + ", Ranking nach reiner Score: " + str(rankIntents[j][2]) +
#          ", Ranking moderiert: " + str(rankIntents[j][3]) + "\n")

if (answerExpected == rankIntents[0][6]):
    correctBB = "yes"
else:
    correctBB = "no"

if answerReceived != rankIntents[0][6]:
    differentAns = "The models got different results "
    if answerExpected == answerReceived:
        corrOne = "- NN was correct."
    else:
        corrOne = "- BB was correct."
else:
    differentAns = "Both models got the same results "
    if answerExpected != answerReceived:
        corrOne = "- neither was correct."
    else:
        corrOne = "- both were correct."

# safe results into a file
vergleichsLog = open('log_perf.txt', 'a')
vergleichsLog.write("The question asked was: " + questionToAsk +
                    "\nThe categorization via NN was " + str(classify(questionToAsk)[0]) + " - correct: " + correctAnswer +
                    ". It took " + timeDifferenceBuilding + " milliseconds to train and build the NN model. "
                    + "The number of epochs was " + str(numberOfEpochs) + " (" + str(float(timeDifferenceBuilding)/float(numberOfEpochs))
                    + " ms per epoch). It took " + str(timeDifferenceAnswer) + " miliseconds to answer the question via the NN model.\nThe categorization via BB was "
                    + rankIntents[0][5] + " - correct: " + correctBB +
                    ". It took " + str(timeDifferenceBarebones) + " milliseconds to build the BB model.\n"
                    + differentAns + corrOne + "\n")
vergleichsLog.close()